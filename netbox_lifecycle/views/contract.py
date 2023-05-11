from django import views

from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView
from netbox_lifecycle.filtersets import SupportContractFilterSet, VendorFilterSet, LicenseAssignmentFilterSet, \
    SupportContractAssignmentFilterSet
from netbox_lifecycle.forms import SupportContractFilterSetForm, VendorFilterSetForm, SupportContractForm, VendorForm, \
    SupportContractAssignmentForm
from netbox_lifecycle.models import SupportContract, Vendor, LicenseAssignment, SupportContractAssignment
from netbox_lifecycle.tables import SupportContractTable, VendorTable, LicenseAssignmentTable, \
    SupportContractAssignmentTable
from utilities.views import ViewTab, register_model_view


__all__ = (
    'VendorListView',
    'VendorView',
    'VendorEditView',
    'VendorDeleteView',
    'SupportContractListView',
    'SupportContractView',
    'SupportContractAssignmentView',
    #'SupportContractLicenseView',
    'SupportContractEditView',
    'SupportContractDeleteView',
    'SupportContractDeviceAssignmentEditView',
    'SupportContractDeviceAssignmentDeleteView',
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


@register_model_view(SupportContract, name='assignments')
class SupportContractAssignmentView(ObjectChildrenView):
    template_name = 'netbox_lifecycle/supportcontract/assignments.html'
    queryset = SupportContract.objects.all()
    child_model = SupportContractAssignment
    table = SupportContractAssignmentTable
    filterset = SupportContractAssignmentFilterSet
    actions = ['add', 'edit', 'delete']
    tab = ViewTab(
        label='Assignments',
        badge=lambda obj: SupportContractAssignment.objects.filter(contract=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(contract=parent)


@register_model_view(SupportContract, 'edit')
class SupportContractEditView(ObjectEditView):
    queryset = SupportContract.objects.all()
    form = SupportContractForm


@register_model_view(SupportContract, 'delete')
class SupportContractDeleteView(ObjectDeleteView):
    queryset = SupportContract.objects.all()


@register_model_view(SupportContractAssignment, 'edit')
class SupportContractDeviceAssignmentEditView(ObjectEditView):
    template_name = 'netbox_lifecycle/supportcontractassignment_edit.html'
    queryset = SupportContractAssignment.objects.all()
    form = SupportContractAssignmentForm


@register_model_view(SupportContractAssignment, 'delete')
class SupportContractDeviceAssignmentDeleteView(ObjectDeleteView):
    queryset = SupportContractAssignment.objects.all()