from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from extras.ui.panels import CustomFieldsPanel, TagsPanel
from netbox.ui import layout, panels
from netbox.views.generic import (
    BulkDeleteView,
    BulkEditView,
    BulkImportView,
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)
from utilities.views import ObjectPermissionRequiredMixin, register_model_view

from netbox_lifecycle.filtersets import EoXAPISettingsFilterSet
from netbox_lifecycle.forms import (
    EoXAPISettingsBulkEditForm,
    EoXAPISettingsFilterForm,
    EoXAPISettingsForm,
    EoXAPISettingsImportForm,
)
from netbox_lifecycle.jobs import EoXManualSyncJob
from netbox_lifecycle.models import EoXAPISettings
from netbox_lifecycle.tables import EoXAPISettingsTable
from netbox_lifecycle.ui import EoXAPISettingsPanel

__all__ = (
    'EoXAPISettingsBulkDeleteView',
    'EoXAPISettingsBulkEditView',
    'EoXAPISettingsBulkImportView',
    'EoXAPISettingsDeleteView',
    'EoXAPISettingsEditView',
    'EoXAPISettingsListView',
    'EoXAPISettingsSyncView',
    'EoXAPISettingsView',
)


@register_model_view(EoXAPISettings, name='list', path='', detail=False)
class EoXAPISettingsListView(ObjectListView):
    queryset = EoXAPISettings.objects.all()
    table = EoXAPISettingsTable
    filterset = EoXAPISettingsFilterSet
    filterset_form = EoXAPISettingsFilterForm


@register_model_view(EoXAPISettings)
class EoXAPISettingsView(ObjectView):
    queryset = EoXAPISettings.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            EoXAPISettingsPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            panels.CommentsPanel(),
        ],
    )


@register_model_view(EoXAPISettings, 'add', detail=False)
@register_model_view(EoXAPISettings, 'edit')
class EoXAPISettingsEditView(ObjectEditView):
    queryset = EoXAPISettings.objects.all()
    form = EoXAPISettingsForm


@register_model_view(EoXAPISettings, 'delete')
class EoXAPISettingsDeleteView(ObjectDeleteView):
    queryset = EoXAPISettings.objects.all()


@register_model_view(EoXAPISettings, 'bulk_edit', detail=False)
class EoXAPISettingsBulkEditView(BulkEditView):
    queryset = EoXAPISettings.objects.all()
    filterset = EoXAPISettingsFilterSet
    table = EoXAPISettingsTable
    form = EoXAPISettingsBulkEditForm


@register_model_view(EoXAPISettings, 'bulk_delete', detail=False)
class EoXAPISettingsBulkDeleteView(BulkDeleteView):
    queryset = EoXAPISettings.objects.all()
    filterset = EoXAPISettingsFilterSet
    table = EoXAPISettingsTable


@register_model_view(EoXAPISettings, 'bulk_import', detail=False)
class EoXAPISettingsBulkImportView(BulkImportView):
    queryset = EoXAPISettings.objects.all()
    model_form = EoXAPISettingsImportForm


@register_model_view(EoXAPISettings, 'sync')
class EoXAPISettingsSyncView(ObjectPermissionRequiredMixin, View):
    """POST-only action that enqueues a one-shot EoX sync for this record."""

    queryset = EoXAPISettings.objects.all()
    permission_required = 'netbox_lifecycle.sync_eoxapisettings'

    def get_required_permission(self):
        return self.permission_required

    def post(self, request, pk):
        cfg = get_object_or_404(self.queryset, pk=pk)
        EoXManualSyncJob.enqueue(instance=cfg)
        messages.success(request, f'EoX sync queued for {cfg}.')
        return redirect(cfg.get_absolute_url())
