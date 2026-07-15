from extras.ui.panels import TagsPanel, CustomFieldsPanel
from netbox.views.generic import (
    BulkDeleteView,
    BulkEditView,
    BulkImportView,
    ObjectChildrenView,
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)
from netbox.ui import panels, layout
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view

from netbox_lifecycle.filtersets import (
    SupportContractAssignmentFilterSet,
    SupportContractFilterSet,
    SupportSKUFilterSet,
    VendorFilterSet,
)
from netbox_lifecycle.forms import (
    SupportContractAssignmentBulkEditForm,
    SupportContractAssignmentFilterForm,
    SupportContractAssignmentForm,
    SupportContractAssignmentImportForm,
    SupportContractBulkEditForm,
    SupportContractFilterForm,
    SupportContractForm,
    SupportContractImportForm,
    SupportSKUBulkEditForm,
    SupportSKUFilterForm,
    SupportSKUForm,
    SupportSKUImportForm,
    VendorBulkEditForm,
    VendorFilterForm,
    VendorForm,
    VendorImportForm,
)
from netbox_lifecycle.models import (
    SupportContract,
    SupportContractAssignment,
    SupportSKU,
    Vendor,
)
from netbox_lifecycle.tables import (
    SupportContractAssignmentTable,
    SupportContractTable,
    SupportSKUTable,
    VendorTable,
)
from netbox_lifecycle.ui import (
    VendorPanel,
    SupportContractPanel,
    SupportContractDatesPanel,
    SupportContractAssignmentPanel,
    SupportContractAssignmentDevicePanel,
    SupportContractAssignmentVMPanel,
    SupportContractAssignmentLicensePanel,
    SupportSKUPanel,
)

__all__ = (
    # SupportContractAssignment
    'SupportContractAssignmentBulkDeleteView',
    'SupportContractAssignmentBulkEditView',
    'SupportContractAssignmentBulkImportView',
    'SupportContractAssignmentDeleteView',
    'SupportContractAssignmentEditView',
    'SupportContractAssignmentListView',
    'SupportContractAssignmentView',
    # SupportContract
    'SupportContractAssignmentsView',
    'SupportContractBulkDeleteView',
    'SupportContractBulkEditView',
    'SupportContractBulkImportView',
    'SupportContractDeleteView',
    'SupportContractEditView',
    'SupportContractListView',
    'SupportContractView',
    # SupportSKU
    'SupportSKUBulkDeleteView',
    'SupportSKUBulkEditView',
    'SupportSKUBulkImportView',
    'SupportSKUDeleteView',
    'SupportSKUEditView',
    'SupportSKUListView',
    'SupportSKUView',
    # Vendor
    'VendorBulkDeleteView',
    'VendorBulkEditView',
    'VendorBulkImportView',
    'VendorDeleteView',
    'VendorEditView',
    'VendorListView',
    'VendorView',
)


@register_model_view(Vendor, name='list', path='', detail=False)
class VendorListView(ObjectListView):
    queryset = Vendor.objects.all()
    table = VendorTable
    filterset = VendorFilterSet
    filterset_form = VendorFilterForm


@register_model_view(Vendor)
class VendorView(GetRelatedModelsMixin, ObjectView):
    queryset = Vendor.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            VendorPanel(),
        ],
        right_panels=[
            panels.RelatedObjectsPanel(),
            panels.CommentsPanel(),
        ],
    )

    def get_extra_context(self, request, instance):
        assignments = SupportContractAssignment.objects.filter(
            contract__vendor=instance
        )
        return {
            'related_models': self.get_related_models(
                request, instance, extra=[(assignments, 'contract_id')]
            ),
        }


@register_model_view(Vendor, 'add', detail=False)
@register_model_view(Vendor, 'edit')
class VendorEditView(ObjectEditView):
    queryset = Vendor.objects.all()
    form = VendorForm


@register_model_view(Vendor, 'delete')
class VendorDeleteView(ObjectDeleteView):
    queryset = Vendor.objects.all()


@register_model_view(Vendor, 'bulk_edit', detail=False)
class VendorBulkEditView(BulkEditView):
    queryset = Vendor.objects.all()
    filterset = VendorFilterSet
    table = VendorTable
    form = VendorBulkEditForm


@register_model_view(Vendor, 'bulk_delete', detail=False)
class VendorBulkDeleteView(BulkDeleteView):
    queryset = Vendor.objects.all()
    filterset = VendorFilterSet
    table = VendorTable


@register_model_view(Vendor, 'bulk_import', detail=False)
class VendorBulkImportView(BulkImportView):
    queryset = Vendor.objects.all()
    model_form = VendorImportForm


@register_model_view(SupportSKU, name='list', path='', detail=False)
class SupportSKUListView(ObjectListView):
    queryset = SupportSKU.objects.all()
    table = SupportSKUTable
    filterset = SupportSKUFilterSet
    filterset_form = SupportSKUFilterForm


@register_model_view(SupportSKU)
class SupportSKUView(ObjectView):
    queryset = SupportSKU.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            SupportSKUPanel(),
            TagsPanel(),
        ],
        right_panels=[
            panels.CommentsPanel(),
            panels.RelatedObjectsPanel(),
        ],
    )


@register_model_view(SupportSKU, 'add', detail=False)
@register_model_view(SupportSKU, 'edit')
class SupportSKUEditView(ObjectEditView):
    queryset = SupportSKU.objects.all()
    form = SupportSKUForm


@register_model_view(SupportSKU, 'delete')
class SupportSKUDeleteView(ObjectDeleteView):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet
    table = SupportSKUTable


@register_model_view(SupportSKU, 'bulk_edit', detail=False)
class SupportSKUBulkEditView(BulkEditView):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet
    table = SupportSKUTable
    form = SupportSKUBulkEditForm


@register_model_view(SupportSKU, 'bulk_delete', detail=False)
class SupportSKUBulkDeleteView(BulkDeleteView):
    queryset = SupportSKU.objects.all()
    filterset = SupportSKUFilterSet
    table = SupportSKUTable


@register_model_view(SupportSKU, 'bulk_import', detail=False)
class SupportSKUBulkImportView(BulkImportView):
    queryset = SupportSKU.objects.all()
    model_form = SupportSKUImportForm


@register_model_view(SupportContract, name='list', path='', detail=False)
class SupportContractListView(ObjectListView):
    queryset = SupportContract.objects.all()
    table = SupportContractTable
    filterset = SupportContractFilterSet
    filterset_form = SupportContractFilterForm


@register_model_view(SupportContract)
class SupportContractView(ObjectView):
    queryset = SupportContract.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            SupportContractPanel(),
            SupportContractDatesPanel(),
            TagsPanel(),
        ],
        right_panels=[
            panels.CommentsPanel(),
            panels.RelatedObjectsPanel(),
        ],
    )


@register_model_view(SupportContract, name='assignments')
class SupportContractAssignmentsView(ObjectChildrenView):
    queryset = SupportContract.objects.all()
    child_model = SupportContractAssignment
    table = SupportContractAssignmentTable
    filterset = SupportContractAssignmentFilterSet
    tab = ViewTab(
        label='Assignments',
        badge=lambda obj: SupportContractAssignment.objects.filter(
            contract=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(contract=parent)


@register_model_view(SupportContract, 'add', detail=False)
@register_model_view(SupportContract, 'edit')
class SupportContractEditView(ObjectEditView):
    queryset = SupportContract.objects.all()
    form = SupportContractForm


@register_model_view(SupportContract, 'delete')
class SupportContractDeleteView(ObjectDeleteView):
    queryset = SupportContract.objects.all()


@register_model_view(SupportContract, 'bulk_edit', detail=False)
class SupportContractBulkEditView(BulkEditView):
    queryset = SupportContract.objects.all()
    filterset = SupportContractFilterSet
    table = SupportContractTable
    form = SupportContractBulkEditForm


@register_model_view(SupportContract, 'bulk_delete', detail=False)
class SupportContractBulkDeleteView(BulkDeleteView):
    queryset = SupportContract.objects.all()
    filterset = SupportContractFilterSet
    table = SupportContractTable


@register_model_view(SupportContract, 'bulk_import', detail=False)
class SupportContractBulkImportView(BulkImportView):
    queryset = SupportContract.objects.all()
    model_form = SupportContractImportForm


@register_model_view(SupportContractAssignment, name='list', path='', detail=False)
class SupportContractAssignmentListView(ObjectListView):
    queryset = SupportContractAssignment.objects.all()
    table = SupportContractAssignmentTable
    filterset = SupportContractAssignmentFilterSet
    filterset_form = SupportContractAssignmentFilterForm
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_edit': {'change'},
        'bulk_delete': {'delete'},
    }


@register_model_view(SupportContractAssignment)
class SupportContractAssignmentView(ObjectView):
    queryset = SupportContractAssignment.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            SupportContractAssignmentPanel(),
            SupportContractAssignmentDevicePanel(),
            SupportContractAssignmentVMPanel(),
            SupportContractAssignmentLicensePanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            panels.CommentsPanel(),
            panels.RelatedObjectsPanel(),
        ],
    )


@register_model_view(SupportContractAssignment, 'add', detail=False)
@register_model_view(SupportContractAssignment, 'edit')
class SupportContractAssignmentEditView(ObjectEditView):
    queryset = SupportContractAssignment.objects.all()
    form = SupportContractAssignmentForm


@register_model_view(SupportContractAssignment, 'delete')
class SupportContractAssignmentDeleteView(ObjectDeleteView):
    queryset = SupportContractAssignment.objects.all()


@register_model_view(SupportContractAssignment, 'bulk_edit', detail=False)
class SupportContractAssignmentBulkEditView(BulkEditView):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet
    table = SupportContractAssignmentTable
    form = SupportContractAssignmentBulkEditForm


@register_model_view(SupportContractAssignment, 'bulk_delete', detail=False)
class SupportContractAssignmentBulkDeleteView(BulkDeleteView):
    queryset = SupportContractAssignment.objects.all()
    filterset = SupportContractAssignmentFilterSet
    table = SupportContractAssignmentTable


@register_model_view(SupportContractAssignment, 'bulk_import', detail=False)
class SupportContractAssignmentBulkImportView(BulkImportView):
    queryset = SupportContractAssignment.objects.all()
    model_form = SupportContractAssignmentImportForm
