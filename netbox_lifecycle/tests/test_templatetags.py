from django.test import TestCase

from netbox_lifecycle.constants import (
    CONTRACT_STATUS_ACTIVE,
    CONTRACT_STATUS_EXPIRED,
    CONTRACT_STATUS_FUTURE,
    CONTRACT_STATUS_UNSPECIFIED,
)
from netbox_lifecycle.templatetags.filters import contract_status_badge


class ContractStatusBadgeFilterTest(TestCase):
    def test_active_status_badge(self):
        result = contract_status_badge(CONTRACT_STATUS_ACTIVE)
        self.assertIn('text-bg-success', result)
        self.assertIn('Active', result)

    def test_future_status_badge(self):
        result = contract_status_badge(CONTRACT_STATUS_FUTURE)
        self.assertIn('text-bg-info', result)
        self.assertIn('Future', result)

    def test_unspecified_status_badge(self):
        result = contract_status_badge(CONTRACT_STATUS_UNSPECIFIED)
        self.assertIn('text-bg-secondary', result)
        self.assertIn('Unspecified', result)

    def test_expired_status_badge(self):
        result = contract_status_badge(CONTRACT_STATUS_EXPIRED)
        self.assertIn('text-bg-danger', result)
        self.assertIn('Expired', result)

    def test_invalid_status_returns_empty(self):
        result = contract_status_badge('invalid')
        self.assertEqual(result, '')

    def test_none_status_returns_empty(self):
        result = contract_status_badge(None)
        self.assertEqual(result, '')
