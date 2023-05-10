import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lifecycle.models import SupportContract, Vendor


__all__ = (
    'VendorTable',
    'SupportContractTable',
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
