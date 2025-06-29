from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de um dicionário usando uma chave fornecida.
    Uso no template: {{ my_dict|get_item:item.NAME }}
    """
    return dictionary.get(key, 0)
