import pytest

from src.utils.lang.lang import Lang, Language


@pytest.fixture
def lang_instance(monkeypatch):
    Lang._instance = None
    monkeypatch.setattr(Lang, "load_translations", lambda self: None)

    instance = Lang()
    instance.translations = {}

    yield instance

    Lang._instance = None


def assert_equal_lists_ignore_order(list1, list2):
    assert set(list1) == set(list2), f"Expected {list1} and {list2} to have the same elements regardless of order"


def test_check_structure_returns_report_with_keys_per_language(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {
            "title": "Title",
            "start": "Start",
        },
        Language.SPANISH: {
            "title": "Titulo",
            "start": "Comenzar",
        },
    }

    report = lang_instance.check_structure()
    print(f"Report: {report}")

    assert report[Language.ENGLISH] == []
    assert report[Language.SPANISH] == []


def test_check_structure_reports_missing_key_per_language(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {"title": "Title", "start": "Start"},
        Language.SPANISH: {"title": "Titulo"},
    }

    report = lang_instance.check_structure()

    assert report[Language.SPANISH]["missing_keys"] == ["start"]
    assert report[Language.ENGLISH]["missing_keys"] == []


def test_check_structure_reports_empty_key_when_value_is_none(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {"title": "Title", "start": "Start"},
        Language.SPANISH: {"title": "Titulo", "start": None},
    }

    report = lang_instance.check_structure()

    assert report[Language.SPANISH]["empty_keys"] == ["start"]
    assert report[Language.ENGLISH]["empty_keys"] == []


def test_check_structure_reports_empty_key_when_value_is_empty_string(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {"title": "Title", "start": "Start"},
        Language.SPANISH: {"title": "Titulo", "start": ""},
    }

    report = lang_instance.check_structure()

    assert report[Language.SPANISH]["empty_keys"] == ["start"]
    assert report[Language.ENGLISH]["empty_keys"] == []


def test_check_structure_multiple_levels(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {"title": "Title", "start": "Start", "menu": {"play": "Play"}},
        Language.SPANISH: {"title": "Titulo", "start": "Comenzar", "menu": {"play": "Jugar"}},
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH]["keys"] == ["menu-play", "start", "title"]
    assert report[Language.SPANISH]["keys"] == ["menu-play", "start", "title"]
    assert report[Language.ENGLISH]["missing_keys"] == []
    assert report[Language.SPANISH]["missing_keys"] == []


def test_check_structure_multiple_levels_with_missing_key(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {"title": "Title", "start": "Start", "menu": {"play": "Play"}},
        Language.SPANISH: {"title": "Titulo", "start": "Comenzar", "menu": {}},
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH]["keys"] == ["menu-play", "start", "title"]
    assert report[Language.SPANISH]["keys"] == ["start", "title"]
    assert report[Language.ENGLISH]["missing_keys"] == []
    assert report[Language.SPANISH]["missing_keys"] == ["menu-play"]
    

def test_check_structure_multiple_levels_with_missing_keys(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {
            "title": "Title",
            "start": "Start",
            "routes": {
                "settings": {
                    "audio": "Audio",
                    "video": "Video",
                },
            },
        },
        Language.SPANISH: {
            "title": "Titulo",
            "start": "Comenzar",
            "routes": {
                "home": "Inicio",
            },
        },
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH] == ["routes.home"]
    assert_equal_lists_ignore_order(
        report[Language.SPANISH],
        ["routes.settings","routes.settings.audio", "routes.settings.video"]
    )
