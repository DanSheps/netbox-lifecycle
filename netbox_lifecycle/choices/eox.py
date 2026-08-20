from django.utils.translation import gettext_lazy as _
from utilities.choices import ChoiceSet

from netbox_lifecycle import constants


class DriverChoices(ChoiceSet):
    CISCO = constants.DRIVER_CISCO
    CHOICES = [
        (CISCO, _('Cisco EoX')),
    ]
