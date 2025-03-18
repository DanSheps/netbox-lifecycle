from dcim.models import Manufacturer, ModuleBay, ModuleType, Module
from dcim.choices import ModuleStatusChoices
from netbox_lifecycle.models import Vendor, SupportSKU, SupportContract
from utilities.testing import create_test_device

__all__ = (
    'create_test_vendor',
    'create_test_supportsku',
    'create_test_supportcontract',
    'create_test_module',
)


def create_test_vendor(name=None):
    if name is None:
        name = 'Vendor'
    return Vendor.objects.create(name=name)


def create_test_supportsku(sku=None, manufacturer=None):
    if manufacturer is None:
        if Manufacturer.objects.all().count() == 0:
            manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        else:
            manufacturer = Manufacturer.objects.first()

    return SupportSKU.objects.create(manufacturer=manufacturer, sku=sku)


def create_test_supportcontract(contract_id=None, vendor=None, start=None, renewal=None, end=None):
    if vendor is None:
        if Vendor.objects.all().count() == 0:
            vendor = create_test_vendor()
        else:
            vendor = Vendor.objects.first()

    return SupportContract.objects.create(vendor=vendor, contract_id=contract_id, start=start, renewal=renewal, end=end)


def create_test_module(device=None, module_bay=None, module_type=None, status=None):
    #For accurate testing purposes, the used Device here can't be one of existing objects
    if device is None:
        device = create_test_device(name='Test Module Device')

    if module_bay is None:
        module_bay = ModuleBay.objects.create(device=device, name='Test ModuleBay')
    
    if module_type is None:
        if ModuleType.objects.all().count() == 0:
            if Manufacturer.objects.all().count() == 0:
                manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
            else:
                manufacturer = Manufacturer.objects.first()
            module_type = ModuleType.objects.create(manufacturer=manufacturer, model='Test ModuleType')
        else:
            module_type = ModuleType.objects.first()

    if status is None:
        status=ModuleStatusChoices.STATUS_ACTIVE
    
    return Module.objects.create(device=device, module_bay=module_bay, module_type=module_type, status=status)
