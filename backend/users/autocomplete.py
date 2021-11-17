import json

from django.contrib.admin.widgets import SELECT2_TRANSLATIONS, AutocompleteSelect
from django.urls import reverse
from django.utils.translation import get_language

from users.client import get_users_data_by_ids


class UsersBackendAutocomplete(AutocompleteSelect):
    def __init__(self, admin_site, attrs=None, choices=(), using=None):
        self.admin_site = admin_site
        self.db = using
        self.choices = choices
        self.attrs = {} if attrs is None else attrs.copy()
        self.i18n_name = SELECT2_TRANSLATIONS.get(get_language())

    def build_attrs(self, base_attrs, extra_attrs=None):
        """
        Set select2's AJAX attributes.
        Attributes can be set using the html5 data attribute.
        Nested attributes require a double dash as per
        https://select2.org/configuration/data-attributes#nested-subkey-options
        """
        # attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs = {}
        attrs.setdefault("class", "")
        attrs.update(
            {
                "data-ajax--cache": "true",
                "data-ajax--delay": 250,
                "data-ajax--type": "GET",
                "data-ajax--url": reverse("admin:users-admin-autocomplete"),
                "data-theme": "admin-autocomplete",
                "data-allow-clear": json.dumps(not self.is_required),
                "data-placeholder": "",  # Allows clearing of the input.
                "lang": self.i18n_name,
                "class": attrs["class"]
                + (" " if attrs["class"] else "")
                + "admin-autocomplete",
            }
        )
        return attrs

    def optgroups(self, name, value, attr=None):
        default = (None, [], 0)
        groups = [default]

        if value and value[0]:
            users_by_id = get_users_data_by_ids(value)
        else:
            users_by_id = {}

        selected_choices = {str(v) for v in value}
        for choice in value:
            if not choice:
                continue

            index = len(default[1])
            subgroup = default[1]
            subgroup.append(
                self.create_option(
                    name,
                    choice,
                    users_by_id[choice]["displayName"],
                    selected_choices,
                    index,
                )
            )
        return groups
