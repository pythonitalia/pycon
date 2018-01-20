from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext as _

class YearFilter(SimpleListFilter):
    title = _('Year',)
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        dates = model_admin.model.objects.values_list('date', flat=True)
        return [(date.year, date.year) for date in dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__year=self.value())
