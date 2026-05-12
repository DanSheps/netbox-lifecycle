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
from netbox_lifecycle.ui import LicensePanel, LicenseAssignmentPanel
from netbox_lifecycle.ui.panels.license import (
    LicenseAssignmentDevicePanel,
    LicenseAssignmentVMPanel,
)
from utilities.views import ViewTab, register_model_view

from netbox_lifecycle.filtersets import LicenseAssignmentFilterSet, LicenseFilterSet
from netbox_lifecycle.forms import (
    LicenseAssignmentBulkEditForm,
    LicenseAssignmentFilterForm,
    LicenseAssignmentForm,
    LicenseAssignmentImportForm,
    LicenseBulkEditForm,
    LicenseFilterForm,
    LicenseForm,
    LicenseImportForm,
)
from netbox_lifecycle.models import License, LicenseAssignment
from netbox_lifecycle.tables import LicenseAssignmentTable, LicenseTable

__all__ = (
    'LicenseAssignmentBulkDeleteView',
    'LicenseAssignmentBulkEditView',
    'LicenseAssignmentBulkImportView',
    'LicenseAssignmentDeleteView',
    'LicenseAssignmentEditView',
    'LicenseAssignmentListView',
    'LicenseAssignmentView',
    'LicenseAssignmentsView',
    'LicenseBulkDeleteView',
    'LicenseBulkEditView',
    'LicenseBulkImportView',
    'LicenseDeleteView',
    'LicenseEditView',
    'LicenseListView',
    'LicenseView',
)


@register_model_view(License, name='list', path='', detail=False)
class LicenseListView(ObjectListView):
    queryset = License.objects.all()
    table = LicenseTable
    filterset = LicenseFilterSet
    filterset_form = LicenseFilterForm


@register_model_view(License)
class LicenseView(ObjectView):
    queryset = License.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            LicensePanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            panels.CommentsPanel(),
            panels.RelatedObjectsPanel(),
        ],
    )


@register_model_view(License, 'add', detail=False)
@register_model_view(License, 'edit')
class LicenseEditView(ObjectEditView):
    queryset = License.objects.all()
    form = LicenseForm


@register_model_view(License, 'delete')
class LicenseDeleteView(ObjectDeleteView):
    queryset = License.objects.all()


@register_model_view(License, 'bulk_edit', detail=False)
class LicenseBulkEditView(BulkEditView):
    queryset = License.objects.all()
    filterset = LicenseFilterSet
    table = LicenseTable
    form = LicenseBulkEditForm


@register_model_view(License, 'bulk_delete', detail=False)
class LicenseBulkDeleteView(BulkDeleteView):
    queryset = License.objects.all()
    filterset = LicenseFilterSet
    table = LicenseTable


@register_model_view(License, 'bulk_import', detail=False)
class LicenseBulkImportView(BulkImportView):
    queryset = License.objects.all()
    model_form = LicenseImportForm


@register_model_view(License, 'assignments')
class LicenseAssignmentsView(ObjectChildrenView):
    queryset = License.objects.all()
    child_model = LicenseAssignment
    table = LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet
    viewname = None
    tab = ViewTab(
        label='License Assignments',
        badge=lambda obj: LicenseAssignment.objects.filter(license=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(license=parent)


@register_model_view(LicenseAssignment, name='list', path='', detail=False)
class LicenseAssignmentListView(ObjectListView):
    queryset = LicenseAssignment.objects.all()
    table = LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet
    filterset_form = LicenseAssignmentFilterForm


@register_model_view(LicenseAssignment)
class LicenseAssignmentView(ObjectView):
    queryset = LicenseAssignment.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            LicenseAssignmentPanel(),
            LicenseAssignmentDevicePanel(),
            LicenseAssignmentVMPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            panels.CommentsPanel(),
            panels.RelatedObjectsPanel(),
        ],
    )


@register_model_view(LicenseAssignment, 'add', detail=False)
@register_model_view(LicenseAssignment, 'edit')
class LicenseAssignmentEditView(ObjectEditView):
    queryset = LicenseAssignment.objects.all()
    form = LicenseAssignmentForm


@register_model_view(LicenseAssignment, 'delete')
class LicenseAssignmentDeleteView(ObjectDeleteView):
    queryset = LicenseAssignment.objects.all()


@register_model_view(LicenseAssignment, 'bulk_edit', detail=False)
class LicenseAssignmentBulkEditView(BulkEditView):
    queryset = LicenseAssignment.objects.all()
    filterset = LicenseAssignmentFilterSet
    table = LicenseAssignmentTable
    form = LicenseAssignmentBulkEditForm


@register_model_view(LicenseAssignment, 'bulk_delete', detail=False)
class LicenseAssignmentBulkDeleteView(BulkDeleteView):
    queryset = LicenseAssignment.objects.all()
    filterset = LicenseAssignmentFilterSet
    table = LicenseAssignmentTable


@register_model_view(LicenseAssignment, 'bulk_import', detail=False)
class LicenseAssignmentBulkImportView(BulkImportView):
    queryset = LicenseAssignment.objects.all()
    model_form = LicenseAssignmentImportForm
