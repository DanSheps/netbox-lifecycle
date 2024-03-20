import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from dcim.models import Manufacturer, Site, DeviceRole, DeviceType, Device
from netbox_lifecycle.models import (
    Vendor, SupportContract, SupportSKU, SupportContractAssignment, License, LicenseAssignment
)


class SupportContractTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        vendors = (
            Vendor(name='Vendor 1'),
            Vendor(name='Vendor 2'),
        )
        Vendor.objects.bulk_create(vendors)

    def test_contract_creation(self):
        contract = SupportContract(
            vendor=Vendor.objects.first(),
            contract_id='1234',
            start=datetime.date.today(),
            renewal=datetime.date.today() + datetime.timedelta(days=1),
            end=datetime.date.today() + datetime.timedelta(days=2)
        )
        contract.full_clean()
        contract.save()

    def test_supportcontract_duplicate_ids(self):
        contract1 = SupportContract(
            vendor=Vendor.objects.first(),
            contract_id='1234',
        )
        contract1.clean()
        contract1.save()

        contract2 = SupportContract(
            vendor=Vendor.objects.first(),
            contract_id='1234',
        )

        # Two support contracts assigned to the same Vendor with the same contract_id should fail validation
        with self.assertRaises(ValidationError):
            contract2.full_clean()

        # Two support contracts assigned to the different Vendors with the same contract_id should pass validation
        contract2.vendor = Vendor.objects.last()
        contract2.full_clean()
        contract2.save()

        # Two support contracts assigned to the different contract_id should pass validation
        contract2.vendor = Vendor.objects.first()
        contract2.contract_id = '5678'
        contract2.full_clean()
        contract2.save()


class SupportSKUTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        manufacturers = (
            Manufacturer(name='Manufacturer 1', slug='manufacturer-1'),
            Manufacturer(name='Manufacturer 2', slug='manufacturer-2'),
        )
        Manufacturer.objects.bulk_create(manufacturers)

    def test_contract_creation(self):
        sku = SupportSKU(
            manufacturer=Manufacturer.objects.first(),
            sku='Support-1',
        )
        sku.full_clean()
        sku.save()

    def test_supportcontract_duplicate_ids(self):
        sku1 = SupportSKU(
            manufacturer=Manufacturer.objects.first(),
            sku='Support-1',
        )
        sku1.clean()
        sku1.save()

        sku2 = SupportSKU(
            manufacturer=Manufacturer.objects.first(),
            sku='Support-1',
        )

        # Two support contracts assigned to the same Manufacturer with the same sku should fail validation
        with self.assertRaises(ValidationError):
            sku2.full_clean()

        # Two support contracts assigned to the different Vendors with the same contract_id should pass validation
        sku2.manufacturer = Manufacturer.objects.last()
        sku2.full_clean()
        sku2.save()

        # Two support contracts assigned to the different contract_id should pass validation
        sku2.manufacturer = Manufacturer.objects.first()
        sku2.sku = 'Support-2'
        sku2.full_clean()
        sku2.save()


class SupportContractAssignmentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer 1', slug='manufacturer-1')
        site = Site.objects.create(name='Test Site', slug='test-site')
        role = DeviceRole.objects.create(name='Test Role', slug='test-role')
        device_type = DeviceType.objects.create(
            model='Test DeviceType', slug='test-devicetype', manufacturer=manufacturer
        )
        device = Device.objects.create(name='Test Device 1', device_type=device_type, role=role, site=site)

        vendor = Vendor.objects.create(name='Vendor 1')
        license = License.objects.create(manufacturer=manufacturer, name='Test License')

        skus = (
            SupportSKU(
                manufacturer=manufacturer,
                sku='SKU 1',
            ),
            SupportSKU(
                manufacturer=manufacturer,
                sku='SKU 2',
            ),
        )
        SupportSKU.objects.bulk_create(skus)

        contract = SupportContract.objects.create(
            vendor=Vendor.objects.first(),
            contract_id='1234',
            start=datetime.date.today(),
            renewal=datetime.date.today() + datetime.timedelta(days=1),
            end=datetime.date.today() + datetime.timedelta(days=2)
        )

        LicenseAssignment.objects.create(
            license=license,
            vendor=vendor,
            device=device,
            quantity=1
        )

    def test_contractassignment_creation(self):
        contract = SupportContract.objects.first()
        sku = SupportSKU.objects.first()
        device = Device.objects.first()
        license = LicenseAssignment.objects.first()

        contract = SupportContractAssignment(
            contract=contract,
            sku=sku,
            device=device
        )
        contract.full_clean()
        contract.save()

    def test_supportcontract_duplicate_ids(self):
        contract = SupportContract.objects.first()
        sku = SupportSKU.objects.first()
        device = Device.objects.first()
        license = LicenseAssignment.objects.first()

        contract1 = SupportContractAssignment(
            contract=contract,
            sku=sku,
            device=device
        )
        contract1.full_clean()
        contract1.save()

        contract2 = SupportContractAssignment(
            contract=contract,
            sku=sku,
            device=device
        )

        with self.assertRaises(ValidationError):
            contract2.full_clean()

        contract2.license = license
        contract2.full_clean()
        contract2.save()
