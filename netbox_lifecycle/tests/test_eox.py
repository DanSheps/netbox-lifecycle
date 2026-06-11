from unittest.mock import patch

from dcim.models import Manufacturer
from django.db.utils import IntegrityError
from django.test import RequestFactory, TestCase

from netbox_lifecycle.choices.eox import DriverChoices
from netbox_lifecycle.jobs import EoXManualSyncJob, EoXSyncJob
from netbox_lifecycle.models import EoXAPISettings
from netbox_lifecycle.utilities.eox import DRIVERS, EoXAPIError, get_driver
from netbox_lifecycle.utilities.eox.drivers import CiscoEoXDriver
from netbox_lifecycle.views.eox import EoXAPISettingsSyncView


class EoXAPISettingsModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Cisco', slug='cisco')

    def _make_cfg(self, url='https://apix.example.com/eox/rest/5', enabled=False):
        cfg = EoXAPISettings.objects.create(
            driver=DriverChoices.CISCO,
            url=url,
            enabled=enabled,
            client_id='client-id',
        )
        cfg.client_secret = 's3cret'
        cfg.save()
        cfg.manufacturers.add(self.manufacturer)
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

    def test_multiple_rows_allowed_no_singleton(self):
        self._make_cfg(url='https://apix.example.com/eox/rest/5')
        # Same driver, different URL — must succeed (no singleton).
        self._make_cfg(url='https://apix.example.com/eox/rest/6')
        self.assertEqual(EoXAPISettings.objects.count(), 2)

    def test_unique_driver_url(self):
        self._make_cfg(url='https://apix.example.com/eox/rest/5')
        with self.assertRaises(IntegrityError):
            EoXAPISettings.objects.create(
                driver=DriverChoices.CISCO,
                url='https://apix.example.com/eox/rest/5',
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
            CiscoEoXDriver(client_id='', client_secret='', base_url='https://x')


class EoXSyncViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Cisco', slug='cisco')
        cls.cfg = EoXAPISettings.objects.create(
            driver=DriverChoices.CISCO,
            url='https://apix.example.com/eox/rest/5',
            enabled=False,
            client_id='client-id',
        )
        cls.cfg.manufacturers.add(cls.manufacturer)

    def test_sync_view_enqueues_manual_job(self):
        request = RequestFactory().post(f'/plugins/lifecycle/eox/{self.cfg.pk}/sync/')
        view = EoXAPISettingsSyncView()
        view.queryset = EoXAPISettings.objects.all()
        # Bypass auth — call the POST handler directly with a patched enqueue.
        request.user = type(
            'U',
            (),
            {
                'has_perms': lambda self, perms: True,
                'has_perm': lambda self, perm: True,
            },
        )()
        with patch.object(EoXManualSyncJob, 'enqueue') as enqueue:
            response = view.post(request, pk=self.cfg.pk)
            enqueue.assert_called_once()
            self.assertEqual(enqueue.call_args.kwargs.get('instance'), self.cfg)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.cfg.get_absolute_url())
