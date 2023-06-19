from bot.messages.environment import environment

AVAILABLE_EVENTS = """
Доступні івенти: 
"""

EVENT_INFO = environment.from_string("""
Назва: {{ title }}
Опис: {{ description }}

Дата: {{ date|datetimeformat }}
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

REMINDER = environment.from_string("""
<b>Шановний учаснику!</b>

Чекаємо тебе завтра о <b>{{ event.date|datetimeformat("%H:%M") }}</b> на <b>{{ event.title }}</b>. 
Твоя присутність багато значить для нас, 
зробимо цю подію незабутньою! До зустрічі.

<i>З повагою,
Організатори</i>
""")
