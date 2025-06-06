from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lifecycle.api.serializers import LicenseSerializer, LicenseAssignmentSerializer
from netbox_lifecycle.filtersets import LicenseAssignmentFilterSet, LicenseFilterSet
from netbox_lifecycle.models import License, LicenseAssignment


__all__ = (
    'LicenseViewSet',
    'LicenseAssignmentViewSet'
)


class LicenseViewSet(NetBoxModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilterSet


class LicenseAssignmentViewSet(NetBoxModelViewSet):
    queryset = LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
    filterset_class = LicenseAssignmentFilterSet
