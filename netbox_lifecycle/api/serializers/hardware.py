from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
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
    assigned_object = serializers.SerializerMethodField(read_only=True)

    end_of_sale = serializers.DateField()
    end_of_maintenance = serializers.DateField()
    end_of_security = serializers.DateField()
    last_contract_date = serializers.DateField()
    end_of_support = serializers.DateField()

    class Meta:
        model = HardwareLifecycle
        fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'assigned_object', 'end_of_sale',
            'end_of_maintenance', 'end_of_security', 'last_contract_date', 'end_of_support', 'notice', 'documentation'
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, instance):
        serializer = get_serializer_for_model(instance.assigned_object, prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(instance.assigned_object, context=context).data
