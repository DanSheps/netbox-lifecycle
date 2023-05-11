from rest_framework.viewsets import ModelViewSet

from netbox_lifecycle.api.serializers import VendorSerializer, SupportContractSerializer, \
    SupportContractDeviceAssignmentSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractDeviceAssignment

__all__ = (
    'VendorViewSet',
    'SupportContractViewSet',
    'SupportContractDeviceAssignmentViewSet',
)


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class SupportContractViewSet(ModelViewSet):
    queryset = SupportContract.objects.all()
    serializer_class = SupportContractSerializer


class SupportContractDeviceAssignmentViewSet(ModelViewSet):
    queryset = SupportContractDeviceAssignment.objects.all()
    serializer_class = SupportContractDeviceAssignmentSerializer