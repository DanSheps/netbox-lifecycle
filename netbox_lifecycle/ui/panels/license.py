from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'LicensePanel',
    'LicenseAssignmentPanel',
)


class LicensePanel(panels.ObjectAttributesPanel):
    manufacturer = attrs.RelatedObjectAttr('manufacturer', linkify=True)
    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class LicenseAssignmentPanel(panels.ObjectAttributesPanel):
    license = attrs.RelatedObjectAttr('license', linkify=True)
    name = attrs.TextAttr('name')
    description = attrs.TextAttr('description')


class LicenseAssignmentDevicePanel(panels.ObjectAttributesPanel):
    title = _('Device Assignment')

    device = attrs.RelatedObjectAttr('device', linkify=True)

    def should_render(self, context):
        if context.get('object').device:
            return True
        return False


class LicenseAssignmentVMPanel(panels.ObjectAttributesPanel):
    title = _('Virtual Machine Assignment')

    virtual_machine = attrs.RelatedObjectAttr('virtual_machine', linkify=True)

    def should_render(self, context):
        if context.get('object').virtual_machine:
            return True
        return False
