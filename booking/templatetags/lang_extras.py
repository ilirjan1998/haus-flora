"""Kleiner Template-Tag für den Sprachumschalter:
baut aus /de/preise/ die URL /en/preise/ und umgekehrt."""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def switch_language_url(context):
    request = context["request"]
    path = request.path
    if path.startswith("/en/"):
        return "/de/" + path[4:]
    if path.startswith("/de/"):
        return "/en/" + path[4:]
    return "/en" + path
