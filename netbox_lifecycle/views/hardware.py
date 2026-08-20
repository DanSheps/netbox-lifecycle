from extras.ui.panels import TagsPanel, CustomFieldsPanel
from netbox.views.generic import (
    BulkDeleteView,
    BulkEditView,
    BulkImportView,
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)
from netbox.ui import panels, layout
from netbox_lifecycle.ui import HardwareLifecyclePanel, HardwareLifecycleDatesPanel
from utilities.views import register_model_view

from netbox_lifecycle.filtersets import HardwareLifecycleFilterSet
from netbox_lifecycle.forms import (
    HardwareLifecycleBulkEditForm,
    HardwareLifecycleFilterForm,
    HardwareLifecycleImportForm,
)
from netbox_lifecycle.forms.model_forms import HardwareLifecycleForm
from netbox_lifecycle.models import HardwareLifecycle
from netbox_lifecycle.tables import HardwareLifecycleTable

__all__ = (
    'HardwareLifecycleBulkDeleteView',
    'HardwareLifecycleBulkEditView',
    'HardwareLifecycleBulkImportView',
    'HardwareLifecycleDeleteView',
    'HardwareLifecycleEditView',
    'HardwareLifecycleListView',
    'HardwareLifecycleView',
)


@register_model_view(HardwareLifecycle, name='list', path='', detail=False)
class HardwareLifecycleListView(ObjectListView):
    queryset = HardwareLifecycle.objects.all()
    table = HardwareLifecycleTable
    filterset = HardwareLifecycleFilterSet
    filterset_form = HardwareLifecycleFilterForm


@register_model_view(HardwareLifecycle)
class HardwareLifecycleView(ObjectView):
    queryset = HardwareLifecycle.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            HardwareLifecyclePanel(),
            HardwareLifecycleDatesPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            panels.RelatedObjectsPanel(),
            panels.CommentsPanel(),
        ],
    )


@register_model_view(HardwareLifecycle, 'add', detail=False)
@register_model_view(HardwareLifecycle, 'edit')
class HardwareLifecycleEditView(ObjectEditView):
    queryset = HardwareLifecycle.objects.all()
    form = HardwareLifecycleForm


@register_model_view(HardwareLifecycle, 'delete')
class HardwareLifecycleDeleteView(ObjectDeleteView):
    queryset = HardwareLifecycle.objects.all()


@register_model_view(HardwareLifecycle, 'bulk_edit', detail=False)
class HardwareLifecycleBulkEditView(BulkEditView):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable
    form = HardwareLifecycleBulkEditForm


@register_model_view(HardwareLifecycle, 'bulk_delete', detail=False)
class HardwareLifecycleBulkDeleteView(BulkDeleteView):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable


@register_model_view(HardwareLifecycle, 'bulk_import', detail=False)
class HardwareLifecycleBulkImportView(BulkImportView):
    queryset = HardwareLifecycle.objects.all()
    model_form = HardwareLifecycleImportForm
