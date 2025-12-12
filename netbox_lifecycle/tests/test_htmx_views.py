from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site

from netbox_lifecycle.models import (
    License,
    LicenseAssignment,
    SupportContract,
    SupportContractAssignment,
    SupportSKU,
    Vendor,
)


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
            end=date.today() + timedelta(days=30),
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
            end=date.today() - timedelta(days=1),
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
            end=date.today() + timedelta(days=30),
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
            start=date.today() + timedelta(days=30),
            end=date.today() + timedelta(days=365),
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
            start=date.today() - timedelta(days=30),
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
            end=date.today() + timedelta(days=30),
        )
        SupportContractAssignment.objects.create(
            contract=active_contract, device=self.device
        )

        # Future contract
        future_contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='FUTURE-MULTI',
            start=date.today() + timedelta(days=30),
            end=date.today() + timedelta(days=365),
        )
        SupportContractAssignment.objects.create(
            contract=future_contract, device=self.device
        )

        # Expired contract
        expired_contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='EXPIRED-MULTI',
            end=date.today() - timedelta(days=1),
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
            end=date.today() + timedelta(days=30),
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
            end=date.today() - timedelta(days=1),
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
