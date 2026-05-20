from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

from netbox_lifecycle.ui.attributes import ColoredDateTimeAttr

__all__ = (
    'VendorPanel',
    'SupportSKUPanel',
    'SupportContractPanel',
    'SupportContractDatesPanel',
    'SupportContractAssignmentPanel',
    'SupportContractAssignmentDevicePanel',
    'SupportContractAssignmentVMPanel',
    'SupportContractAssignmentLicensePanel',
)


class VendorPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class SupportSKUPanel(panels.ObjectAttributesPanel):
    manufacturer = attrs.RelatedObjectAttr('manufacturer', linkify=True)
    sku = attrs.TextAttr('sku', label=_('SKU'))
    description = attrs.TextAttr('description')


class SupportContractPanel(panels.ObjectAttributesPanel):
    vendor = attrs.RelatedObjectAttr('vendor', linkify=True)
    contract_id = attrs.TextAttr('contract_id')
    description = attrs.TextAttr('description')


class SupportContractDatesPanel(panels.ObjectAttributesPanel):
    title = _('Dates')
    start = attrs.DateTimeAttr('start', spec='date')
    renewal = attrs.DateTimeAttr('renewal', spec='date')
    end = ColoredDateTimeAttr('end', spec='date')


class SupportContractAssignmentPanel(panels.ObjectAttributesPanel):
    contract = attrs.RelatedObjectAttr('contract', linkify=True)
    sku = attrs.RelatedObjectAttr('sku', linkify=True)
    end = attrs.DateTimeAttr('end', spec='date')
    description = attrs.TextAttr('description')


class SupportContractAssignmentDevicePanel(panels.ObjectAttributesPanel):
    title = _('Device Assignment')

    device = attrs.RelatedObjectAttr('device', linkify=True)
    module = attrs.RelatedObjectAttr('module', linkify=True)

    def should_render(self, context):
        if context.get('object').device:
            return True
        return False


class SupportContractAssignmentVMPanel(panels.ObjectAttributesPanel):
    title = _('Virtual Machine Assignment')

    virtual_machine = attrs.RelatedObjectAttr('virtual_machine', linkify=True)

    def should_render(self, context):
        if context.get('object').virtual_machine:
            return True
        return False


class SupportContractAssignmentLicensePanel(panels.ObjectAttributesPanel):
    title = _('License Assignment')

    license = attrs.RelatedObjectAttr('license', linkify=True)

    def should_render(self, context):
        if context.get('object').license:
            return True
        return False


class SupportContractAssignmentsPanel(panels.ObjectsTablePanel):
    model = 'netbox_lifecycle.SupportContractAssignment'
    title = _('Support Contracts')
