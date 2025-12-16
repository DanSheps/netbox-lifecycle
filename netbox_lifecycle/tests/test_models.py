import datetime
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from dcim.models import Manufacturer, Site, DeviceRole, DeviceType, Device
from virtualization.models import Cluster, ClusterType, VirtualMachine
from netbox_lifecycle.constants import (
    CONTRACT_STATUS_ACTIVE,
    CONTRACT_STATUS_EXPIRED,
    CONTRACT_STATUS_FUTURE,
    CONTRACT_STATUS_UNSPECIFIED,
)
from netbox_lifecycle.models import (
    Vendor,
    SupportContract,
    SupportSKU,
    SupportContractAssignment,
    License,
    LicenseAssignment,
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
            end=datetime.date.today() + datetime.timedelta(days=2),
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
        manufacturer = Manufacturer.objects.create(
            name='Manufacturer 1', slug='manufacturer-1'
        )
        site = Site.objects.create(name='Test Site', slug='test-site')
        role = DeviceRole.objects.create(name='Test Role', slug='test-role')
        device_type = DeviceType.objects.create(
            model='Test DeviceType', slug='test-devicetype', manufacturer=manufacturer
        )
        device = Device.objects.create(
            name='Test Device 1', device_type=device_type, role=role, site=site
        )

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

        SupportContract.objects.create(
            vendor=Vendor.objects.first(),
            contract_id='1234',
            start=datetime.date.today(),
            renewal=datetime.date.today() + datetime.timedelta(days=1),
            end=datetime.date.today() + datetime.timedelta(days=2),
        )

        LicenseAssignment.objects.create(
            license=license, vendor=vendor, device=device, quantity=1
        )

    def test_contractassignment_creation(self):
        contract = SupportContract.objects.first()
        sku = SupportSKU.objects.first()
        device = Device.objects.first()
        LicenseAssignment.objects.first()

        contract = SupportContractAssignment(contract=contract, sku=sku, device=device)
        contract.full_clean()
        contract.save()

    def test_supportcontract_duplicate_ids(self):
        contract = SupportContract.objects.first()
        sku = SupportSKU.objects.first()
        device = Device.objects.first()
        license = LicenseAssignment.objects.first()

        contract1 = SupportContractAssignment(contract=contract, sku=sku, device=device)
        contract1.full_clean()
        contract1.save()

        contract2 = SupportContractAssignment(contract=contract, sku=sku, device=device)

        with self.assertRaises(ValidationError):
            contract2.full_clean()

        contract2.license = license
        contract2.full_clean()
        contract2.save()


class SupportContractAssignmentStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vendor = Vendor.objects.create(name='Test Vendor')

    def test_status_active_when_end_in_future(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='ACTIVE-001',
            end=date.today() + timedelta(days=30),
        )
        assignment = SupportContractAssignment.objects.create(contract=contract)
        self.assertEqual(assignment.status, CONTRACT_STATUS_ACTIVE)

    def test_status_active_when_end_is_today(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='ACTIVE-002',
            end=date.today(),
        )
        assignment = SupportContractAssignment.objects.create(contract=contract)
        self.assertEqual(assignment.status, CONTRACT_STATUS_ACTIVE)

    def test_status_future_when_start_in_future(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='FUTURE-001',
            start=date.today() + timedelta(days=30),
            end=date.today() + timedelta(days=60),
        )
        assignment = SupportContractAssignment.objects.create(contract=contract)
        self.assertEqual(assignment.status, CONTRACT_STATUS_FUTURE)

    def test_status_expired_when_end_in_past(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='EXPIRED-001',
            end=date.today() - timedelta(days=1),
        )
        assignment = SupportContractAssignment.objects.create(contract=contract)
        self.assertEqual(assignment.status, CONTRACT_STATUS_EXPIRED)

    def test_status_unspecified_when_no_end_date(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='UNSPEC-001',
        )
        assignment = SupportContractAssignment.objects.create(contract=contract)
        self.assertEqual(assignment.status, CONTRACT_STATUS_UNSPECIFIED)

    def test_status_uses_assignment_end_over_contract_end(self):
        contract = SupportContract.objects.create(
            vendor=self.vendor,
            contract_id='OVERRIDE-001',
            end=date.today() + timedelta(days=30),
        )
        assignment = SupportContractAssignment.objects.create(
            contract=contract,
            end=date.today() - timedelta(days=1),
        )
        self.assertEqual(assignment.status, CONTRACT_STATUS_EXPIRED)


class LicenseAssignmentVMTestCase(TestCase):
    """Tests for LicenseAssignment with virtual_machine field."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name='Manufacturer 1', slug='manufacturer-1'
        )
        site = Site.objects.create(name='Test Site', slug='test-site')
        role = DeviceRole.objects.create(name='Test Role', slug='test-role')
        device_type = DeviceType.objects.create(
            model='Test DeviceType', slug='test-devicetype', manufacturer=manufacturer
        )
        cls.device = Device.objects.create(
            name='Test Device 1', device_type=device_type, role=role, site=site
        )

        cluster_type = ClusterType.objects.create(
            name='Test Cluster Type', slug='test-cluster-type'
        )
        cluster = Cluster.objects.create(name='Test Cluster', type=cluster_type)
        cls.vm = VirtualMachine.objects.create(name='Test VM', cluster=cluster)

        cls.vendor = Vendor.objects.create(name='Vendor 1')
        cls.license = License.objects.create(
            manufacturer=manufacturer, name='Test License'
        )

    def test_license_assignment_with_vm(self):
        """Test that a license can be assigned to a virtual machine."""
        assignment = LicenseAssignment(
            license=self.license,
            vendor=self.vendor,
            virtual_machine=self.vm,
            quantity=1,
        )
        assignment.full_clean()
        assignment.save()
        self.assertEqual(assignment.virtual_machine, self.vm)

    def test_license_assignment_device_vm_mutually_exclusive(self):
        """Test that device and virtual_machine are mutually exclusive."""
        assignment = LicenseAssignment(
            license=self.license,
            vendor=self.vendor,
            device=self.device,
            virtual_machine=self.vm,
            quantity=1,
        )
        with self.assertRaises(ValidationError) as context:
            assignment.full_clean()
        self.assertIn('mutually exclusive', str(context.exception))

    def test_license_assignment_name_with_vm(self):
        """Test that the name property works correctly with a VM."""
        assignment = LicenseAssignment.objects.create(
            license=self.license,
            vendor=self.vendor,
            virtual_machine=self.vm,
            quantity=1,
        )
        self.assertIn(self.vm.name, assignment.name)


class SupportContractAssignmentVMTestCase(TestCase):
    """Tests for SupportContractAssignment with virtual_machine field."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name='Manufacturer 1', slug='manufacturer-1'
        )
        site = Site.objects.create(name='Test Site', slug='test-site')
        role = DeviceRole.objects.create(name='Test Role', slug='test-role')
        device_type = DeviceType.objects.create(
            model='Test DeviceType', slug='test-devicetype', manufacturer=manufacturer
        )
        cls.device = Device.objects.create(
            name='Test Device 1', device_type=device_type, role=role, site=site
        )

        cluster_type = ClusterType.objects.create(
            name='Test Cluster Type', slug='test-cluster-type'
        )
        cluster = Cluster.objects.create(name='Test Cluster', type=cluster_type)
        cls.vm = VirtualMachine.objects.create(name='Test VM', cluster=cluster)

        cls.vendor = Vendor.objects.create(name='Vendor 1')
        cls.sku = SupportSKU.objects.create(manufacturer=manufacturer, sku='SKU-1')
        cls.contract = SupportContract.objects.create(
            vendor=cls.vendor,
            contract_id='CONTRACT-VM-1',
            end=date.today() + timedelta(days=30),
        )

    def test_contract_assignment_with_vm(self):
        """Test that a contract can be assigned to a virtual machine."""
        assignment = SupportContractAssignment(
            contract=self.contract,
            sku=self.sku,
            virtual_machine=self.vm,
        )
        assignment.full_clean()
        assignment.save()
        self.assertEqual(assignment.virtual_machine, self.vm)

    def test_contract_assignment_device_vm_mutually_exclusive(self):
        """Test that device and virtual_machine are mutually exclusive."""
        assignment = SupportContractAssignment(
            contract=self.contract,
            sku=self.sku,
            device=self.device,
            virtual_machine=self.vm,
        )
        with self.assertRaises(ValidationError) as context:
            assignment.full_clean()
        self.assertIn('mutually exclusive', str(context.exception))

    def test_contract_assignment_vm_status(self):
        """Test that status property works with VM assignments."""
        assignment = SupportContractAssignment.objects.create(
            contract=self.contract,
            virtual_machine=self.vm,
        )
        self.assertEqual(assignment.status, CONTRACT_STATUS_ACTIVE)
