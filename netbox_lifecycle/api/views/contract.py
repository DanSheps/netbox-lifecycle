from rest_framework.viewsets import ModelViewSet

from netbox_lifecycle.api.serializers import VendorSerializer, SupportContractSerializer, \
    SupportContractAssignmentSerializer, SupportSKUSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU

__all__ = (
    'VendorViewSet',
    'SupportSKUViewSet',
    'SupportContractViewSet',
    'SupportContractAssignmentViewSet',
)


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class SupportSKUViewSet(ModelViewSet):
    queryset = SupportSKU.objects.all()
    serializer_class = SupportSKUSerializer


class SupportContractViewSet(ModelViewSet):
    queryset = SupportContract.objects.all()
    serializer_class = SupportContractSerializer


class SupportContractAssignmentViewSet(ModelViewSet):
    queryset = SupportContractAssignment.objects.all()
    serializer_class = SupportContractAssignmentSerializer
