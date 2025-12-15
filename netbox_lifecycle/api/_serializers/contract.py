from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer, ModuleSerializer
from dcim.api.serializers_.manufacturers import ManufacturerSerializer
from netbox.api.serializers import NetBoxModelSerializer
from virtualization.api.serializers_.virtualmachines import VirtualMachineSerializer
from netbox_lifecycle.api._serializers.license import LicenseAssignmentSerializer
from netbox_lifecycle.api._serializers.vendor import VendorSerializer
from netbox_lifecycle.models import (
    SupportContract,
    SupportContractAssignment,
    SupportSKU,
)

__all__ = (
    'SupportSKUSerializer',
    'SupportContractSerializer',
    'SupportContractAssignmentSerializer',
)


class SupportSKUSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lifecycle-api:supportsku-detail'
    )
    manufacturer = ManufacturerSerializer(nested=True)

    class Meta:
        model = SupportSKU
        fields = (
            'url',
            'id',
            'display',
            'manufacturer',
            'sku',
            'description',
            'comments',
            'tags',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'manufacturer',
            'sku',
        )


class SupportContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lifecycle-api:supportcontract-detail'
    )
    vendor = VendorSerializer(nested=True)
    start = serializers.DateField(required=False)
    renewal = serializers.DateField(required=False)
    end = serializers.DateField(required=False)

    class Meta:
        model = SupportContract
        fields = (
            'url',
            'id',
            'display',
            'vendor',
            'contract_id',
            'start',
            'renewal',
            'end',
            'description',
            'comments',
            'tags',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'vendor',
            'contract_id',
        )


class SupportContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lifecycle-api:supportcontractassignment-detail'
    )
    contract = SupportContractSerializer(nested=True)
    sku = SupportSKUSerializer(nested=True, required=False, allow_null=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    module = ModuleSerializer(nested=True, required=False, allow_null=True)
    virtual_machine = VirtualMachineSerializer(
        nested=True, required=False, allow_null=True
    )
    license = LicenseAssignmentSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = SupportContractAssignment
        fields = (
            'url',
            'id',
            'display',
            'contract',
            'sku',
            'device',
            'module',
            'virtual_machine',
            'license',
            'end',
            'description',
            'comments',
            'tags',
            'custom_fields',
        )

        brief_fields = (
            'url',
            'id',
            'display',
            'contract',
            'sku',
            'device',
            'module',
            'virtual_machine',
            'license',
        )
