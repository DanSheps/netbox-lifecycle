from rest_framework.viewsets import ModelViewSet

from netbox_lifecycle.api.serializers import VendorSerializer, SupportContractSerializer, \
    SupportContractAssignmentSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment

__all__ = (
    'VendorViewSet',
    'SupportContractViewSet',
    'SupportContractAssignmentViewSet',
)


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class SupportContractViewSet(ModelViewSet):
    queryset = SupportContract.objects.all()
    serializer_class = SupportContractSerializer


class SupportContractAssignmentViewSet(ModelViewSet):
    queryset = SupportContractAssignment.objects.all()
    serializer_class = SupportContractAssignmentSerializer