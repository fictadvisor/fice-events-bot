from bot.messages.environment import environment

AVAILABLE_EVENTS = """
Доступні івенти: 
"""

EVENT_INFO = environment.from_string("""
Назва: <b>{{ title }}</b>

Опис: {{ description }}
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
Ваша заявка збережена. Дякуємо за реєстрацію
"""

REMINDER = environment.from_string("""
Із нетерпінням чекаємо зустрічі з тобою на події <b>{{ event.title }}</b>! 🪩

Приходь танцювати, слемитися, ділитися емоціями та відірватися на всю наприкінці семестру! 

<b>Час та місце зустрічі:</b> 24 червня, 17:00, клуб «Барви», Ковальський провулок, 5
""")
