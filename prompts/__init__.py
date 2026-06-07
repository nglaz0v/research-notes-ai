from prompts.system_prompt_base import SYSTEM_PROMPT_BASE

PROMPT_REVIEW = f"""\
{SYSTEM_PROMPT_BASE}

Специфика: тебе дана ОБЗОРНАЯ статья (review article).
Особое внимание удели:
- Обзору существующих подходов и методов
- Сравнительному анализу различных направлений исследований
- Выявлению трендов и перспективных направлений
- Пробелам в текущих исследованиях (research gaps)

Отрази, какие работы и авторы являются ключевыми в данной области.
"""

PROMPT_EXPERIMENTAL = f"""\
{SYSTEM_PROMPT_BASE}

Специфика: тебе дана ЭКСПЕРИМЕНТАЛЬНАЯ статья.
Особое внимание удели:
- Гипотезе и целям эксперимента
- Выборке и методологии
- Количественным результатам и метрикам
- Статистической значимости выводов
- Ограничениям эксперимента

Чётко выделяй численные данные, размеры выборок, p-значения и другие метрики.
"""

PROMPT_THEORETICAL = f"""\
{SYSTEM_PROMPT_BASE}

Специфика: тебе дана ТЕОРЕТИЧЕСКАЯ статья.
Особое внимание удели:
- Теоретической рамке и понятийному аппарату
- Логике аргументации и структуре доказательств
- Новым концептам, моделям или классификациям
- Связям с существующими теориями

Отрази ключевые определения, теоремы, модели или концептуальные новшества.
"""

PROMPTS = {
    "review": PROMPT_REVIEW,
    "experimental": PROMPT_EXPERIMENTAL,
    "theoretical": PROMPT_THEORETICAL,
    "default": SYSTEM_PROMPT_BASE,
}


def get_prompt(article_type: str = "default") -> str:
    """Return system prompt for the given article type."""
    return PROMPTS.get(article_type.lower(), PROMPTS["default"])
