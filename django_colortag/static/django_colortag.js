function django_colortag_label(colortag, options_) {
  // Almost a direct port of templatetags/colortag.py:render_as_button
  const default_options = {
    active: true,
    static: true,
    element: 'span',
    label: true,
  }
  const options = jQuery.extend({}, default_options, options_);

  const attrs = {
    'data-tagid': colortag.id,
    'data-tagslug': colortag.slug,
    'data-background': colortag.color,
  };
  if (!options['no_tooltip'] && colortag.description) {
    $.extend(attrs, {
      'data-toggle': 'tooltip',
      'data-trigger': options['tooltip_trigger'] || 'hover',
      'data-placement': options['tooltip_placement'] || 'top',
      'title': colortag.description,
    });
  }

  const classes = ['colortag'];
  classes.push(colortag.font_white ? 'colortag-dark' : 'colortag-light');
  if (options['active']) {
    classes.push('colortag-active');
  }
  if (options['button']) {
    classes.push('btn');
  }
  if (options['label']) {
    classes.push('label', 'label-' + (options['size'] || 'xs'));
  }
  if (options['class']) {
    classes.push(options['class'].split(' '));
  }
  attrs['class'] = classes.join(' ');
  attrs['style'] = 'background-color: ' + colortag.color + ';';

  for (var k in colortag['data-attrs']) {
    attrs['data-tag' + k] = colortag['data-attrs'][k];
  }

  const attr_strings = Object.keys(attrs).map(function (k) {
    return k + '="' + attrs[k] + '"';
  });
  const flatatt = attr_strings.join(' ');

  const elem = options['element']
  const html = '<' + elem + ' ' + flatatt + '>' + colortag.name + '</' + elem + '>';
  return $(html);
}

function django_colortag_choice() {
	jQuery(this).replaceCheckboxesWithButtons({
		groupClass: 'colortag-container',
		buttonClass: '',
		onicon: 'check',
		officon: 'unchecked',
		nocolor: true,
		buttonSetup: function(input, button, group) {
			button.css('backgroundColor', input.data('background'));
		},
	});
}
