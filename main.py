import flet as ft
import json
import random
import asyncio
import datetime
import os
from pathlib import Path

from category_metadata import CATEGORY_METADATA, CATEGORIES_BY_SOURCE, category_name as localized_category_name


APP_DIR = Path(__file__).resolve().parent
STORAGE_DIR = Path(os.environ.get("FLET_APP_STORAGE_DATA", APP_DIR))
WORDS_DATA_FILE = APP_DIR / "words_data.json"
USER_STATS_FILE = STORAGE_DIR / "user_stats.json"

# --- ПЕРЕВОДЫ ИНТЕРФЕЙСА ---
UI_TEXT = {
    "RU": {
        "title": "Gagauzça üürenmää",
        "learn": "Учить новые слова",
        "review": "Повторить",
        "view_all": "Просмотреть все слова",
        "back": "< Назад в меню",
        "to_menu": "< Назад в меню",
        "reset": "Обнулить категорию",
        "global_title": "ОБЩИЙ ПРОГРЕСС",
        "global_btn": "Повторять все слова",
        "remember": "ЗАПОМНИТЕ СЛОВО",
        "next": "Запомнил, далее",
        "quiz_title": "ПРОВЕРКА ЗНАНИЙ",
        "word_count": "Слово {0} из {1}",
        "correct": "Верно! ✅",
        "wrong": "Ошибка! ❌",
        "finished": "Сессия завершена!",
        "dictionary": "Категория: ",
        "reset_all": "Обнулить весь прогресс",
        "fast_review_btn": "Быстрое повторение",
        "fast_review_success": "Вы всё повторили, поздравляем!",
        "fast_review_fail": "Закончились жизни, повторите слова и попробуйте ещё",
        "statistics": "📊 Статистика",
        "stats_title": "СТАТИСТИКА ПРОФИЛЯ",
        "hard_words": "Самые сложные слова (ошибок):",
        "skip": "Не знаю",
        "category_title": "Изучения и повторения по категориям",
        "true_false_btn": "Правда или Ложь",
        "true_btn": "✅ Правда",
        "false_btn": "❌ Ложь",
        "continue_question": "Продолжить изучение новых слов?",
        "continue_yes": "Да",
        "continue_no": "Нет",
        "all_learned": "Все слова выучены! 🎉",
        "daily_review_btn": "🎯 Ежедневное повторение",
        "daily_review_locked": "Возвращайся завтра 🌙",
        "daily_review_min": "Нужно ≥20 выученных слов",
        "daily_review_score": "Готово! {0}/{1} верно ({2}%)",
        "daily_review_title": "ЕЖЕДНЕВНОЕ ПОВТОРЕНИЕ",
        "confirm_yes": "Да, обнулить",
        "confirm_no": "Отмена",
        "confirm_reset_category": "Обнулить категорию «{0}»? Прогресс этой категории будет потерян.",
        "confirm_reset_all": "Обнулить весь прогресс? Будут удалены изученные слова, статистика ответов и серия занятий."
    },
    "RO": {
        "title": "Gagauzça üürenmää",
        "learn": "Învață cuvinte noi",
        "review": "Repetă",
        "view_all": "Vezi toate cuvintele",
        "back": "< Înapoi la meniu",
        "to_menu": "< Înapoi la meniu",
        "reset": "Resetează categorie",
        "global_title": "PROGRES TOTAL",
        "global_btn": "Repetați toate cuvinte",
        "remember": "ȚINE MINTE CUVÂNTUL",
        "next": "Am reținut, mai departe",
        "quiz_title": "VERIFICAREA CUNOȘTINȚELOR",
        "word_count": "Cuvântul {0} din {1}",
        "correct": "Corect! ✅",
        "wrong": "Eroare! ❌",
        "finished": "Sesiune finalizată!",
        "dictionary": "Categorie: ",
        "reset_all": "Resetează tot progresul",
        "fast_review_btn": "Repetare rapidă",
        "fast_review_success": "Ați repetat totul, felicitări!",
        "fast_review_fail": "S-au terminat viețile, repetați cuvintele și încercați din nou",
        "statistics": "📊 Statistici",
        "stats_title": "STATISTICI PROFIL",
        "hard_words": "Cele mai grele cuvinte (erori):",
        "skip": "Nu știu",
        "category_title": "Studiu și repetare pe categorii",
        "true_false_btn": "Adevărat sau Fals",
        "true_btn": "✅ Adevărat",
        "false_btn": "❌ Fals",
        "continue_question": "Continuați învățarea cuvintelor noi?",
        "continue_yes": "Da",
        "continue_no": "Nu",
        "all_learned": "Toate cuvintele învățate! 🎉",
        "daily_review_btn": "🎯 Repetare zilnică",
        "daily_review_locked": "Revino mâine 🌙",
        "daily_review_min": "Aveți nevoie de ≥20 cuvinte învățate",
        "daily_review_score": "Gata! {0}/{1} corect ({2}%)",
        "daily_review_title": "REPETARE ZILNICĂ",
        "confirm_yes": "Da, resetează",
        "confirm_no": "Anulează",
        "confirm_reset_category": "Resetăm categoria «{0}»? Progresul acestei categorii va fi pierdut.",
        "confirm_reset_all": "Resetăm tot progresul? Vor fi șterse cuvintele învățate, statisticile răspunsurilor și seria de studiu."
    }
}

PHASE1_TEXT = {
    "RU": {
        "nav_home": "Главная", "nav_learn": "Учить", "nav_review": "Повторять",
        "gagauz_language": "Гагаузский язык", "settings": "Настройки",
        "your_progress": "ВАШ ПРОГРЕСС", "words": "слов", "beginner": "Начальный",
        "today": "Сегодня", "daily_review": "Ежедневное повторение",
        "ready_review": "20 слов готовы к повторению", "daily_in_progress": "Продолжить: {0} / 20",
        "daily_complete": "Ежедневное повторение на сегодня завершено", "daily_locked": "Откроется после изучения 20 слов",
        "daily_new_user_hint": "Каждый день здесь вас ждут 20 слов для повторения.",
        "daily_new_user_locked": "Откроется после изучения первых 20 слов.",
        "daily_complete_hint": "Вы можете проверять себя в обычных повторениях или учить новые слова.",
        "start_daily": "Начать повторение", "continue_daily": "Продолжить повторение",
        "continue_learning": "ПРОДОЛЖИТЬ ОБУЧЕНИЕ", "choose_category": "Выбрать другую категорию",
        "continue": "Продолжить изучение этой категории", "no_category": "Выберите первую категорию в разделе «Учить».",
        "welcome_learning": "Приветствуем в изучении гагаузского языка",
        "welcome_gagauz": "Hoş geldiniz!",
        "choose_start": "Выберите, с чего начать изучение",
        "choose_first_topic": "Выбрать первую тему",
        "home_words_learned": "слов выучено",
        "day_streak": "дн. подряд", "streak_hint": "Завершите занятие сегодня, чтобы продолжить серию.",
        "learn_title": "Что вы хотите изучить?", "learn_subtitle": "Выберите тему и учитесь в своём темпе.",
        "conversational": "Разговорный", "advanced": "Продвинутый", "expert": "Эксперт", "locked": "Скоро",
        "back": "Назад", "words_learned": "слов изучено", "learn_new": "Учить новые слова",
        "words_remaining": "слов осталось", "start_learning": "Начать обучение",
        "difficult_words": "Сложные слова", "need_attention": "слов требуют внимания", "review_action": "Повторить",
        "learned_words": "Изученные слова", "view_words": "Посмотреть слова",
        "review_title": "Повторение", "review_subtitle": "Закрепляйте слова короткими тренировками.",
        "daily_desc": "Подборка слов на сегодня.", "difficult_desc": "Повторите слова, в которых ошибались.",
        "quick_review": "Быстрое повторение", "quick_desc": "На скорость, с тремя жизнями.",
        "regular_review": "Обычное повторение", "regular_review_desc": "Выберите правильный перевод.",
        "quiz": "Тест", "quiz_desc": "Определите, верен ли перевод.",
        "review_mode_locked": "Откроется после изучения первой серии слов",
        "start_session": "Начать", "true_false_short": "Да / Нет", "no_difficult": "Пока нет сложных слов",
        "language": "Язык обучения", "russian": "Русский", "romanian": "Румынский",
        "reset_progress": "Сброс прогресса", "reset_category_label": "Сбросить категорию",
        "select_category": "Выберите категорию", "reset_all_hint": "Будут удалены прогресс, статистика ответов и серия занятий.",
        "open_settings": "Открыть настройки", "all_words_learned": "Все слова изучены",
        "close_session": "Закрыть занятие", "question": "Задание", "continue_answer": "Продолжить",
        "correct_answer": "Правильно!", "incorrect_answer": "Не совсем", "correct_was": "Правильный ответ",
        "results": "Результаты", "great_job": "Отличная работа!", "accuracy": "Точность",
        "newly_learned": "Новых слов изучено", "streak_confirmed": "Серия подтверждена",
        "result_excellent_title": "Отлично!", "result_excellent_hint": "Эти слова уже хорошо запомнились.",
        "result_good_title": "Хороший результат", "result_good_hint": "Ещё немного практики — и будет совсем уверенно.",
        "result_practice_title": "Продолжаем", "result_practice_hint": "Слова постепенно закрепляются.",
        "result_attention_title": "Всё приходит с практикой", "result_attention_hint": "Этим словам нужно ещё немного внимания.",
        "learning_result_title": "Серия слов пройдена",
        "learning_result_all": "Все слова этой серии добавлены в изученные.",
        "learning_result_retry": "Некоторые слова встретятся снова в следующих занятиях.",
        "fast_result_title": "Ваш результат", "fast_score": "СЧЁТ", "fast_best_score": "Лучший результат",
        "fast_first_score": "Первый результат сохранён", "fast_new_record": "Новый личный рекорд!",
        "fast_record_tied": "Вы повторили свой лучший результат", "fast_to_record": "До личного рекорда — {0}",
        "try_again": "Попробовать снова",
        "finish": "Завершить", "build_word": "Составьте слово на гагаузском",
        "word_building": "Составление слов", "word_building_desc": "Соберите слово из букв. Некоторые могут быть лишними.",
        "check": "Проверить", "backspace": "Удалить", "clear": "Очистить",
        "what_mean": "Что это значит?",
        "previous_word": "Предыдущее слово",
        "next_word": "Следующее слово", "repeat_learned": "Повторять изученные слова",
        "learning_new_words": "Изучение новых слов",
    },
    "RO": {
        "nav_home": "Acasă", "nav_learn": "Învață", "nav_review": "Repetă",
        "gagauz_language": "Limba găgăuză", "settings": "Setări",
        "your_progress": "PROGRESUL TĂU", "words": "cuvinte", "beginner": "Începător",
        "today": "Astăzi", "daily_review": "Repetare zilnică",
        "ready_review": "20 de cuvinte sunt gata de repetat", "daily_in_progress": "Continuă: {0} / 20",
        "daily_complete": "Repetarea zilnică pentru astăzi este finalizată", "daily_locked": "Disponibilă după 20 de cuvinte învățate",
        "daily_new_user_hint": "În fiecare zi, aici te așteaptă 20 de cuvinte pentru repetare.",
        "daily_new_user_locked": "Se va deschide după învățarea primelor 20 de cuvinte.",
        "daily_complete_hint": "Îți poți verifica cunoștințele prin repetări obișnuite sau poți învăța cuvinte noi.",
        "start_daily": "Începe repetarea", "continue_daily": "Continuă repetarea",
        "continue_learning": "CONTINUĂ ÎNVĂȚAREA", "choose_category": "Alege altă categorie",
        "continue": "Continuă învățarea acestei categorii", "no_category": "Alege prima categorie din secțiunea „Învață”.",
        "welcome_learning": "Bine ați venit la studiul limbii găgăuze",
        "welcome_gagauz": "Hoş geldiniz!",
        "choose_start": "Alege cu ce să începi învățarea",
        "choose_first_topic": "Alege prima temă",
        "home_words_learned": "cuvinte învățate",
        "day_streak": "zile la rând", "streak_hint": "Finalizează o sesiune astăzi pentru a continua seria.",
        "learn_title": "Ce vrei să înveți?", "learn_subtitle": "Alege o temă și învață în ritmul tău.",
        "conversational": "Conversațional", "advanced": "Avansat", "expert": "Expert", "locked": "În curând",
        "back": "Înapoi", "words_learned": "cuvinte învățate", "learn_new": "Învață cuvinte noi",
        "words_remaining": "cuvinte rămase", "start_learning": "Începe învățarea",
        "difficult_words": "Cuvinte dificile", "need_attention": "cuvinte necesită atenție", "review_action": "Repetă",
        "learned_words": "Cuvinte învățate", "view_words": "Vezi cuvintele",
        "review_title": "Repetare", "review_subtitle": "Consolidează vocabularul prin sesiuni scurte.",
        "daily_desc": "Selecția de cuvinte pentru astăzi.", "difficult_desc": "Repetă cuvintele la care ai greșit.",
        "quick_review": "Repetare rapidă", "quick_desc": "Contra cronometru, cu trei vieți.",
        "regular_review": "Repetare obișnuită", "regular_review_desc": "Alege traducerea corectă.",
        "quiz": "Test", "quiz_desc": "Stabilește dacă traducerea este corectă.",
        "review_mode_locked": "Se va deschide după învățarea primei serii de cuvinte",
        "start_session": "Începe", "true_false_short": "Da / Nu", "no_difficult": "Nu există încă cuvinte dificile",
        "language": "Limba de învățare", "russian": "Rusă", "romanian": "Română",
        "reset_progress": "Resetarea progresului", "reset_category_label": "Resetează categoria",
        "select_category": "Alege categoria", "reset_all_hint": "Vor fi șterse progresul, statisticile răspunsurilor și seria de studiu.",
        "open_settings": "Deschide setările", "all_words_learned": "Toate cuvintele sunt învățate",
        "close_session": "Închide sesiunea", "question": "Exercițiu", "continue_answer": "Continuă",
        "correct_answer": "Corect!", "incorrect_answer": "Nu chiar", "correct_was": "Răspunsul corect",
        "results": "Rezultate", "great_job": "Foarte bine!", "accuracy": "Acuratețe",
        "newly_learned": "Cuvinte noi învățate", "streak_confirmed": "Seria este confirmată",
        "result_excellent_title": "Excelent!", "result_excellent_hint": "Aceste cuvinte sunt deja bine memorate.",
        "result_good_title": "Rezultat bun", "result_good_hint": "Încă puțină practică și vei răspunde cu mai multă încredere.",
        "result_practice_title": "Continuăm", "result_practice_hint": "Cuvintele se fixează treptat.",
        "result_attention_title": "Totul vine prin practică", "result_attention_hint": "Aceste cuvinte mai au nevoie de puțină atenție.",
        "learning_result_title": "Seria de cuvinte este parcursă",
        "learning_result_all": "Toate cuvintele din această serie au fost adăugate la cele învățate.",
        "learning_result_retry": "Unele cuvinte vor apărea din nou în lecțiile următoare.",
        "fast_result_title": "Rezultatul tău", "fast_score": "SCOR", "fast_best_score": "Cel mai bun rezultat",
        "fast_first_score": "Primul rezultat a fost salvat", "fast_new_record": "Un nou record personal!",
        "fast_record_tied": "Ți-ai egalat cel mai bun rezultat", "fast_to_record": "Până la recordul personal — {0}",
        "try_again": "Încearcă din nou",
        "finish": "Finalizează", "build_word": "Construiește cuvântul găgăuz",
        "word_building": "Construirea cuvintelor", "word_building_desc": "Construiește cuvântul din litere. Unele pot fi în plus.",
        "check": "Verifică", "backspace": "Șterge", "clear": "Curăță",
        "what_mean": "Ce înseamnă?",
        "previous_word": "Cuvântul anterior",
        "next_word": "Cuvântul următor", "repeat_learned": "Repetă cuvintele învățate",
        "learning_new_words": "Învățarea cuvintelor noi",
    },
}


def russian_plural(count, one, few, many):
    value = abs(int(count))
    if value % 10 == 1 and value % 100 != 11:
        return one
    if value % 10 in (2, 3, 4) and value % 100 not in (12, 13, 14):
        return few
    return many


def word_count_text(count, lang):
    if lang == "RU":
        noun = russian_plural(count, "слово", "слова", "слов")
    else:
        noun = "cuvânt" if abs(int(count)) == 1 else "cuvinte"
    return f"{count} {noun}"


def learned_word_count_text(count, lang):
    if lang == "RU":
        return f"{word_count_text(count, lang)} изучено"
    ending = "cuvânt învățat" if abs(int(count)) == 1 else "cuvinte învățate"
    return f"{count} {ending}"


def learned_of_total_text(learned, total, lang):
    connector = "из" if lang == "RU" else "din"
    return f"{learned_word_count_text(learned, lang)} {connector} {total}"


def remaining_word_count_text(count, lang):
    if lang == "RU":
        return f"{word_count_text(count, lang)} осталось"
    ending = "cuvânt rămas" if abs(int(count)) == 1 else "cuvinte rămase"
    return f"{count} {ending}"


def attention_word_count_text(count, lang):
    if lang == "RU":
        verb = "требует" if abs(int(count)) == 1 else "требуют"
        return f"{word_count_text(count, lang)} {verb} внимания"
    return f"{word_count_text(count, lang)} necesită atenție"


def streak_days_text(count, lang):
    if lang == "RU":
        noun = russian_plural(count, "день", "дня", "дней")
        return f"{count} {noun} подряд"
    noun = "zi" if abs(int(count)) == 1 else "zile"
    return f"{count} {noun} la rând"


def load_data():
    try:
        with WORDS_DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_stats():
    try:
        with USER_STATS_FILE.open("r", encoding="utf-8") as f:
            stats = json.load(f)
    except FileNotFoundError:
        stats = {}
    stats.setdefault("streak_days", 0)
    stats.setdefault("last_login", "")
    stats.setdefault("words", {})
    return stats

def save_stats(stats):
    USER_STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with USER_STATS_FILE.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def word_weight(word, stats, today):
    s = stats["words"].get(str(word["id"]), {})
    correct = s.get("correct_answers", 0)
    wrong = s.get("wrong_answers", 0)
    error_rate = wrong / (wrong + correct + 1)

    last_seen_str = s.get("last_seen", "1970-01-01")
    try:
        last_seen = datetime.date.fromisoformat(last_seen_str)
        days_since = (today - last_seen).days
    except (ValueError, TypeError):
        days_since = 365
    days_since = max(0, min(days_since, 30))

    return 1.0 + error_rate * 5.0 + days_since * 0.3


def weighted_sample(words, stats, today, k):
    if not words or k <= 0:
        return []
    if k >= len(words):
        result = list(words)
        random.shuffle(result)
        return result
    keys = []
    for i, w in enumerate(words):
        weight = word_weight(w, stats, today)
        keys.append((random.random() ** (1.0 / weight), i))
    keys.sort(key=lambda x: -x[0])
    return [words[i] for _, i in keys[:k]]


def build_daily_set(learned_words, stats, today):
    if len(learned_words) < 20:
        return []

    def wrong_count(w):
        return stats["words"].get(str(w["id"]), {}).get("wrong_answers", 0)

    sorted_by_wrong = sorted(learned_words, key=lambda w: (wrong_count(w), random.random()), reverse=True)
    top5 = sorted_by_wrong[:5]
    top5_ids = {w["id"] for w in top5}
    remaining = [w for w in learned_words if w["id"] not in top5_ids]
    rest = weighted_sample(remaining, stats, today, k=15)
    combined = top5 + rest
    random.shuffle(combined)
    return [w["id"] for w in combined]


def register_learning_day(stats, today):
    """Update the streak after a completed session; return whether it changed."""
    last_value = stats.get("last_learning_date")
    try:
        last_day = datetime.date.fromisoformat(last_value) if last_value else None
    except (TypeError, ValueError):
        last_day = None
    if last_day == today:
        return False
    current = max(0, int(stats.get("streak_days", 0) or 0))
    stats["streak_days"] = current + 1 if last_day == today - datetime.timedelta(days=1) else 1
    stats["last_learning_date"] = today.isoformat()
    stats["last_login"] = today.isoformat()
    return True


def merge_data_and_stats(all_words, stats):
    needs_save = False
    for w in all_words:
        w_id = str(w["id"])
        if w_id not in stats["words"]:
            # The dictionary contains learning content only. A new user always
            # starts with zero progress; learned state lives in user_stats.json.
            w["learned"] = False
            stats["words"][w_id] = {
                "learned": False,
                "correct_answers": 0,
                "wrong_answers": 0,
                "last_seen": "1970-01-01"
            }
            needs_save = True
        else:
            defaults = {
                "learned": False,
                "correct_answers": 0,
                "wrong_answers": 0,
                "last_seen": "1970-01-01",
            }
            for field, default in defaults.items():
                if field not in stats["words"][w_id]:
                    stats["words"][w_id][field] = default
                    needs_save = True
            w["learned"] = stats["words"][w_id]["learned"]

    if needs_save:
        save_stats(stats)
    return all_words

def main(page: ft.Page):
    page.title = "Gagauzium"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.assets_dir = "assets"
    page.window.resizable = True
    page.window.center()

    raw_words = load_data()
    user_stats = load_stats()
    all_words = merge_data_and_stats(raw_words, user_stats)

    app_state = {
        "lang": user_stats.get("lang", "RU"),
        "current_batch": [],
        "index": 0,
        "is_quiz": False,
        "mode": "new",
        "current_options": [],
        "option_buttons": {},
        "feedback_text": "",
        "last_word_id": None,
        "last_category": user_stats.get("last_active_category"),
        "current_screen": "home",
        "nav_index": 0,
        "exercise_return_screen": "home",
        "exercise_return_category": None,
        "exercise_view_active": False,
        "session_completion_recorded": False,
        "feedback_active": False,
        "feedback_correct": False,
        "selected_answer": None,
        "session_correct": 0,
        "session_answered": 0,
        "session_new_learned": 0,
        "learning_batch_viewed": False,
        "letter_bank": [],
        "selected_letter_indices": [],
        "fast_timer_value": 1.0,
        "fast_timer_bar": None,
        "stats": user_stats
    }

    BG = "#F8F7F2"
    CARD = "#FFFFFF"
    INK = "#172033"
    MUTED = "#667085"
    INDIGO = "#4353C7"
    INDIGO_DARK = "#222A5D"
    BORDER = "#E8E8ED"

    def phase_text():
        return PHASE1_TEXT[app_state["lang"]]

    def get_category_meta(source_name):
        return CATEGORIES_BY_SOURCE.get(source_name, {
            "key": source_name, "source_name": source_name,
            "ru": source_name, "ro": source_name, "gag": None,
            "icon": "📚", "illustration": None, "order": 999, "level": "beginner",
        })

    def category_words(source_name):
        return [w for w in all_words if w["category"] == source_name]

    def category_counts(source_name):
        words = category_words(source_name)
        learned = sum(1 for w in words if w["learned"])
        difficult = sum(
            1 for w in words
            if w["learned"] and app_state["stats"]["words"].get(str(w["id"]), {}).get("wrong_answers", 0) > 0
        )
        return learned, len(words), difficult

    def category_visual(source_name, size=54):
        meta = get_category_meta(source_name)
        return ft.Container(
            content=ft.Text(meta.get("icon", "📚"), size=max(24, int(size * 0.48))),
            width=size, height=size, alignment=ft.Alignment.CENTER,
            bgcolor="#EEF2FF", border_radius=size / 3,
        )

    def rounded_card(content, padding=18, bgcolor=CARD):
        return ft.Container(
            content=content, padding=padding, bgcolor=bgcolor,
            border=ft.Border.all(1, BORDER), border_radius=22,
            shadow=ft.BoxShadow(blur_radius=10, color="#120F172A", offset=ft.Offset(0, 2)),
        )

    def app_header():
        t = phase_text()
        return ft.Row([
            ft.Image(
                src="icon.svg",
                width=38,
                height=38,
                fit=ft.BoxFit.CONTAIN,
                border_radius=12,
                anti_alias=True,
            ),
            ft.Column([
                ft.Text("Gagauzium", size=19, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(t["gagauz_language"], size=11, color=MUTED),
            ], spacing=0, expand=True),
            ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, icon_color=MUTED, tooltip=t["settings"], on_click=lambda _: show_settings()),
        ], spacing=9, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def on_nav_change(e):
        index = e.control.selected_index
        app_state["nav_index"] = index
        if index == 0:
            show_home()
        elif index == 1:
            show_learn()
        else:
            show_review_hub()

    def set_bottom_navigation(selected_index):
        t = phase_text()
        app_state["nav_index"] = selected_index
        page.navigation_bar = ft.NavigationBar(
            selected_index=selected_index,
            bgcolor="#FFFFFF",
            indicator_color="#E9EDFF",
            elevation=8,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label=t["nav_home"]),
                ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK_OUTLINED, selected_icon=ft.Icons.MENU_BOOK, label=t["nav_learn"]),
                ft.NavigationBarDestination(icon=ft.Icons.REPLAY_OUTLINED, selected_icon=ft.Icons.REPLAY, label=t["nav_review"]),
            ],
            on_change=on_nav_change,
        )

    def prepare_main_screen(screen, nav_index, add_header=True):
        app_state["question_id"] = -1
        app_state["current_screen"] = screen
        page.clean()
        page.scroll = ft.ScrollMode.HIDDEN
        page.bgcolor = BG
        page.padding = ft.Padding.only(left=16, right=16, top=14, bottom=18)
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        set_bottom_navigation(nav_index)
        if add_header:
            page.add(ft.SafeArea(
                content=app_header(),
                avoid_intrusions_bottom=False,
                minimum_padding=ft.Padding.only(top=14),
            ))

    def persist_last_category(source_name):
        app_state["last_category"] = source_name
        if app_state["stats"].get("last_active_category") != source_name:
            app_state["stats"]["last_active_category"] = source_name
            save_stats(app_state["stats"])

    def record_completed_session():
        if app_state.get("session_completion_recorded"):
            return
        app_state["session_completion_recorded"] = True
        today = datetime.date.today()
        if register_learning_day(app_state["stats"], today):
            save_stats(app_state["stats"])

    def displayed_streak():
        current = max(0, int(app_state["stats"].get("streak_days", 0) or 0))
        last_value = app_state["stats"].get("last_learning_date") or app_state["stats"].get("last_login")
        try:
            last_day = datetime.date.fromisoformat(last_value) if last_value else None
        except (TypeError, ValueError):
            last_day = None
        if last_day and last_day < datetime.date.today() - datetime.timedelta(days=1):
            return 0
        return current

    def show_statistics():
        page.clean()
        page.scroll = ft.ScrollMode.HIDDEN
        page.bgcolor = "#F3E5F5"
        lang = app_state["lang"]
        txt = UI_TEXT[lang]

        total_words = len(all_words)
        learned_words = len([w for w in all_words if w["learned"]])
        progress_val = learned_words / total_words if total_words > 0 else 0

        words_with_errors = []
        for w in all_words:
            w_id = str(w["id"])
            errors = app_state["stats"]["words"].get(w_id, {}).get("wrong_answers", 0)
            if errors > 0:
                words_with_errors.append({"word": w, "errors": errors})

        words_with_errors.sort(key=lambda x: x["errors"], reverse=True)
        top_hard = words_with_errors[:10]

        hard_words_column = ft.Column(spacing=10)
        for hw in top_hard:
            w = hw["word"]
            native_word = w.get(lang.lower(), w.get("ru", "---"))
            hard_words_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{native_word} - {w['gag']}", size=16, weight="bold"),
                        ft.Text(f"❌ {hw['errors']}", color="red", size=16, weight="bold")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10, bgcolor="white", border_radius=8
                )
            )

        page.add(
            ft.Container(height=30),
            ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: show_main_menu())], alignment=ft.MainAxisAlignment.START),
            ft.Text(txt["stats_title"], size=25, weight="bold", color="#4A148C"),
            ft.Container(height=20),
            ft.Text(f"Выучено: {learned_words} из {total_words}", size=18, weight="bold"),
            ft.ProgressBar(value=progress_val, color="#4A148C", bgcolor="#eeeeee", width=380, height=20),
            ft.Container(height=30),
            ft.Text(txt["hard_words"], size=18, weight="bold", color="red"),
            ft.Container(height=10),
            hard_words_column if top_hard else ft.Text("Ошибок пока нет!", color="grey"),
            ft.Container(height=40)
        )
        page.update()

    def show_language_selector():
        page.clean()
        page.navigation_bar = None
        page.scroll = None
        page.bgcolor = BG
        page.padding = 0
        page.add(ft.SafeArea(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(height=80),
                    ft.Image(
                        src="icon.svg",
                        width=76,
                        height=76,
                        fit=ft.BoxFit.CONTAIN,
                        border_radius=24,
                        anti_alias=True,
                    ),
                    ft.Container(height=16),
                    ft.Text("Welcome to Gagauzium", size=28, weight="bold", color=INK, text_align=ft.TextAlign.CENTER),
                    ft.Text("Выберите язык обучения\nAlegeți limba de învățare", size=15, color=MUTED, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=28),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Text("🇷🇺", size=24), ft.Text("Русский", size=18, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
                        width=330, height=62, bgcolor=INDIGO, color="white", on_click=lambda _: set_language("RU")
                    ),
                    ft.Container(height=12),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Text("🇷🇴", size=24), ft.Text("Română", size=18, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
                        width=330, height=62, bgcolor="white", color=INK, on_click=lambda _: set_language("RO")
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=24,
            ),
            avoid_intrusions_bottom=False,
            expand=True,
        ))
        page.update()

    def set_language(lang, destination="home"):
        app_state["lang"] = lang
        app_state["stats"]["lang"] = lang
        save_stats(app_state["stats"])
        if destination == "settings":
            show_settings()
        else:
            show_home(reset_scroll=True)

    def show_home(reset_scroll=False):
        nonlocal all_words
        all_words = merge_data_and_stats(load_data(), app_state["stats"])
        prepare_main_screen("home", 0)
        t = phase_text()
        learned_count = sum(1 for w in all_words if w["learned"])
        total_count = len(all_words)
        percentage = round(learned_count / total_count * 100) if total_count else 0
        today = datetime.date.today().isoformat()
        daily = app_state["stats"].get("daily_review") or {}
        daily_is_today = daily.get("date") == today
        daily_index = min(20, daily.get("index", 0)) if daily_is_today else 0
        daily_done = daily_is_today and daily_index >= 20
        if learned_count < 20:
            daily_status, daily_cta, daily_disabled = t["daily_locked"], t["start_daily"], True
        elif daily_done:
            daily_status, daily_cta, daily_disabled = t["daily_complete"], t["start_daily"], True
        elif daily_index > 0:
            daily_status, daily_cta, daily_disabled = t["daily_in_progress"].format(daily_index), t["continue_daily"], False
        else:
            daily_status, daily_cta, daily_disabled = t["ready_review"], t["start_daily"], False

        progress_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(t["your_progress"], size=12, weight=ft.FontWeight.BOLD, color="#B9C5FF"),
                    ft.Container(content=ft.Text(f"{percentage}%", size=12, weight=ft.FontWeight.BOLD, color="white"), padding=ft.Padding.symmetric(horizontal=10, vertical=4), bgcolor="#344071", border_radius=12),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(
                    spans=[
                        ft.TextSpan(str(learned_count), style=ft.TextStyle(size=38, weight=ft.FontWeight.BOLD, color="white")),
                        ft.TextSpan(f" / {word_count_text(total_count, app_state['lang'])}", style=ft.TextStyle(size=14, color="#C9CEDD")),
                    ],
                ),
                ft.ProgressBar(value=learned_count / total_count if total_count else 0, color="#75D3C7", bgcolor="#394269", height=10),
                ft.Text(f"Level 1 · {t['beginner']}", size=11, color="#A9E7DF"),
            ], spacing=10), padding=20, bgcolor=INDIGO_DARK, border_radius=24,
        )

        daily_controls = [
            ft.Row([ft.Text("✨", size=24), ft.Column([ft.Text(t["today"], size=17, weight=ft.FontWeight.BOLD, color=INK), ft.Text(t["daily_review"], size=11, color=MUTED)], spacing=0)], spacing=10),
        ]
        if learned_count == 0:
            daily_controls.extend([
                ft.Text(t["daily_new_user_hint"], size=14, weight=ft.FontWeight.W_600, color=INK),
                ft.Text(t["daily_new_user_locked"], size=12, color=MUTED),
            ])
        else:
            daily_controls.append(ft.Text(daily_status, size=14, weight=ft.FontWeight.W_600, color=INK))
        if learned_count > 0 and daily_done:
            daily_controls.append(ft.Text(t["daily_complete_hint"], size=12, color=MUTED))
        elif learned_count > 0 and not daily_disabled:
            daily_controls.append(ft.ElevatedButton(
                daily_cta,
                icon=ft.Icons.PLAY_ARROW,
                on_click=lambda _: start_session("ALL", "daily"),
                bgcolor=INDIGO,
                color="white",
                height=46,
            ))
        daily_card = rounded_card(ft.Column(
            daily_controls,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ))

        last_category = app_state["stats"].get("last_active_category")
        actual_categories = {w["category"] for w in all_words}
        if learned_count == 0:
            continue_content = ft.Column([
                ft.Text(t["welcome_learning"], size=18, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
                ft.Text(t["welcome_gagauz"], size=16, weight=ft.FontWeight.W_600, color=INDIGO, text_align=ft.TextAlign.CENTER),
                ft.Container(height=2),
                ft.Text(t["choose_start"], size=14, color=MUTED, text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(
                    t["choose_first_topic"],
                    icon=ft.Icons.MENU_BOOK,
                    on_click=lambda _: show_learn(),
                    bgcolor=INDIGO,
                    color="white",
                    height=46,
                ),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        elif last_category in actual_categories:
            learned, total, _ = category_counts(last_category)
            continue_content = ft.Column([
                ft.Text(t["continue_learning"], size=11, weight=ft.FontWeight.BOLD, color=MUTED),
                ft.Row([category_visual(last_category, 62), ft.Column([ft.Text(localized_category_name(last_category, app_state["lang"]), size=18, weight=ft.FontWeight.BOLD, color=INK), ft.Text(get_category_meta(last_category).get("gag") or "", size=11, color=INDIGO), ft.Text(learned_of_total_text(learned, total, app_state["lang"]), size=12, color=MUTED)], spacing=2, expand=True)], spacing=14),
                ft.ProgressBar(value=learned / total if total else 0, color=INDIGO, bgcolor="#E8EAF2", height=8),
                ft.ElevatedButton(
                    content=ft.Text(t["continue"], size=13, text_align=ft.TextAlign.CENTER),
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda _, c=last_category: open_category_detail(c),
                    bgcolor="#20283D",
                    color="white",
                    height=46,
                    style=ft.ButtonStyle(alignment=ft.Alignment.CENTER),
                ),
                ft.TextButton(
                    content=ft.Text(t["choose_category"], size=16, text_align=ft.TextAlign.CENTER),
                    on_click=lambda _: show_learn(),
                    style=ft.ButtonStyle(alignment=ft.Alignment.CENTER),
                ),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        else:
            continue_content = ft.Column([
                ft.Text(t["continue_learning"], size=11, weight=ft.FontWeight.BOLD, color=MUTED),
                ft.Text(t["no_category"], size=14, color=MUTED),
                ft.ElevatedButton(t["choose_category"], icon=ft.Icons.MENU_BOOK, on_click=lambda _: show_learn(), bgcolor=INDIGO, color="white"),
            ], spacing=12)

        streak = displayed_streak()
        streak_card = rounded_card(ft.Row([
            ft.Container(content=ft.Text("🔥", size=24), width=46, height=46, alignment=ft.Alignment.CENTER, bgcolor="#FFF0D9", border_radius=15),
            ft.Column([ft.Text(streak_days_text(streak, app_state["lang"]), size=15, weight=ft.FontWeight.BOLD, color="#8B4513"), ft.Text(t["streak_hint"], size=11, color="#9A633A")], spacing=2, expand=True),
        ], spacing=12), padding=14, bgcolor="#FFF8EC")

        learning_card = rounded_card(continue_content)
        if learned_count == 0:
            page.add(ft.Container(height=4), progress_card, learning_card, daily_card, streak_card, ft.Container(height=8))
        else:
            page.add(ft.Container(height=4), progress_card, daily_card, learning_card, streak_card, ft.Container(height=8))
        page.update()

    def show_main_menu(reset_scroll=False):
        show_home(reset_scroll=reset_scroll)

    def show_learn():
        prepare_main_screen("learn", 1, add_header=False)
        page.scroll = None
        page.padding = 0
        t = phase_text()
        actual = {w["category"] for w in all_words}
        cards = []
        for meta in CATEGORY_METADATA:
            source_name = meta["source_name"]
            if source_name not in actual:
                continue
            learned, total, _ = category_counts(source_name)
            percent = round(learned / total * 100) if total else 0
            subtitle = meta.get("gag") or ""
            cards.append(ft.Container(
                content=ft.Column([
                    ft.Row([category_visual(source_name, 48), ft.Container(content=ft.Text(f"{percent}%", size=10, weight=ft.FontWeight.BOLD, color=INDIGO), padding=ft.Padding.symmetric(horizontal=7, vertical=3), bgcolor="#EEF2FF", border_radius=10, visible=percent > 0)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(localized_category_name(source_name, app_state["lang"]), size=14, weight=ft.FontWeight.BOLD, color=INK, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(subtitle, size=10, color=INDIGO, visible=bool(subtitle)),
                    ft.Container(expand=True),
                    ft.Text(f"{learned} / {total}", size=11, color=MUTED),
                    ft.ProgressBar(value=learned / total if total else 0, color=INDIGO, bgcolor="#E8EAF2", height=6),
                ], spacing=5),
                padding=12, bgcolor=CARD,
                border=ft.Border.all(1, BORDER), border_radius=19,
                shadow=ft.BoxShadow(blur_radius=7, color="#0D0F172A", offset=ft.Offset(0, 2)),
                on_click=lambda _, c=source_name: open_category_detail(c), ink=True,
            ))
        category_grid = ft.GridView(
            controls=cards,
            runs_count=2,
            spacing=11,
            run_spacing=11,
            child_aspect_ratio=0.92,
            padding=ft.Padding.only(bottom=12),
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        page.add(ft.SafeArea(
            content=ft.Container(
                content=ft.Column([
                    app_header(),
                    ft.Container(height=4),
                    ft.Text(t["learn_title"], size=24, weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text(t["learn_subtitle"], size=12, color=MUTED),
                    ft.Row([
                        ft.Container(content=ft.Text(t["beginner"], size=12, weight=ft.FontWeight.BOLD, color="white"), padding=ft.Padding.symmetric(horizontal=14, vertical=9), bgcolor=INDIGO, border_radius=12),
                        *[ft.Container(content=ft.Text(f"🔒 {label}", size=11, color="#98A2B3"), padding=ft.Padding.symmetric(horizontal=11, vertical=9), bgcolor="#EEEFF2", border_radius=12) for label in (t["conversational"], t["advanced"], t["expert"])],
                    ], scroll=ft.ScrollMode.HIDDEN, spacing=7),
                    ft.Container(height=2),
                    category_grid,
                ], spacing=8, expand=True),
                padding=ft.Padding.only(left=16, right=16, top=14),
                expand=True,
            ),
            avoid_intrusions_bottom=False,
            expand=True,
        ))
        page.update()

    def open_category_detail(source_name):
        persist_last_category(source_name)
        show_category_detail(source_name)

    def show_category_detail(source_name):
        prepare_main_screen("category", 1)
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        t = phase_text()
        learned, total, difficult = category_counts(source_name)
        remaining = total - learned
        meta = get_category_meta(source_name)
        page.add(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_learn())], spacing=5),
            rounded_card(ft.Column([
                ft.Row([category_visual(source_name, 82), ft.Column([ft.Text(localized_category_name(source_name, app_state["lang"]), size=24, weight=ft.FontWeight.BOLD, color=INK), ft.Text(meta.get("gag") or "", size=14, color=INDIGO)], spacing=3, expand=True)], spacing=15),
                ft.Row([ft.Text(learned_of_total_text(learned, total, app_state["lang"]), size=12, weight=ft.FontWeight.BOLD, color=INK), ft.Text(f"{round(learned / total * 100) if total else 0}%", size=12, weight=ft.FontWeight.BOLD, color=INDIGO)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=learned / total if total else 0, color=INDIGO, bgcolor="#E8EAF2", height=9),
            ], spacing=12)),
            rounded_card(ft.Column([
                ft.Text("✨ " + t["learn_new"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(remaining_word_count_text(remaining, app_state["lang"]), size=12, color=MUTED),
                ft.ElevatedButton(t["start_learning"] if remaining else t["all_words_learned"], icon=ft.Icons.PLAY_ARROW, on_click=lambda _: start_session(source_name, "new"), disabled=remaining == 0, bgcolor=INDIGO, color="white"),
            ], spacing=9, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)),
            rounded_card(ft.Column([
                ft.Text("⚠️ " + t["difficult_words"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(attention_word_count_text(difficult, app_state["lang"]) if difficult else t["no_difficult"], size=12, color=MUTED),
                ft.ElevatedButton(t["review_action"], icon=ft.Icons.REPLAY, on_click=lambda _: start_session(source_name, "difficult"), disabled=difficult == 0, opacity=0.48 if difficult == 0 else 1.0, bgcolor="#D34A5B", color="white"),
            ], spacing=9, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)),
            rounded_card(ft.Column([
                ft.Text("📖 " + t["learned_words"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(learned_word_count_text(learned, app_state["lang"]), size=12, color=MUTED),
                ft.ElevatedButton(t["view_words"], icon=ft.Icons.LIST_ALT, on_click=lambda _: show_word_list(source_name, learned_only=True), disabled=learned == 0, opacity=0.48 if learned == 0 else 1.0, bgcolor="#16847A", color="white"),
            ], spacing=9, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)),
            ft.Container(height=8),
        )
        page.update()

    def show_review_hub():
        prepare_main_screen("review", 2)
        t = phase_text()
        learned_count = sum(1 for w in all_words if w["learned"])
        difficult_count = sum(1 for w in all_words if w["learned"] and app_state["stats"]["words"].get(str(w["id"]), {}).get("wrong_answers", 0) > 0)
        today = datetime.date.today().isoformat()
        daily = app_state["stats"].get("daily_review") or {}
        daily_done = daily.get("date") == today and daily.get("index", 0) >= 20
        basic_review_locked = learned_count < 4
        basic_review_status = t["review_mode_locked"] if basic_review_locked else None

        def review_card(icon, title, description, badge, action, color, disabled=False, completed=False):
            state_icon = ft.Icons.CHECK_CIRCLE_OUTLINE if completed else (ft.Icons.LOCK_OUTLINE if disabled else None)
            state_color = "#16847A" if completed else ("#98A2B3" if disabled else color)
            visual_bgcolor = "#DFF4E7" if completed else ("#EAECF0" if disabled else color)
            visual_controls = [ft.Text(icon, size=30)]
            if state_icon is not None:
                visual_controls.append(ft.Icon(state_icon, size=23, color=state_color))
            card_controls = [
                ft.Text(title, size=17, weight=ft.FontWeight.BOLD, color=INK, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Text(description, size=12, color=MUTED, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
            ]
            if badge:
                card_controls.append(ft.Text(badge, size=11, weight=ft.FontWeight.W_600, color=state_color, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS))
            card_controls.extend([
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        visual_controls,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN if state_icon is not None else ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                    bgcolor=visual_bgcolor,
                    border_radius=14,
                ),
            ])
            card = rounded_card(ft.Column(card_controls, spacing=10, expand=True))
            card.col = 6
            card.height = 285
            card.on_click = None if disabled else action
            card.ink = not disabled
            card.ink_color = "#16212A5D"
            card.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
            card.opacity = 0.72 if disabled and not completed else 1.0
            card.tooltip = title
            return card

        exercise_cards = [
            review_card("✨", t["daily_review"], t["daily_desc"], t["daily_complete"] if daily_done else (t["ready_review"] if learned_count >= 20 else t["daily_locked"]), lambda _: start_session("ALL", "daily"), INDIGO, learned_count < 20 or daily_done, completed=daily_done),
            review_card("🔁", t["regular_review"], t["regular_review_desc"], basic_review_status, lambda _: start_session("ALL", "review"), "#16847A", basic_review_locked),
            review_card("⚠️", t["difficult_words"], t["difficult_desc"], attention_word_count_text(difficult_count, app_state["lang"]) if difficult_count else t["no_difficult"], lambda _: start_session("ALL", "difficult"), "#D34A5B", difficult_count == 0),
            review_card("⚡", t["quick_review"], t["quick_desc"], basic_review_status, lambda _: start_session("ALL", "fast"), "#5C55C8", basic_review_locked),
            review_card("🔤", t["word_building"], t["word_building_desc"], basic_review_status, lambda _: start_session("ALL", "word_building"), "#B45F06", basic_review_locked),
            review_card("❓", t["true_false_short"], t["quiz_desc"], basic_review_status, lambda _: start_session("ALL", "true_false"), "#16847A", basic_review_locked),
        ]
        page.add(
            ft.Container(height=4), ft.Text(t["review_title"], size=24, weight=ft.FontWeight.BOLD, color=INK), ft.Text(t["review_subtitle"], size=12, color=MUTED),
            ft.ResponsiveRow(exercise_cards, columns=12, spacing=11, run_spacing=11),
            ft.Container(height=8),
        )
        page.update()

    def show_settings():
        prepare_main_screen("settings", app_state.get("nav_index", 0))
        t = phase_text()
        categories = [m for m in CATEGORY_METADATA if any(w["category"] == m["source_name"] for w in all_words)]
        category_select = ft.Dropdown(
            label=t["select_category"], value=app_state.get("last_category") if app_state.get("last_category") in {m["source_name"] for m in categories} else None,
            options=[ft.DropdownOption(key=m["source_name"], text=localized_category_name(m["source_name"], app_state["lang"])) for m in categories],
            border_radius=14, expand=True,
        )
        page.add(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_home()), ft.Container(expand=True)]),
            ft.Text(t["settings"], size=25, weight=ft.FontWeight.BOLD, color=INK),
            rounded_card(ft.Column([
                ft.Text(t["language"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Row([
                    ft.ElevatedButton("🇷🇺 " + t["russian"], on_click=lambda _: set_language("RU", "settings"), bgcolor=INDIGO if app_state["lang"] == "RU" else "#EEEFF4", color="white" if app_state["lang"] == "RU" else INK, expand=True),
                    ft.ElevatedButton("🇷🇴 " + t["romanian"], on_click=lambda _: set_language("RO", "settings"), bgcolor=INDIGO if app_state["lang"] == "RO" else "#EEEFF4", color="white" if app_state["lang"] == "RO" else INK, expand=True),
                ], spacing=8),
            ], spacing=12)),
            rounded_card(ft.Column([
                ft.Text(t["reset_progress"], size=17, weight=ft.FontWeight.BOLD, color="#B42318"),
                category_select,
                ft.OutlinedButton(t["reset_category_label"], icon=ft.Icons.RESTART_ALT, on_click=lambda _: reset_category(category_select.value) if category_select.value else None),
                ft.Divider(color=BORDER),
                ft.Text(t["reset_all_hint"], size=11, color=MUTED),
                ft.OutlinedButton(UI_TEXT[app_state["lang"]]["reset_all"], icon=ft.Icons.DELETE_OUTLINE, on_click=lambda _: reset_all_progress()),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)),
            ft.Container(height=8),
        )
        page.update()

    def show_confirm_dialog(title, message, on_confirm):
        txt = UI_TEXT[app_state["lang"]]

        def close_dlg(_=None):
            page.pop_dialog()

        def confirm(_):
            page.pop_dialog()
            on_confirm()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, weight="bold"),
            content=ft.Text(message),
            actions=[
                ft.TextButton(txt["confirm_no"], on_click=close_dlg),
                ft.ElevatedButton(txt["confirm_yes"], on_click=confirm, bgcolor="red", color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        page.show_dialog(dlg)

    def reset_category(category_name):
        txt = UI_TEXT[app_state["lang"]]
        cat_display = localized_category_name(category_name, app_state["lang"])

        def do_reset():
            for w in all_words:
                if w["category"] == category_name:
                    w["learned"] = False
                    app_state["stats"]["words"][str(w["id"])]["learned"] = False
            save_stats(app_state["stats"])
            show_main_menu()

        show_confirm_dialog(
            title=txt["reset"],
            message=txt["confirm_reset_category"].format(cat_display),
            on_confirm=do_reset,
        )

    def reset_all_progress():
        txt = UI_TEXT[app_state["lang"]]

        def do_reset():
            fresh_word_stats = {}
            for w in all_words:
                w["learned"] = False
                fresh_word_stats[str(w["id"])] = {
                    "learned": False,
                    "correct_answers": 0,
                    "wrong_answers": 0,
                    "last_seen": "1970-01-01",
                }
            app_state["stats"].clear()
            app_state["stats"].update({
                "lang": app_state["lang"],
                "streak_days": 0,
                "last_login": "",
                "words": fresh_word_stats,
            })
            app_state["last_category"] = None
            save_stats(app_state["stats"])
            show_main_menu()

        show_confirm_dialog(
            title=txt["reset_all"],
            message=txt["confirm_reset_all"],
            on_confirm=do_reset,
        )

    def show_word_list(category, learned_only=False):
        persist_last_category(category)
        page.clean()
        page.navigation_bar = None
        page.scroll = None
        page.bgcolor = BG
        page.padding = 16
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        words = [w for w in all_words if w["category"] == category and (w["learned"] or not learned_only)]
        cat_display = localized_category_name(category, lang)

        rows = []
        for i, w in enumerate(words):
            native_word = w.get(lang.lower(), w.get("ru", "---"))
            rows.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(content=ft.Text(native_word, size=16, weight="bold", color="black"), width=150),
                        ft.Text(w["gag"], size=16, color="blue", italic=True, expand=True),
                        ft.Text("✅" if w["learned"] else "⭕", size=14)
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=12, bgcolor="#ffffff" if i % 2 == 0 else "#f9f9f9",
                    border=ft.Border(bottom=ft.BorderSide(1, "#eeeeee"))
                )
            )

        list_view = ft.ListView(controls=rows, expand=True, spacing=0, scroll=ft.ScrollMode.HIDDEN)

        page.add(
            ft.Container(height=30),
            ft.Row([ft.TextButton(content=ft.Text(phase_text()["back"], size=17, weight="bold"), icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_category_detail(category))], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=10),
            ft.Text(f"{txt['dictionary']}{cat_display}", size=20, weight="bold", color="black"),
            ft.Container(height=10),
            list_view,
        )
        page.update()

    def restore_exercise_origin():
        return_screen = app_state.get("exercise_return_screen", "home")
        return_category = app_state.get("exercise_return_category")
        if return_screen == "category" and return_category:
            show_category_detail(return_category)
        elif return_screen == "learn":
            show_learn()
        elif return_screen == "review":
            show_review_hub()
        elif return_screen == "settings":
            show_settings()
        else:
            show_home()

    def return_from_exercise(_=None):
        app_state["question_id"] = app_state.get("question_id", 0) + 1
        if app_state.get("exercise_view_active") and page.views:
            page.views.pop()
        app_state["exercise_view_active"] = False
        page.on_view_pop = None
        restore_exercise_origin()

    def set_session_view(view):
        if app_state.get("exercise_view_active") and page.views:
            page.views[-1] = view
        else:
            page.views.append(view)
            app_state["exercise_view_active"] = True
        page.update()

    def exercise_shell(body, bottom=None, title=None):
        t = phase_text()
        total = max(1, len(app_state["current_batch"]))
        current = min(total, app_state["index"] + 1)
        if app_state["mode"] == "fast":
            progress_bar = ft.ProgressBar(value=app_state.get("fast_timer_value", 1.0), color="#D9363E", bgcolor="#F4D7DA", height=8)
            app_state["fast_timer_bar"] = progress_bar
        else:
            progress_bar = ft.ProgressBar(value=current / total, color=INDIGO, bgcolor="#E7E9F2", height=8)
        controls = [
            ft.Row([
                ft.IconButton(icon=ft.Icons.CLOSE, tooltip=t["close_session"], on_click=return_from_exercise),
                ft.Text(title or t["question"], size=15, weight=ft.FontWeight.BOLD, color=INK, expand=True, text_align=ft.TextAlign.CENTER),
                ft.Text(f"{current} / {total}", size=13, weight=ft.FontWeight.BOLD, color=MUTED),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            progress_bar,
            ft.Container(content=body, expand=True),
        ]
        if bottom is not None:
            if isinstance(bottom, ft.Row):
                controls.append(bottom)
            else:
                controls.append(ft.Row([ft.Container(expand=True), bottom], alignment=ft.MainAxisAlignment.END))
        return ft.View(
            route="/exercise",
            controls=[ft.SafeArea(
                content=ft.Container(
                    content=ft.Column(controls, spacing=14, expand=True),
                    padding=ft.Padding.only(left=18, right=18, top=10, bottom=18),
                    expand=True,
                ),
                expand=True,
            )],
            bgcolor=BG,
            padding=0,
            can_pop=True,
        )

    def start_session(category, mode):
        if app_state.get("current_screen") != "exercise":
            app_state["exercise_return_screen"] = app_state.get("current_screen", "home")
            app_state["exercise_return_category"] = (
                category if app_state["exercise_return_screen"] == "category" and category != "ALL" else None
            )
        app_state["current_screen"] = "exercise"
        page.on_view_pop = return_from_exercise
        if category != "ALL":
            persist_last_category(category)
        app_state["mode"] = mode
        app_state["last_word_id"] = None
        app_state["session_completion_recorded"] = False
        app_state["feedback_active"] = False
        app_state["feedback_correct"] = False
        app_state["selected_answer"] = None
        app_state["session_correct"] = 0
        app_state["session_answered"] = 0
        app_state["session_new_learned"] = 0
        app_state["learning_batch_viewed"] = False
        app_state["selected_letter_indices"] = []
        app_state["fast_timer_value"] = 1.0
        app_state["fast_timer_bar"] = None
        app_state["fast_result_state"] = None
        today = datetime.date.today()
        today_iso = today.isoformat()

        if mode == "difficult":
            words = [
                w for w in all_words
                if w["learned"]
                and (category == "ALL" or w["category"] == category)
                and app_state["stats"]["words"].get(str(w["id"]), {}).get("wrong_answers", 0) > 0
            ]
            app_state["is_quiz"] = True
            app_state["current_batch"] = weighted_sample(words, app_state["stats"], today, k=10 if category == "ALL" else 6)
            app_state["index"] = 0
        elif mode == "fast":
            words = [w for w in all_words if w["learned"]]
            random.shuffle(words)
            app_state["is_quiz"] = True
            app_state["lives"] = 3
            app_state["score"] = 0
            app_state["current_batch"] = words
            app_state["question_id"] = 0
            app_state["index"] = 0
        elif mode == "true_false":
            words = [w for w in all_words if w["learned"]]
            app_state["is_quiz"] = True
            app_state["score"] = 0
            app_state["current_batch"] = weighted_sample(words, app_state["stats"], today, k=15)
            app_state["index"] = 0
        elif mode == "word_building":
            words = [w for w in all_words if w["learned"]]
            app_state["is_quiz"] = True
            app_state["current_batch"] = weighted_sample(words, app_state["stats"], today, k=10)
            app_state["index"] = 0
        elif mode == "daily":
            app_state["is_quiz"] = True
            daily = app_state["stats"].get("daily_review")
            if not daily or daily.get("date") != today_iso:
                learned = [w for w in all_words if w["learned"]]
                word_ids = build_daily_set(learned, app_state["stats"], today)
                daily = {"date": today_iso, "word_ids": word_ids, "index": 0, "correct_count": 0}
                app_state["stats"]["daily_review"] = daily
                save_stats(app_state["stats"])
            word_map = {w["id"]: w for w in all_words}
            app_state["current_batch"] = [word_map[wid] for wid in daily["word_ids"] if wid in word_map]
            app_state["index"] = daily.get("index", 0)
            app_state["session_answered"] = app_state["index"]
            app_state["session_correct"] = daily.get("correct_count", 0)
        elif category == "ALL":
            words = [w for w in all_words if w["learned"]]
            app_state["is_quiz"] = True
            app_state["current_batch"] = weighted_sample(words, app_state["stats"], today, k=10)
            app_state["index"] = 0
        elif mode == "new":
            words = [w for w in all_words if w["category"] == category and not w["learned"]]
            random.shuffle(words)
            app_state["is_quiz"] = False
            app_state["current_batch"] = words[:6]
            app_state["index"] = 0
        else:
            words = [w for w in all_words if w["category"] == category and w["learned"]]
            app_state["is_quiz"] = True
            app_state["current_batch"] = weighted_sample(words, app_state["stats"], today, k=6)
            app_state["index"] = 0

        if not app_state["current_batch"]:
            return_from_exercise()
        elif app_state["is_quiz"]:
            show_quiz_card()
        else:
            show_study_card()

    def show_study_card():
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        if app_state["index"] >= len(app_state["current_batch"]):
            start_practice_phase()
            return
        word = app_state["current_batch"][app_state["index"]]
        native_word = word.get(lang.lower(), word.get("ru", "---"))
        is_first = app_state["index"] == 0
        is_last = app_state["index"] == len(app_state["current_batch"]) - 1
        if is_last:
            app_state["learning_batch_viewed"] = True
        word_card = rounded_card(ft.Column([
            ft.Text(txt["remember"], size=13, color=MUTED),
            ft.Text(native_word, size=32, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
            ft.Divider(color=BORDER),
            ft.Text(word["gag"], size=29, color=INDIGO, italic=True, text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12), padding=28)
        body = ft.Column([
            ft.Container(expand=True),
            ft.Row([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        tooltip=phase_text()["previous_word"],
                        icon_color=MUTED,
                        on_click=lambda _: previous_study_word(),
                        visible=not is_first,
                    ),
                    width=48,
                ),
                ft.Container(content=word_card, expand=True),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.CHEVRON_RIGHT,
                        tooltip=phase_text()["next_word"],
                        icon_color=MUTED,
                        on_click=lambda _: next_study_word(),
                        visible=not is_last,
                    ),
                    width=48,
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            ft.Container(expand=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        bottom = None
        if app_state["learning_batch_viewed"]:
            bottom = ft.ElevatedButton(
                phase_text()["repeat_learned"],
                icon=ft.Icons.REPLAY,
                on_click=lambda _: start_practice_phase(),
                bgcolor=INDIGO,
                color="white",
                height=52,
            )
        set_session_view(exercise_shell(body, bottom, phase_text()["learning_new_words"]))

    def previous_study_word():
        if app_state["index"] > 0:
            app_state["index"] -= 1
            show_study_card()

    def next_study_word():
        app_state["index"] += 1
        show_study_card()

    def start_practice_phase():
        app_state["is_quiz"] = True
        app_state["index"] = 0
        app_state["last_word_id"] = None
        app_state["feedback_active"] = False
        show_quiz_card()

    def word_build_target(word):
        return word["gag"].split(" / ", 1)[0].strip()

    def answer_letters(value):
        return [char for char in value if char.isalpha()]

    def prepare_question(word):
        lang = app_state["lang"]
        mode = app_state["mode"]
        if mode == "word_building":
            target = word_build_target(word)
            letters = answer_letters(target)
            extra_count = 2 if len(letters) < 6 else 3
            target_letter_keys = {char.casefold() for char in letters}
            distractor_pool = sorted({
                char
                for candidate in all_words
                for char in answer_letters(word_build_target(candidate))
                if char.casefold() not in target_letter_keys
            }, key=str.casefold)
            if len(distractor_pool) >= extra_count:
                letters.extend(random.sample(distractor_pool, extra_count))
            else:
                fallback_pool = [
                    char for char in "abcçdefgıijklmnoöprsştuüvyzä"
                    if char.casefold() not in target_letter_keys
                ]
                letters.extend(random.choices(distractor_pool or fallback_pool, k=extra_count))
            random.shuffle(letters)
            app_state["direction"] = "forward"
            app_state["prompt_word"] = word.get(lang.lower(), word.get("ru", "---"))
            app_state["correct_answer"] = "".join(answer_letters(target))
            app_state["letter_bank"] = letters
            app_state["selected_letter_indices"] = []
        else:
            direction = "forward" if mode == "new" else random.choice(["forward", "reverse"])
            app_state["direction"] = direction
            if direction == "forward":
                prompt_word = word.get(lang.lower(), word.get("ru", "---"))
                correct = word["gag"]
                others = list({w["gag"] for w in all_words if w["gag"] != correct})
            else:
                prompt_word = word["gag"]
                correct = word.get(lang.lower(), word.get("ru", "---"))
                others = list({w.get(lang.lower(), w.get("ru", "---")) for w in all_words if w.get(lang.lower(), w.get("ru", "---")) != correct})
            app_state["prompt_word"] = prompt_word
            app_state["correct_answer"] = correct
            if mode == "true_false":
                is_truth = random.choice([True, False])
                app_state["tf_displayed"] = correct if is_truth else (random.choice(others) if others else correct)
                app_state["tf_is_truth"] = is_truth
            else:
                distractors = random.sample(others, min(len(others), 3))
                app_state["current_options"] = distractors + [correct]
                random.shuffle(app_state["current_options"])
        app_state["last_word_id"] = word["id"]
        app_state["feedback_active"] = False
        app_state["selected_answer"] = None
        if mode == "fast":
            app_state["fast_timer_value"] = 1.0
            app_state["question_id"] = app_state.get("question_id", 0) + 1

    def feedback_panel(word):
        t = phase_text()
        native = word.get(app_state["lang"].lower(), word.get("ru", "---"))
        correct = app_state["feedback_correct"]
        skipped = app_state.get("selected_answer") == "__skip__"
        if skipped:
            feedback_controls = [
                ft.Text(f"{t['correct_was']}: {word['gag']} — {native}", size=16, weight=ft.FontWeight.W_600, color=INK),
            ]
        else:
            feedback_controls = [
                ft.Text("✓ " + t["correct_answer"] if correct else "✕ " + t["incorrect_answer"], size=20, weight=ft.FontWeight.BOLD, color="#157347" if correct else "#B42318"),
                ft.Text(f"{word['gag']} — {native}" if correct else f"{t['correct_was']}: {word['gag']} — {native}", size=14, color=INK),
            ]
        return ft.Container(
            content=ft.Column(feedback_controls, spacing=5),
            padding=16,
            bgcolor="#EEF2FF" if skipped else ("#EAF8EF" if correct else "#FDECEC"),
            border_radius=18,
            border=ft.Border.all(1, "#C7D2FE" if skipped else ("#B7E4C7" if correct else "#F3B7B7")),
        )

    def multiple_choice_body(word):
        prompt = app_state["prompt_word"]
        direction = app_state.get("direction", "forward")
        buttons = []
        for option in app_state["current_options"]:
            bgcolor = "#FFFFFF"
            color = INK
            if app_state["feedback_active"]:
                if option == app_state["correct_answer"]:
                    bgcolor, color = "#198754", "white"
                elif option == app_state["selected_answer"]:
                    bgcolor, color = "#D9363E", "white"
            buttons.append(ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Text(option, text_align=ft.TextAlign.CENTER),
                    alignment=ft.Alignment.CENTER,
                ),
                height=54, bgcolor=bgcolor, color=color,
                style=ft.ButtonStyle(alignment=ft.Alignment.CENTER),
                on_click=None if app_state["feedback_active"] else lambda _, value=option: submit_answer(value, word),
            ))
        controls = [
            ft.Container(height=12),
            ft.Text(prompt, size=34, weight=ft.FontWeight.BOLD, color=INDIGO if direction == "reverse" else INK, italic=direction == "reverse", text_align=ft.TextAlign.CENTER),
            ft.Text(phase_text()["what_mean"], size=13, color=MUTED),
            ft.Container(height=10),
            ft.Column(buttons, spacing=10),
        ]
        if app_state["mode"] == "fast":
            controls.insert(0, ft.Row([ft.Text("❤️" * app_state.get("lives", 3), size=18), ft.Text(str(app_state.get("score", 0)), weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        return ft.Column(controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.HIDDEN, expand=True)

    def true_false_body(word):
        txt = UI_TEXT[app_state["lang"]]
        buttons = []
        for value, label in ((True, txt["true_btn"]), (False, txt["false_btn"])):
            bgcolor = "#FFFFFF"
            color = INK
            if app_state["feedback_active"]:
                if value == app_state["tf_is_truth"]:
                    bgcolor, color = "#198754", "white"
                elif value == app_state["selected_answer"]:
                    bgcolor, color = "#D9363E", "white"
            buttons.append(ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Text(label, text_align=ft.TextAlign.CENTER),
                    alignment=ft.Alignment.CENTER,
                ),
                height=62,
                bgcolor=bgcolor,
                color=color,
                style=ft.ButtonStyle(alignment=ft.Alignment.CENTER),
                on_click=None if app_state["feedback_active"] else lambda _, answer=value: submit_answer(answer, word),
            ))
        return ft.Column([
            ft.Container(height=18),
            ft.Text(app_state["prompt_word"], size=34, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
            ft.Text(app_state["tf_displayed"], size=27, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
            ft.Container(height=18),
            ft.Column(buttons, spacing=12),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

    def word_building_body(word):
        t = phase_text()
        selected = app_state["selected_letter_indices"]
        built = "".join(app_state["letter_bank"][i] for i in selected)
        target_length = len(answer_letters(word_build_target(word)))
        display = " ".join(char.upper() for char in built) if built else " ".join("_" for _ in range(target_length))
        if app_state["feedback_active"]:
            answer_bgcolor = "#EAF8EF" if app_state["feedback_correct"] else "#FDECEC"
            answer_border_color = "#B7E4C7" if app_state["feedback_correct"] else "#F3B7B7"
            answer_color = "#157347" if app_state["feedback_correct"] else "#B42318"
        else:
            answer_bgcolor = "#EEF2FF"
            answer_border_color = "#C7D2FE"
            answer_color = INDIGO
        bank = []
        for index, letter in enumerate(app_state["letter_bank"]):
            bank.append(ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Text(letter.upper(), text_align=ft.TextAlign.CENTER),
                    alignment=ft.Alignment.CENTER,
                ),
                width=48, height=48,
                disabled=index in selected or app_state["feedback_active"],
                on_click=lambda _, i=index: select_letter(i),
            ))
        return ft.Column([
            ft.Container(height=8),
            ft.Text(app_state["prompt_word"], size=31, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
            ft.Text(t["build_word"], size=13, color=MUTED),
            ft.Container(
                content=ft.Text(display, size=24, weight=ft.FontWeight.BOLD, color=answer_color, text_align=ft.TextAlign.CENTER),
                padding=18,
                bgcolor=answer_bgcolor,
                border=ft.Border.all(1, answer_border_color),
                border_radius=16,
            ),
            ft.Row(bank, wrap=True, spacing=8, run_spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.OutlinedButton(t["backspace"], icon=ft.Icons.BACKSPACE_OUTLINED, on_click=lambda _: remove_letter(), disabled=not selected or app_state["feedback_active"]),
                ft.OutlinedButton(t["clear"], icon=ft.Icons.CLEAR_ALL, on_click=lambda _: clear_letters(), disabled=not selected or app_state["feedback_active"]),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.ElevatedButton(
                t["check"],
                icon=ft.Icons.CHECK,
                on_click=lambda _: submit_answer(built, word),
                disabled=not selected,
                visible=not app_state["feedback_active"],
                bgcolor=INDIGO,
                color="white",
                height=50,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)

    def show_quiz_card():
        if app_state["index"] >= len(app_state["current_batch"]) or (
            app_state["mode"] == "fast"
            and app_state.get("lives", 0) <= 0
            and not app_state["feedback_active"]
        ):
            show_results()
            return
        word = app_state["current_batch"][app_state["index"]]
        is_new_question = app_state["last_word_id"] != word["id"]
        if is_new_question:
            prepare_question(word)
        mode = app_state["mode"]
        if mode == "true_false":
            body = true_false_body(word)
            title = phase_text()["true_false_short"]
        elif mode == "word_building":
            body = word_building_body(word)
            title = phase_text()["word_building"]
        else:
            body = multiple_choice_body(word)
            if mode == "daily":
                title = UI_TEXT[app_state["lang"]]["daily_review_title"]
            elif mode == "review":
                title = phase_text()["regular_review"]
            else:
                title = phase_text()["quiz"]
        if app_state["feedback_active"]:
            if mode == "word_building":
                body.controls.insert(4, feedback_panel(word))
            else:
                body.controls.append(feedback_panel(word))
            bottom = None if mode == "fast" else ft.ElevatedButton(
                phase_text()["continue_answer"],
                icon=ft.Icons.ARROW_FORWARD,
                on_click=lambda _: continue_after_feedback(),
                bgcolor=INDIGO,
                color="white",
                height=52,
            )
        else:
            bottom = None
            if mode in ("review", "word_building"):
                body.controls.append(ft.TextButton(UI_TEXT[app_state["lang"]]["skip"], on_click=lambda _: submit_answer("__skip__", word)))
        view = exercise_shell(body, bottom, title)
        set_session_view(view)
        if mode == "fast" and is_new_question:
            current_question = app_state["question_id"]
            page.run_task(run_fast_timer, current_question, word)

    async def run_fast_timer(current_question, word):
        for step in range(70):
            await asyncio.sleep(0.1)
            if app_state.get("question_id") != current_question or app_state["feedback_active"]:
                return
            app_state["fast_timer_value"] = 1.0 - ((step + 1) / 70)
            timer_bar = app_state.get("fast_timer_bar")
            if timer_bar is not None:
                timer_bar.value = app_state["fast_timer_value"]
                page.update()
        if app_state.get("question_id") == current_question and not app_state["feedback_active"]:
            submit_answer("__timeout__", word)

    async def auto_continue_fast(current_question):
        await asyncio.sleep(3)
        if (
            app_state["exercise_view_active"]
            and app_state["mode"] == "fast"
            and app_state["feedback_active"]
            and app_state.get("question_id") == current_question
        ):
            continue_after_feedback()

    def select_letter(index):
        if not app_state["feedback_active"] and index not in app_state["selected_letter_indices"]:
            app_state["selected_letter_indices"].append(index)
            show_quiz_card()

    def remove_letter():
        if app_state["selected_letter_indices"] and not app_state["feedback_active"]:
            app_state["selected_letter_indices"].pop()
            show_quiz_card()

    def clear_letters():
        if not app_state["feedback_active"]:
            app_state["selected_letter_indices"] = []
            show_quiz_card()

    def submit_answer(selected, word):
        if app_state["feedback_active"]:
            return
        mode = app_state["mode"]
        if mode == "true_false":
            is_correct = selected == app_state["tf_is_truth"]
        elif mode == "word_building":
            is_correct = str(selected).casefold() == str(app_state["correct_answer"]).casefold()
        else:
            is_correct = selected == app_state["correct_answer"]
        if mode == "fast":
            app_state["question_id"] += 1
        stats = app_state["stats"]["words"][str(word["id"])]
        stats["last_seen"] = datetime.date.today().isoformat()
        app_state["session_answered"] += 1
        app_state["selected_answer"] = selected
        app_state["feedback_correct"] = is_correct
        app_state["feedback_active"] = True
        if is_correct:
            stats["correct_answers"] = stats.get("correct_answers", 0) + 1
            app_state["session_correct"] += 1
            if mode in ("fast", "true_false"):
                app_state["score"] = app_state.get("score", 0) + 1
            if mode == "new" and not stats.get("learned", False):
                stats["learned"] = True
                word["learned"] = True
                app_state["session_new_learned"] += 1
            if mode == "daily":
                app_state["stats"]["daily_review"]["correct_count"] = app_state["stats"]["daily_review"].get("correct_count", 0) + 1
        else:
            stats["wrong_answers"] = stats.get("wrong_answers", 0) + 1
            if mode == "fast":
                app_state["lives"] -= 1
        if mode == "daily":
            app_state["stats"]["daily_review"]["index"] = app_state["index"] + 1
        save_stats(app_state["stats"])
        show_quiz_card()
        if mode == "fast":
            page.run_task(auto_continue_fast, app_state["question_id"])

    def continue_after_feedback():
        if not app_state["feedback_active"]:
            return
        app_state["feedback_active"] = False
        app_state["selected_answer"] = None
        app_state["selected_letter_indices"] = []
        app_state["last_word_id"] = None
        app_state["index"] += 1
        show_quiz_card()

    def show_results():
        record_completed_session()
        t = phase_text()
        mode = app_state["mode"]
        answered = app_state.get("session_answered", 0)
        correct = app_state.get("session_correct", 0)
        newly_learned = app_state.get("session_new_learned", 0)
        accuracy = round(correct / answered * 100) if answered else 0

        if mode == "fast":
            fast_result = app_state.get("fast_result_state")
            if fast_result is None:
                score = app_state.get("score", correct)
                best_exists = "fast_best_score" in app_state["stats"]
                previous_best = max(0, int(app_state["stats"].get("fast_best_score", 0) or 0))
                if not best_exists:
                    best_score = score
                    message = t["fast_first_score"]
                elif score > previous_best:
                    best_score = score
                    message = t["fast_new_record"]
                elif score == previous_best:
                    best_score = previous_best
                    message = t["fast_record_tied"]
                else:
                    best_score = previous_best
                    message = t["fast_to_record"].format(previous_best - score)
                if not best_exists or best_score != previous_best:
                    app_state["stats"]["fast_best_score"] = best_score
                    save_stats(app_state["stats"])
                fast_result = {"score": score, "best_score": best_score, "message": message}
                app_state["fast_result_state"] = fast_result

            emoji = "⚡"
            result_title = t["fast_result_title"]
            result_hint = fast_result["message"]
            result_card_controls = [
                ft.Text(t["fast_score"], size=12, weight=ft.FontWeight.BOLD, color=MUTED),
                ft.Text(str(fast_result["score"]), size=42, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
                ft.Text(f"{t['accuracy']}: {accuracy}%", size=15, weight=ft.FontWeight.BOLD, color=INK),
                ft.Divider(color=BORDER),
                ft.Text(f"{t['fast_best_score']}: {fast_result['best_score']}", size=14, color=MUTED),
                ft.Text(f"🔥 {t['streak_confirmed']}: {streak_days_text(displayed_streak(), app_state['lang'])}", size=14, color="#A15C00"),
            ]
            result_actions = [
                ft.ElevatedButton(t["try_again"], icon=ft.Icons.REPLAY, on_click=lambda _: start_session("ALL", "fast"), bgcolor=INDIGO, color="white", height=54),
                ft.OutlinedButton(t["finish"], icon=ft.Icons.CHECK, on_click=return_from_exercise, height=50),
            ]
        elif mode == "new":
            all_learned = answered > 0 and newly_learned == answered
            emoji = "✨" if all_learned else "🌱"
            result_title = t["learning_result_title"]
            result_hint = t["learning_result_all"] if all_learned else t["learning_result_retry"]
            result_card_controls = [
                ft.Text(str(newly_learned), size=42, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
                ft.Text(t["newly_learned"], size=14, weight=ft.FontWeight.BOLD, color=INK),
                ft.Divider(color=BORDER),
                ft.Text(f"{correct} / {answered} · {t['accuracy'].lower()}: {accuracy}%", size=14, color=MUTED),
                ft.Text(f"🔥 {t['streak_confirmed']}: {streak_days_text(displayed_streak(), app_state['lang'])}", size=14, color="#A15C00"),
            ]
            result_actions = [
                ft.ElevatedButton(t["finish"], icon=ft.Icons.CHECK, on_click=return_from_exercise, bgcolor=INDIGO, color="white", height=54),
            ]
        else:
            if accuracy >= 90:
                emoji, title_key, hint_key = "🎉", "result_excellent_title", "result_excellent_hint"
            elif accuracy >= 70:
                emoji, title_key, hint_key = "✨", "result_good_title", "result_good_hint"
            elif accuracy >= 40:
                emoji, title_key, hint_key = "🌱", "result_practice_title", "result_practice_hint"
            else:
                emoji, title_key, hint_key = "🔄", "result_attention_title", "result_attention_hint"
            result_title = t[title_key]
            result_hint = t[hint_key]
            result_card_controls = [
                ft.Text(f"{correct} / {answered}", size=34, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
                ft.Text(f"{t['accuracy']}: {accuracy}%", size=16, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
                ft.Divider(color=BORDER),
                ft.Text(f"🔥 {t['streak_confirmed']}: {streak_days_text(displayed_streak(), app_state['lang'])}", size=14, color="#A15C00"),
            ]
            result_actions = [
                ft.ElevatedButton(t["finish"], icon=ft.Icons.CHECK, on_click=return_from_exercise, bgcolor=INDIGO, color="white", height=54),
            ]

        result_view = ft.View(
            route="/results",
            controls=[ft.SafeArea(
                content=ft.Container(
                    content=ft.Column([
                        ft.Container(expand=True),
                        ft.Text(t["results"].upper(), size=12, weight=ft.FontWeight.BOLD, color=MUTED, text_align=ft.TextAlign.CENTER),
                        ft.Text(emoji, size=72, text_align=ft.TextAlign.CENTER),
                        ft.Text(result_title, size=28, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
                        ft.Text(result_hint, size=14, color=MUTED, text_align=ft.TextAlign.CENTER),
                        rounded_card(ft.Column(result_card_controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)),
                        ft.Container(expand=True),
                        *result_actions,
                    ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=16, expand=True),
                    padding=ft.Padding.all(22),
                    expand=True,
                ),
                expand=True,
            )],
            bgcolor=BG,
            padding=0,
            can_pop=True,
        )
        set_session_view(result_view)

    async def open_app_after_welcome():
        await asyncio.sleep(3)
        if user_stats.get("lang"):
            show_main_menu(reset_scroll=True)
        else:
            show_language_selector()

    def show_welcome_screen():
        page.clean()
        page.navigation_bar = None
        page.scroll = None
        page.padding = 0
        page.bgcolor = BG
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.add(ft.SafeArea(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(height=64),
                    ft.Image(
                        src="icon.svg",
                        width=132,
                        height=132,
                        fit=ft.BoxFit.CONTAIN,
                        border_radius=28,
                        anti_alias=True,
                    ),
                    ft.Text("Hoş geldiniz!", size=22, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
                    # ft.Text("Gagauzium", size=28, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Text(
                        "Приветствуем в изучении гагаузского языка",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=INK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Bine ați venit la studiul limbii găgăuze",
                        size=18,
                        color=MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(expand=True),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, expand=True),
                padding=ft.Padding.symmetric(horizontal=28),
                expand=True,
            ),
            expand=True,
        ))
        page.update()
        page.run_task(open_app_after_welcome)

    show_welcome_screen()

if __name__ == "__main__":
    ft.run(main)
