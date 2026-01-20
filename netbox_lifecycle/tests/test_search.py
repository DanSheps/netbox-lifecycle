from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase

from netbox_lifecycle.search import (
    SupportContractAssignmentIndex,
    LicenseAssignmentIndex,
)


class SearchIndexDisplayAttrsTestCase(TestCase):
    """
    Test that search index display_attrs reference valid model fields.

    Regression test for GitHub issue #133:
    Search error "SupportContractAssignment has no field named 'vendor'"
    """

    def test_support_contract_assignment_display_attrs_are_valid_fields(self):
        """
        SupportContractAssignmentIndex.display_attrs should only reference
        fields that exist on the SupportContractAssignment model.
        """
        index = SupportContractAssignmentIndex()
        model = index.model

        for attr in index.display_attrs:
            # This should not raise FieldDoesNotExist
            try:
                model._meta.get_field(attr)
            except FieldDoesNotExist:
                self.fail(
                    f"SupportContractAssignmentIndex.display_attrs references "
                    f"non-existent field '{attr}' on {model.__name__}"
                )

    def test_license_assignment_display_attrs_are_valid_fields(self):
        """
        LicenseAssignmentIndex.display_attrs should only reference
        fields that exist on the LicenseAssignment model.
        """
        index = LicenseAssignmentIndex()
        model = index.model

        for attr in index.display_attrs:
            # This should not raise FieldDoesNotExist
            try:
                model._meta.get_field(attr)
            except FieldDoesNotExist:
                self.fail(
                    f"LicenseAssignmentIndex.display_attrs references "
                    f"non-existent field '{attr}' on {model.__name__}"
                )
