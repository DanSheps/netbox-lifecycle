from django import forms
from django.utils.translation import gettext as _

from dcim.models import DeviceType, ModuleType, Manufacturer, Device
from netbox.forms import NetBoxModelForm
from netbox_lifecycle.models import HardwareLifecycle, Vendor, SupportContract, LicenseAssignment, License, \
    SupportContractAssignment, SupportSKU
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import DatePicker


__all__ = (
    'VendorForm',
    'SupportSKUForm',
    'SupportContractForm',
    'SupportContractAssignmentForm',
    'LicenseForm',
    'LicenseAssignmentForm',
    'HardwareLifecycleForm'
)


class VendorForm(NetBoxModelForm):

    class Meta:
        model = Vendor
        fields = ('name', )


class SupportSKUForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=False,
    )

    class Meta:
        model = SupportSKU
        fields = ('manufacturer', 'sku', )


class SupportContractForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        selector=True,
    )

    class Meta:
        model = SupportContract
        fields = ('vendor', 'contract_id', 'start', 'renewal', 'end', )
        widgets = {
            'start': DatePicker(),
            'renewal': DatePicker(),
            'end': DatePicker(),
        }


class SupportContractAssignmentForm(NetBoxModelForm):
    contract = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        selector=True,
    )
    sku = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        required=False,
        selector=True,
        label=_('SKU'),
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    license = DynamicModelChoiceField(
        queryset=LicenseAssignment.objects.all(),
        required=False,
        selector=True,
        label=_('License Assignment'),
    )

    class Meta:
        model = SupportContractAssignment
        fields = ('contract', 'sku', 'device', 'license', 'end')
        widgets = {
            'end': DatePicker(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('device', 'license') if self.cleaned_data[field]
        ]

        if len(selected_objects) == 0:
            raise forms.ValidationErrr({
                selected_objects[1]: "You must select at least a device or license"
            })

        if self.cleaned_data.get('license') and not self.cleaned_data.get('device'):
            self.cleaned_data['device'] = self.cleaned_data.get('license').device


class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=False,
    )

    class Meta:
        model = License
        fields = ('manufacturer', 'name', )


class LicenseAssignmentForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        selector=True,
    )
    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        selector=True,
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
    )

    class Meta:
        model = LicenseAssignment
        fields = ('vendor', 'license', 'device', 'quantity')


class HardwareLifecycleForm(NetBoxModelForm):
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label=_('Device Type'),
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
                initial['module_type'] = instance.assigned_object
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
