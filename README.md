Django colortag
================

Tools to help building data tagging models.
Used for example in A+ and MOOC-Jutut projects to tag feedbacks or users with colored tags.
Project builds on top of Django and django-html5-colorfield.

Installation and usage
----------------------

Requirements:

 * [Django](https://www.djangoproject.com/) 3.2+ (Django 1.11 to Django 3 are supported in versions 2.0 to 2.3 of this project; Django 1.9 and 1.10 are supported in versions 1.X of this project)
 * [django-html5-colorfield](https://github.com/knyghty/django-html5-colorfield) 2.0+
 * [js-jquery-toggle-django](https://github.com/Aalto-LeTech/js-jquery-toggle) for `jquery_toggle.js`
 * (recommended) [raphendyr-django-essentials](https://github.com/raphendyr/raphendyr-django-essentials) for app dependency management

Add stuff to `requirements.txt`:

```
git+https://github.com/Aalto-LeTech/django-colortag.git@2.0.0#egg=django-colortag==2.0.0
```

Install them with `pip install --process-dependency-links -r requirements.txt`
(`--process-dependency-links` is needed, if you don't have `js-jquery-toggle` in `requirements.txt` as it's not disributed via pypi).

Add relevant stuff to `INSTALLED_APPS`:

 * `js_jquery_toggle`, if you are not using app dependency loading
 * `django_colortag`

Add something like this to your html header:

```html+django
<!-- TODO: load bootstrap v3 css -->
<!-- TODO: load jquery -->
<!-- jquery toggle is used by colortag js -->
{% include 'jquery_toggle.head.html' %}
<!-- defines django_colortag_choice js function -->
{% include 'django_colortag.head.html' %}
```

For bootstrap tooltips to work, you need to do something like this:

```javascript
$(function() {
  $('.colortag[data-toggle="tooltip"]').tooltip();
  $('.colortag-choice').each(django_colortag_choice); /* only needed if you use ColortagChoiceFilter, ColortagChoiceField or ColortagSelectMultiple */
});
```

You can render colortag in your templates like this:

```html+django
{{ tag.render_as_button }}
<!-- or -->
{% load colortag %}
{{ tag|colortag_button }}
```

For tags to exists, define model like this:

```python
from django_colortag.models import ColorTag

class ItemTag(ColorTag):
    items = models.ManyToManyField(Items, related_name='tags')
```

You can use colortags in filters like this:

```python
import django_filters
from django_colortag.filters import ColortagChoiceFilter

class TagFilter(django_filters.FilterSet):
    tags = ColortagChoiceFilter()
```
