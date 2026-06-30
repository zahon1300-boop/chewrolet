"""
main/templatetags/url_tags.py — Template teglar.

url_replace: Sahifalash uchun URL parametrlarini almashtiradi.
"""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context: dict, **kwargs: str) -> str:
    """
    Mavjud URL parametrlarini saqlab, yangi parametrlarni qo'shadi.

    Foydalanish:
        ?{% url_replace page=2 %}
        ?{% url_replace page=page_obj.next_page_number %}

    Returns:
        URL query string (masalan: "page=2&category=sedan")
    """
    request = context.get("request")
    if not request:
        return ""

    params = request.GET.copy()
    for key, value in kwargs.items():
        params[key] = str(value)
    return params.urlencode()
