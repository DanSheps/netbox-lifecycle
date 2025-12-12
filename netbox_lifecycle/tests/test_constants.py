from django.test import TestCase

from netbox_lifecycle.constants import (
    CONTRACT_STATUS_ACTIVE,
    CONTRACT_STATUS_EXPIRED,
    CONTRACT_STATUS_FUTURE,
    CONTRACT_STATUS_UNSPECIFIED,
    CONTRACT_STATUS_COLOR,
)


class ContractStatusConstantsTest(TestCase):
    def test_status_constants_defined(self):
        self.assertEqual(CONTRACT_STATUS_ACTIVE, 'active')
        self.assertEqual(CONTRACT_STATUS_FUTURE, 'future')
        self.assertEqual(CONTRACT_STATUS_UNSPECIFIED, 'unspecified')
        self.assertEqual(CONTRACT_STATUS_EXPIRED, 'expired')

    def test_status_color_mapping_complete(self):
        self.assertIn(CONTRACT_STATUS_ACTIVE, CONTRACT_STATUS_COLOR)
        self.assertIn(CONTRACT_STATUS_FUTURE, CONTRACT_STATUS_COLOR)
        self.assertIn(CONTRACT_STATUS_UNSPECIFIED, CONTRACT_STATUS_COLOR)
        self.assertIn(CONTRACT_STATUS_EXPIRED, CONTRACT_STATUS_COLOR)

    def test_status_color_format(self):
        for status, (label, color) in CONTRACT_STATUS_COLOR.items():
            self.assertIsInstance(str(label), str)
            self.assertIn(color, ['success', 'info', 'secondary', 'danger'])
