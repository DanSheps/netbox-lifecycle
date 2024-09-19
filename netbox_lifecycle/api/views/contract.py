
from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lifecycle.api.serializers import VendorSerializer, SupportContractSerializer, \
    SupportContractAssignmentSerializer, SupportSKUSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU

__all__ = (
    'VendorViewSet',
    'SupportSKUViewSet',
    'SupportContractViewSet',
    'SupportContractAssignmentViewSet',
)


class VendorViewSet(NetBoxModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class SupportSKUViewSet(NetBoxModelViewSet):
    queryset = SupportSKU.objects.all()
    serializer_class = SupportSKUSerializer


class SupportContractViewSet(NetBoxModelViewSet):
    queryset = SupportContract.objects.all()
    serializer_class = SupportContractSerializer


class SupportContractAssignmentViewSet(NetBoxModelViewSet):
    queryset = SupportContractAssignment.objects.all()
    serializer_class = SupportContractAssignmentSerializer
