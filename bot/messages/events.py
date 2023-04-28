from bot.messages.environment import environment

AVAILABLE_EVENTS = """
Доступні івенти: 
"""

EVENT_INFO = environment.from_string("""
Назва: {{ title }}
Опис: {{ description }}

Дата: {{ date }}
""")

START_REGISTRATION = """
Для реєстрації на цей івент треба спочатку відповісти на деякі запитання.
"""

CONFIRM_REGISTRATION = environment.from_string("""
Підтвердіть форму

{% for answer in answers %}
<b>{{ loop.index }}. {{ answer.question.text }}</b>
<i>{{ answer.text }}</i>

{% endfor %}
""")

RESET_REGISTRATION = """
Добре. Давайте відповімо на питання з самого початку
"""

SUCCESSFULLY_REGISTERED = """
Ваша заявка збережена. Дякуюємо за реєстрацію
"""