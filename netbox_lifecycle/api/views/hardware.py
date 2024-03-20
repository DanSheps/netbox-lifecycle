from rest_framework.viewsets import ModelViewSet

from netbox_lifecycle.api.serializers import HardwareLifecycleSerializer
from netbox_lifecycle.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleViewSet',
)


class HardwareLifecycleViewSet(ModelViewSet):
    queryset = HardwareLifecycle.objects.all()
    serializer_class = HardwareLifecycleSerializer
