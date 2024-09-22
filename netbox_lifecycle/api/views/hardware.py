from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lifecycle.api.serializers import HardwareLifecycleSerializer
from netbox_lifecycle.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleViewSet',
)


class HardwareLifecycleViewSet(NetBoxModelViewSet):
    queryset = HardwareLifecycle.objects.all()
    serializer_class = HardwareLifecycleSerializer
