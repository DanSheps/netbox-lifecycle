from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField

from netbox_lifecycle.models import SupportContract, SupportSKU, SupportContractAssignment, LicenseAssignment


class SupportContractAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    contract = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        label=_('Contract'),
        required=False,
        selector=True
    )
    sku = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        label=_('SKU'),
        required=False,
        selector=True
    )

    model = SupportContractAssignment
    fieldsets = (
        (None, ('contract', 'sku')),
    )
    nullable_fields = ()


class LicenseAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    vendor = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        label=_('SKU'),
        required=False,
        selector=True
    )
    license = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        label=_('Contract'),
        required=False,
        selector=True
    )

    model = LicenseAssignment
    fieldsets = (
        (None, ('vendor', 'license', 'quantity')),
    )
    nullable_fields = ('quantity', )
