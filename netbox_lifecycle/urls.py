from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import views
from .models import HardwareLifecycle, SupportContract, License, LicenseAssignment, SupportContractDeviceAssignment

urlpatterns = [
    path('lifecycle/', views.HardwareLifecycleListView.as_view(), name='hardwarelifecycle_list'),
    path('lifecycle/add', views.HardwareLifecycleEditView.as_view(), name='hardwarelifecycle_add'),
    path('lifecycle/<int:pk>', views.HardwareLifecycleView.as_view(), name='hardwarelifecycle'),
    path('lifecycle/<int:pk>/edit', views.HardwareLifecycleEditView.as_view(), name='hardwarelifecycle_edit'),
    path('lifecycle/<int:pk>/delete', views.HardwareLifecycleDeleteView.as_view(), name='hardwarelifecycle_delete'),
    path('lifecycle/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='hardwarelifecycle_changelog', kwargs={'model': HardwareLifecycle}),

    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/add', views.VendorEditView.as_view(), name='vendor_add'),
    path('vendors/<int:pk>', views.VendorView.as_view(), name='vendor'),
    path('vendors/<int:pk>/edit', views.VendorEditView.as_view(), name='vendor_edit'),
    path('vendors/<int:pk>/delete', views.VendorDeleteView.as_view(), name='vendor_delete'),
    path('vendors/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='vendor_changelog', kwargs={'model': SupportContract}),

    path('contracts/', views.SupportContractListView.as_view(), name='supportcontract_list'),
    path('contracts/add', views.SupportContractEditView.as_view(), name='supportcontract_add'),
    path('contracts/<int:pk>', views.SupportContractView.as_view(), name='supportcontract'),
    path('contracts/<int:pk>/devices', views.SupportContractDeviceView.as_view(), name='supportcontract_devices'),
    #path('contracts/<int:pk>/licenses', views.SupportContractLicenseView.as_view(), name='supportcontract_licenses'),
    path('contracts/<int:pk>/edit', views.SupportContractEditView.as_view(), name='supportcontract_edit'),
    path('contracts/<int:pk>/delete', views.SupportContractDeleteView.as_view(), name='supportcontract_delete'),
    path('contracts/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='supportcontract_changelog', kwargs={'model': SupportContract}),

    path('contract_assignment/add', views.SupportContractDeviceAssignmentEditView.as_view(), name='supportcontractdeviceassignment_add'),
    path('contract_assignment/<int:pk>/edit', views.SupportContractDeviceAssignmentEditView.as_view(), name='supportcontractdeviceassignment_edit'),
    path('contract_assignment/<int:pk>/delete', views.SupportContractDeviceAssignmentDeleteView.as_view(), name='supportcontractdeviceassignment_delete'),
    path('contract_assignment/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='supportcontractdeviceassignment_changelog', kwargs={'model': SupportContractDeviceAssignment}),

    path('license/', views.LicenseListView.as_view(), name='license_list'),
    path('license/add', views.LicenseEditView.as_view(), name='license_add'),
    path('license/<int:pk>', views.LicenseView.as_view(), name='license'),
    path('license/<int:pk>/assignments', views.LicenseAssignmentView.as_view(), name='license_assignments'),
    path('license/<int:pk>/edit', views.LicenseEditView.as_view(), name='license_edit'),
    path('license/<int:pk>/delete', views.LicenseDeleteView.as_view(), name='license_delete'),
    path('license/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='license_changelog', kwargs={'model': License}),

    path('license_assignment/add', views.LicenseAssignmentEditView.as_view(), name='licenseassignment_add'),
    path('license_assignment/<int:pk>/edit', views.LicenseAssignmentEditView.as_view(), name='licenseassignment_edit'),
    path('license_assignment/<int:pk>/delete', views.LicenseAssignmentDeleteView.as_view(), name='licenseassignment_delete'),
    path('license_assignment/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='licenseassignment_changelog', kwargs={'model': LicenseAssignment}),
]
