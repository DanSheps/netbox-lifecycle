from django.utils.translation import gettext_lazy as _

CONTRACT_STATUS_ACTIVE = 'active'
CONTRACT_STATUS_FUTURE = 'future'
CONTRACT_STATUS_UNSPECIFIED = 'unspecified'
CONTRACT_STATUS_EXPIRED = 'expired'

# (label, badge_color)
CONTRACT_STATUS_COLOR = {
    CONTRACT_STATUS_ACTIVE: (_('Active'), 'success'),
    CONTRACT_STATUS_FUTURE: (_('Future'), 'info'),
    CONTRACT_STATUS_UNSPECIFIED: (_('Unspecified'), 'secondary'),
    CONTRACT_STATUS_EXPIRED: (_('Expired'), 'danger'),
}
