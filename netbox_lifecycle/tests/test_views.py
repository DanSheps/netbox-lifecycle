from dcim.models import Manufacturer, DeviceType, ModuleType
from netbox_lifecycle.utilities.gfk_mixins import HardwareLifecycleViewMixin
from netbox_lifecycle.utilities.testing import create_test_vendor
from utilities.testing import ViewTestCases, create_test_device

from netbox_lifecycle.models import *


class VendorTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = Vendor

    @classmethod
    def setUpTestData(cls):

        vendors = (
            Vendor(name='Vendor 1'),
            Vendor(name='Vendor 2'),
            Vendor(name='Vendor 3'),
        )
        Vendor.objects.bulk_create(vendors)

        cls.form_data = {
            'name': 'Vendor X',
        }

        cls.bulk_edit_data = {
            'description': "A Vendor Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:vendor_{}'


class LicenseTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = License

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer')

        licenses = (
            License(name='License 1', manufacturer=manufacturer),
            License(name='License 2', manufacturer=manufacturer),
            License(name='License 3', manufacturer=manufacturer),
        )
        License.objects.bulk_create(licenses)

        cls.form_data = {'name': 'License X', 'manufacturer': manufacturer.pk}

        cls.bulk_edit_data = {
            'description': "A Vendor Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:license_{}'


class LicenseAssignmentTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = LicenseAssignment

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer')
        device = create_test_device(name='Test Device')
        vendor = create_test_vendor(name='Vendor')

        licenses = (
            License(name='License 1', manufacturer=manufacturer),
            License(name='License 2', manufacturer=manufacturer),
            License(name='License 3', manufacturer=manufacturer),
        )
        License.objects.bulk_create(licenses)

        assignments = (
            LicenseAssignment(license=license, vendor=vendor, device=device)
            for license in licenses
        )
        LicenseAssignment.objects.bulk_create(assignments)

        license = License.objects.create(name='License X', manufacturer=manufacturer)

        cls.form_data = {
            'license': license.pk,
            'vendor': vendor.pk,
            'device': device.pk,
        }

        cls.bulk_edit_data = {
            'description': "A Vendor Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:licenseassignment_{}'


class SupportContractTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = SupportContract

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Vendor')
        contracts = (
            SupportContract(vendor=vendor, contract_id='Contract-123'),
            SupportContract(vendor=vendor, contract_id='Contract-456'),
            SupportContract(vendor=vendor, contract_id='Contract-789'),
        )
        SupportContract.objects.bulk_create(contracts)

        cls.form_data = {
            'vendor': vendor.pk,
            'contract_id': 'Contract X',
        }

        cls.bulk_edit_data = {
            'description': "A Contract Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:supportcontract_{}'


class SupportSKUTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = SupportSKU

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer')
        skus = (
            SupportSKU(manufacturer=manufacturer, sku='SKU-123'),
            SupportSKU(manufacturer=manufacturer, sku='SKU-456'),
            SupportSKU(manufacturer=manufacturer, sku='SKU-789'),
        )
        SupportSKU.objects.bulk_create(skus)

        cls.form_data = {
            'manufacturer': manufacturer.pk,
            'sku': 'SKU X',
        }

        cls.bulk_edit_data = {
            'description': "A Contract Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:supportsku_{}'


class SupportContractAssignmentTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = SupportContractAssignment

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        manufacturer = Manufacturer.objects.create(name='Manufacturer')
        vendor = Vendor.objects.create(name='Vendor')
        sku = SupportSKU.objects.create(manufacturer=manufacturer, sku='SKU-123')
        license = License.objects.create(name='License 1', manufacturer=manufacturer)
        la = LicenseAssignment.objects.create(
            license=license, vendor=vendor, device=device
        )

        contracts = (
            SupportContract(vendor=vendor, contract_id='Contract-123'),
            SupportContract(vendor=vendor, contract_id='Contract-456'),
            SupportContract(vendor=vendor, contract_id='Contract-789'),
        )
        SupportContract.objects.bulk_create(contracts)

        sc_assignments = (
            SupportContractAssignment(
                contract=contract, sku=sku, license=la, device=device
            )
            for contract in contracts
        )
        SupportContractAssignment.objects.bulk_create(sc_assignments)

        contract = SupportContract.objects.create(
            vendor=vendor, contract_id='Contract-X'
        )

        cls.form_data = {
            'contract': contract.pk,
            'sku': sku.pk,
            'license': la.pk,
            'device': device.pk,
        }

        cls.bulk_edit_data = {
            'description': "A Contract Assignment Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:supportcontractassignment_{}'


class HardwareLifecycleTestCase(
    HardwareLifecycleViewMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = HardwareLifecycle

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer", slug="manufacturer"
        )
        device_types = (
            DeviceType(
                manufacturer=manufacturer, model='Device Type 1', slug="device-type-1"
            ),
            DeviceType(
                manufacturer=manufacturer, model='Device Type 2', slug="device-type-2"
            ),
        )
        DeviceType.objects.bulk_create(device_types)

        module_types = (
            ModuleType(manufacturer=manufacturer, model='Module Type 1'),
            ModuleType(manufacturer=manufacturer, model='Module Type 2'),
        )
        ModuleType.objects.bulk_create(module_types)

        lifecycles = (
            HardwareLifecycle(
                assigned_object=device_types[0],
                end_of_sale='2025-01-01',
                end_of_support='2030-01-01',
            ),
            HardwareLifecycle(
                assigned_object=device_types[1],
                end_of_sale='2025-01-01',
                end_of_support='2030-01-01',
            ),
            HardwareLifecycle(
                assigned_object=module_types[0],
                end_of_sale='2025-01-01',
                end_of_support='2030-01-01',
            ),
            HardwareLifecycle(
                assigned_object=module_types[1],
                end_of_sale='2025-01-01',
                end_of_support='2030-01-01',
            ),
        )
        HardwareLifecycle.objects.bulk_create(lifecycles)

        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model='Device Type X', slug='device-type-x'
        )

        cls.form_data = {
            'device_type': device_type.pk,
            'end_of_sale': '2025-01-01',
            'end_of_support': '2025-01-01',
        }

        cls.bulk_edit_data = {
            'description': "A Contract Description",
        }

    def _get_base_url(self):
        return 'plugins:netbox_lifecycle:hardwarelifecycle_{}'
