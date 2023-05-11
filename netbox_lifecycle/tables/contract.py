from django.utils.translation import gettext as _

import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lifecycle.models import SupportContract, Vendor, SupportContractAssignment

__all__ = (
    'VendorTable',
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


class SupportContractTable(NetBoxTable):
    contract_id = tables.Column(
        linkify=True,
        verbose_name='Contract ID'
    )

    devices = tables.Column(
        accessor=tables.A('devices__count'),
        verbose_name='Device Count'
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
    assigned_object_type = tables.Column(
        verbose_name=_('Object Type'),
    )
    assigned_object = tables.Column(
        verbose_name='Assigned Object',
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = SupportContractAssignment
        fields = (
            'pk', 'contract', 'assigned_object_type', 'assigned_object'
        )
        default_columns = (
            'pk', 'contract', 'assigned_object_type', 'assigned_object'
        )
