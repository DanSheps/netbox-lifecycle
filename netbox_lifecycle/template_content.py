
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import hardware, contract

class DeviceHardwareInfoExtension(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        object = self.context.get('object')
        support_contract = contract.SupportContractAssignment.objects.filter(device_id=self.context['object'].id).first()
        hardware_lifecycle = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].device_type.id).first()
        context = {'support_contract': support_contract, 'hardware_lifecycle': hardware_lifecycle}
        return self.render('netbox_lifecycle/inc/support_contract_info.html', extra_context=context)
        
class DeviceHardwareLifecycleInfo(DeviceHardwareInfoExtension):
    model = 'dcim.device'
    kind = 'device'


class DeviceTypeInfoExtension(PluginTemplateExtension):
    model = 'dcim.devicetype'

    def right_page(self):
        object = self.context.get('object')
        hardware_lifecycle = hardware.HardwareLifecycle.objects.filter(assigned_object_id=self.context['object'].id).first()
        context = {'hardware_lifecycle': hardware_lifecycle}
        return self.render('netbox_lifecycle/inc/device_lifecycle_info.html', extra_context=context)

class DeviceTypeHardwareLifecycleInfo(DeviceTypeInfoExtension):
    model = 'dcim.devicetype'
    kind = 'devicetype'


template_extensions = (
    DeviceHardwareLifecycleInfo,
    DeviceTypeHardwareLifecycleInfo,
)