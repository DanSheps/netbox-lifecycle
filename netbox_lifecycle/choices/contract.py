from django.utils.translation import gettext as _
from utilities.choices import ChoiceSet

from netbox_lifecycle import constants


class ContractStatusChoices(ChoiceSet):
    """
    Support contract status choices.
    """

    ACTIVE = constants.CONTRACT_STATUS_ACTIVE
    EXPIRED = constants.CONTRACT_STATUS_EXPIRED
    FUTURE = constants.CONTRACT_STATUS_FUTURE
    UNSPECIFIED = constants.CONTRACT_STATUS_UNSPECIFIED

    CHOICES = (
        (ACTIVE, _('Active')),
        (FUTURE, _('Future')),
        (UNSPECIFIED, _('Unspecified')),
        (EXPIRED, _('Expired')),
    )
