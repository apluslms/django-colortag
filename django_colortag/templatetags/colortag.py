from typing import Optional

from django import template
from django.forms.utils import flatatt
from django.utils.html import format_html

from ..widgets import get_colortag_attrs, get_colortag_classes


register = template.Library()


def render_as_button(
        colortag: "ColorTag",
        extra: Optional[dict[str, object]] = None
        ):
    options = {
        'active': getattr(colortag, 'is_active', False),
        'element': 'span',
        # 'tooltip_trigger': 'hover',
        # 'tooltip_placement': 'top',
        # 'size': 'xs',
        'badge': True,
        'button': True,
    }
    if extra:
        options.update(extra)

    if options.get('static'):
        options['active'] = True
        options['button'] = False

    attrs = get_colortag_attrs(colortag, options)
    classes = get_colortag_classes(colortag, options)
    attrs['class'] = ' '.join(classes)
    attrs['style'] = '--colortag-color: {}; '.format(colortag.color)

    for k, v in getattr(colortag, 'data_attrs', {}).items():
        attrs['data-tag{}'.format(k)] = v

    return format_html('<{element} {attrs}>{name}</{element}>',
                       element=options['element'],
                       name=colortag.name,
                       attrs=flatatt(attrs))


@register.filter
def colortag_button(colortag, options=''):
    extra = {}
    for option in options.split(','):
        parts = option.split('=', 1)
        name, val = parts if len(parts) == 2 else (parts[0], True)
        extra[name] = val

    return render_as_button(colortag, extra)


@register.filter
def colortag(colortag, options=''):
    extra = {'static': True}
    for option in options.split(','):
        parts = option.split('=', 1)
        name, val = parts if len(parts) == 2 else (parts[0], True)
        extra[name] = val

    return render_as_button(colortag, extra)
