from bot.messages.environment import environment

ADMIN_MENU = """
Адмін Панель
"""

ALL_EVENTS = """
Список івентів
"""

EVENT_INFO = environment.from_string("""
Назва: {{ title }}
Опис: {{ description }}

Дата: {{ date|datetimeformat }}
""")

EDIT_TITLE = """
Введіть нову назву
"""

EDIT_DESCRIPTION = """
Введіть новий опис
"""

EDIT_DATE = """
Введіть нову дату в такому форматі: 18:30 20-04-1889
"""

EDIT_QUESTION = """
Введіть нове питання
"""

ALL_QUESTIONS = """
Усі питання
"""

QUESTION_INFO = environment.from_string("""
{{ text }}
""")

ADD_QUESTION = """
Введіть текст питання
"""

ADD_EVENT = """
Введіть назву івенту
"""

INPUT_DESCRIPTION = """
Введіть опис івенту
"""

INPUT_DATE = """
Введіть дату в такому форматі: 18:30 20-04-1889
"""

CONFIRM_EVENT = environment.from_string("""
Назва: {{ title }}
Опис: {{ description }}
Дата: {{ date|datetimeformat }}

Підтвердити?
""")

RESET_EVENT = """
Почнемо все спочатку. Введіть назву
"""
