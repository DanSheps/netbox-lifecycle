from dcim.models import Manufacturer
from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import (
    CSVChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet

from netbox_lifecycle.choices.eox import DriverChoices
from netbox_lifecycle.models import EoXAPISettings

__all__ = (
    'EoXAPISettingsBulkEditForm',
    'EoXAPISettingsFilterForm',
    'EoXAPISettingsForm',
    'EoXAPISettingsImportForm',
)


class EoXAPISettingsForm(NetBoxModelForm):
    manufacturers = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        selector=True,
        label=_('Manufacturers'),
    )
    client_secret = forms.CharField(
        label=_('OAuth Client Secret'),
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text=_(
            'Leave blank to keep the existing secret. Stored encrypted at rest.'
        ),
    )

    fieldsets = (
        FieldSet('driver', 'url', 'manufacturers', 'enabled', name=_('Endpoint')),
        FieldSet('client_id', 'client_secret', name=_('Credentials')),
        FieldSet('sync_interval', name=_('Schedule')),
    )

    class Meta:
        model = EoXAPISettings
        fields = (
            'driver',
            'url',
            'manufacturers',
            'enabled',
            'client_id',
            'client_secret',
            'sync_interval',
            'description',
            'comments',
            'tags',
        )

    def clean(self):
        super().clean()
        secret = self.cleaned_data.get('client_secret', '').strip()
        if secret:
            self.instance.client_secret = secret


class EoXAPISettingsFilterForm(NetBoxModelFilterSetForm):
    model = EoXAPISettings
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('driver', 'enabled', 'manufacturer_id', name=_('Endpoint')),
    )

    driver = forms.MultipleChoiceField(
        choices=DriverChoices,
        required=False,
        label=_('Driver'),
    )
    enabled = forms.NullBooleanField(
        required=False,
        label=_('Enabled'),
        widget=forms.Select(
            choices=((None, '---------'), (True, _('Yes')), (False, _('No'))),
        ),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer'),
    )
    tag = TagFilterField(model)


class EoXAPISettingsImportForm(NetBoxModelImportForm):
    driver = CSVChoiceField(
        choices=DriverChoices,
        label=_('Driver'),
    )

    class Meta:
        model = EoXAPISettings
        fields = (
            'driver',
            'url',
            'enabled',
            'client_id',
            'sync_interval',
            'description',
            'comments',
            'tags',
        )


class EoXAPISettingsBulkEditForm(NetBoxModelBulkEditForm):
    enabled = forms.NullBooleanField(
        required=False,
        widget=forms.Select(
            choices=((None, '---------'), (True, _('Yes')), (False, _('No'))),
        ),
    )
    sync_interval = forms.IntegerField(
        required=False,
        label=_('Sync interval (minutes)'),
    )
    description = forms.CharField(
        max_length=200,
        required=False,
        label=_('Description'),
    )

    model = EoXAPISettings
    fieldsets = (FieldSet('enabled', 'sync_interval', 'description'),)
    nullable_fields = ('description',)
