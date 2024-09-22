import strawberry_django
from netbox_lifecycle import filtersets, models

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'VendorFilter',
    'SupportSKUFilter',
    'SupportContractFilter',
    'SupportContractAssignmentFilter',
    'LicenseFilter',
    'LicenseAssignmentFilter',
    'HardwareLifecycleFilter',
)


@strawberry_django.filter(models.Vendor, lookups=True)
@autotype_decorator(filtersets.VendorFilterSet)
class VendorFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.SupportSKU, lookups=True)
@autotype_decorator(filtersets.SupportSKUFilterSet)
class SupportSKUFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.SupportContract, lookups=True)
@autotype_decorator(filtersets.SupportContractFilterSet)
class SupportContractFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.SupportContractAssignment, lookups=True)
@autotype_decorator(filtersets.SupportContractAssignmentFilterSet)
class SupportContractAssignmentFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.License, lookups=True)
@autotype_decorator(filtersets.LicenseFilterSet)
class LicenseFilter(BaseFilterMixin):
    pass
    pass


@strawberry_django.filter(models.LicenseAssignment, lookups=True)
@autotype_decorator(filtersets.LicenseAssignmentFilterSet)
class LicenseAssignmentFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.HardwareLifecycle, lookups=True)
@autotype_decorator(filtersets.HardwareLifecycleFilterSet)
class HardwareLifecycleFilter(BaseFilterMixin):
    pass
