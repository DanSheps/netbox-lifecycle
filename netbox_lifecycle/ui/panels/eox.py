from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = ('EoXAPISettingsPanel',)


class EoXAPISettingsPanel(panels.ObjectAttributesPanel):
    driver = attrs.TextAttr('get_driver_display', label=_('Driver'))
    manufacturer = attrs.RelatedObjectAttr('manufacturer', label=_('Manufacturer'))
    enabled = attrs.BooleanAttr('enabled', label=_('Enabled'))
    client_id = attrs.TextAttr('client_id', label=_('OAuth Client ID'))
    sync_interval = attrs.TextAttr('sync_interval', label=_('Sync interval (minutes)'))
    last_synced = attrs.DateTimeAttr('last_synced', label=_('Last synced'))
    description = attrs.TextAttr('description')
