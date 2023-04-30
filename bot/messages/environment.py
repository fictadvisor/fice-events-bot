from datetime import datetime

from jinja2 import Environment

from bot.constants.date_format import DATE_FORMAT

environment = Environment(trim_blocks=True, enable_async=True)


def datetimeformat(value: datetime, format_date: str = DATE_FORMAT) -> str:
    return value.strftime(format_date)


environment.filters["datetimeformat"] = datetimeformat
