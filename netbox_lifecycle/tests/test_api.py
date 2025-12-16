from django.urls import reverse
from rest_framework import status

from dcim.models import Manufacturer, DeviceType, Module, ModuleBay, ModuleType
from extras.models import Tag
from virtualization.models import Cluster, ClusterType, VirtualMachine
from utilities.testing import APIViewTestCases, APITestCase, create_test_device

from netbox_lifecycle.models import *
from netbox_lifecycle.utilities.gfk_mixins import DateFieldMixin


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_lifecycle-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VendorTest(APIViewTestCases.APIViewTestCase):
    model = Vendor
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = [
        'display',
        'id',
        'name',
        'url',
    ]

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
    bulk_update_data = {'description': "A Vendor description"}

    @classmethod
    def setUpTestData(cls):
        vendors = [
            Vendor(name="Vendor 1"),
            Vendor(name="Vendor 2"),
            Vendor(name="Vendor 3"),
        ]
        Vendor.objects.bulk_create(vendors)

    def test_create_vendor_with_tags(self):
        """Test creating a vendor with tags via the API."""
        self.add_permissions('netbox_lifecycle.add_vendor')
        Tag.objects.create(name='Test Tag', slug='test-tag')
        url = reverse('plugins-api:netbox_lifecycle-api:vendor-list')
        data = {
            'name': 'Vendor with Tags',
            'tags': [{'name': 'Test Tag'}],
        }
        response = self.client.post(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['tags']), 1)
        self.assertEqual(response.data['tags'][0]['name'], 'Test Tag')


class LicenseTest(APIViewTestCases.APIViewTestCase):
    model = License
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = [
        'display',
        'id',
        'name',
        'url',
    ]

    user_permissions = ('dcim.view_manufacturer',)

    bulk_update_data = {'description': "A License description"}

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name='Generic Manufacturer', slug='generic-manufacturer'
        )
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
    brief_fields = [
        'device',
        'display',
        'id',
        'license',
        'url',
        'vendor',
        'virtual_machine',
    ]

    user_permissions = (
        'netbox_lifecycle.view_license',
        'netbox_lifecycle.view_vendor',
        'dcim.view_device',
        'virtualization.view_virtualmachine',
    )

    bulk_update_data = {'description': "A licenseassignment description"}

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Vendor')
        manufacturer = Manufacturer.objects.create(
            name='Generic Manufacturer', slug='generic-manufacturer'
        )
        device = create_test_device(name='Test Device')

        # Create VM fixtures
        cluster_type = ClusterType.objects.create(
            name='Test Cluster Type', slug='test-cluster-type'
        )
        cluster = Cluster.objects.create(name='Test Cluster', type=cluster_type)
        cls.vm = VirtualMachine.objects.create(name='Test VM', cluster=cluster)

        licenses = [
            License(manufacturer=manufacturer, name='License 1'),
            License(manufacturer=manufacturer, name='License 2'),
            License(manufacturer=manufacturer, name='License 3'),
            License(manufacturer=manufacturer, name='License 4'),
            License(manufacturer=manufacturer, name='License 5'),
            License(manufacturer=manufacturer, name='License 6'),
            License(manufacturer=manufacturer, name='License 7'),
        ]

        License.objects.bulk_create(licenses)
        cls.licenses = licenses
        cls.vendor = vendor

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

    def test_create_license_assignment_with_vm(self):
        """Test creating a license assignment with a virtual machine"""
        self.add_permissions('netbox_lifecycle.add_licenseassignment')
        url = reverse('plugins-api:netbox_lifecycle-api:licenseassignment-list')
        data = {
            'vendor': self.vendor.pk,
            'license': self.licenses[6].pk,
            'virtual_machine': self.vm.pk,
        }
        response = self.client.post(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['virtual_machine']['id'], self.vm.pk)


class SupportSKUTest(APIViewTestCases.APIViewTestCase):
    model = SupportSKU
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = [
        'display',
        'id',
        'manufacturer',
        'sku',
        'url',
    ]

    user_permissions = ('dcim.view_manufacturer',)

    bulk_update_data = {'description': "A Support SKU description"}

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name='Generic Manufacturer', slug='generic-manufacturer'
        )

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
    brief_fields = [
        'contract_id',
        'display',
        'id',
        'url',
        'vendor',
    ]

    user_permissions = (
        'netbox_lifecycle.view_supportsku',
        'netbox_lifecycle.view_vendor',
    )

    bulk_update_data = {'description': "A Support SKU description"}

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
    brief_fields = [
        'contract',
        'device',
        'display',
        'id',
        'license',
        'module',
        'sku',
        'url',
        'virtual_machine',
    ]

    user_permissions = (
        'netbox_lifecycle.view_supportcontract',
        'netbox_lifecycle.view_vendor',
        'dcim.view_device',
        'dcim.view_module',
        'virtualization.view_virtualmachine',
    )

    bulk_update_data = {'description': "A assignment description"}

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name='Manufacturer', slug='manufacturer'
        )
        vendor = Vendor.objects.create(name='Vendor')
        device = create_test_device(name='Test Device')

        # Create module fixtures
        module_type = ModuleType.objects.create(
            manufacturer=manufacturer, model='Test Module Type'
        )
        module_bay = ModuleBay.objects.create(device=device, name='Module Bay 1')
        module = Module.objects.create(
            device=device, module_bay=module_bay, module_type=module_type
        )
        cls.module = module

        # Create VM fixtures
        cluster_type = ClusterType.objects.create(
            name='Test Cluster Type', slug='test-cluster-type'
        )
        cluster = Cluster.objects.create(name='Test Cluster', type=cluster_type)
        cls.vm = VirtualMachine.objects.create(name='Test VM', cluster=cluster)

        sku = SupportSKU.objects.create(sku='SKU', manufacturer=manufacturer)

        contracts = [
            SupportContract(vendor=vendor, contract_id='NB1000-1'),
            SupportContract(vendor=vendor, contract_id='NB1000-2'),
            SupportContract(vendor=vendor, contract_id='NB1000-3'),
            SupportContract(vendor=vendor, contract_id='NB1000-4'),
            SupportContract(vendor=vendor, contract_id='NB1000-5'),
            SupportContract(vendor=vendor, contract_id='NB1000-6'),
            SupportContract(vendor=vendor, contract_id='NB1000-7'),
        ]

        SupportContract.objects.bulk_create(contracts)
        cls.contracts = contracts

        assignments = [
            SupportContractAssignment(contract=contracts[0], device=device, sku=sku),
            SupportContractAssignment(contract=contracts[1], device=device, sku=sku),
            SupportContractAssignment(contract=contracts[2], device=device, sku=sku),
        ]
        SupportContractAssignment.objects.bulk_create(assignments)

        cls.create_data = [
            {
                'contract': contracts[3].pk,
                'device': device.pk,
                'sku': sku.pk,
            },
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
        ]

    def test_create_support_contract_assignment_with_module(self):
        """Test creating a support contract assignment with a module"""
        self.add_permissions('netbox_lifecycle.add_supportcontractassignment')
        contract = SupportContract.objects.first()
        url = reverse('plugins-api:netbox_lifecycle-api:supportcontractassignment-list')
        data = {
            'contract': contract.pk,
            'module': self.module.pk,
        }
        response = self.client.post(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['module']['id'], self.module.pk)

    def test_create_support_contract_assignment_with_vm(self):
        """Test creating a support contract assignment with a virtual machine"""
        self.add_permissions('netbox_lifecycle.add_supportcontractassignment')
        url = reverse('plugins-api:netbox_lifecycle-api:supportcontractassignment-list')
        data = {
            'contract': self.contracts[6].pk,
            'virtual_machine': self.vm.pk,
        }
        response = self.client.post(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['virtual_machine']['id'], self.vm.pk)


class HardwareLifecycleTest(DateFieldMixin, APIViewTestCases.APIViewTestCase):
    model = HardwareLifecycle
    view_namespace = "plugins-api:netbox_lifecycle"
    brief_fields = [
        'assigned_object_id',
        'assigned_object_type',
        'display',
        'end_of_sale',
        'id',
        'url',
    ]

    user_permissions = ('dcim.view_devicetype',)

    bulk_update_data = {'description': "A assignment description"}

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name='Manufacturer', slug='generic-manufacturer'
        )
        device_types = [
            DeviceType(
                model='Device Type 1', manufacturer=manufacturer, slug='device-type-1'
            ),
            DeviceType(
                model='Device Type 2', manufacturer=manufacturer, slug='device-type-2'
            ),
            DeviceType(
                model='Device Type 3', manufacturer=manufacturer, slug='device-type-3'
            ),
            DeviceType(
                model='Device Type 4', manufacturer=manufacturer, slug='device-type-4'
            ),
            DeviceType(
                model='Device Type 5', manufacturer=manufacturer, slug='device-type-5'
            ),
            DeviceType(
                model='Device Type 6', manufacturer=manufacturer, slug='device-type-6'
            ),
        ]

        DeviceType.objects.bulk_create(device_types)

        hardware_lifecycles = [
            HardwareLifecycle(
                assigned_object=device_types[0],
                end_of_sale='2030-01-01',
                end_of_support='2030-01-01',
            ),
            HardwareLifecycle(
                assigned_object=device_types[1],
                end_of_sale='2030-01-01',
                end_of_support='2040-01-01',
            ),
            HardwareLifecycle(
                assigned_object=device_types[2],
                end_of_sale='2030-01-01',
                end_of_support='2050-01-01',
            ),
        ]
        HardwareLifecycle.objects.bulk_create(hardware_lifecycles)

        cls.create_data = [
            {
                'assigned_object_id': device_types[3].pk,
                'assigned_object_type': 'dcim.devicetype',
                'end_of_sale': '2030-01-01',
                'end_of_support': '2030-01-01',
            },
            {
                'assigned_object_id': device_types[4].pk,
                'assigned_object_type': 'dcim.devicetype',
                'end_of_sale': '2030-01-01',
                'end_of_support': '2040-01-01',
            },
            {
                'assigned_object_id': device_types[5].pk,
                'assigned_object_type': 'dcim.devicetype',
                'end_of_sale': '2030-01-01',
                'end_of_support': '2050-01-01',
            },
        ]

        # Additional device types for null date tests
        cls.device_type_for_null_test = DeviceType.objects.create(
            model='Device Type Null Test',
            manufacturer=manufacturer,
            slug='device-type-null',
        )
        cls.device_type_for_explicit_null = DeviceType.objects.create(
            model='Device Type Explicit Null',
            manufacturer=manufacturer,
            slug='device-type-explicit-null',
        )
        cls.device_type_for_update_null = DeviceType.objects.create(
            model='Device Type Update Null',
            manufacturer=manufacturer,
            slug='device-type-update-null',
        )

    def test_create_lifecycle_with_omitted_dates(self):
        """Test creating a hardware lifecycle with omitted date fields."""
        self.add_permissions('netbox_lifecycle.add_hardwarelifecycle')
        url = reverse('plugins-api:netbox_lifecycle-api:hardwarelifecycle-list')
        data = {
            'assigned_object_id': self.device_type_for_null_test.pk,
            'assigned_object_type': 'dcim.devicetype',
        }
        response = self.client.post(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['end_of_sale'])
        self.assertIsNone(response.data['end_of_support'])
        self.assertIsNone(response.data['end_of_maintenance'])
        self.assertIsNone(response.data['end_of_security'])

    def test_create_lifecycle_with_explicit_null_dates(self):
        """Test creating a hardware lifecycle with explicit null values for dates."""
        self.add_permissions('netbox_lifecycle.add_hardwarelifecycle')
        url = reverse('plugins-api:netbox_lifecycle-api:hardwarelifecycle-list')
        data = {
            'assigned_object_id': self.device_type_for_explicit_null.pk,
            'assigned_object_type': 'dcim.devicetype',
            'end_of_sale': None,
            'end_of_support': None,
            'end_of_maintenance': None,
            'end_of_security': None,
        }
        response = self.client.post(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['end_of_sale'])
        self.assertIsNone(response.data['end_of_support'])
        self.assertIsNone(response.data['end_of_maintenance'])
        self.assertIsNone(response.data['end_of_security'])

    def test_update_lifecycle_dates_to_null(self):
        """Test updating a hardware lifecycle to set dates to null."""
        self.add_permissions('netbox_lifecycle.change_hardwarelifecycle')
        # Create lifecycle with dates
        lifecycle = HardwareLifecycle.objects.create(
            assigned_object=self.device_type_for_update_null,
            end_of_sale='2030-01-01',
            end_of_support='2035-01-01',
        )
        url = reverse(
            'plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail',
            kwargs={'pk': lifecycle.pk},
        )
        data = {
            'end_of_sale': None,
            'end_of_support': None,
        }
        response = self.client.patch(url, data, format='json', **self.header)
        self.assertHttpStatus(response, status.HTTP_200_OK)
        self.assertIsNone(response.data['end_of_sale'])
        self.assertIsNone(response.data['end_of_support'])
