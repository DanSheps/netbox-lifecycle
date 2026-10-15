import django_tables2 as tables
from django.utils.translation import gettext as _
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsTable',)


EOX_SYNC_BUTTON = """
{% load i18n %}
{% if perms.netbox_lifecycle.sync_eoxapisettings %}
  {% url 'plugins:netbox_lifecycle:eoxapisettings_sync' pk=record.pk as sync_url %}
  <button class="btn btn-primary btn-sm" type="submit"
          formaction="{{ sync_url }}?return_url={{ request.get_full_path|urlencode }}"
          formmethod="post">
    <i class="mdi mdi-sync" aria-hidden="true"></i> {% trans "Sync" %}
  </button>
{% endif %}
"""


class EoXAPISettingsTable(NetBoxTable):
    driver = ChoiceFieldColumn(verbose_name=_('Driver'), linkify=True)
    manufacturer = tables.Column(linkify=True, verbose_name=_('Manufacturer'))
    enabled = tables.BooleanColumn(verbose_name=_('Enabled'))
    sync_interval = tables.Column(verbose_name=_('Interval (min)'))
    last_synced = tables.DateTimeColumn(verbose_name=_('Last synced'))
    actions = columns.ActionsColumn(extra_buttons=EOX_SYNC_BUTTON)

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
