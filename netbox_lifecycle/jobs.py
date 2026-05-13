"""
Background jobs for the netbox-lifecycle plugin.

CiscoEoXSyncJob
---------------
Queries the Cisco EoX API for all DeviceTypes and ModuleTypes whose
manufacturer name matches the configured list, then updates (or creates)
their HardwareLifecycle records with the returned end-of-life dates.

Lookup order (per item):
  1. Try a Device/Module serial number associated with this DeviceType/ModuleType
  2. Fall back to the DeviceType/ModuleType part_number field

The job reschedules itself using ``enqueue_once()`` so the configured
interval is honoured dynamically.  Initial scheduling is triggered when
the user saves the settings page (or calls ``enqueue_once()`` manually).
"""

import logging

from netbox.jobs import JobRunner

logger = logging.getLogger(__name__)

__all__ = ('CiscoEoXSyncJob',)


class CiscoEoXSyncJob(JobRunner):
    class Meta:
        name = 'Cisco EoX Sync'

    def run(self, *args, **kwargs):
        from django.contrib.contenttypes.models import ContentType

        from dcim.models import Device, DeviceType, Module, ModuleType

        from netbox_lifecycle.models import HardwareLifecycle
        from netbox_lifecycle.utilities.cisco_eox_api import (
            CiscoEoXAPIError,
            CiscoEoXApiClient,
        )
        from netbox_lifecycle.utilities.settings_loader import get_cisco_eox_settings

        # ------------------------------------------------------------------
        # Load configuration
        # ------------------------------------------------------------------
        cfg = get_cisco_eox_settings()
        if cfg is None:
            self.logger.warning(
                'Cisco EoX sync is not configured or not enabled. Skipping.'
            )
            return

        self.logger.info(
            'Starting Cisco EoX sync for manufacturers: %s',
            cfg.manufacturer_names,
        )

        client = CiscoEoXApiClient(
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
        )

        updated = 0
        skipped = 0
        errored = 0

        # ------------------------------------------------------------------
        # Helper: resolve EoX data for one item
        # ------------------------------------------------------------------
        def _sync_item(item, ct, serial_qs, part_number_attr='part_number'):
            nonlocal updated, skipped, errored

            eox_data = None
            label = f'{item._meta.verbose_name} "{item}"'

            # 1. Try serial number from a related device/module
            serial = (
                serial_qs.filter(**{f'{item._meta.model_name}__pk': item.pk})
                .exclude(serial='')
                .values_list('serial', flat=True)
                .first()
            )
            if serial:
                try:
                    records = client.get_eox_by_serial([serial])
                    if records:
                        eox_data = client.parse_eox_record(records[0])
                        self.logger.debug(
                            '%s — EoX data found via serial %s (product: %s)',
                            label,
                            serial,
                            eox_data.get('_eol_product_id'),
                        )
                except CiscoEoXAPIError as exc:
                    self.logger.debug(
                        '%s — serial lookup failed (%s), will try part_number.', label, exc
                    )

            # 2. Fall back to part_number
            if eox_data is None:
                part_number = getattr(item, part_number_attr, '') or ''
                if part_number:
                    try:
                        records = client.get_eox_by_product_id([part_number])
                        if records:
                            eox_data = client.parse_eox_record(records[0])
                            self.logger.debug(
                                '%s — EoX data found via part_number %s',
                                label,
                                part_number,
                            )
                    except CiscoEoXAPIError as exc:
                        self.logger.warning(
                            '%s — part_number lookup failed: %s', label, exc
                        )
                        errored += 1
                        return

            if eox_data is None:
                self.logger.debug('%s — no EoX data found; skipping.', label)
                skipped += 1
                return

            # Strip internal-only keys before saving
            lifecycle_fields = {
                k: v for k, v in eox_data.items() if not k.startswith('_')
            }
            # Remove None values so existing dates are not blanked unintentionally
            # when only partial data is returned
            lifecycle_fields = {k: v for k, v in lifecycle_fields.items() if v is not None}

            HardwareLifecycle.objects.update_or_create(
                assigned_object_type=ct,
                assigned_object_id=item.pk,
                defaults=lifecycle_fields,
            )
            updated += 1

        # ------------------------------------------------------------------
        # Process DeviceTypes
        # ------------------------------------------------------------------
        dt_ct = ContentType.objects.get_for_model(DeviceType)
        device_types = DeviceType.objects.filter(
            manufacturer__name__in=cfg.manufacturer_names_list
        ).select_related('manufacturer')

        self.logger.info('Processing %d DeviceTypes …', device_types.count())
        for dt in device_types:
            _sync_item(dt, dt_ct, Device.objects, part_number_attr='part_number')

        # ------------------------------------------------------------------
        # Process ModuleTypes
        # ------------------------------------------------------------------
        mt_ct = ContentType.objects.get_for_model(ModuleType)
        module_types = ModuleType.objects.filter(
            manufacturer__name__in=cfg.manufacturer_names_list
        ).select_related('manufacturer')

        self.logger.info('Processing %d ModuleTypes …', module_types.count())
        for mt in module_types:
            _sync_item(mt, mt_ct, Module.objects, part_number_attr='part_number')

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        self.logger.info(
            'Cisco EoX sync complete — updated: %d, skipped: %d, errored: %d',
            updated,
            skipped,
            errored,
        )

        # ------------------------------------------------------------------
        # Reschedule for next run
        # ------------------------------------------------------------------
        # Reload cfg in case it changed while this job was running
        cfg = get_cisco_eox_settings()
        if cfg and cfg.enabled:
            CiscoEoXSyncJob.enqueue_once(interval=cfg.sync_interval)
            self.logger.debug(
                'Rescheduled Cisco EoX sync in %d minutes.', cfg.sync_interval
            )
