from typing import List

import strawberry
import strawberry_django

from .types import *


@strawberry.type(name="Query")
class VendorQuery:
    vendor: VendorType = strawberry_django.field()
    vendor_list: List[VendorType] = strawberry_django.field()


@strawberry.type(name="Query")
class SupportSKUQuery:
    support_sku: SupportSKUType = strawberry_django.field()
    support_sku_list: List[SupportSKUType] = strawberry_django.field()


@strawberry.type(name="Query")
class SupportContractQuery:
    support_contract: SupportContractType = strawberry_django.field()
    support_contract_list: List[SupportContractType] = strawberry_django.field()


@strawberry.type(name="Query")
class SupportContractAssignmentQuery:
    support_contract_assignment: SupportContractAssignmentType = strawberry_django.field()
    support_contract_assignment_list: List[SupportContractAssignmentType] = strawberry_django.field()


@strawberry.type(name="Query")
class LicenseQuery:
    license: LicenseType = strawberry_django.field()
    license_list: List[LicenseType] = strawberry_django.field()


@strawberry.type(name="Query")
class LicenseAssignmentQuery:
    license_assignment: LicenseAssignmentType = strawberry_django.field()
    license_assignment_list: List[LicenseAssignmentType] = strawberry_django.field()


@strawberry.type(name="Query")
class HardwareLifecycleQuery:
    hardware_lifecycle: HardwareLifecycleType = strawberry_django.field()
    hardware_lifecycle_list: List[HardwareLifecycleType] = strawberry_django.field()


schema = [
    VendorQuery,
    SupportSKUQuery,
    SupportContractQuery,
    SupportContractAssignmentQuery,
    LicenseQuery,
    LicenseAssignmentQuery,
    HardwareLifecycleQuery,
]
