from dcim.models import Manufacturer
from netbox_lifecycle.models import Vendor, SupportSKU, SupportContract

__all__ = (
    'create_test_vendor',
    'create_test_supportsku',
    'create_test_supportcontract',
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
