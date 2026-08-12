"""Presentation metadata for the vocabulary categories.

The ``source_name`` values intentionally match ``words_data.json`` exactly.
They are stable lookup keys; user progress remains keyed by word ID.
"""

CATEGORY_METADATA = [
    {"key": "pronouns", "source_name": "Местоимения", "ru": "Местоимения", "ro": "Pronume", "gag": "Adıllar", "icon": "💬", "illustration": None, "order": 1, "level": "beginner"},
    {"key": "questions", "source_name": "Вопросы", "ru": "Вопросы", "ro": "Întrebări", "gag": "Sormalar", "icon": "❓", "illustration": None, "order": 2, "level": "beginner"},
    {"key": "basics", "source_name": "Базовые", "ru": "Базовые слова", "ro": "Cuvinte de bază", "gag": "Temel laflar", "icon": "✨", "illustration": None, "order": 3, "level": "beginner"},
    {"key": "time", "source_name": "Время", "ru": "Время", "ro": "Timp", "gag": "Vakıt", "icon": "🕐", "illustration": None, "order": 4, "level": "beginner"},
    {"key": "numbers", "source_name": "Цифры", "ru": "Цифры", "ro": "Numere", "gag": "Sayılar", "icon": "🔢", "illustration": None, "order": 5, "level": "beginner"},
    {"key": "family", "source_name": "Семья", "ru": "Семья", "ro": "Familie", "gag": "Aylä", "icon": "👨‍👩‍👧", "illustration": None, "order": 6, "level": "beginner"},
    {"key": "food", "source_name": "Еда", "ru": "Еда", "ro": "Mâncare", "gag": "İimäk", "icon": "🍲", "illustration": None, "order": 7, "level": "beginner"},
    {"key": "verbs", "source_name": "Глаголы", "ru": "Глаголы", "ro": "Verbe", "gag": "İşliklär", "icon": "⚡", "illustration": None, "order": 8, "level": "beginner"},
    {"key": "adjectives", "source_name": "Прилагательные", "ru": "Прилагательные", "ro": "Adjective", "gag": "Nışannar", "icon": "📝", "illustration": None, "order": 9, "level": "beginner"},
    {"key": "anatomy", "source_name": "Анатомия", "ru": "Анатомия", "ro": "Anatomie", "gag": "Anatomiya", "icon": "🫀", "illustration": None, "order": 10, "level": "beginner"},
    {"key": "nature", "source_name": "Природа", "ru": "Природа", "ro": "Natură", "gag": "Tabiat", "icon": "🌿", "illustration": None, "order": 11, "level": "beginner"},
    {"key": "animals", "source_name": "Животные", "ru": "Животные", "ro": "Animale", "gag": "Hayvannar", "icon": "🐾", "illustration": None, "order": 12, "level": "beginner"},
    {"key": "home", "source_name": "Дом и Предметы", "ru": "Дом и предметы", "ro": "Casă și obiecte", "gag": "Ev hem nesnelär", "icon": "🏠", "illustration": None, "order": 13, "level": "beginner"},
    {"key": "professions", "source_name": "Профессии", "ru": "Профессии", "ro": "Profesii", "gag": "Zanaatlar", "icon": "💼", "illustration": None, "order": 14, "level": "beginner"},
    {"key": "colors", "source_name": "Цвета", "ru": "Цвета", "ro": "Culori", "gag": "Renklär", "icon": "🎨", "illustration": None, "order": 15, "level": "beginner"},
    {"key": "city_transport", "source_name": "Город и Транспорт", "ru": "Город и транспорт", "ro": "Oraș și transport", "gag": None, "icon": "🚌", "illustration": None, "order": 16, "level": "beginner"},
    {"key": "health", "source_name": "Здоровье и Медицина", "ru": "Здоровье и медицина", "ro": "Sănătate și medicină", "gag": None, "icon": "🩺", "illustration": None, "order": 17, "level": "beginner"},
    {"key": "clothing", "source_name": "Одежда", "ru": "Одежда", "ro": "Îmbrăcăminte", "gag": "Giiyim", "icon": "👕", "illustration": None, "order": 18, "level": "beginner"},
    {"key": "feelings", "source_name": "Чувства", "ru": "Чувства", "ro": "Sentimente", "gag": None, "icon": "💛", "illustration": None, "order": 19, "level": "beginner"},
    {"key": "school_science", "source_name": "Школа и Наука", "ru": "Школа и наука", "ro": "Școală și știință", "gag": None, "icon": "🎓", "illustration": None, "order": 20, "level": "beginner"},
    {"key": "kitchen", "source_name": "Кухня", "ru": "Кухня", "ro": "Bucătărie", "gag": None, "icon": "🥄", "illustration": None, "order": 21, "level": "beginner"},
    {"key": "tools", "source_name": "Инструменты", "ru": "Инструменты", "ro": "Instrumente", "gag": None, "icon": "🛠️", "illustration": None, "order": 22, "level": "beginner"},
    {"key": "money_trade", "source_name": "Деньги и Торговля", "ru": "Деньги и торговля", "ro": "Bani și comerț", "gag": None, "icon": "🪙", "illustration": None, "order": 23, "level": "beginner"},
    {"key": "sport_art", "source_name": "Спорт и Искусство", "ru": "Спорт и искусство", "ro": "Sport și artă", "gag": None, "icon": "🏅", "illustration": None, "order": 24, "level": "beginner"},
    {"key": "conjunctions", "source_name": "Союзы и Связки", "ru": "Союзы и связки", "ro": "Conjuncții și legături", "gag": None, "icon": "🔗", "illustration": None, "order": 25, "level": "beginner"},
]

CATEGORIES_BY_SOURCE = {item["source_name"]: item for item in CATEGORY_METADATA}


def category_name(source_name, lang):
    """Return the localized category name without changing its source key."""
    item = CATEGORIES_BY_SOURCE.get(source_name)
    if not item:
        return source_name
    return item.get(lang.lower()) or item["ru"]
