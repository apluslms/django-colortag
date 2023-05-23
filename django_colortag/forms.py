from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import ColorTag

class ColorTagForm(forms.ModelForm):
    class Meta:
        model = ColorTag
        fields = (
            'name',
            'slug',
            'description',
            'color',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean(self):
        cleaned_data = self.cleaned_data # NOTE: ignore unique constraints, so DO NOT call super().clean()

        # create slug from name if there is no slug, but there is name
        name = cleaned_data.get('name')
        if not cleaned_data.get('slug') and name:
            cleaned_data['slug'] = slugify(name)

        return cleaned_data
