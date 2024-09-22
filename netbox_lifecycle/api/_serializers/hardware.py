from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.models import HardwareLifecycle
from utilities.api import get_serializer_for_model


__all__ = (
    'HardwareLifecycleSerializer',
)


class HardwareLifecycleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )

    end_of_sale = serializers.DateField()
    end_of_maintenance = serializers.DateField(required=False)
    end_of_security = serializers.DateField(required=False)
    last_contract_date = serializers.DateField(required=False)
    end_of_support = serializers.DateField()

    class Meta:
        model = HardwareLifecycle
        fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'end_of_sale',
            'end_of_maintenance', 'end_of_security', 'last_contract_date', 'end_of_support', 'notice', 'documentation',
            'description', 'comments',
        )
        brief_fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'end_of_sale',
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, instance):
        serializer = get_serializer_for_model(instance.assigned_object)
        context = {'request': self.context['request']}
        return serializer(instance.assigned_object, context=context, nested=True).data
