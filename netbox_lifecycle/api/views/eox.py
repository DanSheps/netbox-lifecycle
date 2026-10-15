from netbox.api.viewsets import NetBoxModelViewSet

from netbox_lifecycle.api.serializers import EoXAPISettingsSerializer
from netbox_lifecycle.filtersets import EoXAPISettingsFilterSet
from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsViewSet',)


class EoXAPISettingsViewSet(NetBoxModelViewSet):
    queryset = EoXAPISettings.objects.all()
    serializer_class = EoXAPISettingsSerializer
    filterset_class = EoXAPISettingsFilterSet
