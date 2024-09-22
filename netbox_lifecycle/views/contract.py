from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView, \
    BulkDeleteView, BulkEditView
from netbox_lifecycle.filtersets import SupportContractFilterSet, VendorFilterSet, LicenseAssignmentFilterSet, \
    SupportContractAssignmentFilterSet, SupportSKUFilterSet
from netbox_lifecycle.forms import SupportContractFilterForm, VendorFilterForm, SupportContractForm, VendorForm, \
    SupportContractAssignmentForm, SupportSKUFilterForm, SupportSKUForm, SupportContractAssignmentBulkEditForm, \
    SupportContractAssignmentFilterForm, VendorBulkEditForm, SupportSKUBulkEditForm, SupportContractBulkEditForm
from netbox_lifecycle.models import SupportContract, Vendor, LicenseAssignment, SupportContractAssignment, SupportSKU
from netbox_lifecycle.tables import SupportContractTable, VendorTable, LicenseAssignmentTable, \
    SupportContractAssignmentTable, SupportSKUTable
from utilities.views import ViewTab, register_model_view


__all__ = (
    # Vendor
    'VendorListView',
    'VendorView',
    'VendorEditView',
    'VendorBulkEditView',
    'VendorDeleteView',
    'VendorBulkDeleteView',

    # SupportSKU
    'SupportSKUListView',
    'SupportSKUView',
    'SupportSKUEditView',
    'SupportSKUBulkEditView',
    'SupportSKUDeleteView',
    'SupportSKUBulkDeleteView',

    # SupportContract
    'SupportContractListView',
    'SupportContractView',
    'SupportContractEditView',
    'SupportContractBulkEditView',
    'SupportContractDeleteView',
    'SupportContractBulkDeleteView',
    'SupportContractAssignmentsView',

    # SupportContractAssignment
    'SupportContractAssignmentListView',
    'SupportContractAssignmentView',
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
    filterset_form = VendorFilterForm


@register_model_view(Vendor)
class VendorView(ObjectView):
    queryset = Vendor.objects.all()


@register_model_view(Vendor, 'edit')
class VendorEditView(ObjectEditView):
    queryset = Vendor.objects.all()
    form = VendorForm


@register_model_view(Vendor, 'bulk_edit')
class VendorBulkEditView(BulkEditView):
    queryset = Vendor.objects.all()
    filterset = VendorFilterSet
    table = VendorTable
    form = VendorBulkEditForm


@register_model_view(Vendor, 'delete')
class VendorDeleteView(ObjectDeleteView):
    queryset = Vendor.objects.all()


@register_model_view(Vendor, 'bulk_delete')
class VendorBulkDeleteView(BulkDeleteView):
    queryset = Vendor.objects.all()
    filterset = VendorFilterSet
    table = VendorTable


@register_model_view(SupportSKU, name='list')
class SupportSKUListView(ObjectListView):
    queryset = SupportSKU.objects.all()
    table = SupportSKUTable
    filterset = SupportSKUFilterSet
    filterset_form = SupportSKUFilterForm


@register_model_view(SupportSKU)
class SupportSKUView(ObjectView):
    queryset = SupportSKU.objects.all()


@register_model_view(SupportSKU, 'edit')
class SupportSKUEditView(ObjectEditView):
    queryset = SupportSKU.objects.all()
    form = SupportSKUForm


@register_model_view(SupportSKU, 'bulk_edit')
class SupportSKUBulkEditView(BulkEditView):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet
    table = SupportSKUTable
    form = SupportSKUBulkEditForm


@register_model_view(SupportSKU, 'delete')
class SupportSKUDeleteView(ObjectDeleteView):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet
    table = SupportSKUTable


@register_model_view(SupportSKU, 'bulk_delete')
class SupportSKUBulkDeleteView(BulkDeleteView):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet
    table = SupportSKUTable


@register_model_view(SupportContract, name='list')
class SupportContractListView(ObjectListView):
    queryset = SupportContract.objects.all()
    table = SupportContractTable
    filterset = SupportContractFilterSet
    filterset_form = SupportContractFilterForm


@register_model_view(SupportContract)
class SupportContractView(ObjectView):
    queryset = SupportContract.objects.all()


@register_model_view(SupportContract, name='assignments')
class SupportContractAssignmentsView(ObjectChildrenView):
    template_name = 'netbox_lifecycle/supportcontract/assignments.html'
    queryset = SupportContract.objects.all()
    child_model = SupportContractAssignment
    table = SupportContractAssignmentTable
    filterset = SupportContractAssignmentFilterSet
    actions = {
        'add': {'add'},
        'edit': {'change'},
        'delete': {'delete'}
    }
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


@register_model_view(SupportContract, 'bulk_edit')
class SupportContractBulkEditView(BulkEditView):
    queryset = SupportContract.objects.all()
    filterset = SupportContractFilterSet
    table = SupportContractTable
    form = SupportContractBulkEditForm


@register_model_view(SupportContract, 'delete')
class SupportContractDeleteView(ObjectDeleteView):
    queryset = SupportContract.objects.all()


@register_model_view(SupportContract, 'bulk_delete')
class SupportContractBulkDeleteView(BulkDeleteView):
    queryset = SupportContract.objects.all()
    filterset = SupportContractFilterSet
    table = SupportContractTable


@register_model_view(SupportContractAssignment, name='list')
class SupportContractAssignmentListView(ObjectListView):
    queryset = SupportContractAssignment.objects.all()
    table = SupportContractAssignmentTable
    filterset = SupportContractAssignmentFilterSet
    filterset_form = SupportContractAssignmentFilterForm
    actions = {
        'add': {'add'},
        'edit': {'change'},
        'delete': {'delete'},
        'bulk_edit': {'change'},
        'bulk_delete': {'delete'}
    }


@register_model_view(SupportContract)
class SupportContractAssignmentView(ObjectView):
    queryset = SupportContractAssignment.objects.all()


@register_model_view(SupportContractAssignment, 'edit')
class SupportContractAssignmentEditView(ObjectEditView):
    template_name = 'netbox_lifecycle/supportcontractassignment_edit.html'
    queryset = SupportContractAssignment.objects.all()
    form = SupportContractAssignmentForm


@register_model_view(SupportContractAssignment, 'delete')
class SupportContractAssignmentDeleteView(ObjectDeleteView):
    queryset = SupportContractAssignment.objects.all()


class SupportContractAssignmentBulkEditView(BulkEditView):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet
    table = SupportContractAssignmentTable
    form = SupportContractAssignmentBulkEditForm


class SupportContractAssignmentBulkDeleteView(BulkDeleteView):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet
    table = SupportContractAssignmentTable
