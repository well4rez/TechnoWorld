from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


def _group_int_str(s: str) -> str:
    s = str(s)
    if s == '':
        return ''
    sign = ''
    if s.startswith('-'):
        sign = '-'
        s = s[1:]
    # remove any leading zeros except keep single zero
    s = s.lstrip('0') or '0'
    parts = []
    while s:
        parts.append(s[-3:])
        s = s[:-3]
    return sign + ' '.join(reversed(parts))


@register.filter
def format_price(value):
    """Format numeric price with spaces as thousands separators.

    Examples:
        1000 -> '1 000'
        1200.5 -> '1 200.5'
        '1 000 000' -> '1 000 000'
    """
    if value is None:
        return ''

    s = str(value).strip()
    if s == '':
        return ''

    # Try to parse as Decimal after removing spaces and using dot as decimal separator
    try:
        normalized = s.replace(' ', '').replace(',', '.')
        d = Decimal(normalized)
    except (InvalidOperation, ValueError, TypeError):
        # Fallback: try to split and group integer part
        if '.' in s:
            int_part, dec = s.split('.', 1)
            int_part = int_part.replace(' ', '')
            return _group_int_str(int_part) + '.' + dec
        else:
            return _group_int_str(s.replace(' ', ''))

    sign = '-' if d < 0 else ''
    d_abs = abs(d)

    # Determine if integer
    if d_abs == d_abs.to_integral():
        int_part = str(d_abs.to_integral())
        decimal_part = ''
    else:
        # Keep up to 2 decimal places, remove trailing zeros
        s2 = format(d_abs.normalize(), 'f')
        if '.' in s2:
            int_part, dec = s2.split('.', 1)
            dec = dec.rstrip('0')
            decimal_part = '.' + dec if dec else ''
        else:
            int_part = s2
            decimal_part = ''

    formatted_int = _group_int_str(int_part)
    return f"{sign}{formatted_int}{decimal_part}"
