from django.db import models
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from colorfield.fields import ColorField
from functools import total_ordering

from .templatetags.colortag import render_as_button
from .utils import use_white_font

MAX_LENGTH = 20


@total_ordering
class ColorTag(models.Model):
    class Meta:
        abstract = True
        ordering = ['slug']

    name = models.CharField(max_length=MAX_LENGTH, help_text=_("Display name for tag"))
    slug = models.SlugField(max_length=MAX_LENGTH, help_text=_("Slug key for tag. If left blank, one is created from name"))
    description = models.CharField(max_length=155, blank=True, help_text=_("Describe the usage or meaning of this tag"))
    color = ColorField(default="#CD0000", help_text=_("Color that is used as background for this tag"))

    @cached_property
    def font_white(self):
        return use_white_font(self.color)

    @cached_property
    def font_color(self):
        return '#FFF' if self.font_white else '#000'

    def render_as_button(self, **options):
        return render_as_button(self, options)

    @cached_property
    def html_button(self):
        return render_as_button(self)

    @cached_property
    def html_label(self):
        return render_as_button(self, {'static': True})

    def __str__(self):
        return 'ColorTag({!r}, {!r}, {!r})'.format(
            self.name, self.slug, self.description
        )

    def __eq__(self, other):
        """Compare slugs if other is a string. Otherwise delegate to super"""
        if isinstance(other, str):
            return self.slug == other
        else:
            return super().__eq__(other)

    def __gt__(self, other):
        """Compare ColorTags by slug"""
        if isinstance(other, ColorTag):
            return self.slug > other.slug
        else:
            return NotImplemented

    def is_valid_slug(self, slug):
        """
        Check if the slug is valid. By default any slug is valid; you might want
        to override e.g. to implement uniqueness checks
        """
        return True

    def save(self, *args, **kwargs):
        assert self.name

        slug_candidate = self.slug or slugify(self.name)
        for i in range(1000):
            if self.is_valid_slug(slug_candidate):
                break
            else:
                slug_candidate += get_random_string(length=1)
        else:
            raise RuntimeError('Out of slugs')

        self.slug = slug_candidate

        return super().save(*args, **kwargs)
