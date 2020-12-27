from i18n.strings import LazyI18nString


def test_init_with_dictionary():
    s = LazyI18nString({"en": "Hello World!", "it": "Ciao Mondo!"})

    assert s.data == {"en": "Hello World!", "it": "Ciao Mondo!"}
    assert bool(s) is True


def test_init_json():
    s = LazyI18nString('{"en": "Hello World!", "it": "Ciao Mondo!"}')

    assert s.data == {"en": "Hello World!", "it": "Ciao Mondo!"}
    assert bool(s) is True


def test_init_invalid_json():
    s = LazyI18nString("Hello World!")

    assert s.data == "Hello World!"
    assert bool(s) is True


def test_empty_string():
    s = LazyI18nString({})

    assert s.data == {}
    assert bool(s) is False


def test_equal():
    s1 = LazyI18nString({"en": "Hello World!", "it": "Ciao Mondo!"})
    s2 = LazyI18nString({"en": "Hello World!", "it": "Ciao Mondo!"})

    assert s1 == s2


def test_not_equal_none():
    s1 = LazyI18nString({"en": "Hello World!", "it": "Ciao Mondo!"})
    s2 = None

    assert not s1 == s2


def test_not_equal():
    s1 = LazyI18nString({"en": "Hello World!", "it": "Ciao Mondo!"})
    s2 = LazyI18nString({"en": "Goodbye World!", "it": "Arrivederci Mondo!"})

    assert not s1 == s2
