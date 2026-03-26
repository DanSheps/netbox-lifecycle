from netbox.views.generic import (
    BulkDeleteView,
    BulkEditView,
    BulkImportView,
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)
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


@register_model_view(HardwareLifecycle, name='list')
class HardwareLifecycleListView(ObjectListView):
    queryset = HardwareLifecycle.objects.all()
    table = HardwareLifecycleTable
    filterset = HardwareLifecycleFilterSet
    filterset_form = HardwareLifecycleFilterForm


@register_model_view(HardwareLifecycle)
class HardwareLifecycleView(ObjectView):
    queryset = HardwareLifecycle.objects.all()

    def get_extra_context(self, request, instance):

        return {}


@register_model_view(HardwareLifecycle, 'edit')
class HardwareLifecycleEditView(ObjectEditView):
    queryset = HardwareLifecycle.objects.all()
    form = HardwareLifecycleForm


@register_model_view(HardwareLifecycle, 'bulk_edit')
class HardwareLifecycleBulkEditView(BulkEditView):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable
    form = HardwareLifecycleBulkEditForm


@register_model_view(HardwareLifecycle, 'delete')
class HardwareLifecycleDeleteView(ObjectDeleteView):
    queryset = HardwareLifecycle.objects.all()


@register_model_view(HardwareLifecycle, 'bulk_delete')
class HardwareLifecycleBulkDeleteView(BulkDeleteView):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable


@register_model_view(HardwareLifecycle, 'bulk_import')
class HardwareLifecycleBulkImportView(BulkImportView):
    queryset = HardwareLifecycle.objects.all()
    model_form = HardwareLifecycleImportForm
