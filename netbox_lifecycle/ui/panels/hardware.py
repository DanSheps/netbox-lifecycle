from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'HardwareLifecyclePanel',
    'HardwareLifecycleDatesPanel',
)

from netbox_lifecycle.ui.attributes.datetime import ColoredDateTimeAttr


class HardwareLifecyclePanel(panels.ObjectAttributesPanel):
    manufacturer = attrs.RelatedObjectAttr('assigned_object.manufacturer', linkify=True)
    assigned_object = attrs.RelatedObjectAttr(
        'assigned_object', linkify=True, label=_('Assigned Object')
    )
    description = attrs.TextAttr('description')

    def render(self, context):

        return super().render(context)


class HardwareLifecycleDatesPanel(panels.ObjectAttributesPanel):
    title = _('Dates')
    end_of_sale = ColoredDateTimeAttr('end_of_sale', spec='date')
    end_of_maintenance = ColoredDateTimeAttr('end_of_maintenance', spec='date')
    end_of_security = ColoredDateTimeAttr('end_of_security', spec='date')
    last_contract_attach = ColoredDateTimeAttr('last_contract_attach', spec='date')
    last_contract_renewal = ColoredDateTimeAttr('last_contract_renewal', spec='date')
    end_of_support = ColoredDateTimeAttr('end_of_support', spec='date')
