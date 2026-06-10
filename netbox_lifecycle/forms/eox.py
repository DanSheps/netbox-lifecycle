from django import forms
from django.utils.translation import gettext_lazy as _

from netbox_lifecycle.models import EoXAPISettings


class EoXAPISettingsForm(PrimaryModelForm):

    url = forms.CharField(
        required=True,
        label=_('EoX API URL')
    )

    driver = forms.ChoiceField(
        choices=DriverChoiceSet,
        required=True,
        label=_('EoX Driver')
    )

    manufacturers = DynamicModelMultipleChoiceField(
        queryset=EoXAPISetting.objects.all(),
        required=True,
        selector=True,
        quick_add=True,
        label=_('Manufacturers')
    )

    client_secret = forms.CharField(
        label='OAuth Client Secret',
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text=(
            'Leave blank to keep the existing secret.  '
            'Stored encrypted at rest.'
        ),
    )

    sync_interval = forms.ChoiceField(
        label='Sync Interval',
        choices=SyncIntervalChoiceSet,
        help_text='How often the background sync job should run.',
    )

    class Meta:
        model = EoXAPISettings
        fields = (
            'url',
            'driver',
            'manufacturers',
            'enabled',
            'client_id',
            'client_secret',
            'sync_interval',
        )

        def clean(self):
            super.clean()

            new_secret = self.cleaned_data.get('client_secret', '').strip()
            if new_secret:
                self.cleaned_data['_client_secret'] = new_secret
