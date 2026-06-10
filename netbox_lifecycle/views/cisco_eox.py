"""
Views for the Cisco EoX Settings page.

Three views are provided:

* CiscoEoXSettingsView    — display current settings + recent job history
* CiscoEoXSettingsEditView — edit/save the CiscoEoXSettings record
* CiscoEoXRunNowView       — POST-only; immediately enqueues the sync job
"""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from netbox_lifecycle.forms.eox import CiscoEoXSettingsForm
from netbox_lifecycle.jobs import CiscoEoXSyncJob
from netbox_lifecycle.models.eox import CiscoEoXSettings

__all__ = (
    'CiscoEoXSettingsView',
    'CiscoEoXSettingsEditView',
    'CiscoEoXRunNowView',
)


class CiscoEoXSettingsView(PermissionRequiredMixin, View):
    """Display the current Cisco EoX settings and recent job history."""

    permission_required = 'netbox_lifecycle.view_ciscoeoxsettings'
    template_name = 'netbox_lifecycle/cisco_eox_settings.html'

    def get(self, request):
        settings_obj = CiscoEoXSettings.get_or_create_settings()

        # Recent jobs — core.models.Job tracks JobRunner executions
        try:
            from core.models import Job

            recent_jobs = Job.objects.filter(name=CiscoEoXSyncJob.Meta.name).order_by(
                '-created'
            )[:10]
        except Exception:
            recent_jobs = []

        return render(
            request,
            self.template_name,
            {
                'settings_obj': settings_obj,
                'recent_jobs': recent_jobs,
            },
        )


class CiscoEoXSettingsEditView(PermissionRequiredMixin, View):
    """Create or update the singleton CiscoEoXSettings record."""

    permission_required = 'netbox_lifecycle.change_ciscoeoxsettings'
    template_name = 'netbox_lifecycle/cisco_eox_settings_edit.html'

    def get(self, request):
        settings_obj = CiscoEoXSettings.get_or_create_settings()
        form = CiscoEoXSettingsForm(instance=settings_obj)
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'settings_obj': settings_obj,
            },
        )

    def post(self, request):
        settings_obj = CiscoEoXSettings.get_or_create_settings()
        form = CiscoEoXSettingsForm(request.POST, instance=settings_obj)

        if form.is_valid():
            saved = form.save()

            # Re-schedule the sync job with the (potentially new) interval
            if saved.enabled and saved.client_id:
                CiscoEoXSyncJob.enqueue_once(interval=saved.sync_interval)
                messages.success(
                    request,
                    f'Cisco EoX sync scheduled (interval: {saved.sync_interval_display}).',
                )
            elif not saved.enabled:
                messages.info(request, 'Cisco EoX sync disabled. No job has been scheduled.')

            return redirect('plugins:netbox_lifecycle:cisco_eox_settings')

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'settings_obj': settings_obj,
            },
        )


class CiscoEoXRunNowView(PermissionRequiredMixin, View):
    """Immediately enqueue the Cisco EoX sync job (staff action)."""

    permission_required = 'netbox_lifecycle.change_ciscoeoxsettings'

    def post(self, request):
        from netbox_lifecycle.utilities.settings_loader import get_cisco_eox_settings

        cfg = get_cisco_eox_settings()
        if cfg is None:
            messages.error(
                request,
                'Cisco EoX is not configured or not enabled. '
                'Please save your settings first.',
            )
        else:
            CiscoEoXSyncJob.enqueue()
            messages.success(request, 'Cisco EoX sync job has been queued.')

        return redirect('plugins:netbox_lifecycle:cisco_eox_settings')
