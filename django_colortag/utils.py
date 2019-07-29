def _rgb_from_hexcode(color):
    color = color.lstrip('#')
    chars = len(color)
    if chars == 1:
        rgb = [color+color] * 3
    elif chars == 2:
        rgb = [color] * 3
    elif chars == 3:
        rgb = [c+c for c in color]
    if chars == 6:
        rgb = [color[0:2], color[2:4], color[4:6]]
    else:
        rgb = ['ff', 'ff', 'ff']
    return rgb


def _srgb_to_rgb(color):
    value = int(color, 16) / 255
    if value <= 0.03928:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4


def luminance(color, *, ccir=False):
    """
    Return relative luminance of a color code given in hex.

    W3C relative luminance definition:
      https://www.w3.org/TR/WCAG20/#relativeluminancedef
    """
    rgb = _rgb_from_hexcode(color)
    r, g, b = [_srgb_to_rgb(channel) for channel in rgb]
    if ccir:
        # CCIR 601:
        return 0.299 * r + 0.587 * g + 0.114 * b
    else:
        # ITU-R, BT. 709 (W3C recommendation
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    # ref: https://en.wikipedia.org/wiki/Luma_(video)#Rec._601_luma_versus_Rec._709_luma_coefficients


def use_white_font(color, *, threshold=0.17913, **kwargs):
    # Based on W3C recommendation:
    #  sqrt(1.05 * 0.05) - 0.05 ~= 0.17913
    return luminance(color, **kwargs) <= threshold
