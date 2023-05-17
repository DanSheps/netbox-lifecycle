from django.utils.translation import gettext as _

import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from netbox_lifecycle.models import SupportContract, Vendor, SupportContractAssignment, SupportSKU

__all__ = (
    'VendorTable',
    'SupportSKUTable',
    'SupportContractTable',
    'SupportContractAssignmentTable'
)


class VendorTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        verbose_name='Name'
    )

    class Meta(NetBoxTable.Meta):
        model = Vendor
        fields = (
            'pk', 'name',
        )
        default_columns = (
            'pk', 'name',
        )


class SupportSKUTable(NetBoxTable):

    class Meta(NetBoxTable.Meta):
        model = SupportSKU
        fields = (
            'pk', 'manufacturer', 'sku'
        )
        default_columns = (
            'pk', 'manufacturer', 'sku',
        )


class SupportContractTable(NetBoxTable):
    contract_id = tables.Column(
        linkify=True,
        verbose_name='Contract ID'
    )

    class Meta(NetBoxTable.Meta):
        model = SupportContract
        fields = (
            'pk', 'contract_id', 'start', 'renewal', 'end'
        )
        default_columns = (
            'pk', 'contract_id',
        )


class SupportContractAssignmentTable(NetBoxTable):
    contract = tables.Column(
        linkify=True
    )
    sku = tables.Column(
        verbose_name='SKU',
        linkify=True,
    )
    assigned_object_type = tables.Column(
        verbose_name=_('Object Type'),
    )
    assigned_object = tables.Column(
        verbose_name='Assigned Object',
        linkify=True,
        orderable=False,
    )
    device_name = tables.Column(
        verbose_name='Device Name',
        accessor='assigned_object__name',
        linkify=False,
        orderable=False,
    )
    device_serial = tables.Column(
        verbose_name='Serial Number',
        accessor='assigned_object__serial',
        orderable=False,
    )
    device_model = tables.Column(
        verbose_name='Device Model',
        accessor='assigned_object__device_type__model',
        linkify=False,
        orderable=False,
    )
    device_status = ChoiceFieldColumn(
        verbose_name='Device Status',
        accessor='assigned_object__status',
        orderable=False,
    )
    license_name = tables.Column(
        verbose_name='License',
        accessor='assigned_object__license__name',
        linkify=False,
        orderable=False,
    )
    quantity = tables.Column(
        verbose_name='Quantity',
        accessor='assigned_object__quantity',
        orderable=False,
    )
    renewal = tables.Column(
        verbose_name='Renewal Date',
        accessor='contract__renewal',
    )
    end = tables.Column(
        verbose_name='End Date',
        accessor='end_date',
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = SupportContractAssignment
        fields = (
            'pk', 'contract', 'sku', 'assigned_object_type', 'assigned_object', 'device_name', 'license_name',
            'device_model', 'device_serial', 'quantity', 'renewal', 'end'
        )
        default_columns = (
            'pk', 'contract', 'sku', 'device_name', 'license_name', 'device_model', 'device_serial'
        )
