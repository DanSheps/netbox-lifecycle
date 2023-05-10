from rest_framework.viewsets import ModelViewSet

from netbox_lifecycle.api.serializers import VendorSerializer, SupportContractSerializer
from netbox_lifecycle.models import Vendor, SupportContract


__all__ = (
    'VendorViewSet',
    'SupportContractViewSet'
)


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class SupportContractViewSet(ModelViewSet):
    queryset = SupportContract.objects.all()
    serializer_class = SupportContractSerializer