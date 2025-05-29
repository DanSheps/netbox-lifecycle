from typing import Annotated, Union

import strawberry
import strawberry_django

from core.graphql.filter_mixins import BaseObjectTypeFilterMixin
from netbox_lifecycle import filtersets, models


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
class VendorFilter(BaseObjectTypeFilterMixin):
    pass


@strawberry_django.filter(models.SupportSKU, lookups=True)
class SupportSKUFilter(BaseObjectTypeFilterMixin):
    manufacturer: Annotated['ManufacturerFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    manufacturer_id: strawberry.ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.SupportContract, lookups=True)
class SupportContractFilter(BaseObjectTypeFilterMixin):
    vendor: Annotated['ManufacturerFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    vendor_id: strawberry.ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.SupportContractAssignment, lookups=True)
class SupportContractAssignmentFilter(BaseObjectTypeFilterMixin):
    contract: Annotated['SupportContractFilter', strawberry.lazy('netbox_lifecycle.graphql.filters')] | None = strawberry_django.filter_field()
    contract_id: strawberry.ID | None = strawberry_django.filter_field()
    sku: Annotated['SupportSKUFilter', strawberry.lazy('netbox_lifecycle.graphql.filters')] | None = strawberry_django.filter_field()
    sku_id: strawberry.ID | None = strawberry_django.filter_field()
    device: Annotated['DeviceFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    device_id: strawberry.ID | None = strawberry_django.filter_field()
    license: Annotated['LicenseFilter', strawberry.lazy('netbox_lifecycle.graphql.filters')] | None = strawberry_django.filter_field()
    license_id: strawberry.ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.License, lookups=True)
class LicenseFilter(BaseObjectTypeFilterMixin):
    manufacturer: Annotated['ManufacturerFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    manufacturer_id: strawberry.ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.LicenseAssignment, lookups=True)
class LicenseAssignmentFilter(BaseObjectTypeFilterMixin):
    vendor: Annotated['VendorFilter', strawberry.lazy('netbox_lifecycle.graphql.filters')] | None = strawberry_django.filter_field()
    vendor_id: strawberry.ID | None = strawberry_django.filter_field()
    license: Annotated['LicenseFilter', strawberry.lazy('netbox_lifecycle.graphql.filters')] | None = strawberry_django.filter_field()
    license_id: strawberry.ID | None = strawberry_django.filter_field()
    device: Annotated['DeviceFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    device_id: strawberry.ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.HardwareLifecycle, lookups=True)
class HardwareLifecycleFilter(BaseObjectTypeFilterMixin):
    device_type: Annotated['DeviceTypeFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    device_type_id: strawberry.ID | None = strawberry_django.filter_field()
    module_type: Annotated['ModuleTypeFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    module_type_id: strawberry.ID | None = strawberry_django.filter_field()

    assigned_object_type: Annotated['ContentTypeFilter', strawberry.lazy('core.graphql.filters')] | None = (
        strawberry_django.filter_field()
    )
    assigned_object_id: strawberry.ID | None = strawberry_django.filter_field()
