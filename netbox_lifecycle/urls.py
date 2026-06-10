from django.urls import path, include
from utilities.urls import get_model_urls

from . import views

app_name = 'netbox_lifecycle'


urlpatterns = [
    path(
        'lifecycles/',
        include(get_model_urls(app_name, 'hardwarelifecycle', detail=False)),
    ),
    path(
        'lifecycles/<int:pk>/', include(get_model_urls(app_name, 'hardwarelifecycle'))
    ),
    path('vendor/', include(get_model_urls(app_name, 'vendor', detail=False))),
    path('vendor/<int:pk>/', include(get_model_urls(app_name, 'vendor'))),
    path(
        'contract/', include(get_model_urls(app_name, 'supportcontract', detail=False))
    ),
    path('contract/<int:pk>/', include(get_model_urls(app_name, 'supportcontract'))),
    path(
        'contract-assignments/',
        include(get_model_urls(app_name, 'supportcontractassignment', detail=False)),
    ),
    path(
        'contract-assignments/<int:pk>/',
        include(get_model_urls(app_name, 'supportcontractassignment')),
    ),
    path('sku/', include(get_model_urls(app_name, 'supportsku', detail=False))),
    path('sku/<int:pk>/', include(get_model_urls(app_name, 'supportsku'))),
    path('license/', include(get_model_urls(app_name, 'license', detail=False))),
    path('license/<int:pk>/', include(get_model_urls(app_name, 'license'))),
    path(
        'license-assignments/',
        include(get_model_urls(app_name, 'licenseassignment', detail=False)),
    ),
    path(
        'license-assignments/<int:pk>/',
        include(get_model_urls(app_name, 'licenseassignment')),
    ),
    # Cisco EoX settings
    path(
        'cisco-eox/settings/',
        views.CiscoEoXSettingsView.as_view(),
        name='cisco_eox_settings',
    ),
    path(
        'cisco-eox/settings/edit/',
        views.CiscoEoXSettingsEditView.as_view(),
        name='cisco_eox_settings_edit',
    ),
    path(
        'cisco-eox/run-now/',
        views.CiscoEoXRunNowView.as_view(),
        name='cisco_eox_run_now',
    ),
]
