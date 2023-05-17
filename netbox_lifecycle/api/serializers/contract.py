from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.nested_serializers import NestedManufacturerSerializer, NestedDeviceSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from netbox_lifecycle.api.nested_serializers import NestedVendorSerializer, NestedSupportContractSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU

__all__ = (
    'VendorSerializer',
    'SupportSKUSerializer',
    'SupportContractSerializer',
    'SupportContractAssignmentSerializer',
)

from utilities.api import get_serializer_for_model


class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name')


class SupportSKUSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = SupportSKU
        fields = ('url', 'id', 'display', 'manufacturer', 'sku')


class SupportContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    vendor = NestedVendorSerializer()
    start = serializers.DateField()
    renewal = serializers.DateField()
    end = serializers.DateField()

    class Meta:
        model = SupportContract
        fields = ('url', 'id', 'display', 'vendor', 'contract_id', 'start', 'renewal', 'end', )


class SupportContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:licenseassignment-detail')
    contract = NestedSupportContractSerializer()

    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SupportContractAssignment
        fields = (
            'url', 'id', 'display', 'contract', 'assigned_object_type', 'assigned_object_id',
            'assigned_object', 'end'
        )

    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, instance):
        serializer = get_serializer_for_model(instance.assigned_object, prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(instance.assigned_object, context=context).data
