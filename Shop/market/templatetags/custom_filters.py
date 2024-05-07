from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
   'eur': '\u20AC',
}

forbidden_words = ['', '', '',]


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code='rub'):
    """ value: значение, к которому нужно применить фильтр """
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'  # Возвращаемое функцией значение подставится в шаблон.


# добавили фильтр - цензор на поиск нецензурных слов, который звменяет все букву символом,
# кроме первой и последней букв. Слова необходимо внести в пустой список.
@register.filter(name='censor')
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
