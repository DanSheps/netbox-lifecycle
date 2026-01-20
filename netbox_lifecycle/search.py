from netbox.search import SearchIndex, register_search
from netbox_lifecycle.models import *


@register_search
class VendorIndex(SearchIndex):
    model = Vendor
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('description',)


@register_search
class SupportSKUIndex(SearchIndex):
    model = SupportSKU
    fields = (
        ('sku', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('manufacturer', 'description')


@register_search
class SupportContractIndex(SearchIndex):
    model = SupportContract
    fields = (
        ('contract_id', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('vendor', 'start', 'renewal', 'end', 'description')


@register_search
class SupportContractAssignmentIndex(SearchIndex):
    model = SupportContractAssignment
    fields = (
        ('contract', 100),
        ('sku', 300),
        ('device', 400),
        ('license', 500),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('contract', 'sku', 'device', 'end', 'description')


@register_search
class LicenseIndex(SearchIndex):
    model = License
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('manufacturer', 'description')


@register_search
class LicenseAssignmentIndex(SearchIndex):
    model = LicenseAssignment
    fields = (
        ('license', 100),
        ('vendor', 200),
        ('device', 300),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('license', 'vendor', 'device', 'description')
