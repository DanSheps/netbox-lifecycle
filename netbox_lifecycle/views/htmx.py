from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View

from dcim.models import Device

from netbox_lifecycle.constants import (
    CONTRACT_STATUS_ACTIVE,
    CONTRACT_STATUS_EXPIRED,
    CONTRACT_STATUS_FUTURE,
    CONTRACT_STATUS_UNSPECIFIED,
)
from netbox_lifecycle.models import SupportContractAssignment


__all__ = (
    'DeviceContractsHTMXView',
    'DeviceContractsExpiredHTMXView',
)


class DeviceContractsHTMXView(LoginRequiredMixin, View):
    """HTMX endpoint for device contract card content."""

    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        assignments = SupportContractAssignment.objects.filter(
            device=device
        ).select_related(
            'contract', 'contract__vendor', 'sku', 'sku__manufacturer', 'license'
        )

        grouped = {
            CONTRACT_STATUS_ACTIVE: [],
            CONTRACT_STATUS_FUTURE: [],
            CONTRACT_STATUS_UNSPECIFIED: [],
            CONTRACT_STATUS_EXPIRED: [],
        }
        for assignment in assignments:
            grouped[assignment.status].append(assignment)

        return render(
            request,
            'netbox_lifecycle/htmx/device_contracts.html',
            {
                'device': device,
                'active': grouped[CONTRACT_STATUS_ACTIVE],
                'future': grouped[CONTRACT_STATUS_FUTURE],
                'unspecified': grouped[CONTRACT_STATUS_UNSPECIFIED],
                'expired_count': len(grouped[CONTRACT_STATUS_EXPIRED]),
            },
        )


class DeviceContractsExpiredHTMXView(LoginRequiredMixin, View):
    """HTMX endpoint for expired contracts only."""

    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        expired = [
            a
            for a in SupportContractAssignment.objects.filter(
                device=device
            ).select_related(
                'contract', 'contract__vendor', 'sku', 'sku__manufacturer', 'license'
            )
            if a.status == CONTRACT_STATUS_EXPIRED
        ]

        return render(
            request,
            'netbox_lifecycle/htmx/contract_list.html',
            {
                'assignments': expired,
            },
        )
