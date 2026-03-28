from dcim.models import Device
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View
from virtualization.models import VirtualMachine

from netbox_lifecycle.constants import (
    CONTRACT_STATUS_ACTIVE,
    CONTRACT_STATUS_EXPIRED,
    CONTRACT_STATUS_FUTURE,
    CONTRACT_STATUS_UNSPECIFIED,
)
from netbox_lifecycle.models import LicenseAssignment, SupportContractAssignment

MAX_LICENSE_DISPLAY = 10

__all__ = (
    'DeviceContractsExpiredHTMXView',
    'DeviceContractsHTMXView',
    'DeviceLicensesHTMXView',
    'VirtualMachineContractsExpiredHTMXView',
    'VirtualMachineContractsHTMXView',
    'VirtualMachineLicensesHTMXView',
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


class VirtualMachineContractsHTMXView(LoginRequiredMixin, View):
    """HTMX endpoint for virtual machine contract card content."""

    def get(self, request, pk):
        virtual_machine = get_object_or_404(VirtualMachine, pk=pk)
        assignments = SupportContractAssignment.objects.filter(
            virtual_machine=virtual_machine
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
            'netbox_lifecycle/htmx/virtualmachine_contracts.html',
            {
                'virtual_machine': virtual_machine,
                'active': grouped[CONTRACT_STATUS_ACTIVE],
                'future': grouped[CONTRACT_STATUS_FUTURE],
                'unspecified': grouped[CONTRACT_STATUS_UNSPECIFIED],
                'expired_count': len(grouped[CONTRACT_STATUS_EXPIRED]),
            },
        )


class DeviceLicensesHTMXView(LoginRequiredMixin, View):
    """HTMX endpoint for device license card content."""

    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        assignments = LicenseAssignment.objects.filter(device=device).select_related(
            'license', 'license__manufacturer', 'vendor'
        )

        total_count = assignments.count()
        show_all_url = None
        if total_count > MAX_LICENSE_DISPLAY:
            show_all_url = (
                f'/plugins/lifecycle/license-assignment/?device_id={device.pk}'
            )
            assignments = assignments[:MAX_LICENSE_DISPLAY]

        return render(
            request,
            'netbox_lifecycle/htmx/device_licenses.html',
            {
                'device': device,
                'assignments': assignments,
                'show_all_url': show_all_url,
            },
        )


class VirtualMachineLicensesHTMXView(LoginRequiredMixin, View):
    """HTMX endpoint for virtual machine license card content."""

    def get(self, request, pk):
        virtual_machine = get_object_or_404(VirtualMachine, pk=pk)
        assignments = LicenseAssignment.objects.filter(
            virtual_machine=virtual_machine
        ).select_related('license', 'license__manufacturer', 'vendor')

        total_count = assignments.count()
        show_all_url = None
        if total_count > MAX_LICENSE_DISPLAY:
            show_all_url = f'/plugins/lifecycle/license-assignment/?virtual_machine_id={virtual_machine.pk}'
            assignments = assignments[:MAX_LICENSE_DISPLAY]

        return render(
            request,
            'netbox_lifecycle/htmx/virtualmachine_licenses.html',
            {
                'virtual_machine': virtual_machine,
                'assignments': assignments,
                'show_all_url': show_all_url,
            },
        )


class VirtualMachineContractsExpiredHTMXView(LoginRequiredMixin, View):
    """HTMX endpoint for expired contracts only (virtual machine)."""

    def get(self, request, pk):
        virtual_machine = get_object_or_404(VirtualMachine, pk=pk)
        expired = [
            a
            for a in SupportContractAssignment.objects.filter(
                virtual_machine=virtual_machine
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
