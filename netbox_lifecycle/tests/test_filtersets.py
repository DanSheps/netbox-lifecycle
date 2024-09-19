from django.test import TestCase

from dcim.models import Manufacturer, Device, DeviceType, ModuleType
from utilities.testing import create_test_device

from netbox_lifecycle.filtersets import *
from netbox_lifecycle.models import *

from netbox_lifecycle.utilities.testing import *


class VendorTestCase(TestCase):
    queryset = Vendor.objects.all()
    filterset = VendorFilterSet

    @classmethod
    def setUpTestData(cls):
        vendors = (
            Vendor(name="Vendor 1"),
            Vendor(name="Vendor 2"),
            Vendor(name="Vendor 3"),
        )
        Vendor.objects.bulk_create(vendors)

    def test_q(self):
        params = {'q': 'Vendor 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {'name': ['Vendor 1', 'Vendor 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class SupportSKUTestCase(TestCase):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet

    @classmethod
    def setUpTestData(cls):
        manufacturers = (
            Manufacturer(name="Manufacturer 1", slug="manufacturer-1"),
            Manufacturer(name="Manufacturer 2", slug="manufacturer-2"),
        )
        Manufacturer.objects.bulk_create(manufacturers)

        skus = (
            create_test_supportsku(sku='Support 1', manufacturer=manufacturers[0]),
            create_test_supportsku(sku='Support 2', manufacturer=manufacturers[0]),
            create_test_supportsku(sku='Support 3', manufacturer=manufacturers[1]),
        )

    def test_q(self):
        params = {'q': 'Support 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_sku(self):
        params = {'sku': ['Support 1', 'Support 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.get(name='Manufacturer 1')

        params = {'manufacturer': [manufacturer.slug, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'manufacturer_id': [manufacturer.pk, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class SupportContractTestCase(TestCase):
    queryset = SupportContract.objects.all()
    filterset = SupportContractFilterSet

    @classmethod
    def setUpTestData(cls):
        vendors = (
            create_test_vendor('Vendor 1'),
            create_test_vendor('Vendor 2'),
        )

        contracts = (
            create_test_supportcontract(contract_id='Contract 1', vendor=vendors[0]),
            create_test_supportcontract(contract_id='Contract 2', vendor=vendors[0]),
            create_test_supportcontract(contract_id='Contract 3', vendor=vendors[1]),
        )

    def test_q(self):
        params = {'q': 'Contract 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_contract_id(self):
        params = {'contract_id': ['Contract 1', 'Contract 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_vendor(self):
        vendor = Vendor.objects.first()

        params = {'vendor': [vendor.name, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'vendor_id': [vendor.pk, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class SupportContractAssignmentTestCase(TestCase):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        vendor = create_test_vendor()
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        device = create_test_device(name='Device')
        license = License.objects.create(name='License', manufacturer=manufacturer)
        license_assignment = LicenseAssignment.objects.create(license=license, vendor=vendor)

        skus = (
            create_test_supportsku(sku='SKU 1', manufacturer=manufacturer),
            create_test_supportsku(sku='SKU 2', manufacturer=manufacturer),
            create_test_supportsku(sku='SKU 3', manufacturer=manufacturer),
            create_test_supportsku(sku='SKU 4', manufacturer=manufacturer),
        )

        contracts = (
            create_test_supportcontract(contract_id='Contract 1', vendor=vendor),
            create_test_supportcontract(contract_id='Contract 2', vendor=vendor),
            create_test_supportcontract(contract_id='Contract 3', vendor=vendor),
        )

        assignments = (
            SupportContractAssignment(contract=contracts[0], sku=skus[0]),
            SupportContractAssignment(contract=contracts[0], sku=skus[1]),
            SupportContractAssignment(contract=contracts[1], sku=skus[0], device=device),
            SupportContractAssignment(contract=contracts[1], sku=skus[1], device=device),
            SupportContractAssignment(contract=contracts[2], sku=skus[2], license=license_assignment),
            SupportContractAssignment(contract=contracts[2], sku=skus[3], license=license_assignment),
        )
        SupportContractAssignment.objects.bulk_create(assignments)

    def test_q(self):
        params = {'q': 'Contract 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_contract(self):
        contract = SupportContract.objects.first()

        params = {'contract_id': [contract.pk, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'contract': [contract.contract_id, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_sku(self):
        sku = SupportSKU.objects.first()

        params = {'sku_id': [sku.pk, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'sku': [sku.sku, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_device(self):
        device = Device.objects.first()

        params = {'device_id': [device.pk, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'device': [device.name, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_device(self):
        device = Device.objects.first()

        params = {'device_id': [device.pk, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'device': [device.name, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_license(self):
        license = License.objects.first()

        params = {'license': [license.name, ]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class LicenseTestCase(TestCase):
    queryset = License.objects.all()
    filterset = LicenseFilterSet

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", slug="manufacturer")
        licenses = (
            License(name="License 1", manufacturer=manufacturer),
            License(name="License 2", manufacturer=manufacturer),
            License(name="License 3", manufacturer=manufacturer),
        )
        License.objects.bulk_create(licenses)

    def test_q(self):
        params = {'q': 'License 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {'name': ['License 1', 'License 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class LicenseAssignmentTestCase(TestCase):
    queryset = LicenseAssignment.objects.all()
    filterset = LicenseAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", slug="manufacturer")
        vendors = (
            create_test_vendor(name='Vendor 1'),
            create_test_vendor(name='Vendor 2'),
            create_test_vendor(name='Vendor 3'),
        )

        devices = (
            create_test_device(name='Device 1'),
            create_test_device(name='Device 2'),
        )

        licenses = (
            License(name="License 1", manufacturer=manufacturer),
            License(name="License 2", manufacturer=manufacturer),
            License(name="License 3", manufacturer=manufacturer),
            License(name="License 4", manufacturer=manufacturer),
            License(name="License 5", manufacturer=manufacturer),
        )
        License.objects.bulk_create(licenses)

        assignments = (
            LicenseAssignment(license=licenses[0], vendor=vendors[0]),
            LicenseAssignment(license=licenses[1], vendor=vendors[1]),
            LicenseAssignment(license=licenses[2], vendor=vendors[2]),
            LicenseAssignment(license=licenses[3], vendor=vendors[2], device=devices[0]),
            LicenseAssignment(license=licenses[4], vendor=vendors[2], device=devices[1]),
        )
        LicenseAssignment.objects.bulk_create(assignments)

    def test_q(self):
        params = {'q': 'License 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_license(self):
        assigned_objects = License.objects.all()[0:2]

        params = {'license_id': [assigned_objects[0].pk, assigned_objects[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'license': [assigned_objects[0].name, assigned_objects[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_vendor(self):
        assigned_objects = Vendor.objects.all()[0:2]

        params = {'vendor_id': [assigned_objects[0].pk, assigned_objects[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'vendor': [assigned_objects[0].name, assigned_objects[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_device(self):
        assigned_objects = Device.objects.all()[0:2]

        params = {'device_id': [assigned_objects[0].pk, assigned_objects[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'device': [assigned_objects[0].name, assigned_objects[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class HardwareLifecycleTestCase(TestCase):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", slug="manufacturer")
        device_types = (
            DeviceType(manufacturer=manufacturer, model='Device Type 1', slug='device-type-1'),
            DeviceType(manufacturer=manufacturer, model='Device Type 2', slug='device-type-2'),
        )
        DeviceType.objects.bulk_create(device_types)

        module_types = (
            ModuleType(manufacturer=manufacturer, model='Module Type 1'),
            ModuleType(manufacturer=manufacturer, model='Module Type 2'),
        )
        ModuleType.objects.bulk_create(module_types)

        lifecycles = (
            HardwareLifecycle(assigned_object=device_types[0], end_of_sale='2025-01-01', end_of_support='2030-01-01'),
            HardwareLifecycle(assigned_object=device_types[1], end_of_sale='2025-01-01', end_of_support='2030-01-01'),
            HardwareLifecycle(assigned_object=module_types[0], end_of_sale='2025-01-01', end_of_support='2030-01-01'),
            HardwareLifecycle(assigned_object=module_types[1], end_of_sale='2025-01-01', end_of_support='2030-01-01'),
        )
        HardwareLifecycle.objects.bulk_create(lifecycles)

    def test_q(self):
        params = {'q': 'Device Type 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_device_type(self):
        assigned_objects = DeviceType.objects.all()[0:2]

        params = {'device_type_id': [assigned_objects[0].pk, assigned_objects[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'device_type': [assigned_objects[0].model, assigned_objects[1].model]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_module_type(self):
        assigned_objects = ModuleType.objects.all()[0:2]

        params = {'module_type_id': [assigned_objects[0].pk, assigned_objects[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'module_type': [assigned_objects[0].model, assigned_objects[1].model]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
