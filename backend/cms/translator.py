import json
from wagtail_localize.machine_translators.base import BaseMachineTranslator
from openai import OpenAI
from wagtail_localize.strings import StringValue
from pydantic import BaseModel
from django.conf import settings


class Translations(BaseModel):
    translations: list[str]


class OpenAITranslator(BaseMachineTranslator):
    display_name = "OpenAI"

    def translate(self, source_locale, target_locale, strings):
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        source_locale_display_name = source_locale.get_display_name()
        target_locale_display_name = target_locale.get_display_name()

        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a professional translator specializing in inclusive, gender-neutral language.
Translate the {source_locale_display_name} website copy provided into {target_locale_display_name} while adhering to these guidelines:
- Do not assume or imply gender in any way.
- Do not translate the name of the conference "PyCon Italia."
- Always translate "male" and "female" as "man" and "woman," avoiding gendered language where possible.
- When referring to Python, always translate it as "Python programming language" and never as "serpent" or "snake."
- When referring to Python, you can use "Python," but never translate it as just "language." Always specify "Python programming language" if needed for clarity.
- Ensure the translation is clear, inclusive, and respects the diversity of the audience.
""",
                },
                {
                    "role": "user",
                    "content": json.dumps([string.data for string in strings]),
                },
            ],
            model="gpt-4o-mini",
            response_format=Translations,
        )
        translations = response.choices[0].message.parsed.translations
        return {
            string: StringValue(translation)
            for string, translation in zip(strings, translations)
        }

    def can_translate(self, source_locale, target_locale):
        return source_locale.language_code != target_locale.language_code
