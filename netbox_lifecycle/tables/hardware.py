import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lifecycle.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleTable',
)


class HardwareLifecycleTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        accessor='name'
    )

    assigned_object = tables.Column(
        linkify=True,
        verbose_name='Hardware'
    )
    assigned_object_count = tables.Column(
        verbose_name='Assigned Object Count'
    )

    class Meta(NetBoxTable.Meta):
        model = HardwareLifecycle
        fields = (
            'pk', 'name', 'assigned_object', 'end_of_sale', 'end_of_maintenance', 'end_of_security', 'end_of_support'
        )
        default_columns = (
            'pk', 'name', 'assigned_object', 'end_of_sale', 'end_of_maintenance'
        )
