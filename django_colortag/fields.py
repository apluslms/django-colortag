from django.forms import models, fields

from .widgets import (
    ColortagSelectMultiple,
    ColortagIEMultiWidget,
    ColortagIEAndOrWidget
)


class ModelChoiceInstanceIterator(models.ModelChoiceIterator):
    def choice(self, obj):
        # Add the model instance to the iterated items.
        (value, label) = super().choice(obj)
        return (value, label, obj)

class ColortagChoiceField(models.ModelMultipleChoiceField):
    widget = ColortagSelectMultiple
    iterator = ModelChoiceInstanceIterator
    # The iterator is used in the self.choices property, which is also set to
    # widget.choices. This custom iterator includes the original model instance
    # so that the widget may render instance-specific attributes in HTML.

    def label_from_instance(self, obj):
        return obj.name


class ColortagIEField(models.ModelMultipleChoiceField):
    widget = ColortagIEMultiWidget
    iterator = ModelChoiceInstanceIterator

    def set_queryset(self, queryset):
        self.queryset = queryset
        self.widget.set_subwidgets(queryset)

    def clean(self, value):
        includes = []
        excludes = []
        for v in value:
            if v == None or len(v) < 2:
                continue
            elif v[0] == 'I':
                includes.append(v[1:])
            elif v[0] == 'E':
                excludes.append(v[1:])
        includes_qs = super().clean(includes)
        excludes_qs = super().clean(excludes)
        return (includes_qs, excludes_qs)


class ColortagIEAndOrField(fields.MultiValueField):
    widget = ColortagIEAndOrWidget

    def __init__(self, queryset, *args, **kwargs):
        kwargs.setdefault('require_all_fields', False)
        subfields = (
            fields.BooleanField(required=False),
            ColortagIEField(queryset, required=False)
        )
        super().__init__(subfields, *args, **kwargs)

    def set_queryset(self, queryset):
        self.queryset = queryset
        self.fields[1].queryset = queryset
        self.widget.set_subwidgets(queryset)

    def compress(self, data_list):
        return data_list
