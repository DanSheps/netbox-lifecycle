from django import forms

from netbox_lifecycle.models.cisco_eox import SYNC_INTERVAL_CHOICES, CiscoEoXSettings

__all__ = ('CiscoEoXSettingsForm',)


class CiscoEoXSettingsForm(forms.ModelForm):
    """
    Form for editing the singleton CiscoEoXSettings record.

    The client_secret field is rendered with a password widget so the value
    is never echoed back to the browser.  Leaving the field blank on edit
    preserves the existing encrypted value in the database.
    """

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
        choices=SYNC_INTERVAL_CHOICES,
        help_text='How often the background sync job should run.',
    )

    class Meta:
        model = CiscoEoXSettings
        fields = (
            'enabled',
            'client_id',
            'client_secret',
            'sync_interval',
            'manufacturer_names',
        )
        help_texts = {
            'client_id': (
                'Client ID from Cisco API Console '
                '(<a href="https://apiconsole.cisco.com/" target="_blank">'
                'apiconsole.cisco.com</a>).'
            ),
            'manufacturer_names': (
                'Comma-separated list of manufacturer names to query '
                '(e.g. <code>Cisco,Cisco Systems</code>).'
            ),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Only update the encrypted secret if a new value was provided
        new_secret = self.cleaned_data.get('client_secret', '').strip()
        if new_secret:
            instance.client_secret = new_secret
        # else: leave instance._client_secret unchanged (already loaded from DB)

        # Coerce sync_interval to int (ChoiceField returns strings)
        instance.sync_interval = int(self.cleaned_data['sync_interval'])

        if commit:
            instance.save()
        return instance
