from typing import Annotated, Any, Union

import strawberry
import strawberry_django

from dcim.graphql.types import ManufacturerType, DeviceType, DeviceTypeType, ModuleTypeType, ModuleType
from extras.graphql.mixins import CustomFieldsMixin, TagsMixin
from netbox.graphql.types import NetBoxObjectType, ObjectType
from .filters import *

from netbox_lifecycle import models

__all__ = (
    'VendorType',
    'SupportSKUType',
    'SupportContractType',
    'SupportContractAssignmentType',
    'LicenseType',
    'LicenseAssignmentType',
    'HardwareLifecycleType',
)


@strawberry_django.type(
    models.Vendor,
    fields='__all__',
    filters=VendorFilter
)
class VendorType(NetBoxObjectType):
    name: str


@strawberry_django.type(
    models.SupportSKU,
    fields='__all__',
    filters=SupportSKUFilter
)
class SupportSKUType(NetBoxObjectType):

    sku: str
    manufacturer: ManufacturerType


@strawberry_django.type(
    models.SupportContract,
    fields='__all__',
    filters=SupportContractFilter
)
class SupportContractType(NetBoxObjectType):

    vendor: VendorType
    contract_id: str
    start: str | None
    renewal: str | None
    end: str | None


@strawberry_django.type(
    models.License,
    fields='__all__',
    filters=LicenseFilter
)
class LicenseType(NetBoxObjectType):

    manufacturer: ManufacturerType
    name: str


@strawberry_django.type(
    models.SupportContractAssignment,
    fields='__all__',
    filters=SupportContractAssignmentFilter
)
class SupportContractAssignmentType(NetBoxObjectType):
    contract: SupportContractType
    sku: SupportSKUType | None
    device: DeviceType | None
    license: LicenseType | None
    end: str | None


@strawberry_django.type(
    models.LicenseAssignment,
    fields='__all__',
    filters=LicenseAssignmentFilter
)
class LicenseAssignmentType(NetBoxObjectType):
    license: LicenseType
    vendor: VendorType
    device: DeviceType | None
    quantity: int | None


@strawberry_django.type(
    models.HardwareLifecycle,
    fields='__all__',
    filters=HardwareLifecycleFilter
)
class HardwareLifecycleType(NetBoxObjectType):
    assigned_object_type: Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    assigned_object_id: int
    assigned_object: Annotated[Union[
        Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')],
        Annotated["ModuleType", strawberry.lazy('dcim.graphql.types')],],
        strawberry.union("HardwareLifecycleObjectTypes")] | None
    end_of_sale: str
    end_of_maintenance: str | None
    end_of_security: str | None
    last_contract_date: str | None
    end_of_support: str
    notice: str | None
    documentation: str | None


class HardwareLifecycleObjectTypes:
    class Meta:
        types = (
            DeviceTypeType,
            ModuleTypeType,
        )

    @classmethod
    def resolve_type(cls, instance, info):
        if type(instance) is DeviceType:
            return DeviceTypeType
        if type(instance) is ModuleType:
            return ModuleTypeType
