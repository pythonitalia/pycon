from wagtail_localize.strings import StringValue

from cms.translator import OpenAITranslator


def test_openai_translator_can_translate(locale):
    en_locale = locale("en")
    it_locale = locale("it")

    translator = OpenAITranslator({})

    assert translator.can_translate(en_locale, it_locale)


def test_openai_translator_cant_translate_to_same_language(locale):
    en_locale = locale("en")

    translator = OpenAITranslator({})

    assert not translator.can_translate(en_locale, en_locale)


def test_openai_translator(locale, mocker):
    mock_openai = mocker.patch("cms.translator.OpenAI")
    mock_completion = mock_openai.return_value.beta.chat.completions
    mock_completion.parse.return_value.choices[0].message.parsed.translations = [
        "Test 1",
        "Test 2",
    ]

    en_locale = locale("en")
    it_locale = locale("it")

    translator = OpenAITranslator({})

    strings = [
        StringValue("Hello, world!"),
        StringValue("This is a test."),
    ]

    translation = translator.translate(en_locale, it_locale, strings)

    assert translation[strings[0]].data == "Test 1"
    assert translation[strings[1]].data == "Test 2"
