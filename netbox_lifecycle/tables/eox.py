import django_tables2 as tables
from django.utils.translation import gettext as _
from netbox.tables import ChoiceFieldColumn, NetBoxTable

from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsTable',)


class EoXAPISettingsTable(NetBoxTable):
    driver = ChoiceFieldColumn(verbose_name=_('Driver'), linkify=True)
    manufacturer = tables.Column(linkify=True, verbose_name=_('Manufacturer'))
    enabled = tables.BooleanColumn(verbose_name=_('Enabled'))
    sync_interval = tables.Column(verbose_name=_('Interval (min)'))
    last_synced = tables.DateTimeColumn(verbose_name=_('Last synced'))

    class Meta(NetBoxTable.Meta):
        model = EoXAPISettings
        fields = (
            'pk',
            'driver',
            'manufacturer',
            'enabled',
            'client_id',
            'sync_interval',
            'last_synced',
            'description',
            'comments',
        )
        default_columns = (
            'pk',
            'driver',
            'manufacturer',
            'enabled',
            'sync_interval',
            'last_synced',
        )
