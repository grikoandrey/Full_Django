from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
   'eur': '\u20AC',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code='rub'):
    """ value: значение, к которому нужно применить фильтр """
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'  # Возвращаемое функцией значение подставится в шаблон.
