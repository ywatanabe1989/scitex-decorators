#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-05-31 20:00:00 (Claude)"
# File: /tests/scitex/gen/test__alternate_kwarg.py

from scitex_decorators import alternate_kwarg


class TestAlternateKwarg:
    """Test cases for alternate_kwarg function."""

    def test_alternate_key_used_when_primary_missing_result_primary_key_alt_value(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == "alt_value"

    def test_alternate_key_used_when_primary_missing_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_primary_key_preserved_when_present_result_primary_key_primary_value(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": "primary_value", "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == "primary_value"

    def test_primary_key_preserved_when_present_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": "primary_value", "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_none_value_in_primary_key_replaced_result_primary_key_alt_value(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": None, "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == "alt_value"

    def test_none_value_in_primary_key_replaced_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": None, "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_empty_string_in_primary_key_replaced_result_primary_key_alt_value(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": "", "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == "alt_value"

    def test_empty_string_in_primary_key_replaced_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": "", "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_false_value_in_primary_key_replaced_result_primary_key_alt_value(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": False, "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == "alt_value"

    def test_false_value_in_primary_key_replaced_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": False, "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_zero_value_in_primary_key_replaced_result_primary_key_alt_value(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": 0, "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == "alt_value"

    def test_zero_value_in_primary_key_replaced_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": 0, "alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_no_alternate_key_present_result_primary_key_is_none(self):
        # Arrange
        # Arrange
        kwargs = {"other_key": "other_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] is None

    def test_no_alternate_key_present_result_other_key_other_value(self):
        # Arrange
        # Arrange
        kwargs = {"other_key": "other_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["other_key"] == "other_value"


    def test_neither_key_present(self):
        """Test behavior when neither key is present."""
        # Arrange
        kwargs = {"other_key": "other_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Assert
        assert result["primary_key"] is None

    def test_modifies_original_dict_kwargs_is_result(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert kwargs is result  # Same object reference

    def test_modifies_original_dict_alt_key_not_in_kwargs(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in kwargs

    def test_modifies_original_dict_primary_key_in_kwargs(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": "alt_value"}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "primary_key" in kwargs


    def test_complex_values_result_primary_key_nested_value(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": {"nested": "value"}}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == {"nested": "value"}

    def test_complex_values_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"alt_key": {"nested": "value"}}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    def test_list_values_result_primary_key_1_2_3(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": [], "alt_key": [1, 2, 3]}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert result["primary_key"] == [1, 2, 3]

    def test_list_values_alt_key_not_in_result(self):
        # Arrange
        # Arrange
        kwargs = {"primary_key": [], "alt_key": [1, 2, 3]}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Act
        # Assert
        # Assert
        assert "alt_key" not in result


    @pytest.mark.parametrize(
        "primary_val,alt_val,expected",
        [
            (None, "alt", "alt"),
            ("", "alt", "alt"),
            (False, "alt", "alt"),
            (0, "alt", "alt"),
            ("primary", "alt", "primary"),
            (True, "alt", True),
            (1, "alt", 1),
            ("non-empty", "alt", "non-empty"),
        ],
    )
    def test_parametrized_values_result_primary_key_expected(self, primary_val, alt_val, expected):
        """Parametrized test for various value combinations."""
        # Arrange
        kwargs = {"primary_key": primary_val, "alt_key": alt_val}
        # Act
        result = alternate_kwarg(kwargs, "primary_key", "alt_key")
        # Assert
        assert result["primary_key"] == expected


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# --------------------------------------------------------------------------------
# Start of Source Code from: /home/ywatanabe/proj/scitex-code/src/scitex/gen/_alternate_kwarg.py
# --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-02 13:30:41 (ywatanabe)"
# # File: ./scitex_repo/src/scitex/gen/_alternate_kwarg.py
#
#
# def alternate_kwarg(kwargs, primary_key, alternate_key):
#     alternate_value = kwargs.pop(alternate_key, None)
#     kwargs[primary_key] = kwargs.get(primary_key) or alternate_value
#     return kwargs
#
#
# # EOF

# --------------------------------------------------------------------------------
# End of Source Code from: /home/ywatanabe/proj/scitex-code/src/scitex/gen/_alternate_kwarg.py
# --------------------------------------------------------------------------------
