from itertools import chain

from django.forms import widgets
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


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


class ColortagMixIn:
    option_inherits_attrs = False
    class_name = 'colortag'

    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs=attrs, choices=choices)
        if 'class' in self.attrs:
            self.attrs['class'] += ' ' + self.class_name
        else:
            self.attrs['class'] = self.class_name


class ColortagSelectMultiple(ColortagMixIn, widgets.CheckboxSelectMultiple):
    class_name = 'colortag-choice'

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


class ColortagIncludeExcludeWidget(ColortagMixIn, widgets.Select):
    class_name = 'colortag-inc-exc'

    def __init__(self, attrs=None, tag=None):
        assert tag, "The choice must be defined"
        opts = { 'button': True }
        if attrs == None:
            attrs = {}
        attrs.update(get_colortag_attrs(tag, opts))
        attrs['data-class'] = ' '.join(get_colortag_classes(tag, opts))
        choices = [
            ('', tag.name),
            ('I' + str(tag.pk), "Include"),
            ('E' + str(tag.pk), "Exclude"),
        ]
        self.__text = tag.name
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        option['attrs']['data-text'] = self.__text
        return option


class ColortagIEMultiWidget(widgets.MultiWidget):
    template_name = "django_colortag/widgets/colortag_multiwidget.html"
    class_name = 'colortag-ie-group'

    def __init__(self, attrs=None, choices=None):
        widgets = [ColortagIncludeExcludeWidget(attrs, c) for c in choices] if choices else []
        super().__init__(widgets, attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' ' + self.class_name
        else:
            self.attrs['class'] = self.class_name

    def set_subwidgets(self, choices):
        self.widgets = [ColortagIncludeExcludeWidget(tag=c) for c in choices]
        self.widgets_names = ['_%s' % i for i in range(len(self.widgets))]

    def decompress(self, value):
        if value == None:
            return [None for w in self.widgets]
        return value


class AndOrWidget(widgets.CheckboxInput):
    template_name = "django_colortag/widgets/colortag_andor.html"

    def __init__(self, attrs=None, check_test=None, label=None):
        self.label = label
        if attrs == None:
            attrs = {}
        attrs.setdefault('data-off-text', _("Match any (OR)"))
        attrs.setdefault('data-on-text', _("Match all (AND)"))
        # TODO: generate a help text, use an info-circle and a tooltip to display
        super().__init__(attrs, check_test)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = self.label
        return context


class ColortagIEAndOrWidget(widgets.MultiWidget):

    def __init__(self, attrs=None, choices=None):
        widgets = (
            AndOrWidget(label="Feedbacks must have all selected tags"),
            ColortagIEMultiWidget(attrs, choices)
        )
        super().__init__(widgets, attrs)

    def set_subwidgets(self, choices):
        self.widgets[1].set_subwidgets(choices)

    def decompress(self, value):
        if value == None:
            return [None, None]
        return value
