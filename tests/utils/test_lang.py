import pytest

from src.services import Lang, Language


@pytest.fixture
def lang_instance(monkeypatch):
    Lang._instance = None
    monkeypatch.setattr(Lang, 'load_translations', lambda self: None)

    instance = Lang()
    instance.translations = {}

    yield instance

    Lang._instance = None


def assert_equal_lists_ignore_order(list1, list2):
    assert set(list1) == set(list2), (
        f'Expected {list1} and {list2} to have the same elements regardless of order'
    )


def test_check_structure_returns_report_with_keys_per_language(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {
            'title': 'Title',
            'start': 'Start',
        },
        Language.SPANISH: {
            'title': 'Titulo',
            'start': 'Comenzar',
        },
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH] == [], 'Expected no missing keys for English'
    assert report[Language.SPANISH] == [], 'Expected no missing keys for Spanish'


def test_check_structure_reports_missing_key_per_language(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {'title': 'Title', 'start': 'Start'},
        Language.SPANISH: {'title': 'Titulo'},
    }

    report = lang_instance.check_structure()

    assert report[Language.SPANISH] == ['start'], (
        'Expected "start" to be reported as missing for Spanish'
    )
    assert report[Language.ENGLISH] == [], 'Expected no missing keys for English'


def test_check_structure_allows_none_values(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {'title': 'Title', 'start': 'Start'},
        Language.SPANISH: {'title': 'Titulo', 'start': None},
    }

    report = lang_instance.check_structure()

    assert report[Language.SPANISH] == []
    assert report[Language.ENGLISH] == []


def test_check_structure_multiple_levels(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {
            'title': 'Title',
            'start': 'Start',
            'menu': {'play': 'Play'},
        },
        Language.SPANISH: {
            'title': 'Titulo',
            'start': 'Comenzar',
            'menu': {'play': 'Jugar'},
        },
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH] == []
    assert report[Language.SPANISH] == []


def test_check_structure_multiple_levels_with_missing_key(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {
            'title': 'Title',
            'start': 'Start',
            'menu': {'play': 'Play'},
        },
        Language.SPANISH: {'title': 'Titulo', 'start': 'Comenzar', 'menu': {}},
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH] == []
    assert report[Language.SPANISH] == ['menu.play']


def test_check_structure_multiple_levels_with_missing_keys(lang_instance: Lang):
    lang_instance.translations = {
        Language.ENGLISH: {
            'title': 'Title',
            'start': 'Start',
            'routes': {
                'settings': {
                    'audio': 'Audio',
                    'video': 'Video',
                },
            },
        },
        Language.SPANISH: {
            'title': 'Titulo',
            'start': 'Comenzar',
            'routes': {
                'home': 'Inicio',
            },
        },
    }

    report = lang_instance.check_structure()

    assert report[Language.ENGLISH] == ['routes.home']
    assert_equal_lists_ignore_order(
        report[Language.SPANISH],
        ['routes.settings', 'routes.settings.audio', 'routes.settings.video'],
    )
