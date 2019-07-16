from django.db.models import Q

import django_filters

from .fields import (
    ColortagChoiceField,
    ColortagIEField,
    ColortagIEAndOrField
)


class ColortagChoiceFilter(django_filters.ModelMultipleChoiceFilter):
    field_class = ColortagChoiceField


class ColortagIncludeExcludeFilter(django_filters.ModelMultipleChoiceFilter):
    field_class = ColortagIEField

    def filter(self, qs, values, conjoined=False):
        includes, excludes = values
        if not includes and not excludes:
            return qs

        if not conjoined:
            q = Q()
        for v in set(includes):
            predicate = self.get_filter_predicate(v)
            if conjoined:
                qs = qs.filter(**predicate)
            else:
                q |= Q(**predicate)
        if not conjoined:
            qs = qs.filter(q)

        for v in set(excludes):
            predicate = self.get_filter_predicate(v)
            qs = qs.exclude(**predicate)

        return qs.distinct() if self.distinct else qs


class ColortagIEAndOrFilter(ColortagIncludeExcludeFilter):
    field_class = ColortagIEAndOrField

    def filter(self, qs, values):
        conjoined, inc_exc = values
        return super().filter(qs, inc_exc, conjoined=conjoined)
