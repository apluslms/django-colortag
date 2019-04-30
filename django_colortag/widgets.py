from itertools import chain

from django.forms import widgets
from django.utils.encoding import force_text


def get_colortag_attrs(colortag, options):
    attrs = {
        'data-tagid': colortag.id,
        'data-tagslug': colortag.slug,
        'data-background': '{}'.format(colortag.color),
    }
    if not options.get('no_tooltip') and colortag.description:
        attrs.update({
            'data-toggle': 'tooltip',
            'data-trigger': options.get('tooltip_trigger', 'hover'),
            'data-placement': options.get('tooltip_placement', 'top'),
            'title': colortag.description,
        })
    return attrs


def get_colortag_classes(colortag, options):
    cls = set(('colortag',))
    cls.add('colortag-dark' if colortag.font_white else 'colortag-light')
    if options.get('active'):
        cls.add('colortag-active')
    if options.get('button'):
        cls.add('btn')
    if options.get('label'):
        cls.update(('label', 'label-{}'.format(options.get('size', 'xs'))))
    if options.get('class'):
        cls.update(options['class'].split(' '))
    return cls


class ColortagSelectMultiple(widgets.CheckboxSelectMultiple):

    option_inherits_attrs = False # option checkboxes need not inherit attributes from the list element

    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs=attrs, choices=choices)
        if 'class' in self.attrs:
            self.attrs['class'] += ' colortag-choice'
        else:
            self.attrs['class'] = 'colortag-choice'

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        # Copied from https://github.com/django/django/blob/stable/1.11.x/django/forms/widgets.py#L570
        # (Django 1.11 django.forms.widgets.ChoiceWidget method optgroups)
        # and then slightly modified so that self.choices includes
        # model instances in addition to the HTML input values and labels.
        # Model instances in self.choices originate from the field ColortagChoiceField.
        groups = []
        has_selected = False

        for index, (option_value, option_label, colortag_instance) in enumerate(chain(self.choices)):
            if option_value is None:
                option_value = ''

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (
                    force_text(subvalue) in value and
                    (has_selected is False or self.allow_multiple_selected)
                )
                if selected is True and has_selected is False:
                    has_selected = True
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
                    colortag_instance=colortag_instance,
                ))
                if subindex is not None:
                    subindex += 1
        return groups

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None,
            colortag_instance=None):
        # colortag_instance is a new parameter that is not used in the super class method.
        # The overridden optgroups method uses this method.
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if colortag_instance is None:
            return option
        # Add custom attributes to the option (one checkbox) that are based on
        # the corresponding ColorTag instance.
        opts = { 'button': True }
        attrs = option['attrs']
        attrs.update(get_colortag_attrs(colortag_instance, opts))
        attrs['data-class'] = ' '.join(get_colortag_classes(colortag_instance, opts))
        return option

