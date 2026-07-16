from unittest.mock import patch

from dcim.models import Manufacturer
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from utilities.testing import TestCase as NetBoxTestCase

from netbox_lifecycle.choices.eox import DriverChoices
from netbox_lifecycle.jobs import EoXManualSyncJob, EoXSyncJob
from netbox_lifecycle.models import EoXAPISettings
from netbox_lifecycle.utilities.eox import DRIVERS, EoXAPIError, get_driver
from netbox_lifecycle.utilities.eox.drivers import CiscoEoXDriver


class EoXAPISettingsModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Cisco', slug='cisco')
        cls.manufacturer2 = Manufacturer.objects.create(name='Meraki', slug='meraki')

    def _make_cfg(self, manufacturer=None, enabled=False):
        cfg = EoXAPISettings.objects.create(
            driver=DriverChoices.CISCO,
            manufacturer=manufacturer or self.manufacturer,
            enabled=enabled,
            client_id='client-id',
        )
        cfg.client_secret = 's3cret'
        cfg.save()
        return cfg

    def test_client_secret_round_trip(self):
        cfg = self._make_cfg()
        cfg.refresh_from_db()
        self.assertEqual(cfg.client_secret, 's3cret')
        # Encrypted value in the DB column is not the plaintext.
        self.assertNotEqual(cfg._client_secret, 's3cret')

    def test_empty_client_secret(self):
        cfg = self._make_cfg()
        cfg.client_secret = ''
        cfg.save()
        cfg.refresh_from_db()
        self.assertEqual(cfg.client_secret, '')
        self.assertEqual(cfg._client_secret, '')

    def test_multiple_rows_allowed_per_driver(self):
        self._make_cfg(manufacturer=self.manufacturer)
        # Same driver, different manufacturer — must succeed.
        self._make_cfg(manufacturer=self.manufacturer2)
        self.assertEqual(EoXAPISettings.objects.count(), 2)

    def test_unique_driver_manufacturer(self):
        self._make_cfg(manufacturer=self.manufacturer)
        with self.assertRaises(IntegrityError):
            EoXAPISettings.objects.create(
                driver=DriverChoices.CISCO,
                manufacturer=self.manufacturer,
            )

    def test_save_schedules_job_when_enabled(self):
        with patch.object(EoXSyncJob, 'enqueue_once') as enqueue_once:
            cfg = self._make_cfg(enabled=True)
            enqueue_once.assert_called()
            kwargs = enqueue_once.call_args.kwargs
            self.assertEqual(kwargs.get('instance'), cfg)
            self.assertEqual(kwargs.get('interval'), cfg.sync_interval)

    def test_save_does_not_schedule_when_disabled(self):
        with patch.object(EoXSyncJob, 'enqueue_once') as enqueue_once:
            self._make_cfg(enabled=False)
            enqueue_once.assert_not_called()


class EoXDriverRegistryTests(TestCase):

    def test_cisco_registered(self):
        self.assertIn(DriverChoices.CISCO, DRIVERS)
        self.assertIs(get_driver(DriverChoices.CISCO), CiscoEoXDriver)

    def test_unknown_driver_raises(self):
        with self.assertRaises(EoXAPIError):
            get_driver('does-not-exist')

    def test_driver_requires_credentials(self):
        with self.assertRaises(EoXAPIError):
            CiscoEoXDriver(client_id='', client_secret='')

    def test_driver_exposes_api_url(self):
        # The API URL lives on the driver class, not in user-managed config.
        self.assertTrue(CiscoEoXDriver.api_url)


class EoXSyncViewTests(NetBoxTestCase):
    user_permissions = ('netbox_lifecycle.sync_eoxapisettings',)

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Cisco', slug='cisco')
        cls.cfg = EoXAPISettings.objects.create(
            driver=DriverChoices.CISCO,
            manufacturer=cls.manufacturer,
            enabled=False,
            client_id='client-id',
        )

    def test_sync_view_enqueues_manual_job(self):
        url = reverse(
            'plugins:netbox_lifecycle:eoxapisettings_sync', kwargs={'pk': self.cfg.pk}
        )
        with patch.object(EoXManualSyncJob, 'enqueue') as enqueue:
            response = self.client.post(url)
            enqueue.assert_called_once()
            self.assertEqual(enqueue.call_args.kwargs.get('instance'), self.cfg)
        self.assertHttpStatus(response, 302)
        self.assertEqual(response.url, self.cfg.get_absolute_url())

    def test_sync_view_requires_permission(self):
        self.remove_permissions('netbox_lifecycle.sync_eoxapisettings')
        url = reverse(
            'plugins:netbox_lifecycle:eoxapisettings_sync', kwargs={'pk': self.cfg.pk}
        )
        with patch.object(EoXManualSyncJob, 'enqueue') as enqueue:
            response = self.client.post(url)
            enqueue.assert_not_called()
        self.assertHttpStatus(response, 403)
