from django.test import TestCase

from dcim.models import Device, Manufacturer
from utilities.testing import create_test_device

from netbox_lifecycle.forms import *
from netbox_lifecycle.models import *


class VendorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_vendor(self):
        form = VendorForm(data={
            'name': 'Vendor 1',
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class LicenseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')

    def test_license(self):
        form = LicenseForm(data={
            'name': 'License 1',
            'manufacturer': Manufacturer.objects.first().pk
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class LicenseAssignmentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        create_test_device(name='Device')
        Vendor.objects.create(name='Vendor')
        License.objects.create(manufacturer=manufacturer, name='License')

    def test_assignment(self):
        form = LicenseAssignmentForm(data={
            'license': License.objects.first().pk,
            'vendor': Vendor.objects.first().pk,
            'device': Device.objects.first().pk,
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class SupportContractTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Vendor')

    def test_contract(self):
        form = SupportContractForm(data={
            'contract_id': 'Contract-1',
            'vendor': Vendor.objects.first().pk
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class SupportSKUTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')

    def test_sku(self):
        form = SupportSKUForm(data={
            'sku': 'SKU-1',
            'manufacturer': Manufacturer.objects.first().pk
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class SupportContractAssignmentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Vendor')
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        device = create_test_device(name='Test Device')
        SupportSKU.objects.create(manufacturer=manufacturer, sku='SKU-1')
        SupportContract.objects.create(vendor=vendor, contract_id='Contract')
        license = License.objects.create(manufacturer=manufacturer)
        license_assignment = LicenseAssignment.objects.create(license=license, vendor=vendor, device=device)

    def test_assignment_fail_without_device_or_license(self):
        form = SupportContractAssignmentForm(data={
            'contract': SupportContract.objects.first().pk,
            'sku': SupportSKU.objects.first().pk,
            'vendor': Vendor.objects.first().pk,
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_assignment_with_device(self):
        form = SupportContractAssignmentForm(data={
            'contract': SupportContract.objects.first().pk,
            'sku': SupportSKU.objects.first().pk,
            'vendor': Vendor.objects.first().pk,
            'device': Device.objects.first().pk,
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_assignment_with_license(self):
        form = SupportContractAssignmentForm(data={
            'contract': SupportContract.objects.first().pk,
            'sku': SupportSKU.objects.first().pk,
            'vendor': Vendor.objects.first().pk,
            'license': LicenseAssignment.objects.first().pk,
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_assignment_with_device_and_license(self):
        form = SupportContractAssignmentForm(data={
            'contract': SupportContract.objects.first().pk,
            'sku': SupportSKU.objects.first().pk,
            'vendor': Vendor.objects.first().pk,
            'device': Device.objects.first().pk,
            'license': LicenseAssignment.objects.first().pk,
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_assignment_with_device_and_license_with_different_device(self):
        form = SupportContractAssignmentForm(data={
            'contract': SupportContract.objects.first().pk,
            'sku': SupportSKU.objects.first().pk,
            'vendor': Vendor.objects.first().pk,
            'device': create_test_device(name='New Test Device'),
            'license': LicenseAssignment.objects.first().pk,
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
