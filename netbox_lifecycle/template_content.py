from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from netbox.plugins import PluginTemplateExtension

from .models import hardware

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('netbox_lifecycle', {})


class BaseLifecycleContent(PluginTemplateExtension):
    """Base class for lifecycle template extensions."""

    lifecycle_content_type = None  # Override: 'devicetype' or 'moduletype'
    lifecycle_object_id_attr = None  # Override: attribute name for object ID

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

    def _render_lifecycle_info(self):
        return self.render(
            'netbox_lifecycle/inc/hardware_lifecycle_info.html',
            extra_context={'lifecycle_info': self._get_lifecycle_info()},
        )

    def right_page(self):
        if self.get_lifecycle_card_position() == 'right_page':
            return self._render_lifecycle_info()
        return ''

    def left_page(self):
        if self.get_lifecycle_card_position() == 'left_page':
            return self._render_lifecycle_info()
        return ''

    def full_width_page(self):
        if self.get_lifecycle_card_position() == 'full_width_page':
            return self._render_lifecycle_info()
        return ''


class DeviceLifecycleContent(BaseLifecycleContent):
    models = ['dcim.device']
    lifecycle_content_type = 'devicetype'
    lifecycle_object_id_attr = 'device_type_id'

    def get_contract_card_position(self):
        return PLUGIN_SETTINGS.get('contract_card_position', 'right_page')

    def _render_contract_card(self):
        obj = self.context.get('object')
        return self.render(
            'netbox_lifecycle/inc/contract_card_placeholder.html',
            extra_context={
                'htmx_url': reverse(
                    'plugins:netbox_lifecycle:device_contracts_htmx',
                    kwargs={'pk': obj.pk},
                ),
            },
        )

    def right_page(self):
        result = ''
        if self.get_lifecycle_card_position() == 'right_page':
            result += self._render_lifecycle_info()
        if self.get_contract_card_position() == 'right_page':
            result += self._render_contract_card()
        return result

    def left_page(self):
        result = ''
        if self.get_lifecycle_card_position() == 'left_page':
            result += self._render_lifecycle_info()
        if self.get_contract_card_position() == 'left_page':
            result += self._render_contract_card()
        return result

    def full_width_page(self):
        result = ''
        if self.get_lifecycle_card_position() == 'full_width_page':
            result += self._render_lifecycle_info()
        if self.get_contract_card_position() == 'full_width_page':
            result += self._render_contract_card()
        return result


class ModuleLifecycleContent(BaseLifecycleContent):
    models = ['dcim.module']
    lifecycle_content_type = 'moduletype'
    lifecycle_object_id_attr = 'module_type_id'


class DeviceTypeLifecycleContent(BaseLifecycleContent):
    models = ['dcim.devicetype']
    lifecycle_content_type = 'devicetype'
    lifecycle_object_id_attr = 'id'


class ModuleTypeLifecycleContent(BaseLifecycleContent):
    models = ['dcim.moduletype']
    lifecycle_content_type = 'moduletype'
    lifecycle_object_id_attr = 'id'


class VirtualMachineContractContent(PluginTemplateExtension):
    """Template extension for VirtualMachine detail pages showing contracts."""

    models = ['virtualization.virtualmachine']

    def get_contract_card_position(self):
        return PLUGIN_SETTINGS.get('contract_card_position', 'right_page')

    def _render_contract_card(self):
        obj = self.context.get('object')
        return self.render(
            'netbox_lifecycle/inc/contract_card_placeholder.html',
            extra_context={
                'htmx_url': reverse(
                    'plugins:netbox_lifecycle:virtualmachine_contracts_htmx',
                    kwargs={'pk': obj.pk},
                ),
            },
        )

    def right_page(self):
        if self.get_contract_card_position() == 'right_page':
            return self._render_contract_card()
        return ''

    def left_page(self):
        if self.get_contract_card_position() == 'left_page':
            return self._render_contract_card()
        return ''

    def full_width_page(self):
        if self.get_contract_card_position() == 'full_width_page':
            return self._render_contract_card()
        return ''


template_extensions = (
    DeviceLifecycleContent,
    ModuleLifecycleContent,
    DeviceTypeLifecycleContent,
    ModuleTypeLifecycleContent,
    VirtualMachineContractContent,
)
