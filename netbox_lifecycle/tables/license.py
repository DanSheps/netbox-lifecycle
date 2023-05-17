import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lifecycle.models import License, LicenseAssignment


__all__ = (
    'LicenseTable',
    'LicenseAssignmentTable',
)


class LicenseTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        verbose_name='Name'
    )
    manufacturer = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            'pk', 'name',
        )
        default_columns = (
            'pk', 'name',
        )


class LicenseAssignmentTable(NetBoxTable):
    license = tables.Column(
        linkify=True
    )
    vendor = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = (
            'pk', 'license', 'vendor', 'device', 'quantity'
        )
        default_columns = (
            'pk', 'license', 'vendor', 'device'
        )
