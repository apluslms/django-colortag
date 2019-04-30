from django.forms import models

from .widgets import ColortagSelectMultiple


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
