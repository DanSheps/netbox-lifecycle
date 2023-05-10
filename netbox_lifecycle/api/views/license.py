from rest_framework.viewsets import ModelViewSet

from netbox_lifecycle.api.serializers import LicenseSerializer, LicenseAssignmentSerializer
from netbox_lifecycle.models import License, LicenseAssignment


__all__ = (
    'LicenseViewSet',
    'LicenseAssignmentViewSet'
)


class LicenseViewSet(ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer


class LicenseAssignmentViewSet(ModelViewSet):
    queryset = LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
