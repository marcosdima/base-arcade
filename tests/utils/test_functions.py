import pytest
from src.utils import Functions


@pytest.fixture
def nested_dict():
    return {
        "a": 1,
        "b": {
            "c": 2,
            "d": {
                "e": 3,
            },
        },
    }


def test_get_dict_keys_returns_all_keys_including_nested_keys(nested_dict):
    keys = Functions.get_dict_keys(nested_dict)
    assert keys == ["a", "b", "b.c", "b.d", "b.d.e"]


def test_get_dict_keys_with_custom_separator(nested_dict):
    keys = Functions.get_dict_keys(nested_dict, separator="/")
    assert keys == ["a", "b", "b/c", "b/d", "b/d/e"]    
