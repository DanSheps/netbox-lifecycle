from django.urls import reverse
from rest_framework import status

from dcim.models import Manufacturer, DeviceType, Module, ModuleBay, ModuleType
from dcim.choices import ModuleStatusChoices
from utilities.testing import APIViewTestCases, APITestCase, create_test_device

from netbox_lifecycle.models import *
from netbox_lifecycle.utilities.gfk_mixins import DateFieldMixin
from netbox_lifecycle.utilities.testing import create_test_module


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_lifecycle-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VendorTest(APIViewTestCases.APIViewTestCase):
    model = Vendor
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['display', 'id', 'name', 'url', ]

    create_data = [
        {
            'name': 'Vendor 4',
        },
        {
            'name': 'Vendor 5',
        },
        {
            'name': 'Vendor 6',
        },
    ]
    bulk_update_data = {
        'description': "A Vendor description"
    }

    @classmethod
    def setUpTestData(cls):
        vendors = [
            Vendor(name="Vendor 1"),
            Vendor(name="Vendor 2"),
            Vendor(name="Vendor 3"),
        ]
        Vendor.objects.bulk_create(vendors)


class LicenseTest(APIViewTestCases.APIViewTestCase):
    model = License
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['display', 'id', 'name', 'url', ]

    user_permissions = ('dcim.view_manufacturer',)

    bulk_update_data = {
        'description': "A License description"
    }

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Generic Manufacturer', slug='generic-manufacturer')
        licenses = [
            License(manufacturer=manufacturer, name='License 1'),
            License(manufacturer=manufacturer, name='License 2'),
            License(manufacturer=manufacturer, name='License 3'),
        ]
        License.objects.bulk_create(licenses)

        cls.create_data = [
            {
                'name': 'License 4',
                'manufacturer': manufacturer.pk,
            },
            {
                'name': 'License 5',
                'manufacturer': manufacturer.pk,
            },
            {
                'name': 'License 6',
                'manufacturer': manufacturer.pk,
            },
        ]


class LicenseAssignmentTest(APIViewTestCases.APIViewTestCase):
    model = LicenseAssignment
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['device', 'display', 'id', 'license', 'url', 'vendor']

    user_permissions = ('netbox_lifecycle.view_license', 'netbox_lifecycle.view_vendor', 'dcim.view_device', )

    bulk_update_data = {
        'description': "A licenseassignment description"
    }

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Vendor')
        manufacturer = Manufacturer.objects.create(name='Generic Manufacturer', slug='generic-manufacturer')
        device = create_test_device(name='Test Device')
        licenses = [
            License(manufacturer=manufacturer, name='License 1'),
            License(manufacturer=manufacturer, name='License 2'),
            License(manufacturer=manufacturer, name='License 3'),
            License(manufacturer=manufacturer, name='License 4'),
            License(manufacturer=manufacturer, name='License 5'),
            License(manufacturer=manufacturer, name='License 6'),
        ]

        License.objects.bulk_create(licenses)

        license_assignments = [
            LicenseAssignment(vendor=vendor, license=licenses[0], device=device),
            LicenseAssignment(vendor=vendor, license=licenses[1], device=device),
            LicenseAssignment(vendor=vendor, license=licenses[2], device=device),
        ]
        LicenseAssignment.objects.bulk_create(license_assignments)

        cls.create_data = [
            {
                'vendor': vendor.pk,
                'license': licenses[3].pk,
                'device': device.pk,
            },
            {
                'vendor': vendor.pk,
                'license': licenses[4].pk,
                'device': device.pk,
            },
            {
                'vendor': vendor.pk,
                'license': licenses[5].pk,
                'device': device.pk,
            },
        ]


class SupportSKUTest(APIViewTestCases.APIViewTestCase):
    model = SupportSKU
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['display', 'id', 'manufacturer', 'sku', 'url', ]

    user_permissions = ('dcim.view_manufacturer', )

    bulk_update_data = {
        'description': "A Support SKU description"
    }

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Generic Manufacturer', slug='generic-manufacturer')

        supportskus = [
            SupportSKU(sku='Support SKU 1', manufacturer=manufacturer),
            SupportSKU(sku='Support SKU 2', manufacturer=manufacturer),
            SupportSKU(sku='Support SKU 3', manufacturer=manufacturer),
        ]
        SupportSKU.objects.bulk_create(supportskus)

        cls.create_data = [
            {
                'sku': 'Support SKU 4',
                'manufacturer': manufacturer.pk,
            },
            {
                'sku': 'Support SKU 5',
                'manufacturer': manufacturer.pk,
            },
            {
                'sku': 'Support SKU 6',
                'manufacturer': manufacturer.pk,
            },
        ]


class SupportContractTest(APIViewTestCases.APIViewTestCase):
    model = SupportContract
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['contract_id', 'display', 'id', 'url', 'vendor', ]

    user_permissions = ('netbox_lifecycle.view_supportsku', 'netbox_lifecycle.view_vendor', )

    bulk_update_data = {
        'description': "A Support SKU description"
    }

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Vendor')

        supportcontract = [
            SupportContract(contract_id='NB1000-1', vendor=vendor),
            SupportContract(contract_id='NB1000-2', vendor=vendor),
            SupportContract(contract_id='NB1000-3', vendor=vendor),
        ]
        SupportContract.objects.bulk_create(supportcontract)

        cls.create_data = [
            {
                'contract_id': 'NB1000-4',
                'vendor': vendor.pk,
            },
            {
                'contract_id': 'NB1000-5',
                'vendor': vendor.pk,
            },
            {
                'contract_id': 'NB1000-6',
                'vendor': vendor.pk,
            },
        ]


class SupportContractAssignmentTest(APIViewTestCases.APIViewTestCase):
    model = SupportContractAssignment
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['contract', 'device', 'display', 'id', 'license', 'module', 'sku', 'url', ]

    user_permissions = ('netbox_lifecycle.view_supportcontract', 'netbox_lifecycle.view_vendor', 'dcim.view_device', 'dcim.view_module', )

    bulk_update_data = {
        'description': "A assignment description"
    }

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        vendor = Vendor.objects.create(name='Vendor')
        device = create_test_device(name='Test Device')
        module = create_test_module()

        sku = SupportSKU.objects.create(sku='SKU', manufacturer=manufacturer)

        contracts = [
            SupportContract(vendor=vendor, contract_id='NB1000-1'),
            SupportContract(vendor=vendor, contract_id='NB1000-2'),
            SupportContract(vendor=vendor, contract_id='NB1000-3'),
            SupportContract(vendor=vendor, contract_id='NB1000-4'),
            SupportContract(vendor=vendor, contract_id='NB1000-5'),
            SupportContract(vendor=vendor, contract_id='NB1000-6'),
            SupportContract(vendor=vendor, contract_id='NB1000-7'),
            SupportContract(vendor=vendor, contract_id='NB1000-8'),
        ]

        SupportContract.objects.bulk_create(contracts)

        assignments = [
            SupportContractAssignment(contract=contracts[0], device=device, sku=sku),
            SupportContractAssignment(contract=contracts[1], device=device, sku=sku),
            SupportContractAssignment(contract=contracts[2], module=module, sku=sku),
            SupportContractAssignment(contract=contracts[3], module=module, sku=sku),
        ]
        SupportContractAssignment.objects.bulk_create(assignments)

        cls.create_data = [
            {
                'contract': contracts[4].pk,
                'device': device.pk,
                'sku': sku.pk,
            },
            {
                'contract': contracts[5].pk,
                'device': device.pk,
                'sku': sku.pk,
            },
            {
                'contract': contracts[6].pk,
                'module': module.pk,
                'sku': sku.pk,
            },
            {
                'contract': contracts[7].pk,
                'module': module.pk,
                'sku': sku.pk,
            },
        ]


class HardwareLifecycleTest(DateFieldMixin, APIViewTestCases.APIViewTestCase):
    model = HardwareLifecycle
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = ['assigned_object_id', 'assigned_object_type', 'display', 'end_of_sale', 'id', 'url', ]

    user_permissions = ('dcim.view_devicetype', )

    bulk_update_data = {
        'description': "A assignment description"
    }

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='generic-manufacturer')
        device_types = [
            DeviceType(model='Device Type 1', manufacturer=manufacturer, slug='device-type-1'),
            DeviceType(model='Device Type 2', manufacturer=manufacturer, slug='device-type-2'),
            DeviceType(model='Device Type 3', manufacturer=manufacturer, slug='device-type-3'),
            DeviceType(model='Device Type 4', manufacturer=manufacturer, slug='device-type-4'),
            DeviceType(model='Device Type 5', manufacturer=manufacturer, slug='device-type-5'),
            DeviceType(model='Device Type 6', manufacturer=manufacturer, slug='device-type-6'),
        ]

        DeviceType.objects.bulk_create(device_types)

        hardware_lifecycles = [
            HardwareLifecycle(
                assigned_object=device_types[0], end_of_sale='2030-01-01', end_of_support='2030-01-01'
            ),
            HardwareLifecycle(
                assigned_object=device_types[1], end_of_sale='2030-01-01', end_of_support='2040-01-01'
            ),
            HardwareLifecycle(
                assigned_object=device_types[2], end_of_sale='2030-01-01', end_of_support='2050-01-01'
            ),
        ]
        HardwareLifecycle.objects.bulk_create(hardware_lifecycles)

        cls.create_data = [
            {
                'assigned_object_id': device_types[3].pk,
                'assigned_object_type': 'dcim.devicetype',
                'end_of_sale': '2030-01-01',
                'end_of_support': '2030-01-01'
            },
            {
                'assigned_object_id': device_types[4].pk,
                'assigned_object_type': 'dcim.devicetype',
                'end_of_sale': '2030-01-01',
                'end_of_support': '2040-01-01'
            },
            {
                'assigned_object_id': device_types[5].pk,
                'assigned_object_type': 'dcim.devicetype',
                'end_of_sale': '2030-01-01',
                'end_of_support': '2050-01-01'
            },
        ]
