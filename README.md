Django colortag
===============

Tools to help building data tagging models.
Used for example in A+ and MOOC-Jutut projects to tag feedbacks or users with colored tags.
Project builds on top of Django and django-html5-colorfield.

Installation and usage
----------------------

Requirements:

 * [Django](https://www.djangoproject.com/) 3.2+
   (Django 4.2 is supported in the versions 2.4, 2.5 and 3.0 of this project;
   Django 1.11 to Django 3 are supported in versions 2.0 to 2.3 of this project;
   Django 1.9 and 1.10 are supported in versions 1.X of this project)
 * [jQuery](https://jquery.com/) (3.2+ is required for version 2.5+ version of this project)
 * [django-html5-colorfield](https://github.com/knyghty/django-html5-colorfield) 2.0+
 * [js-jquery-toggle-django](https://github.com/apluslms/js-jquery-toggle) for `jquery_toggle.js`
 * (recommended) [django-essentials](https://github.com/apluslms/django-essentials) for app dependency management

Add stuff to `requirements.txt`:

```
git+https://github.com/apluslms/django-colortag.git@3.0.0#egg=django-colortag~=3.0.0
```

Install them with `pip install --process-dependency-links -r requirements.txt`
(`--process-dependency-links` is needed, if you don't have `js-jquery-toggle` in `requirements.txt` as it's not disributed via pypi).

Add relevant stuff to `INSTALLED_APPS`:

 * `js_jquery_toggle`, if you are not using app dependency loading
 * `django_colortag`

Add something like this to your html header:

```html+django
<!-- TODO: load bootstrap v5 css -->
<!-- TODO: load jquery -->
<!-- jquery toggle is used by colortag js if using django_colortag_choice -->
{% include 'jquery_toggle.head.html' %}
<!-- defines django_colortag_choice js function and setup for inc-exc-filters -->
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

### Using `ColortagIncludeExcludeFilter` and the `ColortagIEAndOrFilter`

The `ColortagIncludeExcludeFilter` and the `ColortagIEAndOrFilter` can be used to generate filters where for each tag you can determine if search results should include or exclude the tag in question.
When using the `ColortagIncludeExcludeFilter`, search results are limited to those that have all of the selected tags to be included.
However, when using the `ColortagIEAndOrFilter`, the user can specify if the tags to be included should be joined with an OR or an AND operator.

For example, if the OR option is selected, and the tags *Respond* and *URGENT!* are selected to be included, while the *DONE* and *Other teacher* tags are selected to be excluded, the filter applies the following search query to the tags:
  *Respond* OR *URGENT!* AND NOT *DONE* AND NOT *Other teacher*
I.e. the filter limits the search results to those that have either (or both) of the tags *Respond* or *URGENT!*, but do not have the tag *DONE* nor the tag *Other teacher*.
If the *AND* option would have been selected, the query would have otherwise been identical, but search results would have had to have both *Respond* AND *URGENT!*.

![ColortagIEAndOrFilter with tags respectively set to the states: exclude, inactive, exclude, include, include](/images/colortag-inc-exc-and-or-example.png)

When using the either `ColortagIncludeExcludeFilter` and the `ColortagIEAndOrFilter`, by default none of the tags are taken into account in the search (and these inactive search tags appear gray with an empty checkbox icon).
To indicate that the search should include a tag, the tag button is clicked once, and the button turns colored with a checked checkbox icon.
If the search should exclude that tag, the tag button can be clicked a second time. The exclude selection appears as an outline button with a X icon.
To return the tag button to its default state, it can be clicked a third time.
The tag buttons can also be *right clicked* to toggle the state in the opposite direction (e.g., right clicking on the default state changes it to the exclude state.)

![Normal clicks toggle button state from default to include to exclude to default. Right clicks toggle button state in the opposite direction, default to exclude to include to default.](/images/colortag-toggle-viz.png)

The `ColortagIncludeExcludeFilter` has an information box with helptext/instructions which appears as a popover when the trigger (gray circle with a question mark icon) is hovered or focused.
Also the OR and AND options have tooltips.
(The default texts are in both English and Finnish.)
All of these default contents can be overwritten by providing the following key-value pairs as attrs to the Filter:
```python
  'helptext': {
      'title': 'the title the helptext popover should have',
      'content': 'the text content of the popover',
  },
  'or-tooltip': 'text that appears on hover over the OR button',
  'and-tooltip': 'text that appears on hover over the AND button',
```

The rendering and styling of `ColortagIncludeExcludeFilter` and `ColortagIEAndOrFilter` is fully done by the default widgets and the JS files included in this repository (from version 2.5 onwards).
Therefore, when setting up these filters, the only thing you need to implement in your project's JS file for these filters is setting up Bootstrap tooltips.
