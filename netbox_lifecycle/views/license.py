from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView
from netbox_lifecycle.filtersets import LicenseFilterSet, LicenseAssignmentFilterSet
from netbox_lifecycle.forms import LicenseFilterSetForm, LicenseForm, LicenseAssignmentForm
from netbox_lifecycle.models import License, LicenseAssignment
from netbox_lifecycle.tables import LicenseTable, LicenseAssignmentTable
from utilities.views import ViewTab, register_model_view


__all__ = (
    'LicenseListView',
    'LicenseView',
    'LicenseEditView',
    'LicenseDeleteView',
    'LicenseAssignmentView',
    'LicenseAssignmentEditView',
    'LicenseAssignmentDeleteView',
)

@register_model_view(License, name='list')
class LicenseListView(ObjectListView):
    queryset = License.objects.all()
    table = LicenseTable
    filterset = LicenseFilterSet
    filterset_form = LicenseFilterSetForm


@register_model_view(License)
class LicenseView(ObjectView):
    queryset = License.objects.all()


@register_model_view(License, 'edit')
class LicenseEditView(ObjectEditView):
    queryset = License.objects.all()
    form = LicenseForm


@register_model_view(License, 'delete')
class LicenseDeleteView(ObjectDeleteView):
    queryset = License.objects.all()



@register_model_view(License, 'assignments')
class LicenseAssignmentView(ObjectChildrenView):
    template_name = 'netbox_lifecycle/license/assignments.html'
    queryset = License.objects.all()
    child_model = LicenseAssignment
    table = LicenseAssignmentTable
    filterset = LicenseAssignmentFilterSet
    viewname = None
    actions = ['add', 'edit', 'delete']
    tab = ViewTab(
        label='License Assignments',
        badge=lambda obj: LicenseAssignment.objects.filter(license=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(license=parent)


@register_model_view(LicenseAssignment, 'edit')
class LicenseAssignmentEditView(ObjectEditView):
    queryset = LicenseAssignment.objects.all()
    form = LicenseAssignmentForm


@register_model_view(LicenseAssignment, 'delete')
class LicenseAssignmentDeleteView(ObjectDeleteView):
    queryset = LicenseAssignment.objects.all()

