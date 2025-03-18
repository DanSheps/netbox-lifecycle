
from django.contrib.contenttypes.models import ContentType
from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import hardware, contract, license


class DeviceHardwareInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        max_items_display = 5
        match self.kind:
            case "device":
                licenses = license.LicenseAssignment.objects.filter(device_id=self.context['object'].id)[:max_items_display]
                support_contract = contract.SupportContractAssignment.objects.filter(device_id=self.context['object'].id).first()
                content_type = ContentType.objects.get(app_label="dcim", model="devicetype")
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].device_type_id,
                                                                           assigned_object_type_id=content_type.id).first()
            case "module":
                licenses = None
                content_type = ContentType.objects.get(app_label="dcim", model="moduletype")
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].module_type_id,
                                                                           assigned_object_type_id=content_type.id).first()
            case "devicetype" | "moduletype":
                licenses = None
                content_type = ContentType.objects.get(app_label="dcim", model=self.kind)
                lifecycle_info = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].id,
                                                                           assigned_object_type_id=content_type.id).first()
        context = {'max_items_display': max_items_display, 'licenses': licenses, 'support_contract': support_contract,
                   'lifecycle_info': lifecycle_info}
        return self.render('netbox_lifecycle/inc/licenses_info.html', extra_context=context)


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
    model = 'dcim.device'
    kind = 'device'


class ModuleHardwareLifecycleInfo(TypeInfoExtension):
    model = 'dcim.module'
    kind = 'module'


class DeviceTypeHardwareLifecycleInfo(TypeInfoExtension):
    model = 'dcim.devicetype'
    kind = 'devicetype'


class ModuleTypeHardwareLifecycleInfo(TypeInfoExtension):
    model = 'dcim.moduletype'
    kind = 'moduletype'


template_extensions = (
    DeviceHardwareLifecycleInfo,
    ModuleHardwareLifecycleInfo,
    DeviceTypeHardwareLifecycleInfo,
    ModuleTypeHardwareLifecycleInfo,
)
