from netbox.api.viewsets import NetBoxModelViewSet

from netbox_lifecycle.api.serializers import (
    SupportContractAssignmentSerializer,
    SupportContractSerializer,
    SupportSKUSerializer,
    VendorSerializer,
)
from netbox_lifecycle.filtersets import (
    SupportContractAssignmentFilterSet,
    SupportContractFilterSet,
    SupportSKUFilterSet,
    VendorFilterSet,
)
from netbox_lifecycle.models import (
    SupportContract,
    SupportContractAssignment,
    SupportSKU,
    Vendor,
)

__all__ = (
    'SupportContractAssignmentViewSet',
    'SupportContractViewSet',
    'SupportSKUViewSet',
    'VendorViewSet',
)


class VendorViewSet(NetBoxModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filterset_class = VendorFilterSet


class SupportSKUViewSet(NetBoxModelViewSet):
    queryset = SupportSKU.objects.all()
    serializer_class = SupportSKUSerializer
    filterset_class = SupportSKUFilterSet


class SupportContractViewSet(NetBoxModelViewSet):
    queryset = SupportContract.objects.all()
    serializer_class = SupportContractSerializer
    filterset_class = SupportContractFilterSet


class SupportContractAssignmentViewSet(NetBoxModelViewSet):
    queryset = SupportContractAssignment.objects.all()
    serializer_class = SupportContractAssignmentSerializer
    filterset_class = SupportContractAssignmentFilterSet
