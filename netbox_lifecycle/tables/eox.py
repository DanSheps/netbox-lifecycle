import django_tables2 as tables
from django.utils.translation import gettext as _
from netbox.tables import ChoiceFieldColumn, NetBoxTable

from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsTable',)


class EoXAPISettingsTable(NetBoxTable):
    driver = ChoiceFieldColumn(verbose_name=_('Driver'))
    url = tables.Column(linkify=True, verbose_name=_('API URL'))
    enabled = tables.BooleanColumn(verbose_name=_('Enabled'))
    sync_interval = tables.Column(verbose_name=_('Interval (min)'))
    last_synced = tables.DateTimeColumn(verbose_name=_('Last synced'))

    class Meta(NetBoxTable.Meta):
        model = EoXAPISettings
        fields = (
            'pk',
            'driver',
            'url',
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
            'url',
            'enabled',
            'sync_interval',
            'last_synced',
        )
