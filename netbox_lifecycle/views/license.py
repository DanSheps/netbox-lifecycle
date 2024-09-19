from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView, \
    BulkEditView, BulkDeleteView
from netbox_lifecycle.filtersets import LicenseFilterSet, LicenseAssignmentFilterSet
from netbox_lifecycle.forms import LicenseFilterForm, LicenseForm, LicenseAssignmentForm, \
    LicenseAssignmentBulkEditForm, LicenseAssignmentFilterForm, LicenseBulkEditForm
from netbox_lifecycle.models import License, LicenseAssignment
from netbox_lifecycle.tables import LicenseTable, LicenseAssignmentTable
from utilities.views import ViewTab, register_model_view


__all__ = (
    'LicenseListView',
    'LicenseView',
    'LicenseEditView',
    'LicenseBulkEditView',
    'LicenseDeleteView',
    'LicenseBulkDeleteView',
    'LicenseAssignmentsView',
    'LicenseAssignmentListView',
    'LicenseAssignmentView',
    'LicenseAssignmentEditView',
    'LicenseAssignmentDeleteView',
    'LicenseAssignmentBulkEditView',
    'LicenseAssignmentBulkDeleteView',
)


@register_model_view(License, name='list')
class LicenseListView(ObjectListView):
    queryset = License.objects.all()
    table = LicenseTable
    filterset = LicenseFilterSet
    filterset_form = LicenseFilterForm


@register_model_view(License)
class LicenseView(ObjectView):
    queryset = License.objects.all()


@register_model_view(License, 'edit')
class LicenseEditView(ObjectEditView):
    queryset = License.objects.all()
    form = LicenseForm


@register_model_view(License, 'bulk_edit')
class LicenseBulkEditView(BulkEditView):
    queryset = License.objects.all()
    filterset = LicenseFilterSet
    table = LicenseTable
    form = LicenseBulkEditForm


@register_model_view(License, 'delete')
class LicenseDeleteView(ObjectDeleteView):
    queryset = License.objects.all()


@register_model_view(License, 'bulk_delete')
class LicenseBulkDeleteView(BulkDeleteView):
    queryset = License.objects.all()
    filterset = LicenseFilterSet
    table = LicenseTable


@register_model_view(License, 'assignments')
class LicenseAssignmentsView(ObjectChildrenView):
    template_name = 'netbox_lifecycle/license/assignments.html'
    queryset = License.objects.all()
    child_model = LicenseAssignment
    table = LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet
    viewname = None
    actions = {
        'add': {'add'},
        'edit': {'change'},
        'delete': {'delete'}
    }
    tab = ViewTab(
        label='License Assignments',
        badge=lambda obj: LicenseAssignment.objects.filter(license=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(license=parent)


@register_model_view(LicenseAssignment, name='list')
class LicenseAssignmentListView(ObjectListView):
    queryset = LicenseAssignment.objects.all()
    table = LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet
    filterset_form = LicenseAssignmentFilterForm


@register_model_view(LicenseAssignment)
class LicenseAssignmentView(ObjectView):
    queryset = LicenseAssignment.objects.all()


@register_model_view(LicenseAssignment, 'edit')
class LicenseAssignmentEditView(ObjectEditView):
    queryset = LicenseAssignment.objects.all()
    form = LicenseAssignmentForm


@register_model_view(LicenseAssignment, 'delete')
class LicenseAssignmentDeleteView(ObjectDeleteView):
    queryset = LicenseAssignment.objects.all()


@register_model_view(LicenseAssignment, 'bulk_edit')
class LicenseAssignmentBulkEditView(BulkEditView):
    queryset = LicenseAssignment.objects.all()
    filterset = LicenseAssignmentFilterSet
    table = LicenseAssignmentTable
    form = LicenseAssignmentBulkEditForm


@register_model_view(LicenseAssignment, 'bulk_delete')
class LicenseAssignmentBulkDeleteView(BulkDeleteView):
    queryset = LicenseAssignment.objects.all()
    filterset = LicenseAssignmentFilterSet
    table = LicenseAssignmentTable
