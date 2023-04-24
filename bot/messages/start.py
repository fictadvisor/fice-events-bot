from bot.messages.environment import environment

START = """
Вітаємо вас в боті для реєстрації на івенти
"""

REGISTER = """
Для того щоб побачити список івентів потрібно спочатку пройти коротку реєстрацію.
"""

START_FORM = """
Давай спочатку пройдемо невеличку реєстрацію. Як ваше ПІБ?
"""

INPUT_FACULTY = """
Ваш Факультет?
"""

INPUT_GROUP = """
Ваша група?
"""

CONFIRM_INPUT = environment.from_string("""
ПІБ: {{ fullname }}
Факультет: {{ faculty }}
Група: {{ group }}
    
Правильно?
""")

RESET_FORM = """
Почнемо все спочатку. Як твоє ПІБ?
"""

SUCCESS_FORM = """
Дякуємо за реєстрацію
"""