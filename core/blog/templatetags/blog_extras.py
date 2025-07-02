from django import template
from django.utils import timezone as tz

register = template.Library()


@register.filter(name="date_format")
def date_format(value: tz.datetime) -> str:
    """Format a date to a more readable format."""
    if value is None:
        return ""

    interval = tz.now() - value
    if interval.days == 0:
        seconds = interval.total_seconds()
        m, _ = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h >= 1:
            return f"{int(h)} hours ago"
        elif m >= 1:
            return f"{int(m)} minutes ago"
        else:
            return "Now"
    elif interval.days == 1:
        return value.strftime("Yesterday, %H:%M")
    elif abs(interval.days / 365) < 1:
        return value.strftime("%a, %b %d, %H:%M")
    return value.strftime("%a, %b %d, %Y, %H:%M")
