"""
Background jobs for EoX synchronization.

Two distinct job classes, both per-instance (bound to a single EoXAPISettings row):

* EoXSyncJob       — recurring background sync. Scheduled via
                     ``EoXAPISettings.save()`` calling ``enqueue_once`` with
                     the row's own ``sync_interval``; re-enqueues itself at
                     the end of each run so interval changes are honored.
* EoXManualSyncJob — one-shot, operator-initiated. Triggered by the "Run
                     Now" action; does NOT re-enqueue.

Both share ``_run_sync(cfg, log)`` so the actual API work lives in one
place.
"""

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from netbox.jobs import JobRunner

__all__ = ('EoXSyncJob', 'EoXManualSyncJob')


def _run_sync(cfg, log) -> None:
    """Run one full EoX sync pass for a single EoXAPISettings row."""
    from dcim.models import Device, DeviceType, Module, ModuleType

    from netbox_lifecycle.models import HardwareLifecycle
    from netbox_lifecycle.utilities.eox import EoXAPIError, get_driver

    driver_cls = get_driver(cfg.driver)
    client = driver_cls(
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
    )

    manufacturer_id = cfg.manufacturer_id
    if not manufacturer_id:
        log.info(f'No manufacturer configured for {cfg} — nothing to sync.')
        return

    updated = skipped = errored = 0

    def _sync_item(item, ct, serial_qs, type_field):
        nonlocal updated, skipped, errored
        eox_data = None
        label = f'{item._meta.verbose_name} "{item}"'

        serial = (
            serial_qs.filter(**{f'{type_field}__pk': item.pk})
            .exclude(serial='')
            .values_list('serial', flat=True)
            .first()
        )
        if serial:
            try:
                records = client.get_eox_by_serial([serial])
                if records:
                    eox_data = client.parse_eox_record(records[0])
                    log.debug(
                        f'{label} — EoX data found via serial {serial} '
                        f'(product: {eox_data.get("_eol_product_id")})'
                    )
            except EoXAPIError as exc:
                log.debug(
                    f'{label} — serial lookup failed ({exc}), will try part_number.'
                )

        if eox_data is None:
            part_number = getattr(item, 'part_number', '') or ''
            if part_number:
                try:
                    records = client.get_eox_by_product_id([part_number])
                    if records:
                        eox_data = client.parse_eox_record(records[0])
                        log.debug(
                            f'{label} — EoX data found via part_number {part_number}'
                        )
                except EoXAPIError as exc:
                    log.warning(f'{label} — part_number lookup failed: {exc}')
                    errored += 1
                    return

        if eox_data is None:
            log.debug(f'{label} — no EoX data found; skipping.')
            skipped += 1
            return

        # Strip internal-only keys and None values so existing dates aren't blanked
        lifecycle_fields = {
            k: v for k, v in eox_data.items() if not k.startswith('_') and v is not None
        }

        HardwareLifecycle.objects.update_or_create(
            assigned_object_type=ct,
            assigned_object_id=item.pk,
            defaults=lifecycle_fields,
        )
        updated += 1

    dt_ct = ContentType.objects.get_for_model(DeviceType)
    device_types = DeviceType.objects.filter(
        manufacturer_id=manufacturer_id
    ).select_related('manufacturer')
    log.info(f'Processing {device_types.count()} DeviceTypes for {cfg}.')
    for dt in device_types:
        _sync_item(dt, dt_ct, Device.objects, 'device_type')

    mt_ct = ContentType.objects.get_for_model(ModuleType)
    module_types = ModuleType.objects.filter(
        manufacturer_id=manufacturer_id
    ).select_related('manufacturer')
    log.info(f'Processing {module_types.count()} ModuleTypes for {cfg}.')
    for mt in module_types:
        _sync_item(mt, mt_ct, Module.objects, 'module_type')

    log.info(
        f'EoX sync complete for {cfg} — updated: {updated}, skipped: {skipped}, errored: {errored}'
    )


def _finalize(cfg) -> None:
    """Stamp last_synced without re-triggering save()'s enqueue side effects."""
    type(cfg).objects.filter(pk=cfg.pk).update(last_synced=timezone.now())


class EoXSyncJob(JobRunner):
    """Recurring per-instance background sync; reschedules itself at end of run."""

    class Meta:
        name = 'EoX Sync'

    def run(self, *args, **kwargs):
        cfg = self.job.object
        if cfg is None:
            self.logger.warning(
                'EoXSyncJob ran without a bound EoXAPISettings instance.'
            )
            return

        _run_sync(cfg, self.logger)
        _finalize(cfg)

        # Re-read the row in case it was edited while the job was running, then
        # only re-enqueue if it's still enabled.
        cfg.refresh_from_db()
        if cfg.enabled:
            EoXSyncJob.enqueue_once(instance=cfg, interval=cfg.sync_interval)
            self.logger.debug(
                f'Rescheduled EoX sync for {cfg} in {cfg.sync_interval} minutes.'
            )


class EoXManualSyncJob(JobRunner):
    """Operator-initiated one-shot sync — does NOT reschedule itself."""

    class Meta:
        name = 'EoX Manual Sync'

    def run(self, *args, **kwargs):
        cfg = self.job.object
        if cfg is None:
            self.logger.warning(
                'EoXManualSyncJob ran without a bound EoXAPISettings instance.'
            )
            return

        _run_sync(cfg, self.logger)
        _finalize(cfg)
