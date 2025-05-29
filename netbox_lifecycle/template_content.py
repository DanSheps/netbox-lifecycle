
from django.contrib.contenttypes.models import ContentType
from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import hardware, contract


def log_info(message: str):
    from logging import getLogger
    logger = getLogger('netbox_lifecycle.template_content')
    logger.info(f'{message}')

class DeviceHardwareInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        support_contract = contract.SupportContractAssignment.objects.filter(device_id=self.context['object'].id).first()
        log_info(f'Kind is: {self.kind}')
        match self.kind:
            case "device":
                content_type = ContentType.objects.get(app_label="dcim", model="devicetype")
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(
                    assigned_object_id=self.context['object'].device_type_id,
                    assigned_object_type_id=content_type.id
                ).first()
            case "module":
                content_type = ContentType.objects.get(app_label="dcim", model="moduletype")
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(
                    assigned_object_id=self.context['object'].module_type_id,
                    assigned_object_type_id=content_type.id
                ).first()
            case "devicetype" | "moduletype":
                content_type = ContentType.objects.get(app_label="dcim", model=self.kind)
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(
                    assigned_object_id=self.context['object'].id,
                    assigned_object_type_id=content_type.id
                ).first()
        context = {'support_contract': support_contract, 'lifecycle_info': lifecycle_info}
        return self.render('netbox_lifecycle/inc/support_contract_info.html', extra_context=context)


class TypeInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        match self.kind:
            case "device":
                content_type = ContentType.objects.get(app_label="dcim", model="devicetype")
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].device_type_id,
                                                                           assigned_object_type_id=content_type.id).first()
            case "module":
                content_type = ContentType.objects.get(app_label="dcim", model="moduletype")
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].module_type_id,
                                                                           assigned_object_type_id=content_type.id).first()
            case "devicetype" | "moduletype":
                content_type = ContentType.objects.get(app_label="dcim", model=self.kind)
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].id,
                                                                           assigned_object_type_id=content_type.id).first()

        context = {'lifecycle_info': lifecycle_info}
        return self.render('netbox_lifecycle/inc/hardware_lifecycle_info.html', extra_context=context)


class DeviceHardwareLifecycleInfo(DeviceHardwareInfoExtension):
    models = ['dcim.device', ]
    kind = 'device'


class ModuleHardwareLifecycleInfo(TypeInfoExtension):
    models = ['dcim.module', ]
    kind = 'module'


class DeviceTypeHardwareLifecycleInfo(TypeInfoExtension):
    models = ['dcim.devicetype', ]
    kind = 'devicetype'


class ModuleTypeHardwareLifecycleInfo(TypeInfoExtension):
    models = ['dcim.moduletype', ]
    kind = 'moduletype'


template_extensions = (
    DeviceHardwareLifecycleInfo,
    ModuleHardwareLifecycleInfo,
    DeviceTypeHardwareLifecycleInfo,
    ModuleTypeHardwareLifecycleInfo,
)
