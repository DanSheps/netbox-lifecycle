from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginTemplateExtension
from netbox.ui import panels, actions

from .models import hardware
from .ui import HardwareLifecyclePanel, HardwareLifecycleDatesPanel

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('netbox_lifecycle', {})


class BaseMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = None
        self.field_name = None
        self.lifecycle_content_type = None
        self.lifecycle_object_id_attr = None

    def get_context(self, context):
        """
        Return the context data to be used when rendering the panel.
        Borrowed from netbox/ui/panels.py

        Parameters:
            context (dict): The template context
        """
        obj = context.get('object')
        self.model_name = obj._meta.model_name if obj is not None else None
        if self.model_name in ['device', 'devicetype']:
            self.lifecycle_content_type = 'devicetype'
            self.lifecycle_object_id_attr = 'device_type_id'
        elif self.model_name in ['module', 'moduletype']:
            self.lifecycle_content_type = 'moduletype'
            self.lifecycle_object_id_attr = 'module_type_id'
        else:
            self.lifecycle_content_type = None

        if self.model_name == 'device':
            self.field_name = 'device_id'
        elif self.model_name == 'module':
            self.field_name = 'module_id'
        elif self.model_name == 'virtualmachine':
            self.field_name = 'virtual_machine_id'
        else:
            self.field_name = None

        return {
            'request': context.get('request'),
            'object': context.get('object'),
            'perms': context.get('perms'),
            'panel_class': self.__class__.__name__,
        }

    def right_page(self):
        result = ''
        if hasattr(self, '_render_lifecycle_info'):
            result += self._render_lifecycle_info('right_page')
        if hasattr(self, '_render_contract_card'):
            result += self._render_contract_card('right_page', expired=False)
            result += self._render_contract_card('right_page', expired=True)
        if hasattr(self, '_render_license_card'):
            result += self._render_license_card('right_page')
        return result

    def left_page(self):
        result = ''
        if hasattr(self, '_render_lifecycle_info'):
            result += self._render_lifecycle_info('left_page')
        if hasattr(self, '_render_contract_card'):
            result += self._render_contract_card('left_page', expired=False)
            result += self._render_contract_card('left_page', expired=True)
        if hasattr(self, '_render_license_card'):
            result += self._render_license_card('left_page')
        return result

    def full_width_page(self):
        result = ''
        if hasattr(self, '_render_lifecycle_info'):
            result += self._render_lifecycle_info('full_width_page')
        if hasattr(self, '_render_contract_card'):
            result += self._render_contract_card('full_width_page', expired=False)
            result += self._render_contract_card('full_width_page', expired=True)
        if hasattr(self, '_render_license_card'):
            result += self._render_license_card('full_width_page')
        return result


class LifecycleMixin:

    def get_lifecycle_card_position(self):
        return PLUGIN_SETTINGS.get('lifecycle_card_position', 'right_page')

    def _get_lifecycle_info(self):
        obj = self.context.get('object')
        content_type = ContentType.objects.get(
            app_label='dcim', model=self.lifecycle_content_type
        )
        object_id = getattr(obj, self.lifecycle_object_id_attr, obj.id)
        return hardware.HardwareLifecycle.objects.filter(
            assigned_object_id=object_id,
            assigned_object_type_id=content_type.id,
        ).first()

    def _render_lifecycle_info(self, location=None):
        if self.get_lifecycle_card_position() != location:
            return ''

        context = self.get_context(self.context)
        obj = self._get_lifecycle_info()
        context['object'] = obj

        content = HardwareLifecyclePanel().render(
            context
        ) + HardwareLifecycleDatesPanel().render(context)
        return content


class ContractMixin:

    def get_contract_card_position(self):
        return PLUGIN_SETTINGS.get('contract_card_position', 'right_page')

    def _render_contract_card(self, location=None, expired=None):
        if self.get_contract_card_position() != location:
            return ''

        title = _('Contracts')
        filter = {}
        action = []
        if expired is True or expired is False:
            filter = {'expired': expired}
            title = _('Expired Contracts') if expired else _('Active Contracts')

        if not expired:
            action = [
                actions.AddObject(
                    'netbox_lifecycle.SupportContractAssignment',
                    url_params={
                        self.model_name: lambda ctx: ctx['object'].pk,
                    },
                ),
            ]

        context = self.get_context(self.context)
        panel = panels.ObjectsTablePanel(
            title=title,
            model='netbox_lifecycle.supportcontractassignment',
            filters={self.field_name: lambda ctx: ctx['object'].pk, **filter},
            include_columns=[
                'contract',
                'sku',
            ],
            exclude_columns=[
                'device_name',
                'module_name',
                'virtual_machine_name',
                'license_name',
                'device_model',
                'device_serial',
                'module_serial',
                'device_status',
                'virtual_machine_status',
                'quantity',
                'renewal',
                'end',
                'description',
                'comments',
                'actions',
            ],
            actions=action,
        )
        return panel.render(context=context)


class LicenseMixin:

    def get_license_card_position(self):
        return PLUGIN_SETTINGS.get('license_card_position', 'right_page')

    def _render_license_card(self, location=None, exclude=None, include=None):
        if self.get_license_card_position() != location:
            return ''

        action = [
            actions.AddObject(
                'netbox_lifecycle.LicenseAssignment',
                url_params={
                    self.model_name: lambda ctx: ctx['object'].pk,
                },
            ),
        ]

        context = self.get_context(self.context)
        panel = panels.ObjectsTablePanel(
            title=_('Licenses'),
            model='netbox_lifecycle.licenseassignment',
            filters={self.field_name: lambda ctx: ctx['object'].pk},
            include_columns=[
                'vendor' 'license',
                'quantity',
            ],
            exclude_columns=[
                'device',
                'virtual_machine',
                'description',
                'comments',
                'actions',
            ],
            actions=action,
        )
        return panel.render(context=context)


class DeviceContent(
    ContractMixin, LicenseMixin, LifecycleMixin, BaseMixin, PluginTemplateExtension
):
    models = ['dcim.device']
    lifecycle_content_type = 'devicetype'
    lifecycle_object_id_attr = 'device_type_id'


class ModuleLifecycleContent(
    ContractMixin, LifecycleMixin, BaseMixin, PluginTemplateExtension
):
    models = ['dcim.module']


class DeviceTypeLifecycleContent(LifecycleMixin, BaseMixin, PluginTemplateExtension):
    models = ['dcim.devicetype']


class ModuleTypeLifecycleContent(LifecycleMixin, BaseMixin, PluginTemplateExtension):
    models = ['dcim.moduletype']


class VirtualMachineContractContent(ContractMixin, LicenseMixin, BaseMixin, PluginTemplateExtension):
    """Template extension for VirtualMachine detail pages showing contracts and licenses."""

    models = ['virtualization.virtualmachine']


template_extensions = (
    DeviceContent,
    ModuleLifecycleContent,
    DeviceTypeLifecycleContent,
    ModuleTypeLifecycleContent,
    VirtualMachineContractContent,
)
