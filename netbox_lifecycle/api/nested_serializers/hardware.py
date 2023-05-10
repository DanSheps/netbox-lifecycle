from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import WritableNestedSerializer
from netbox_lifecycle.models import HardwareLifecycle


class HardwareLifecycleNestedSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:hardwarelifecycle-detail')
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HardwareLifecycle
        fields = ('url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'assigned_object', )
