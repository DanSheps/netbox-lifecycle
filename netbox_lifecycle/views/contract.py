from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView, \
    BulkDeleteView, BulkEditView
from netbox_lifecycle.filtersets import SupportContractFilterSet, VendorFilterSet, LicenseAssignmentFilterSet, \
    SupportContractAssignmentFilterSet, SupportSKUFilterSet
from netbox_lifecycle.forms import SupportContractFilterSetForm, VendorFilterSetForm, SupportContractForm, VendorForm, \
    SupportContractAssignmentForm, SupportSKUFilterSetForm, SupportSKUForm, SupportContractAssignmentBulkEditForm, \
    SupportContractAssignmentFilterSetForm
from netbox_lifecycle.models import SupportContract, Vendor, LicenseAssignment, SupportContractAssignment, SupportSKU
from netbox_lifecycle.tables import SupportContractTable, VendorTable, LicenseAssignmentTable, \
    SupportContractAssignmentTable, SupportSKUTable
from utilities.views import ViewTab, register_model_view


__all__ = (
    'VendorListView',
    'VendorView',
    'VendorEditView',
    'VendorDeleteView',
    'SupportSKUListView',
    'SupportSKUView',
    'SupportSKUEditView',
    'SupportSKUDeleteView',
    'SupportContractListView',
    'SupportContractView',
    'SupportContractAssignmentView',
    'SupportContractEditView',
    'SupportContractDeleteView',
    'SupportContractAssignmentListView',
    'SupportContractAssignmentEditView',
    'SupportContractAssignmentDeleteView',
    'SupportContractAssignmentBulkEditView',
    'SupportContractAssignmentBulkDeleteView',
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


@register_model_view(SupportSKU, name='list')
class SupportSKUListView(ObjectListView):
    queryset = SupportSKU.objects.all()
    table = SupportSKUTable
    filterset = SupportSKUFilterSet
    filterset_form = SupportSKUFilterSetForm


@register_model_view(SupportSKU)
class SupportSKUView(ObjectView):
    queryset = SupportSKU.objects.all()


@register_model_view(SupportSKU, 'edit')
class SupportSKUEditView(ObjectEditView):
    queryset = SupportSKU.objects.all()
    form = SupportSKUForm


@register_model_view(SupportSKU, 'delete')
class SupportSKUDeleteView(ObjectDeleteView):
    queryset = SupportSKU.objects.all()


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
class SupportContractAssignmentEditView(ObjectEditView):
    template_name = 'netbox_lifecycle/supportcontractassignment_edit.html'
    queryset = SupportContractAssignment.objects.all()
    form = SupportContractAssignmentForm


@register_model_view(SupportContractAssignment, 'delete')
class SupportContractAssignmentDeleteView(ObjectDeleteView):
    queryset = SupportContractAssignment.objects.all()


@register_model_view(SupportContractAssignment, name='list')
class SupportContractAssignmentListView(ObjectListView):
    queryset = SupportContractAssignment.objects.all()
    table = SupportContractAssignmentTable
    filterset = SupportContractAssignmentFilterSet
    filterset_form = SupportContractAssignmentFilterSetForm
    actions = ['add', 'edit', 'delete', 'bulk_edit', 'bulk_delete']


class SupportContractAssignmentBulkEditView(BulkEditView):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet
    table = SupportContractAssignmentTable
    form = SupportContractAssignmentBulkEditForm


class SupportContractAssignmentBulkDeleteView(BulkDeleteView):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet
    table = SupportContractAssignmentTable
