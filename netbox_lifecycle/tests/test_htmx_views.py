from datetime import datetime, timedelta, timezone

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from virtualization.models import Cluster, ClusterType, VirtualMachine

from netbox_lifecycle.models import (
    License,
    LicenseAssignment,
    SupportContract,
    SupportContractAssignment,
    SupportSKU,
    Vendor,
)
from netbox_lifecycle.views.htmx import MAX_LICENSE_DISPLAY

User = get_user_model()


class DeviceContractsHTMXViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer', slug='test-manufacturer'
        )
        device_type = DeviceType.objects.create(
            manufacturer=cls.manufacturer, model='Test Model', slug='test-model'
        )
        device_role = DeviceRole.objects.create(name='Test Role', slug='test-role')
        site = Site.objects.create(name='Test Site', slug='test-site')
        cls.device = Device.objects.create(
            name='Test Device',
            device_type=device_type,
            role=device_role,
            site=site,
        )
        cls.vendor = Vendor.objects.create(name='Test Vendor')
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def test_device_contracts_htmx_view(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='TEST-001',
            end=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
        )
        SupportContractAssignment.objects.create(contract=contract, device=self.device)

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST-001')
        self.assertContains(response, 'Active')

    def test_device_contracts_expired_htmx_view(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='EXPIRED-001',
            end=datetime.now(tz=timezone.utc).date() - timedelta(days=1),
        )
        SupportContractAssignment.objects.create(contract=contract, device=self.device)

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_expired',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EXPIRED-001')

    def test_device_contracts_requires_login(self):
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_device_contracts_with_sku(self):
        """Test that SKU is displayed in the contract list."""
        sku = SupportSKU.objects.create(
            manufacturer=self.manufacturer,
            sku='SKU-PREMIUM-24x7',
        )
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='TEST-SKU-001',
            end=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
        )
        SupportContractAssignment.objects.create(
            contract=contract, device=self.device, sku=sku
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST-SKU-001')
        self.assertContains(response, 'SKU-PREMIUM-24x7')

    def test_device_contracts_future(self):
        """Test that future contracts are displayed in the Future tab."""
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='FUTURE-001',
            start=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
            end=datetime.now(tz=timezone.utc).date() + timedelta(days=365),
        )
        SupportContractAssignment.objects.create(contract=contract, device=self.device)

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FUTURE-001')
        self.assertContains(response, 'Future')

    def test_device_contracts_unspecified(self):
        """Test that contracts without end date show in Unspecified tab."""
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='UNSPEC-001',
            start=datetime.now(tz=timezone.utc).date() - timedelta(days=30),
            end=None,
        )
        SupportContractAssignment.objects.create(contract=contract, device=self.device)

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UNSPEC-001')
        self.assertContains(response, 'Unspecified')

    def test_device_contracts_no_contracts(self):
        """Test empty state when device has no contracts."""
        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'None')

    def test_device_contracts_multiple_statuses(self):
        """Test that multiple contract statuses are grouped correctly."""
        # Active contract
        active_contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='ACTIVE-MULTI',
            end=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
        )
        SupportContractAssignment.objects.create(
            contract=active_contract, device=self.device
        )

        # Future contract
        future_contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='FUTURE-MULTI',
            start=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
            end=datetime.now(tz=timezone.utc).date() + timedelta(days=365),
        )
        SupportContractAssignment.objects.create(
            contract=future_contract, device=self.device
        )

        # Expired contract
        expired_contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='EXPIRED-MULTI',
            end=datetime.now(tz=timezone.utc).date() - timedelta(days=1),
        )
        SupportContractAssignment.objects.create(
            contract=expired_contract, device=self.device
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check all tabs are present
        self.assertContains(response, 'Active')
        self.assertContains(response, 'Future')
        self.assertContains(response, 'Expired')
        # Check contracts
        self.assertContains(response, 'ACTIVE-MULTI')
        self.assertContains(response, 'FUTURE-MULTI')
        # Expired is lazy-loaded, so contract ID won't be in initial response

    def test_device_contracts_with_license(self):
        """Test contract assignment with license is displayed."""
        license_obj = License.objects.create(
            manufacturer=self.manufacturer,
            name='Enterprise License',
        )
        license_assignment = LicenseAssignment.objects.create(
            license=license_obj,
            vendor=self.vendor,
            device=self.device,
            quantity=1,
        )
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='LICENSE-001',
            end=datetime.now(tz=timezone.utc).date() + timedelta(days=30),
        )
        SupportContractAssignment.objects.create(
            contract=contract,
            device=self.device,
            license=license_assignment,
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LICENSE-001')

    def test_expired_contracts_requires_login(self):
        """Test that expired contracts endpoint requires authentication."""
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_expired',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_expired_contracts_with_sku(self):
        """Test that expired contracts show SKU."""
        sku = SupportSKU.objects.create(
            manufacturer=self.manufacturer,
            sku='SKU-EXPIRED-SUPPORT',
        )
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='EXPIRED-SKU-001',
            end=datetime.now(tz=timezone.utc).date() - timedelta(days=1),
        )
        SupportContractAssignment.objects.create(
            contract=contract, device=self.device, sku=sku
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_contracts_expired',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EXPIRED-SKU-001')
        self.assertContains(response, 'SKU-EXPIRED-SUPPORT')


class DeviceLicensesHTMXViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name='License Manufacturer', slug='license-manufacturer'
        )
        device_type = DeviceType.objects.create(
            manufacturer=cls.manufacturer, model='License Model', slug='license-model'
        )
        device_role = DeviceRole.objects.create(
            name='License Role', slug='license-role'
        )
        site = Site.objects.create(name='License Site', slug='license-site')
        cls.device = Device.objects.create(
            name='License Device',
            device_type=device_type,
            role=device_role,
            site=site,
        )
        cls.vendor = Vendor.objects.create(name='License Vendor')
        cls.license = License.objects.create(
            manufacturer=cls.manufacturer,
            name='Test License',
        )
        cls.user = User.objects.create_user(username='licenseuser', password='testpass')

    def test_device_licenses_requires_login(self):
        url = reverse(
            'plugins:netbox_lifecycle:device_licenses_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_device_licenses_empty(self):
        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_licenses_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'None')

    def test_device_licenses_with_assignment(self):
        LicenseAssignment.objects.create(
            license=self.license,
            vendor=self.vendor,
            device=self.device,
            quantity=5,
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_licenses_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test License')
        self.assertContains(response, 'License Manufacturer')
        self.assertContains(response, 'License Vendor')
        self.assertContains(response, '5')

    def test_device_licenses_assign_button(self):
        LicenseAssignment.objects.create(
            license=self.license,
            vendor=self.vendor,
            device=self.device,
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_licenses_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assign License')
        self.assertContains(response, f'device={self.device.pk}')

    def test_device_licenses_show_all_link(self):
        for i in range(MAX_LICENSE_DISPLAY + 1):
            lic = License.objects.create(
                manufacturer=self.manufacturer,
                name=f'Bulk License {i}',
            )
            LicenseAssignment.objects.create(
                license=lic,
                vendor=self.vendor,
                device=self.device,
            )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_licenses_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Show all Licenses')

    def test_device_licenses_no_show_all_when_under_limit(self):
        LicenseAssignment.objects.create(
            license=self.license,
            vendor=self.vendor,
            device=self.device,
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:device_licenses_htmx',
            kwargs={'pk': self.device.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Show all Licenses')


class VirtualMachineLicensesHTMXViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name='VM License Mfg', slug='vm-license-mfg'
        )
        cluster_type = ClusterType.objects.create(
            name='VM Cluster Type', slug='vm-cluster-type'
        )
        cluster = Cluster.objects.create(name='VM Cluster', type=cluster_type)
        cls.virtual_machine = VirtualMachine.objects.create(
            name='License VM',
            cluster=cluster,
        )
        cls.vendor = Vendor.objects.create(name='VM License Vendor')
        cls.license = License.objects.create(
            manufacturer=cls.manufacturer,
            name='VM Test License',
        )
        cls.user = User.objects.create_user(
            username='vmlicenseuser', password='testpass'
        )

    def test_vm_licenses_requires_login(self):
        url = reverse(
            'plugins:netbox_lifecycle:virtualmachine_licenses_htmx',
            kwargs={'pk': self.virtual_machine.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_vm_licenses_empty(self):
        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:virtualmachine_licenses_htmx',
            kwargs={'pk': self.virtual_machine.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'None')

    def test_vm_licenses_with_assignment(self):
        LicenseAssignment.objects.create(
            license=self.license,
            vendor=self.vendor,
            virtual_machine=self.virtual_machine,
            quantity=10,
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:virtualmachine_licenses_htmx',
            kwargs={'pk': self.virtual_machine.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VM Test License')
        self.assertContains(response, 'VM License Mfg')
        self.assertContains(response, 'VM License Vendor')
        self.assertContains(response, '10')

    def test_vm_licenses_assign_button(self):
        LicenseAssignment.objects.create(
            license=self.license,
            vendor=self.vendor,
            virtual_machine=self.virtual_machine,
        )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:virtualmachine_licenses_htmx',
            kwargs={'pk': self.virtual_machine.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assign License')
        self.assertContains(response, f'virtual_machine={self.virtual_machine.pk}')

    def test_vm_licenses_show_all_link(self):
        for i in range(MAX_LICENSE_DISPLAY + 1):
            lic = License.objects.create(
                manufacturer=self.manufacturer,
                name=f'VM Bulk License {i}',
            )
            LicenseAssignment.objects.create(
                license=lic,
                vendor=self.vendor,
                virtual_machine=self.virtual_machine,
            )

        self.client.force_login(self.user)
        url = reverse(
            'plugins:netbox_lifecycle:virtualmachine_licenses_htmx',
            kwargs={'pk': self.virtual_machine.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Show all Licenses')
