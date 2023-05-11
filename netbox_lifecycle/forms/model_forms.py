from django import forms
from django.utils.translation import gettext as _

from dcim.models import DeviceType, ModuleType, Manufacturer, Device
from netbox.forms import NetBoxModelForm
from netbox_lifecycle.models import HardwareLifecycle, Vendor, SupportContract, LicenseAssignment, License, \
    SupportContractDeviceAssignment
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import DatePicker


__all__ = (
    'VendorForm',
    'SupportContractForm',
    'SupportContractDeviceAssignmentForm',
    'LicenseForm',
    'LicenseAssignmentForm',
    'HardwareLifecycleForm'
)


class VendorForm(NetBoxModelForm):

    class Meta:
        model = Vendor
        fields = ('name', )


class SupportContractForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=False,
    )
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        selector=True,
    )

    class Meta:
        model = SupportContract
        fields = ('manufacturer', 'vendor', 'contract_id', 'start', 'renewal', 'end', )
        widgets = {
            'start': DatePicker(),
            'renewal': DatePicker(),
            'end': DatePicker(),
        }


class SupportContractDeviceAssignmentForm(NetBoxModelForm):
    contract = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        required=False,
        selector=True,
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
    )

    class Meta:
        model = SupportContractDeviceAssignment
        fields = ('contract', 'device')


class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=False,
    )

    class Meta:
        model = License
        fields = ('name', 'manufacturer', )


class LicenseAssignmentForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        selector=True,
    )
    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        selector=True,
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
    )

    class Meta:
        model = LicenseAssignment
        fields = ('vendor', 'license', 'device')


class HardwareLifecycleForm(NetBoxModelForm):
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label=_('Module Type'),
    )

    class Meta:
        model = HardwareLifecycle
        fields = (
            'last_contract_date', 'end_of_sale', 'end_of_maintenance', 'end_of_security', 'end_of_support', 'notice',
            'documentation'
        )
        widgets = {
            'last_contract_date': DatePicker(),
            'end_of_sale': DatePicker(),
            'end_of_maintenance': DatePicker(),
            'end_of_security': DatePicker(),
            'end_of_support': DatePicker(),
        }

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is DeviceType:
                initial['device_type'] = instance.assigned_object
            elif type(instance.assigned_object) is ModuleType:
                initial['device_type'] = instance.assigned_object
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('device_type', 'module_type') if self.cleaned_data[field]
        ]

        if len(selected_objects) > 1:
            raise forms.ValidationError({
                selected_objects[1]: "You can only have a lifecycle for a device or module type"
            })
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None
