from django.contrib.admin import FieldListFilter

from countries import countries


class CountryFilter(FieldListFilter):
    """
    Custom filter for Country fields in Django Admin.

    This filter will display only the countries that are actually used in the
    objects of the model.
    Each country is displayed with its name and emoji.
    """

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = "%s__exact" % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        self.field_generic = "%s__" % field_path
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        """
        Return the expected parameters for the filter.

        This is used by Django admin to build the correct query string.
        """
        return [self.lookup_kwarg]

    def choices(self, changelist):
        """
        Generate the choices for the filter.

        This method retrieves the countries actually used in the model instances
        and yields the choices for the filter.
        """
        # Retrieve the distinct country codes used in the model
        used_countries = set(
            changelist.model.objects.values_list(self.field_path, flat=True)
        )

        # Map these codes to their corresponding names and emojis
        country_choices = [
            (country.code, f"{country.name} {country.emoji}")
            for country in countries
            if country.code in used_countries
        ]

        for code, name in country_choices:
            yield {
                "selected": self.lookup_val == str(code),
                "query_string": changelist.get_query_string({self.lookup_kwarg: code}),
                "display": name,
            }
