from django import views

from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView
from netbox_lifecycle.filtersets import SupportContractFilterSet, VendorFilterSet
from netbox_lifecycle.forms import SupportContractFilterSetForm, VendorFilterSetForm, SupportContractForm, VendorForm
from netbox_lifecycle.models import SupportContract, Vendor
from netbox_lifecycle.tables import SupportContractTable, VendorTable
from utilities.views import ViewTab, register_model_view


__all__ = (
    'VendorListView',
    'VendorView',
    'VendorEditView',
    'VendorDeleteView',
    'SupportContractListView',
    'SupportContractView',
    'SupportContractDeviceView',
    'SupportContractEditView',
    'SupportContractDeleteView',
)


@register_model_view(Vendor, name='list')
class VendorListView(ObjectListView):
    queryset = Vendor.objects.all()
    table = VendorTable
    filterset = VendorFilterSet
    filterset_form = VendorFilterSetForm


@register_model_view(Vendor)
class VendorView(ObjectView):
    queryset = Vendor.objects.all()


@register_model_view(Vendor, 'edit')
class VendorEditView(ObjectEditView):
    queryset = Vendor.objects.all()
    form = VendorForm


@register_model_view(Vendor, 'delete')
class VendorDeleteView(ObjectDeleteView):
    queryset = Vendor.objects.all()


@register_model_view(SupportContract, name='list')
class SupportContractListView(ObjectListView):
    queryset = SupportContract.objects.all()
    table = SupportContractTable
    filterset = SupportContractFilterSet
    filterset_form = SupportContractFilterSetForm


@register_model_view(SupportContract)
class SupportContractView(ObjectView):
    queryset = SupportContract.objects.all()


@register_model_view(SupportContract, name='devices')
class SupportContractDeviceView(ObjectChildrenView):
    template_name = 'netbox_lifecycle/supportcontract_devices.html'
    queryset = SupportContract.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    actions = []
    tab = ViewTab(
        label='Devices',
        badge=lambda obj: obj.devices.count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(contracts=parent)



@register_model_view(SupportContract, 'edit')
class SupportContractEditView(ObjectEditView):
    queryset = SupportContract.objects.all()
    form = SupportContractForm


@register_model_view(SupportContract, 'delete')
class SupportContractDeleteView(ObjectDeleteView):
    queryset = SupportContract.objects.all()
