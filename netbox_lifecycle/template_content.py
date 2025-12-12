from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from netbox.plugins import PluginTemplateExtension

from .models import hardware

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('netbox_lifecycle', {})


class DeviceLifecycleContent(PluginTemplateExtension):
    models = ['dcim.device']

    def get_contract_card_position(self):
        return PLUGIN_SETTINGS.get('contract_card_position', '')

    def _render_lifecycle_info(self):
        object = self.context.get('object')
        content_type = ContentType.objects.get(app_label='dcim', model='devicetype')
        lifecycle_info = hardware.HardwareLifecycle.objects.filter(
            assigned_object_id=object.device_type_id,
            assigned_object_type_id=content_type.id,
        ).first()
        return self.render(
            'netbox_lifecycle/inc/hardware_lifecycle_info.html',
            extra_context={'lifecycle_info': lifecycle_info},
        )

    def _render_contract_card(self):
        object = self.context.get('object')
        return self.render(
            'netbox_lifecycle/inc/contract_card_placeholder.html',
            extra_context={
                'htmx_url': reverse(
                    'plugins:netbox_lifecycle:device_contracts_htmx',
                    kwargs={'pk': object.pk},
                ),
            },
        )

    def right_page(self):
        result = self._render_lifecycle_info()
        if self.get_contract_card_position() == 'right_page':
            result += self._render_contract_card()
        return result

    def left_page(self):
        if self.get_contract_card_position() == 'left_page':
            return self._render_contract_card()
        return ''

    def full_width_page(self):
        if self.get_contract_card_position() == 'full_width_page':
            return self._render_contract_card()
        return ''


class ModuleLifecycleContent(PluginTemplateExtension):
    models = ['dcim.module']

    def right_page(self):
        object = self.context.get('object')
        content_type = ContentType.objects.get(app_label='dcim', model='moduletype')
        lifecycle_info = hardware.HardwareLifecycle.objects.filter(
            assigned_object_id=object.module_type_id,
            assigned_object_type_id=content_type.id,
        ).first()
        return self.render(
            'netbox_lifecycle/inc/hardware_lifecycle_info.html',
            extra_context={'lifecycle_info': lifecycle_info},
        )


class DeviceTypeLifecycleContent(PluginTemplateExtension):
    models = ['dcim.devicetype']

    def right_page(self):
        object = self.context.get('object')
        content_type = ContentType.objects.get(app_label='dcim', model='devicetype')
        lifecycle_info = hardware.HardwareLifecycle.objects.filter(
            assigned_object_id=object.id,
            assigned_object_type_id=content_type.id,
        ).first()
        return self.render(
            'netbox_lifecycle/inc/hardware_lifecycle_info.html',
            extra_context={'lifecycle_info': lifecycle_info},
        )


class ModuleTypeLifecycleContent(PluginTemplateExtension):
    models = ['dcim.moduletype']

    def right_page(self):
        object = self.context.get('object')
        content_type = ContentType.objects.get(app_label='dcim', model='moduletype')
        lifecycle_info = hardware.HardwareLifecycle.objects.filter(
            assigned_object_id=object.id,
            assigned_object_type_id=content_type.id,
        ).first()
        return self.render(
            'netbox_lifecycle/inc/hardware_lifecycle_info.html',
            extra_context={'lifecycle_info': lifecycle_info},
        )


template_extensions = (
    DeviceLifecycleContent,
    ModuleLifecycleContent,
    DeviceTypeLifecycleContent,
    ModuleTypeLifecycleContent,
)
