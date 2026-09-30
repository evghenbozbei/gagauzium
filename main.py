import flet as ft
import json
import random
import asyncio
import datetime
import os
import re
from pathlib import Path

from category_metadata import CATEGORY_METADATA, CATEGORIES_BY_SOURCE, category_name as localized_category_name


APP_DIR = Path(__file__).resolve().parent
STORAGE_DIR = Path(os.environ.get("FLET_APP_STORAGE_DATA", APP_DIR))
WORDS_DATA_FILE = APP_DIR / "words_data.json"
USER_STATS_FILE = STORAGE_DIR / "user_stats.json"

# The first two learning batches in the numbers category follow the natural
# counting order instead of the usual random selection: 1-5, then 6-10.
# These IDs are stable vocabulary identifiers from words_data.json.
NUMBER_FOUNDATION_BATCH_IDS = (
    (36, 37, 38, 39, 40),
    (41, 42, 43, 44, 45),
)

# Review exercises only offer word building for entries of reasonable length.
WORD_BUILD_MAX_LETTERS = 12

# --- ПЕРЕВОДЫ ИНТЕРФЕЙСА ---
UI_TEXT = {
    "RU": {
        "reset": "Обнулить категорию",
        "remember": "ЗАПОМНИТЕ СЛОВО",
        "reset_all": "Обнулить весь прогресс",
        "statistics": "📊 Статистика",
        "no_errors": "Ошибок пока нет!",
        "skip": "Не знаю",
        "true_btn": "✅ Правда",
        "false_btn": "❌ Ложь",
        "confirm_yes": "Да, обнулить",
        "confirm_no": "Отмена",
        "confirm_reset_category": "Обнулить категорию «{0}»? Прогресс этой категории будет потерян.",
        "confirm_reset_all": "Обнулить весь прогресс? Будут удалены изученные слова, статистика ответов и серия занятий."
    },
    "RO": {
        "reset": "Resetează categorie",
        "remember": "ȚINE MINTE CUVÂNTUL",
        "reset_all": "Resetează tot progresul",
        "statistics": "📊 Statistici",
        "no_errors": "Nu există încă greșeli!",
        "skip": "Nu știu",
        "true_btn": "✅ Adevărat",
        "false_btn": "❌ Fals",
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
        "ready_review": "20 слов готовы к повторению", "daily_in_progress": "Продолжить: {0} / {1}",
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
        "streak_hint": "Завершите занятие сегодня, чтобы продолжить серию.",
        "learn_title": "Что вы хотите изучить?", "learn_subtitle": "Выберите тему и учитесь в своём темпе.",
        "conversational": "Разговорный", "advanced": "Продвинутый", "expert": "Эксперт",
        "back": "Назад", "learn_new": "Учить новые слова",
        "start_learning": "Начать обучение",
        "difficult_words": "Сложные слова", "review_action": "Повторить",
        "difficult_progress": "Закрепление: {0} из 2", "difficult_resolved": "Слово больше не требует внимания.",
        "category_statistics": "Статистика категории", "view_all_words": "Посмотреть все слова",
        "category_words_title": "Слова категории",
        "review_title": "Повторение", "review_subtitle": "Закрепляйте слова короткими тренировками.",
        "daily_desc": "Подборка слов на сегодня.", "difficult_desc": "Повторите слова, в которых ошибались.",
        "quick_review": "Быстрое повторение", "quick_desc": "На скорость, с тремя жизнями.",
        "regular_review": "Обычное повторение", "regular_review_desc": "Выберите правильный перевод.",
        "quiz": "Тест", "quiz_desc": "Определите, верен ли перевод.",
        "review_mode_locked": "Откроется после изучения первой серии слов",
        "true_false_short": "Да / Нет", "no_difficult": "Пока нет сложных слов",
        "true_false_correct_translation": "А правильный перевод — это:",
        "language": "Язык обучения", "russian": "Русский", "romanian": "Румынский",
        "statistics_hint": "Общий прогресс и слова, которые требуют внимания.", "open_statistics": "Открыть статистику",
        "reset_progress": "Сброс прогресса", "reset_category_label": "Сбросить категорию",
        "select_category": "Выберите категорию", "reset_all_hint": "Будут удалены прогресс, статистика ответов и серия занятий.",
        "all_words_learned": "Все слова изучены",
        "close_session": "Закрыть занятие", "question": "Задание", "continue_answer": "Продолжить",
        "correct_answer": "Правильно!", "incorrect_answer": "Не совсем", "correct_was": "Правильный ответ",
        "results": "Результаты", "accuracy": "Точность",
        "newly_learned": "Новых слов изучено", "streak_confirmed": "Серия подтверждена",
        "result_excellent_title": "Отлично!", "result_excellent_hint": "Эти слова уже хорошо запомнились.",
        "result_good_title": "Хороший результат", "result_good_hint": "Ещё немного практики — и будет совсем уверенно.",
        "result_practice_title": "Продолжаем", "result_practice_hint": "Слова постепенно закрепляются.",
        "result_attention_title": "Всё приходит с практикой", "result_attention_hint": "Этим словам нужно ещё немного внимания.",
        "learning_result_title": "Серия слов пройдена",
        "learning_result_all": "Все слова этой серии добавлены в изученные.",
        "learning_result_retry": "Некоторые слова встретятся снова в следующих занятиях.",
        "milestone_50_title": "Рубеж в 50 слов!",
        "milestone_50_hint": "Поздравляем! Вы преодолели отметку в 50 изученных слов.",
        "milestone_words_total": "Всего слов изучено",
        "fast_result_title": "Ваш результат", "fast_score": "СЧЁТ", "fast_best_score": "Лучший результат",
        "fast_first_score": "Первый результат сохранён", "fast_new_record": "Новый личный рекорд!",
        "fast_record_tied": "Вы повторили свой лучший результат", "fast_to_record": "До личного рекорда — {0}",
        "try_again": "Попробовать снова",
        "finish": "Завершить", "build_word": "Составьте слово на гагаузском",
        "word_building": "Составление слов", "word_building_desc": "Соберите слово из букв. Некоторые могут быть лишними.",
        "matching_pairs": "Найди пары", "matching_pairs_desc": "Соедините слова с правильными переводами.",
        "matching_instruction": "Выберите слово слева и его перевод справа.",
        "matching_pairs_locked": "Откроется после изучения первых 5 слов",
        "mega_review": "Большое повторение", "mega_review_desc": "Смешанная тренировка со всеми видами упражнений.",
        "mega_review_locked": "Откроется после изучения первых 10 слов",
        "check": "Проверить", "backspace": "Удалить", "clear": "Очистить",
        "what_mean": "Что это значит?",
        "previous_word": "Предыдущее слово",
        "next_word": "Следующее слово", "repeat_learned": "Закрепить изученные слова",
        "learning_new_words": "Изучение новых слов",
        "level_one": "Уровень 1", "knowledge_check": "Проверка знаний",
        "stats_subtitle": "Ваш прогресс и слова, в которых вы ошибались.",
        "stats_overall": "Общий прогресс", "answer_accuracy": "Точность ответов",
        "study_streak": "Серия занятий", "hard_words_title": "Слова, требующие внимания",
    },
    "RO": {
        "nav_home": "Acasă", "nav_learn": "Învață", "nav_review": "Repetă",
        "gagauz_language": "Limba găgăuză", "settings": "Setări",
        "your_progress": "PROGRESUL TĂU", "words": "cuvinte", "beginner": "Începător",
        "today": "Astăzi", "daily_review": "Repetare zilnică",
        "ready_review": "20 de cuvinte sunt gata de repetat", "daily_in_progress": "Continuă: {0} / {1}",
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
        "streak_hint": "Finalizează o sesiune astăzi pentru a continua seria.",
        "learn_title": "Ce vrei să înveți?", "learn_subtitle": "Alege o temă și învață în ritmul tău.",
        "conversational": "Conversațional", "advanced": "Avansat", "expert": "Expert",
        "back": "Înapoi", "learn_new": "Învață cuvinte noi",
        "start_learning": "Începe învățarea",
        "difficult_words": "Cuvinte dificile", "review_action": "Repetă",
        "difficult_progress": "Consolidare: {0} din 2", "difficult_resolved": "Cuvântul nu mai necesită atenție.",
        "category_statistics": "Statisticile categoriei", "view_all_words": "Vezi toate cuvintele",
        "category_words_title": "Cuvintele categoriei",
        "review_title": "Repetare", "review_subtitle": "Consolidează vocabularul prin sesiuni scurte.",
        "daily_desc": "Selecția de cuvinte pentru astăzi.", "difficult_desc": "Repetă cuvintele la care ai greșit.",
        "quick_review": "Repetare rapidă", "quick_desc": "Contra cronometru, cu trei vieți.",
        "regular_review": "Repetare obișnuită", "regular_review_desc": "Alege traducerea corectă.",
        "quiz": "Test", "quiz_desc": "Stabilește dacă traducerea este corectă.",
        "review_mode_locked": "Se va deschide după învățarea primei serii de cuvinte",
        "true_false_short": "Da / Nu", "no_difficult": "Nu există încă cuvinte dificile",
        "true_false_correct_translation": "Iar traducerea corectă este:",
        "language": "Limba de învățare", "russian": "Rusă", "romanian": "Română",
        "statistics_hint": "Progresul general și cuvintele care necesită atenție.", "open_statistics": "Deschide statisticile",
        "reset_progress": "Resetarea progresului", "reset_category_label": "Resetează categoria",
        "select_category": "Alege categoria", "reset_all_hint": "Vor fi șterse progresul, statisticile răspunsurilor și seria de studiu.",
        "all_words_learned": "Toate cuvintele sunt învățate",
        "close_session": "Închide sesiunea", "question": "Exercițiu", "continue_answer": "Continuă",
        "correct_answer": "Corect!", "incorrect_answer": "Nu chiar", "correct_was": "Răspunsul corect",
        "results": "Rezultate", "accuracy": "Acuratețe",
        "newly_learned": "Cuvinte noi învățate", "streak_confirmed": "Seria este confirmată",
        "result_excellent_title": "Excelent!", "result_excellent_hint": "Aceste cuvinte sunt deja bine memorate.",
        "result_good_title": "Rezultat bun", "result_good_hint": "Încă puțină practică și vei răspunde cu mai multă încredere.",
        "result_practice_title": "Continuăm", "result_practice_hint": "Cuvintele se fixează treptat.",
        "result_attention_title": "Totul vine prin practică", "result_attention_hint": "Aceste cuvinte mai au nevoie de puțină atenție.",
        "learning_result_title": "Seria de cuvinte este parcursă",
        "learning_result_all": "Toate cuvintele din această serie au fost adăugate la cele învățate.",
        "learning_result_retry": "Unele cuvinte vor apărea din nou în lecțiile următoare.",
        "milestone_50_title": "Pragul de 50 de cuvinte!",
        "milestone_50_hint": "Felicitări! Ai depășit pragul de 50 de cuvinte învățate.",
        "milestone_words_total": "Total cuvinte învățate",
        "fast_result_title": "Rezultatul tău", "fast_score": "SCOR", "fast_best_score": "Cel mai bun rezultat",
        "fast_first_score": "Primul rezultat a fost salvat", "fast_new_record": "Un nou record personal!",
        "fast_record_tied": "Ți-ai egalat cel mai bun rezultat", "fast_to_record": "Până la recordul personal — {0}",
        "try_again": "Încearcă din nou",
        "finish": "Finalizează", "build_word": "Construiește cuvântul găgăuz",
        "word_building": "Construirea cuvintelor", "word_building_desc": "Construiește cuvântul din litere. Unele pot fi în plus.",
        "matching_pairs": "Găsește perechile", "matching_pairs_desc": "Potrivește cuvintele cu traducerile corecte.",
        "matching_instruction": "Alege cuvântul din stânga și traducerea lui din dreapta.",
        "matching_pairs_locked": "Se va deschide după învățarea primelor 5 cuvinte",
        "mega_review": "Recapitulare completă", "mega_review_desc": "Antrenament mixt cu toate tipurile de exerciții.",
        "mega_review_locked": "Se va deschide după învățarea primelor 10 cuvinte",
        "check": "Verifică", "backspace": "Șterge", "clear": "Curăță",
        "what_mean": "Ce înseamnă?",
        "previous_word": "Cuvântul anterior",
        "next_word": "Cuvântul următor", "repeat_learned": "Consolidează cuvintele învățate",
        "learning_new_words": "Învățarea cuvintelor noi",
        "level_one": "Nivelul 1", "knowledge_check": "Verificarea cunoștințelor",
        "stats_subtitle": "Progresul tău și cuvintele la care ai greșit.",
        "stats_overall": "Progres general", "answer_accuracy": "Acuratețea răspunsurilor",
        "study_streak": "Seria de studiu", "hard_words_title": "Cuvinte care necesită atenție",
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


def requires_attention(word_stats):
    return bool(word_stats.get("needs_attention", word_stats.get("wrong_answers", 0) > 0))


def update_word_performance(word_stats, is_correct, mode, today):
    word_stats["last_seen"] = today.isoformat()
    if is_correct:
        word_stats["correct_answers"] = word_stats.get("correct_answers", 0) + 1
        if mode == "difficult" and requires_attention(word_stats):
            streak = max(0, int(word_stats.get("difficult_correct_streak", 0) or 0)) + 1
            word_stats["difficult_correct_streak"] = min(streak, 2)
            if streak >= 2:
                word_stats["needs_attention"] = False
    else:
        word_stats["wrong_answers"] = word_stats.get("wrong_answers", 0) + 1
        word_stats["needs_attention"] = True
        word_stats["difficult_correct_streak"] = 0


def display_letter(char):
    """Uppercase a letter without merging the Gagauz i/İ and ı/I pairs."""
    if char == "i":
        return "İ"
    if char == "ı":
        return "I"
    return char.upper()


def answer_variants(text):
    """Split a dictionary value such as 'büük / büyük' into comparable variants."""
    return {part.strip().casefold() for part in str(text).split("/") if part.strip()}


def word_build_target(word):
    """Return the first variant of an entry, without explanatory parentheses."""
    first_variant = str(word["gag"]).split("/")[0]
    target = re.sub(r"\s*\([^)]*\)", "", first_variant).strip()
    return target or str(word["gag"]).strip()


def answer_letters(value):
    return [char for char in value if char.isalpha()]


def word_build_characters(value):
    """Letters to assemble plus separators that are shown already in place."""
    return [char for char in value if char.isalpha() or char in " -"]


def word_build_letter_count(word):
    return len(answer_letters(word_build_target(word)))


def word_build_hint_positions(template):
    """Return template positions whose letters are shown as hints."""
    letter_positions = [index for index, char in enumerate(template) if char.isalpha()]
    letter_count = len(letter_positions)
    has_separator = any(not char.isalpha() for char in template)
    hint_count = 2 if has_separator or letter_count >= 9 else (1 if letter_count >= 6 else 0)
    if hint_count == 0:
        return []
    if hint_count == 1:
        return [letter_positions[len(letter_positions) // 2]]

    if has_separator:
        segments = []
        segment = []
        for index, char in enumerate(template):
            if not char.isalpha():
                if segment:
                    segments.append(segment)
                segment = []
            else:
                segment.append(index)
        if segment:
            segments.append(segment)
        if len(segments) >= 2:
            first = segments[0][len(segments[0]) // 2]
            second = segments[-1][len(segments[-1]) // 2]
            if abs(first - second) > 1:
                return sorted([first, second])

    interior = letter_positions[1:-1] or letter_positions
    first = interior[len(interior) // 3]
    second = interior[(2 * len(interior)) // 3]
    if abs(first - second) <= 1:
        alternatives = [position for position in interior if abs(position - first) > 1]
        if alternatives:
            second = max(alternatives, key=lambda position: abs(position - first))
    return sorted({first, second})


def native_word_text(word, lang):
    """Return the word's translation in the interface language."""
    return str(word.get(lang.lower(), word.get("ru", "---")))


def valid_answers(word, direction, words, lang):
    """Return every dictionary value that correctly translates the prompt.

    Homonyms (ay = луна / месяц) and shared translations (mare = большой /
    море) make several answers valid for the same prompt. ``forward`` asks
    for the Gagauz word, ``reverse`` for the translation.
    """
    def gagauz(entry):
        return str(entry["gag"])

    def native(entry):
        return native_word_text(entry, lang)

    prompt_of, answer_of = (native, gagauz) if direction == "forward" else (gagauz, native)
    prompt_variants = answer_variants(prompt_of(word))
    acceptable = {answer_of(word)}
    acceptable.update(
        answer_of(entry) for entry in words
        if answer_variants(prompt_of(entry)) & prompt_variants
    )
    return acceptable


def wrong_answers(direction, acceptable, words, lang):
    """Return wrong options that share no variant with a valid answer."""
    acceptable_variants = set().union(*(answer_variants(value) for value in acceptable))
    values = {
        str(entry["gag"]) if direction == "forward" else native_word_text(entry, lang)
        for entry in words
    }
    return sorted(value for value in values if not answer_variants(value) & acceptable_variants)


def entries_are_equivalent(first, second, lang):
    """Whether two entries can be matched with each other's translation."""
    return (
        first["id"] == second["id"]
        or bool(answer_variants(native_word_text(first, lang)) & answer_variants(native_word_text(second, lang)))
        or bool(answer_variants(first["gag"]) & answer_variants(second["gag"]))
    )


def load_data():
    try:
        with WORDS_DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def set_aside_corrupted_stats():
    """Keep an unreadable progress file for inspection instead of crashing."""
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        os.replace(USER_STATS_FILE, USER_STATS_FILE.with_name(f"user_stats.corrupt-{stamp}.json"))
    except OSError:
        pass

def load_stats():
    stats = {}
    try:
        with USER_STATS_FILE.open("r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            stats = loaded
        else:
            set_aside_corrupted_stats()
    except FileNotFoundError:
        pass
    except ValueError:
        # Includes JSONDecodeError and UnicodeDecodeError.
        set_aside_corrupted_stats()
    stats.setdefault("streak_days", 0)
    stats.setdefault("last_login", "")
    stats.setdefault("milestone_50_completed", False)
    stats.setdefault("words", {})
    return stats

def save_stats(stats):
    # Write a complete copy first and swap it in atomically, so an interrupted
    # write never leaves a truncated user_stats.json behind.
    USER_STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = USER_STATS_FILE.with_name(USER_STATS_FILE.name + ".tmp")
    with temp_file.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_file, USER_STATS_FILE)

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


def select_new_learning_batch(words, category, batch_size=6):
    """Choose a new-word batch, preserving the introductory number order."""
    unlearned = [
        word for word in words
        if word["category"] == category and not word["learned"]
    ]

    category_key = CATEGORIES_BY_SOURCE.get(category, {}).get("key")
    if category_key == "numbers":
        unlearned_by_id = {word["id"]: word for word in unlearned}
        for batch_ids in NUMBER_FOUNDATION_BATCH_IDS:
            pending = [
                unlearned_by_id[word_id]
                for word_id in batch_ids
                if word_id in unlearned_by_id
            ]
            if pending:
                return pending

    random.shuffle(unlearned)
    return unlearned[:batch_size]


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


def new_word_stats():
    """Progress record of a word the user has never studied."""
    return {
        "learned": False,
        "correct_answers": 0,
        "wrong_answers": 0,
        "last_seen": "1970-01-01",
        "needs_attention": False,
        "difficult_correct_streak": 0,
    }


def daily_review_length(daily):
    return len(daily.get("word_ids", [])) if daily else 0


def reset_words_progress(stats, word_ids):
    """Forget all progress of the given words, including today's daily review.

    Words already answered in the daily review stay counted; the ones still
    ahead are removed so the reset words do not come back as review.
    """
    for word_id in word_ids:
        stats["words"][str(word_id)] = new_word_stats()
    daily = stats.get("daily_review")
    if daily and daily.get("word_ids"):
        removed = set(word_ids)
        index = daily.get("index", 0)
        answered, upcoming = daily["word_ids"][:index], daily["word_ids"][index:]
        daily["word_ids"] = answered + [word_id for word_id in upcoming if word_id not in removed]


def merge_data_and_stats(all_words, stats):
    needs_save = False
    for w in all_words:
        w_id = str(w["id"])
        if w_id not in stats["words"]:
            # The dictionary contains learning content only. A new user always
            # starts with zero progress; learned state lives in user_stats.json.
            w["learned"] = False
            stats["words"][w_id] = new_word_stats()
            needs_save = True
        else:
            defaults = {
                "learned": False,
                "correct_answers": 0,
                "wrong_answers": 0,
                "last_seen": "1970-01-01",
                "needs_attention": stats["words"][w_id].get("wrong_answers", 0) > 0,
                "difficult_correct_streak": 0,
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
    page.window.width = 390
    page.window.height = 844
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
        "session_mode": "new",
        "current_options": [],
        "option_buttons": {},
        "feedback_text": "",
        "last_word_id": None,
        "last_category": user_stats.get("last_active_category"),
        "learn_scroll_offset": 0.0,
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
        "session_milestone_50": False,
        "learning_batch_viewed": False,
        "learning_matching_started": False,
        "learning_matching_words": [],
        "learning_word_count": 0,
        "learning_extra_count": 0,
        "learning_extra_started": False,
        "learning_extra_stages": [],
        "learning_extra_index": 0,
        "learning_wrong_ids": [],
        "letter_bank": [],
        "selected_letter_indices": [],
        "word_build_template": [],
        "word_build_fixed_positions": {},
        "matching_left_id": None,
        "matching_right_id": None,
        "matching_matched_ids": [],
        "matching_matched_right_ids": [],
        "matching_wrong_pair": None,
        "tf_followup_active": False,
        "tf_followup_options": [],
        "fast_timer_value": 1.0,
        "fast_timer_bar": None,
        "stats": user_stats
    }

    BG = "#F8F7F2"
    SCREEN_BACKGROUNDS = {
        "home": "#EDEEF8",
        "learn": "#EAF2EC",
        "category": "#F4F0EB",
        "review": "#F3EDE8",
        "exercise": "#ECEEF5",
    }
    CATEGORY_STYLES = {
        # Palettes adapted from the supplied design reference.
        "family": {"gradient": ["#DBEAFE", "#F8FAFF", "#E0E7FF"], "border": "#93C5FD", "accent": "#2563EB", "icon_bg": "#BFDBFE"},
        "food": {"gradient": ["#FEF3C7", "#FFFDF5", "#FFEDD5"], "border": "#FCD34D", "accent": "#D97706", "icon_bg": "#FDE68A"},
        "numbers": {"gradient": ["#D1FAE5", "#F8FFFC", "#CCFBF1"], "border": "#6EE7B7", "accent": "#059669", "icon_bg": "#A7F3D0"},
        "time": {"gradient": ["#F3E8FF", "#FFFAFF", "#EDE9FE"], "border": "#C4B5FD", "accent": "#7C3AED", "icon_bg": "#DDD6FE"},
        "animals": {"gradient": ["#FCE7F3", "#FFF9FC", "#FFE4E6"], "border": "#F9A8D4", "accent": "#DB2777", "icon_bg": "#FBCFE8"},
        "nature": {"gradient": ["#CFFAFE", "#F8FDFF", "#E0F2FE"], "border": "#67E8F9", "accent": "#0891B2", "icon_bg": "#A5F3FC"},
        "home": {"gradient": ["#E0E7FF", "#F8FAFF", "#DBEAFE"], "border": "#A5B4FC", "accent": "#4F46E5", "icon_bg": "#C7D2FE"},
        "clothing": {"gradient": ["#CCFBF1", "#F8FFFC", "#D1FAE5"], "border": "#5EEAD4", "accent": "#0F766E", "icon_bg": "#99F6E4"},
        "professions": {"gradient": ["#FFEDD5", "#FFFBF5", "#FEF3C7"], "border": "#FDBA74", "accent": "#EA580C", "icon_bg": "#FED7AA"},
        "city_transport": {"gradient": ["#E0F2FE", "#F8FDFF", "#DBEAFE"], "border": "#7DD3FC", "accent": "#0284C7", "icon_bg": "#BAE6FD"},
        "colors": {"gradient": ["#FAE8FF", "#FFFAFF", "#F3E8FF"], "border": "#E879F9", "accent": "#A21CAF", "icon_bg": "#F5D0FE"},
        "verbs": {"gradient": ["#FEF9C3", "#FFFDF5", "#FEF3C7"], "border": "#FDE047", "accent": "#A16207", "icon_bg": "#FEF08A"},
        "anatomy": {"gradient": ["#ECFCCB", "#FBFFF5", "#D1FAE5"], "border": "#BEF264", "accent": "#4D7C0F", "icon_bg": "#D9F99D"},
        # Matching calm palettes for categories not covered by the reference.
        "pronouns": {"gradient": ["#E0F2FE", "#F8FDFF", "#CFFAFE"], "border": "#7DD3FC", "accent": "#0369A1", "icon_bg": "#BAE6FD"},
        "questions": {"gradient": ["#EDE9FE", "#FFFAFF", "#FCE7F3"], "border": "#C4B5FD", "accent": "#6D28D9", "icon_bg": "#DDD6FE"},
        "basics": {"gradient": ["#E2E8F0", "#FAFCFF", "#DBEAFE"], "border": "#94A3B8", "accent": "#475569", "icon_bg": "#CBD5E1"},
        "adjectives": {"gradient": ["#FFE4E6", "#FFFAF7", "#FFEDD5"], "border": "#FDA4AF", "accent": "#BE123C", "icon_bg": "#FECDD3"},
        "health": {"gradient": ["#FEE2E2", "#FFFAFA", "#CFFAFE"], "border": "#FCA5A5", "accent": "#B91C1C", "icon_bg": "#FECACA"},
        "feelings": {"gradient": ["#FFEDD5", "#FFF9FC", "#FCE7F3"], "border": "#FDBA74", "accent": "#C24175", "icon_bg": "#FBCFE8"},
        "school_science": {"gradient": ["#DBEAFE", "#F8FAFF", "#EDE9FE"], "border": "#A5B4FC", "accent": "#4338CA", "icon_bg": "#C7D2FE"},
        "kitchen": {"gradient": ["#FEF3C7", "#FFFAF7", "#FFE4E6"], "border": "#FCD34D", "accent": "#C2410C", "icon_bg": "#FDE68A"},
        "tools": {"gradient": ["#E7E5E4", "#FFFCFA", "#FFEDD5"], "border": "#A8A29E", "accent": "#9A3412", "icon_bg": "#D6D3D1"},
        "money_trade": {"gradient": ["#D1FAE5", "#FBFFF5", "#FEF9C3"], "border": "#6EE7B7", "accent": "#047857", "icon_bg": "#A7F3D0"},
        "sport_art": {"gradient": ["#FFEDD5", "#FFFAFF", "#F3E8FF"], "border": "#FDBA74", "accent": "#C2410C", "icon_bg": "#FED7AA"},
        "conjunctions": {"gradient": ["#E0E7FF", "#FFFAFF", "#F3E8FF"], "border": "#A5B4FC", "accent": "#5B21B6", "icon_bg": "#C7D2FE"},
    }
    DEFAULT_CATEGORY_STYLE = {
        "gradient": ["#F8FAFC", "#FFFFFF", "#F1F5F9"],
        "border": "#CBD5E1",
        "accent": "#4353C7",
        "icon_bg": "#E2E8F0",
    }
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

    def get_category_style(source_name):
        category_key = get_category_meta(source_name).get("key")
        return CATEGORY_STYLES.get(category_key, DEFAULT_CATEGORY_STYLE)

    def category_words(source_name):
        return [w for w in all_words if w["category"] == source_name]

    def category_counts(source_name):
        words = category_words(source_name)
        learned = sum(1 for w in words if w["learned"])
        difficult = sum(
            1 for w in words
            if w["learned"] and requires_attention(app_state["stats"]["words"].get(str(w["id"]), {}))
        )
        return learned, len(words), difficult

    def category_visual(source_name, size=54):
        meta = get_category_meta(source_name)
        style = get_category_style(source_name)
        return ft.Container(
            content=ft.Text(meta.get("icon", "📚"), size=max(24, int(size * 0.48))),
            width=size, height=size, alignment=ft.Alignment.CENTER,
            bgcolor=style["icon_bg"], border_radius=size / 3,
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

    def clear_navigation_view():
        """Return rendering to the root view before building a regular screen."""
        while len(page.views) > 1:
            page.views.pop()
        page.on_view_pop = None
        app_state["system_back_action"] = None

    def handle_system_back(e):
        """Run the same navigation as the visible screen's Back button."""
        if len(page.views) > 1 and e.view is not None and e.view in page.views:
            page.views.remove(e.view)
        elif len(page.views) > 1:
            page.views.pop()

        back_action = app_state.get("system_back_action")
        app_state["system_back_action"] = None
        page.on_view_pop = None
        if back_action:
            back_action()
        else:
            show_home()

    def present_navigation_view(route, back_action):
        """Make an internal screen respond to Android's system Back gesture."""
        view = ft.View(
            route=route,
            controls=list(page.controls),
            navigation_bar=page.navigation_bar,
            bgcolor=page.bgcolor,
            padding=page.padding,
            scroll=page.scroll,
            vertical_alignment=page.vertical_alignment,
            horizontal_alignment=page.horizontal_alignment,
            spacing=page.spacing,
            can_pop=True,
        )
        page.controls.clear()
        page.navigation_bar = None
        while len(page.views) > 1:
            page.views.pop()
        page.views.append(view)
        app_state["system_back_action"] = back_action
        page.on_view_pop = handle_system_back

    def stage_page_controls(*controls):
        """Build a screen without sending intermediate frames to the client."""
        page.controls.extend(controls)

    def prepare_main_screen(screen, nav_index, add_header=True):
        app_state["question_id"] = -1
        app_state["current_screen"] = screen
        clear_navigation_view()
        page.controls.clear()
        page.scroll = ft.ScrollMode.HIDDEN
        page.bgcolor = SCREEN_BACKGROUNDS.get(screen, BG)
        page.padding = ft.Padding.only(left=16, right=16, top=14, bottom=18)
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        set_bottom_navigation(nav_index)
        if add_header:
            stage_page_controls(ft.SafeArea(
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
        prepare_main_screen("statistics", app_state.get("nav_index", 0))
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        lang = app_state["lang"]
        t = phase_text()

        total_words = len(all_words)
        learned_words = sum(1 for w in all_words if w["learned"])
        percentage = round(learned_words / total_words * 100) if total_words else 0
        word_stats = app_state["stats"]["words"]
        correct_total = sum(s.get("correct_answers", 0) for s in word_stats.values())
        answers_total = correct_total + sum(s.get("wrong_answers", 0) for s in word_stats.values())
        accuracy = f"{round(correct_total / answers_total * 100)}%" if answers_total else "—"
        best_fast = app_state["stats"].get("fast_best_score")

        hard_words = sorted(
            (
                (w, word_stats.get(str(w["id"]), {}).get("wrong_answers", 0))
                for w in all_words
                if w["learned"] and requires_attention(word_stats.get(str(w["id"]), {}))
            ),
            key=lambda item: item[1],
            reverse=True,
        )[:10]

        def stat_tile(icon, value, label):
            return ft.Container(
                content=ft.Column([
                    ft.Text(icon, size=20),
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text(label, size=11, color=MUTED, max_lines=2),
                ], spacing=4),
                padding=14, bgcolor=CARD, border=ft.Border.all(1, BORDER), border_radius=18,
                col=4,
            )

        hard_rows = [
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(native_word_text(w, lang), size=15, weight=ft.FontWeight.BOLD, color=INK),
                        ft.Text(w["gag"], size=13, color=INDIGO, italic=True),
                    ], spacing=2, expand=True),
                    ft.Container(
                        content=ft.Text(f"✕ {errors}", size=12, weight=ft.FontWeight.BOLD, color="#B42318"),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                        bgcolor="#FDECEC", border_radius=10,
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding.symmetric(horizontal=14, vertical=11),
                bgcolor="#FFFFFF", border=ft.Border.all(1, BORDER), border_radius=15,
            )
            for w, errors in hard_words
        ]

        stage_page_controls(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_settings())]),
            ft.Text(UI_TEXT[lang]["statistics"], size=25, weight=ft.FontWeight.BOLD, color=INK),
            ft.Text(t["stats_subtitle"], size=12, color=MUTED),
            rounded_card(ft.Column([
                ft.Row([
                    ft.Text(t["stats_overall"], size=13, weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text(f"{percentage}%", size=13, weight=ft.FontWeight.BOLD, color=INDIGO),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(learned_of_total_text(learned_words, total_words, lang), size=12, color=MUTED),
                ft.ProgressBar(value=learned_words / total_words if total_words else 0, color=INDIGO, bgcolor="#E8EAF2", height=9),
            ], spacing=10), bgcolor="#E9EDFF"),
            ft.ResponsiveRow([
                stat_tile("🎯", accuracy, t["answer_accuracy"]),
                stat_tile("🔥", str(displayed_streak()), t["study_streak"]),
                stat_tile("⚡", str(best_fast) if best_fast is not None else "—", t["fast_best_score"]),
            ], columns=12, spacing=10, run_spacing=10),
            rounded_card(ft.Column([
                ft.Text("⚠️ " + t["hard_words_title"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                *(hard_rows or [ft.Text(UI_TEXT[lang]["no_errors"], size=13, color=MUTED)]),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH), bgcolor="#F7EDEF"),
            ft.Container(height=8),
        )
        present_navigation_view("/statistics", show_settings)
        page.update()

    def show_language_selector():
        clear_navigation_view()
        page.controls.clear()
        page.navigation_bar = None
        page.scroll = None
        page.bgcolor = BG
        page.padding = 0
        stage_page_controls(ft.SafeArea(
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
                    ft.Button(
                        content=ft.Row([ft.Text("🇷🇺", size=24), ft.Text("Русский", size=18, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
                        width=330, height=62, bgcolor=INDIGO, color="white", on_click=lambda _: set_language("RU")
                    ),
                    ft.Container(height=12),
                    ft.Button(
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
            show_home()

    def show_home():
        prepare_main_screen("home", 0)
        t = phase_text()
        learned_count = sum(1 for w in all_words if w["learned"])
        total_count = len(all_words)
        percentage = round(learned_count / total_count * 100) if total_count else 0
        today = datetime.date.today().isoformat()
        daily = app_state["stats"].get("daily_review") or {}
        daily_is_today = daily.get("date") == today
        daily_length = daily_review_length(daily) if daily_is_today else 0
        daily_index = min(daily_length, daily.get("index", 0)) if daily_is_today else 0
        daily_done = daily_is_today and daily_index >= daily_length
        if learned_count < 20:
            daily_status, daily_cta, daily_disabled = t["daily_locked"], t["start_daily"], True
        elif daily_done:
            daily_status, daily_cta, daily_disabled = t["daily_complete"], t["start_daily"], True
        elif daily_index > 0:
            daily_status, daily_cta, daily_disabled = t["daily_in_progress"].format(daily_index, daily_length), t["continue_daily"], False
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
                ft.Text(f"{t['level_one']} · {t['beginner']}", size=11, color="#A9E7DF"),
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
            daily_controls.append(ft.Button(
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
        ), bgcolor="#E9EDFF")

        last_category = app_state["stats"].get("last_active_category")
        actual_categories = {w["category"] for w in all_words}
        if learned_count == 0:
            continue_content = ft.Column([
                ft.Text(t["welcome_learning"], size=18, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
                ft.Text(t["welcome_gagauz"], size=16, weight=ft.FontWeight.W_600, color=INDIGO, text_align=ft.TextAlign.CENTER),
                ft.Container(height=2),
                ft.Text(t["choose_start"], size=14, color=MUTED, text_align=ft.TextAlign.CENTER),
                ft.Button(
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
                ft.Button(
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
                ft.Button(t["choose_category"], icon=ft.Icons.MENU_BOOK, on_click=lambda _: show_learn(), bgcolor=INDIGO, color="white"),
            ], spacing=12)

        streak = displayed_streak()
        streak_card = rounded_card(ft.Row([
            ft.Container(content=ft.Text("🔥", size=24), width=46, height=46, alignment=ft.Alignment.CENTER, bgcolor="#FFF0D9", border_radius=15),
            ft.Column([ft.Text(streak_days_text(streak, app_state["lang"]), size=15, weight=ft.FontWeight.BOLD, color="#8B4513"), ft.Text(t["streak_hint"], size=11, color="#9A633A")], spacing=2, expand=True),
        ], spacing=12), padding=14, bgcolor="#FFF8EC")

        learning_card = rounded_card(continue_content, bgcolor="#EAF4ED")
        if learned_count == 0:
            stage_page_controls(ft.Container(height=4), progress_card, learning_card, daily_card, streak_card, ft.Container(height=8))
        else:
            stage_page_controls(ft.Container(height=4), progress_card, daily_card, learning_card, streak_card, ft.Container(height=8))
        page.update()


    def remember_learn_scroll(e):
        app_state["learn_scroll_offset"] = max(0.0, float(e.pixels))

    async def restore_learn_scroll(category_grid, offset):
        await asyncio.sleep(0)
        if app_state.get("current_screen") == "learn" and offset > 0:
            await category_grid.scroll_to(offset=offset, duration=0)

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
            style = get_category_style(source_name)
            learned, total, _ = category_counts(source_name)
            percent = round(learned / total * 100) if total else 0
            subtitle = meta.get("gag") or ""
            cards.append(ft.Container(
                content=ft.Column([
                    ft.Row([category_visual(source_name, 48), ft.Container(content=ft.Text(f"{percent}%", size=10, weight=ft.FontWeight.BOLD, color=style["accent"]), padding=ft.Padding.symmetric(horizontal=7, vertical=3), bgcolor=style["icon_bg"], border=ft.Border.all(1, style["border"]), border_radius=10, visible=percent > 0)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(localized_category_name(source_name, app_state["lang"]), size=14, weight=ft.FontWeight.BOLD, color=INK, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(subtitle, size=10, color=style["accent"], visible=bool(subtitle)),
                    ft.Container(expand=True),
                    ft.Text(f"{learned} / {total}", size=11, color=MUTED),
                    ft.ProgressBar(value=learned / total if total else 0, color=style["accent"], bgcolor=style["icon_bg"], height=6),
                ], spacing=5),
                padding=12,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=style["gradient"],
                ),
                border=ft.Border.all(1, style["border"]), border_radius=19,
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
            build_controls_on_demand=False,
            on_scroll=remember_learn_scroll,
            scroll_interval=50,
            expand=True,
        )
        saved_scroll_offset = app_state.get("learn_scroll_offset", 0.0)
        stage_page_controls(ft.SafeArea(
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
        present_navigation_view("/learn", show_home)
        page.update()
        if saved_scroll_offset > 0:
            page.run_task(restore_learn_scroll, category_grid, saved_scroll_offset)

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
        stage_page_controls(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_learn())], spacing=5),
            rounded_card(ft.Column([
                ft.Row([category_visual(source_name, 82), ft.Column([ft.Text(localized_category_name(source_name, app_state["lang"]), size=24, weight=ft.FontWeight.BOLD, color=INK), ft.Text(meta.get("gag") or "", size=14, color=INDIGO)], spacing=3, expand=True)], spacing=15),
                ft.Row([ft.Text(learned_of_total_text(learned, total, app_state["lang"]), size=12, weight=ft.FontWeight.BOLD, color=INK), ft.Text(f"{round(learned / total * 100) if total else 0}%", size=12, weight=ft.FontWeight.BOLD, color=INDIGO)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=learned / total if total else 0, color=INDIGO, bgcolor="#E8EAF2", height=9),
            ], spacing=12), bgcolor="#E9EDFF"),
            rounded_card(ft.Column([
                ft.Text("✨ " + t["learn_new"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(remaining_word_count_text(remaining, app_state["lang"]), size=12, color=MUTED),
                ft.Button(t["start_learning"] if remaining else t["all_words_learned"], icon=ft.Icons.PLAY_ARROW, on_click=lambda _: start_session(source_name, "new"), disabled=remaining == 0, bgcolor=INDIGO, color="white"),
            ], spacing=9, horizontal_alignment=ft.CrossAxisAlignment.STRETCH), bgcolor="#EAF4ED"),
            rounded_card(ft.Column([
                ft.Text("⚠️ " + t["difficult_words"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(attention_word_count_text(difficult, app_state["lang"]) if difficult else t["no_difficult"], size=12, color=MUTED),
                ft.Button(t["review_action"], icon=ft.Icons.REPLAY, on_click=lambda _: start_session(source_name, "difficult"), disabled=difficult == 0, opacity=0.48 if difficult == 0 else 1.0, bgcolor="#D34A5B", color="white"),
            ], spacing=9, horizontal_alignment=ft.CrossAxisAlignment.STRETCH), bgcolor="#F7EDEF"),
            rounded_card(ft.Column([
                ft.Text("📊 " + t["category_statistics"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(learned_of_total_text(learned, total, app_state["lang"]), size=12, color=MUTED),
                ft.Button(t["view_all_words"], icon=ft.Icons.LIST_ALT, on_click=lambda _: show_word_list(source_name), bgcolor="#16847A", color="white"),
            ], spacing=9, horizontal_alignment=ft.CrossAxisAlignment.STRETCH), bgcolor="#E8F4F2"),
            ft.Container(height=8),
        )
        present_navigation_view("/category", show_learn)
        page.update()

    def show_review_hub():
        prepare_main_screen("review", 2)
        t = phase_text()
        learned_count = sum(1 for w in all_words if w["learned"])
        difficult_count = sum(1 for w in all_words if w["learned"] and requires_attention(app_state["stats"]["words"].get(str(w["id"]), {})))
        today = datetime.date.today().isoformat()
        daily = app_state["stats"].get("daily_review") or {}
        daily_done = daily.get("date") == today and daily.get("index", 0) >= daily_review_length(daily)
        basic_review_locked = learned_count < 4
        basic_review_status = t["review_mode_locked"] if basic_review_locked else None
        matching_locked = len(matching_candidates()) < 5
        matching_status = t["matching_pairs_locked"] if matching_locked else None
        mega_review_locked = len(matching_candidates()) < 10
        mega_review_status = t["mega_review_locked"] if mega_review_locked else None

        review_styles = {
            "daily": {"gradient": ["#E0E7FF", "#F8FAFF", "#EDE9FE"], "border": "#A5B4FC", "accent": "#4F46E5", "icon_bg": "#C7D2FE"},
            "difficult": {"gradient": ["#FFE4E6", "#FFFAF7", "#FFEDD5"], "border": "#FDA4AF", "accent": "#BE123C", "icon_bg": "#FECDD3"},
            "regular": {"gradient": ["#D1FAE5", "#F8FFFC", "#CCFBF1"], "border": "#6EE7B7", "accent": "#047857", "icon_bg": "#A7F3D0"},
            "fast": {"gradient": ["#F3E8FF", "#FFFAFF", "#FAE8FF"], "border": "#D8B4FE", "accent": "#7E22CE", "icon_bg": "#E9D5FF"},
            "word_building": {"gradient": ["#FEF3C7", "#FFFDF5", "#FEF9C3"], "border": "#FCD34D", "accent": "#B45309", "icon_bg": "#FDE68A"},
            "true_false": {"gradient": ["#E0F2FE", "#F8FDFF", "#CFFAFE"], "border": "#7DD3FC", "accent": "#0369A1", "icon_bg": "#BAE6FD"},
            "matching": {"gradient": ["#FCE7F3", "#FFF9FC", "#F3E8FF"], "border": "#F9A8D4", "accent": "#BE185D", "icon_bg": "#FBCFE8"},
            "mega": {"gradient": ["#FFEDD5", "#FFFBF5", "#FEF3C7"], "border": "#FDBA74", "accent": "#C2410C", "icon_bg": "#FED7AA"},
        }

        def review_card(icon, title, description, badge, action, style, disabled=False, completed=False, height=270):
            state_icon = ft.Icons.CHECK_CIRCLE_OUTLINE if completed else (ft.Icons.LOCK_OUTLINE if disabled else None)
            state_color = "#16847A" if completed else ("#98A2B3" if disabled else style["accent"])
            visual_bgcolor = "#DFF4E7" if completed else style["icon_bg"]
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
            card = rounded_card(ft.Column(card_controls, spacing=10, expand=True), bgcolor=None)
            card.gradient = ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=style["gradient"],
            )
            card.border = ft.Border.all(1, style["border"])
            card.col = 6
            card.height = height
            card.on_click = None if disabled else action
            card.ink = not disabled
            card.ink_color = "#16212A5D"
            card.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
            card.opacity = 0.72 if disabled and not completed else 1.0
            card.tooltip = title
            return card

        exercise_cards = [
            review_card("✨", t["daily_review"], t["daily_desc"], t["daily_complete"] if daily_done else (t["ready_review"] if learned_count >= 20 else t["daily_locked"]), lambda _: start_session("ALL", "daily"), review_styles["daily"], learned_count < 20 or daily_done, completed=daily_done, height=290),
            review_card("⚠️", t["difficult_words"], t["difficult_desc"], attention_word_count_text(difficult_count, app_state["lang"]) if difficult_count else t["no_difficult"], lambda _: start_session("ALL", "difficult"), review_styles["difficult"], difficult_count == 0, height=290),
            review_card("🔁", t["regular_review"], t["regular_review_desc"], basic_review_status, lambda _: start_session("ALL", "review"), review_styles["regular"], basic_review_locked),
            review_card("⚡", t["quick_review"], t["quick_desc"], basic_review_status, lambda _: start_session("ALL", "fast"), review_styles["fast"], basic_review_locked),
            review_card("🔤", t["word_building"], t["word_building_desc"], basic_review_status, lambda _: start_session("ALL", "word_building"), review_styles["word_building"], basic_review_locked),
            review_card("❓", t["true_false_short"], t["quiz_desc"], basic_review_status, lambda _: start_session("ALL", "true_false"), review_styles["true_false"], basic_review_locked),
            review_card("🧩", t["matching_pairs"], t["matching_pairs_desc"], matching_status, lambda _: start_session("ALL", "matching"), review_styles["matching"], matching_locked),
            review_card("🌟", t["mega_review"], t["mega_review_desc"], mega_review_status, lambda _: start_session("ALL", "mega"), review_styles["mega"], mega_review_locked),
        ]
        stage_page_controls(
            ft.Container(height=4), ft.Text(t["review_title"], size=24, weight=ft.FontWeight.BOLD, color=INK), ft.Text(t["review_subtitle"], size=12, color=MUTED),
            ft.ResponsiveRow(exercise_cards, columns=12, spacing=11, run_spacing=11),
            ft.Container(height=8),
        )
        present_navigation_view("/review", show_home)
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
        stage_page_controls(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_home()), ft.Container(expand=True)]),
            ft.Text(t["settings"], size=25, weight=ft.FontWeight.BOLD, color=INK),
            rounded_card(ft.Column([
                ft.Text(t["language"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Row([
                    ft.Button("🇷🇺 " + t["russian"], on_click=lambda _: set_language("RU", "settings"), bgcolor=INDIGO if app_state["lang"] == "RU" else "#EEEFF4", color="white" if app_state["lang"] == "RU" else INK, expand=True),
                    ft.Button("🇷🇴 " + t["romanian"], on_click=lambda _: set_language("RO", "settings"), bgcolor=INDIGO if app_state["lang"] == "RO" else "#EEEFF4", color="white" if app_state["lang"] == "RO" else INK, expand=True),
                ], spacing=8),
            ], spacing=12)),
            rounded_card(ft.Column([
                ft.Text(UI_TEXT[app_state["lang"]]["statistics"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(t["statistics_hint"], size=12, color=MUTED),
                ft.Button(t["open_statistics"], icon=ft.Icons.QUERY_STATS, on_click=lambda _: show_statistics(), bgcolor=INDIGO, color="white"),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)),
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
        present_navigation_view("/settings", show_home)
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
                ft.Button(txt["confirm_yes"], on_click=confirm, bgcolor="red", color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        page.show_dialog(dlg)

    def reset_category(category_name):
        txt = UI_TEXT[app_state["lang"]]
        cat_display = localized_category_name(category_name, app_state["lang"])

        def do_reset():
            category_word_ids = []
            for w in all_words:
                if w["category"] == category_name:
                    w["learned"] = False
                    category_word_ids.append(w["id"])
            reset_words_progress(app_state["stats"], category_word_ids)
            save_stats(app_state["stats"])
            show_home()

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
                fresh_word_stats[str(w["id"])] = new_word_stats()
            app_state["stats"].clear()
            app_state["stats"].update({
                "lang": app_state["lang"],
                "streak_days": 0,
                "last_login": "",
                "milestone_50_completed": False,
                "words": fresh_word_stats,
            })
            app_state["last_category"] = None
            save_stats(app_state["stats"])
            show_home()

        show_confirm_dialog(
            title=txt["reset_all"],
            message=txt["confirm_reset_all"],
            on_confirm=do_reset,
        )

    def show_word_list(category):
        persist_last_category(category)
        prepare_main_screen("category_words", 1)
        page.scroll = None
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        lang = app_state["lang"]
        t = phase_text()
        words = [w for w in all_words if w["category"] == category]
        cat_display = localized_category_name(category, lang)
        learned = sum(1 for w in words if w["learned"])
        total = len(words)
        percentage = round(learned / total * 100) if total else 0

        rows = []
        for w in words:
            native_word = w.get(lang.lower(), w.get("ru", "---"))
            is_learned = w["learned"]
            rows.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(native_word, size=16, weight=ft.FontWeight.BOLD, color=INK),
                            ft.Text(w["gag"], size=14, color=INDIGO, italic=True),
                        ], spacing=2, expand=True),
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE if is_learned else ft.Icons.RADIO_BUTTON_UNCHECKED,
                            size=25,
                            color="#16847A" if is_learned else "#B3BAC5",
                        ),
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding.symmetric(horizontal=15, vertical=13),
                    bgcolor="#F5FBF8" if is_learned else CARD,
                    border=ft.Border.all(1, "#B9E0D5" if is_learned else BORDER),
                    border_radius=17,
                )
            )

        list_view = ft.ListView(
            controls=rows,
            expand=True,
            spacing=8,
            padding=ft.Padding.only(bottom=10),
            scroll=ft.ScrollMode.HIDDEN,
        )

        stage_page_controls(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_category_detail(category))]),
            ft.Text(t["category_words_title"], size=24, weight=ft.FontWeight.BOLD, color=INK),
            ft.Text(cat_display, size=14, color=MUTED),
            rounded_card(ft.Column([
                ft.Row([
                    ft.Text(learned_of_total_text(learned, total, lang), size=13, weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text(f"{percentage}%", size=13, weight=ft.FontWeight.BOLD, color=INDIGO),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=learned / total if total else 0, color="#16847A", bgcolor="#E8EAF2", height=9),
            ], spacing=10), padding=15),
            list_view,
        )
        present_navigation_view("/category/words", lambda: show_category_detail(category))
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
        if app_state.get("session_mode") == "new" and app_state.get("is_quiz", False):
            word_count = len(app_state["current_batch"])
            total = word_count + app_state.get("learning_extra_count", 0) + 1
            if app_state.get("learning_matching_started", False):
                current = total
            elif app_state.get("learning_extra_started", False):
                current = word_count + app_state.get("learning_extra_index", 0) + 1
            else:
                current = app_state["index"] + 1
        else:
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
            bgcolor=SCREEN_BACKGROUNDS["exercise"],
            padding=0,
            can_pop=True,
        )

    def native_text(word):
        return native_word_text(word, app_state["lang"])

    def acceptable_answers(word, direction):
        return valid_answers(word, direction, all_words, app_state["lang"])

    def answer_distractors(direction, acceptable):
        return wrong_answers(direction, acceptable, all_words, app_state["lang"])

    def words_are_equivalent(first, second):
        return entries_are_equivalent(first, second, app_state["lang"])

    def matching_candidates():
        """Return learned words with unambiguous labels in both columns."""
        candidates = []
        seen_native = set()
        seen_gagauz = set()
        lang_key = app_state["lang"].lower()
        for word in all_words:
            if not word["learned"]:
                continue
            native = str(word.get(lang_key, word.get("ru", "---"))).strip()
            gagauz = str(word.get("gag", "")).strip()
            native_key = native.casefold()
            gagauz_key = gagauz.casefold()
            if not native or not gagauz or native_key in seen_native or gagauz_key in seen_gagauz:
                continue
            candidates.append(word)
            seen_native.add(native_key)
            seen_gagauz.add(gagauz_key)
        return candidates

    def build_mega_review_stages(today):
        """Build a mixed session while avoiding repeated words when possible."""
        candidates = matching_candidates()
        if len(candidates) < 10:
            return []
        selected = weighted_sample(candidates, app_state["stats"], today, k=min(19, len(candidates)))
        matching_words = selected[:10]
        simple_words = list(selected[10:])

        refill_pool = list(candidates)
        random.shuffle(refill_pool)
        while len(simple_words) < 9:
            if not refill_pool:
                refill_pool = list(candidates)
                random.shuffle(refill_pool)
            simple_words.append(refill_pool.pop())

        # Word building gets words of reasonable length; if there are too few,
        # the remaining slots become regular questions.
        simple_words = simple_words[:9]
        build_positions = [
            index for index, word in enumerate(simple_words)
            if word_build_letter_count(word) <= WORD_BUILD_MAX_LETTERS
        ][:3]
        build_words = [simple_words[index] for index in build_positions]
        other_words = [word for index, word in enumerate(simple_words) if index not in build_positions]
        other_modes = ["review"] * (6 - len(build_words)) + ["true_false"] * 3
        random.shuffle(other_modes)
        stages = [{"mode": "word_building", "word": word} for word in build_words]
        stages.extend(
            {"mode": mode, "word": word}
            for mode, word in zip(other_modes, other_words)
        )
        stages.extend([
            {"mode": "matching", "words": matching_words[:5]},
            {"mode": "matching", "words": matching_words[5:10]},
        ])

        for _ in range(12):
            random.shuffle(stages)
            if all(stages[index]["mode"] != stages[index + 1]["mode"] for index in range(len(stages) - 1)):
                break
        return stages

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
        app_state["session_mode"] = mode
        app_state["last_word_id"] = None
        app_state["session_completion_recorded"] = False
        app_state["feedback_active"] = False
        app_state["feedback_correct"] = False
        app_state["selected_answer"] = None
        app_state["session_correct"] = 0
        app_state["session_answered"] = 0
        app_state["session_new_learned"] = 0
        app_state["session_milestone_50"] = False
        app_state["learning_batch_viewed"] = False
        app_state["learning_matching_started"] = False
        app_state["learning_matching_words"] = []
        app_state["learning_word_count"] = 0
        app_state["learning_extra_count"] = 0
        app_state["learning_extra_started"] = False
        app_state["learning_extra_stages"] = []
        app_state["learning_extra_index"] = 0
        app_state["learning_wrong_ids"] = []
        app_state["selected_letter_indices"] = []
        app_state["word_build_template"] = []
        app_state["word_build_fixed_positions"] = {}
        app_state["matching_left_id"] = None
        app_state["matching_right_id"] = None
        app_state["matching_matched_ids"] = []
        app_state["matching_matched_right_ids"] = []
        app_state["matching_wrong_pair"] = None
        app_state["tf_followup_active"] = False
        app_state["tf_followup_options"] = []
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
                and requires_attention(app_state["stats"]["words"].get(str(w["id"]), {}))
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
            buildable = [w for w in words if word_build_letter_count(w) <= WORD_BUILD_MAX_LETTERS]
            app_state["is_quiz"] = True
            app_state["current_batch"] = weighted_sample(buildable or words, app_state["stats"], today, k=10)
            app_state["index"] = 0
        elif mode == "mega":
            app_state["is_quiz"] = True
            app_state["score"] = 0
            app_state["current_batch"] = build_mega_review_stages(today)
            app_state["index"] = 0
        elif mode == "matching":
            words = matching_candidates()
            usable_count = min(len(words), 20)
            usable_count -= usable_count % 5
            selected_words = weighted_sample(words, app_state["stats"], today, k=usable_count)
            app_state["is_quiz"] = True
            app_state["current_batch"] = [
                selected_words[index:index + 5]
                for index in range(0, len(selected_words), 5)
            ]
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
            app_state["is_quiz"] = False
            app_state["current_batch"] = select_new_learning_batch(all_words, category)
            app_state["learning_matching_words"] = list(app_state["current_batch"])
            app_state["learning_word_count"] = len(app_state["current_batch"])
            app_state["learning_extra_count"] = min(3, (len(app_state["current_batch"]) + 1) // 2)
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
            bottom = ft.Button(
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

    def build_learning_extra_stages():
        words = list(app_state.get("learning_matching_words", []))
        count = app_state.get("learning_extra_count", 0)
        if not words or count <= 0:
            return []

        wrong_ids = set(app_state.get("learning_wrong_ids", []))
        stage_modes = ["true_false"]
        if count >= 2:
            stage_modes.append("word_building")
        if count >= 3:
            stage_modes.append("true_false")

        stages = []
        used_ids = set()
        if "word_building" in stage_modes:
            suitable = [word for word in words if len(answer_letters(word_build_target(word))) <= 10]
            build_pool = suitable or words
            preferred = [word for word in build_pool if word["id"] in wrong_ids]
            build_word = min(preferred or build_pool, key=lambda word: len(answer_letters(word_build_target(word))))
            stages.append({"mode": "word_building", "word": build_word})
            used_ids.add(build_word["id"])

        true_false_count = stage_modes.count("true_false")
        for _ in range(true_false_count):
            unused = [word for word in words if word["id"] not in used_ids]
            preferred = [word for word in unused if word["id"] in wrong_ids]
            pool = preferred or unused or words
            selected_word = random.choice(pool)
            stages.append({"mode": "true_false", "word": selected_word})
            used_ids.add(selected_word["id"])

        random.shuffle(stages)
        return stages

    def prepare_question(word):
        lang = app_state["lang"]
        mode = app_state["mode"]
        if mode == "word_building":
            target = word_build_target(word)
            template = word_build_characters(target)
            fixed_positions = {
                index: char
                for index, char in enumerate(template)
                if not char.isalpha()
            }
            for index in word_build_hint_positions(template):
                fixed_positions[index] = template[index]
            letters = [
                char
                for index, char in enumerate(template)
                if char.isalpha() and index not in fixed_positions
            ]
            answer_letter_count = sum(char.isalpha() for char in template)
            extra_count = 2 if answer_letter_count < 6 else 3
            target_letter_keys = {char.casefold() for char in template if char.isalpha()}
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
            app_state["correct_answer"] = "".join(template)
            app_state["acceptable_answers"] = {app_state["correct_answer"].casefold()}
            app_state["letter_bank"] = letters
            app_state["selected_letter_indices"] = []
            app_state["word_build_template"] = template
            app_state["word_build_fixed_positions"] = fixed_positions
        else:
            direction = "forward" if mode == "new" else random.choice(["forward", "reverse"])
            app_state["direction"] = direction
            if direction == "forward":
                prompt_word = native_text(word)
                correct = word["gag"]
            else:
                prompt_word = word["gag"]
                correct = native_text(word)
            acceptable = acceptable_answers(word, direction)
            others = answer_distractors(direction, acceptable)
            app_state["prompt_word"] = prompt_word
            app_state["correct_answer"] = correct
            app_state["acceptable_answers"] = {value.casefold() for value in acceptable}
            if mode == "true_false":
                is_truth = random.choice([True, False]) if others else True
                app_state["tf_displayed"] = correct if is_truth else random.choice(others)
                app_state["tf_is_truth"] = is_truth
            else:
                distractors = random.sample(others, min(len(others), 3))
                app_state["current_options"] = distractors + [correct]
                random.shuffle(app_state["current_options"])
        app_state["last_word_id"] = word["id"]
        app_state["feedback_active"] = False
        app_state["selected_answer"] = None
        app_state["tf_followup_active"] = False
        app_state["tf_followup_options"] = []
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
        if app_state["mode"] == "difficult" and correct:
            word_stats = app_state["stats"]["words"].get(str(word["id"]), {})
            if requires_attention(word_stats):
                feedback_controls.append(ft.Text(
                    t["difficult_progress"].format(word_stats.get("difficult_correct_streak", 0)),
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color="#157347",
                ))
            else:
                feedback_controls.append(ft.Text(
                    t["difficult_resolved"],
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color="#157347",
                ))
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
            buttons.append(ft.Button(
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
        if app_state.get("tf_followup_active", False):
            option_cards = []
            for option in app_state["tf_followup_options"]:
                bgcolor, color, border_color = "#FFFFFF", INK, BORDER
                if app_state["feedback_active"]:
                    if option == app_state["correct_answer"]:
                        bgcolor, color, border_color = "#EAF8EF", "#157347", "#91D5A8"
                    elif option == app_state["selected_answer"]:
                        bgcolor, color, border_color = "#FDECEC", "#B42318", "#F3B7B7"
                option_cards.append(ft.Button(
                    content=ft.Container(
                        content=ft.Text(
                            option,
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=3,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        alignment=ft.Alignment.CENTER,
                    ),
                    height=132,
                    bgcolor=bgcolor,
                    elevation=0,
                    style=ft.ButtonStyle(
                        padding=ft.Padding.symmetric(horizontal=10, vertical=10),
                        side=ft.BorderSide(1, border_color),
                        shape=ft.RoundedRectangleBorder(radius=18),
                    ),
                    on_click=None if app_state["feedback_active"] else lambda _, answer=option: submit_answer(answer, word),
                ))
            return ft.Column([
                ft.Container(height=18),
                ft.Text(app_state["prompt_word"], size=34, weight=ft.FontWeight.BOLD, color=INK, text_align=ft.TextAlign.CENTER),
                ft.Text(app_state["tf_displayed"], size=27, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text(phase_text()["true_false_correct_translation"], size=16, weight=ft.FontWeight.W_600, color=INK, text_align=ft.TextAlign.CENTER),
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=card, expand=True)
                                for card in option_cards
                            ], spacing=12),
                            height=132,
                        ),
                    ], spacing=14, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                    padding=ft.Padding.only(bottom=14),
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, expand=True)

        buttons = []
        for value, label in ((True, txt["true_btn"]), (False, txt["false_btn"])):
            bgcolor = "#FFFFFF"
            color = INK
            if app_state["feedback_active"]:
                if value == app_state["tf_is_truth"]:
                    bgcolor, color = "#198754", "white"
                elif value == app_state["selected_answer"]:
                    bgcolor, color = "#D9363E", "white"
            buttons.append(ft.Button(
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
        selected_letters = [app_state["letter_bank"][index] for index in selected]
        template = app_state["word_build_template"]
        fixed_positions = app_state["word_build_fixed_positions"]
        built_chars = []
        display_chars = []
        selected_index = 0
        for position in range(len(template)):
            if position in fixed_positions:
                char = fixed_positions[position]
            elif selected_index < len(selected_letters):
                char = selected_letters[selected_index]
                selected_index += 1
            else:
                char = None
            if char is not None:
                built_chars.append(char)
                display_chars.append(display_letter(char))
            else:
                display_chars.append("_")
        built = "".join(built_chars)
        display = " ".join(display_chars)
        required_letter_count = sum(
            char.isalpha() and position not in fixed_positions
            for position, char in enumerate(template)
        )
        answer_complete = len(selected) == required_letter_count
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
            bank.append(ft.Button(
                content=ft.Container(
                    content=ft.Text(display_letter(letter), text_align=ft.TextAlign.CENTER),
                    alignment=ft.Alignment.CENTER,
                ),
                width=48, height=48,
                disabled=index in selected or answer_complete or app_state["feedback_active"],
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
            ft.Button(
                t["check"],
                icon=ft.Icons.CHECK,
                on_click=lambda _: submit_answer(built, word),
                disabled=not answer_complete,
                visible=not app_state["feedback_active"],
                bgcolor=INDIGO,
                color="white",
                height=50,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)

    def matching_button(word, side):
        lang_key = app_state["lang"].lower()
        word_id = word["id"]
        matched = word_id in app_state["matching_matched_ids" if side == "left" else "matching_matched_right_ids"]
        selected_id = app_state["matching_left_id"] if side == "left" else app_state["matching_right_id"]
        wrong_pair = app_state.get("matching_wrong_pair")
        is_wrong = bool(wrong_pair and word_id == wrong_pair[0 if side == "left" else 1])
        is_selected = word_id == selected_id

        if matched:
            return ft.Container(height=66)
        if is_wrong:
            bgcolor, color, border_color = "#FDECEC", "#B42318", "#F3B7B7"
        elif is_selected:
            bgcolor, color, border_color = "#EEF2FF", INDIGO, "#AAB8FF"
        else:
            bgcolor, color, border_color = "#FFFFFF", INK, BORDER

        label = word.get(lang_key, word.get("ru", "---")) if side == "left" else word["gag"]
        return ft.Button(
            content=ft.Container(
                content=ft.Text(
                    str(label),
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=color,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                alignment=ft.Alignment.CENTER,
            ),
            height=66,
            bgcolor=bgcolor,
            elevation=0,
            style=ft.ButtonStyle(
                padding=ft.Padding.symmetric(horizontal=8, vertical=6),
                side=ft.BorderSide(1, border_color),
                shape=ft.RoundedRectangleBorder(radius=14),
            ),
            on_click=lambda _, wid=word_id, column=side: select_matching_word(column, wid),
        )

    def current_matching_words():
        if app_state.get("session_mode") == "new" and app_state.get("learning_matching_started", False):
            return app_state["learning_matching_words"]
        if app_state.get("session_mode") == "mega":
            return app_state["current_batch"][app_state["index"]]["words"]
        return app_state["current_batch"][app_state["index"]]

    def show_matching_round():
        learning_final = (
            app_state.get("session_mode") == "new"
            and app_state.get("learning_matching_started", False)
        )
        if not learning_final and app_state["index"] >= len(app_state["current_batch"]):
            show_results()
            return
        t = phase_text()
        words = current_matching_words()
        right_words = list(words)
        random_state = random.Random(f"{app_state['index']}:{','.join(str(w['id']) for w in words)}")
        for _ in range(8):
            random_state.shuffle(right_words)
            if all(left["id"] != right["id"] for left, right in zip(words, right_words)):
                break
        else:
            right_words = words[1:] + words[:1]
        round_complete = len(app_state["matching_matched_ids"]) == len(words)
        if round_complete:
            continue_matching_round()
            return

        status = None
        if app_state.get("matching_wrong_pair"):
            status = ft.Text("✕ " + t["incorrect_answer"], size=15, weight=ft.FontWeight.BOLD, color="#B42318", text_align=ft.TextAlign.CENTER)

        body_controls = [
            ft.Container(height=4),
            ft.Text(t["matching_instruction"], size=13, color=MUTED, text_align=ft.TextAlign.CENTER),
        ]
        if status is not None:
            body_controls.append(status)
        body_controls.append(ft.Row([
            ft.Column([matching_button(word, "left") for word in words], spacing=10, expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            ft.Column([matching_button(word, "right") for word in right_words], spacing=10, expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START, expand=True))

        set_session_view(exercise_shell(ft.Column(body_controls, spacing=14, expand=True), None, t["matching_pairs"]))

    def select_matching_word(side, word_id):
        if word_id in app_state["matching_matched_ids" if side == "left" else "matching_matched_right_ids"]:
            return
        app_state["matching_wrong_pair"] = None
        app_state[f"matching_{side}_id"] = word_id
        left_id = app_state["matching_left_id"]
        right_id = app_state["matching_right_id"]
        if left_id is not None and right_id is not None:
            # A round can hold homonyms (внук / внучка = unuka / torun), so a
            # pair counts when the labels match, not only when the IDs do.
            words_by_id = {word["id"]: word for word in current_matching_words()}
            is_correct = words_are_equivalent(words_by_id[left_id], words_by_id[right_id])
            word_stats = app_state["stats"]["words"][str(left_id)]
            update_word_performance(word_stats, is_correct, "matching", datetime.date.today())
            app_state["session_answered"] += 1
            if is_correct:
                app_state["session_correct"] += 1
                app_state["matching_matched_ids"].append(left_id)
                app_state["matching_matched_right_ids"].append(right_id)
            else:
                app_state["matching_wrong_pair"] = (left_id, right_id)
            app_state["matching_left_id"] = None
            app_state["matching_right_id"] = None
            save_stats(app_state["stats"])
        show_matching_round()

    def continue_matching_round():
        app_state["matching_left_id"] = None
        app_state["matching_right_id"] = None
        app_state["matching_matched_ids"] = []
        app_state["matching_matched_right_ids"] = []
        app_state["matching_wrong_pair"] = None
        app_state["last_word_id"] = None
        if app_state.get("session_mode") == "new" and app_state.get("learning_matching_started", False):
            show_results()
            return
        app_state["index"] += 1
        show_quiz_card()

    def show_quiz_card():
        session_mode = app_state.get("session_mode", app_state["mode"])
        batch_complete = app_state["index"] >= len(app_state["current_batch"])
        learning_extra_active = False
        if batch_complete and session_mode == "new":
            if not app_state.get("learning_extra_started", False):
                app_state["learning_extra_stages"] = build_learning_extra_stages()
                app_state["learning_extra_started"] = True
                app_state["learning_extra_index"] = 0
            learning_extra_active = app_state["learning_extra_index"] < len(app_state["learning_extra_stages"])
            if not learning_extra_active and not app_state.get("learning_matching_started", False):
                app_state["learning_matching_started"] = True
                app_state["mode"] = "matching"
                app_state["matching_left_id"] = None
                app_state["matching_right_id"] = None
                app_state["matching_matched_ids"] = []
                app_state["matching_matched_right_ids"] = []
                app_state["matching_wrong_pair"] = None
                show_matching_round()
                return
        if (batch_complete and not learning_extra_active) or (
            session_mode == "fast"
            and app_state.get("lives", 0) <= 0
            and not app_state["feedback_active"]
        ):
            show_results()
            return
        if learning_extra_active:
            stage = app_state["learning_extra_stages"][app_state["learning_extra_index"]]
            app_state["mode"] = stage["mode"]
            word = stage["word"]
        elif session_mode == "mega":
            stage = app_state["current_batch"][app_state["index"]]
            app_state["mode"] = stage["mode"]
            if stage["mode"] == "matching":
                show_matching_round()
                return
            word = stage["word"]
        elif app_state["mode"] == "matching":
            show_matching_round()
            return
        else:
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
            title = {
                "daily": phase_text()["daily_review"],
                "review": phase_text()["regular_review"],
                "difficult": phase_text()["difficult_words"],
                "fast": phase_text()["quick_review"],
                "new": phase_text()["knowledge_check"],
            }.get(mode, phase_text()["quiz"])
        if app_state["feedback_active"]:
            if mode == "word_building":
                body.controls.insert(4, feedback_panel(word))
            else:
                body.controls.append(feedback_panel(word))
            bottom = None if mode == "fast" else ft.Button(
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

    def start_true_false_followup(word):
        correct = str(app_state["correct_answer"])
        rejected = str(app_state["tf_displayed"])
        acceptable = acceptable_answers(word, app_state.get("direction", "forward"))
        distractors = [
            value for value in answer_distractors(app_state.get("direction", "forward"), acceptable)
            if value.casefold() != rejected.casefold()
        ]
        distractor = random.choice(distractors) if distractors else rejected
        options = [correct, distractor]
        random.shuffle(options)
        app_state["tf_followup_active"] = True
        app_state["tf_followup_options"] = options
        app_state["selected_answer"] = None
        show_quiz_card()

    def submit_answer(selected, word):
        if app_state["feedback_active"]:
            return
        mode = app_state["mode"]
        if mode == "true_false":
            if app_state.get("tf_followup_active", False):
                is_correct = str(selected).casefold() in app_state["acceptable_answers"]
            elif app_state["tf_is_truth"] is False and selected is False:
                start_true_false_followup(word)
                return
            else:
                is_correct = selected == app_state["tf_is_truth"]
        elif mode == "word_building":
            is_correct = str(selected).casefold() == str(app_state["correct_answer"]).casefold()
        else:
            is_correct = str(selected).casefold() in app_state["acceptable_answers"]
        if mode == "fast":
            app_state["question_id"] += 1
        stats = app_state["stats"]["words"][str(word["id"])]
        update_word_performance(stats, is_correct, mode, datetime.date.today())
        app_state["session_answered"] += 1
        app_state["selected_answer"] = selected
        app_state["feedback_correct"] = is_correct
        app_state["feedback_active"] = True
        if is_correct:
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
            if mode == "fast":
                app_state["lives"] -= 1
            if mode == "new" and word["id"] not in app_state["learning_wrong_ids"]:
                app_state["learning_wrong_ids"].append(word["id"])
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
        if (
            app_state.get("session_mode") == "new"
            and app_state.get("learning_extra_started", False)
            and app_state.get("learning_extra_index", 0) < len(app_state.get("learning_extra_stages", []))
        ):
            app_state["learning_extra_index"] += 1
        else:
            app_state["index"] += 1
        show_quiz_card()

    def show_results():
        record_completed_session()
        t = phase_text()
        mode = app_state.get("session_mode", app_state["mode"])
        answered = app_state.get("session_answered", 0)
        correct = app_state.get("session_correct", 0)
        newly_learned = app_state.get("session_new_learned", 0)
        accuracy = round(correct / answered * 100) if answered else 0
        learned_total = sum(1 for word in all_words if word["learned"])
        if (
            mode == "new"
            and learned_total >= 50
            and not app_state["stats"].get("milestone_50_completed", False)
        ):
            app_state["stats"]["milestone_50_completed"] = True
            app_state["session_milestone_50"] = True
            save_stats(app_state["stats"])
        milestone_50_reached = mode == "new" and app_state.get("session_milestone_50", False)

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
                ft.Button(t["try_again"], icon=ft.Icons.REPLAY, on_click=lambda _: start_session("ALL", "fast"), bgcolor=INDIGO, color="white", height=54),
                ft.OutlinedButton(t["finish"], icon=ft.Icons.CHECK, on_click=return_from_exercise, height=50),
            ]
        elif mode == "new":
            learning_word_count = app_state.get("learning_word_count", 0)
            all_learned = learning_word_count > 0 and newly_learned == learning_word_count
            if milestone_50_reached:
                emoji = "🏆"
                result_title = t["milestone_50_title"]
                result_hint = t["milestone_50_hint"]
                result_card_controls = [
                    ft.Text(str(learned_total), size=42, weight=ft.FontWeight.BOLD, color=INDIGO, text_align=ft.TextAlign.CENTER),
                    ft.Text(t["milestone_words_total"], size=14, weight=ft.FontWeight.BOLD, color=INK),
                    ft.Divider(color=BORDER),
                    ft.Text(f"+{newly_learned} · {t['newly_learned'].lower()}", size=14, color=MUTED),
                    ft.Text(f"🔥 {t['streak_confirmed']}: {streak_days_text(displayed_streak(), app_state['lang'])}", size=14, color="#A15C00"),
                ]
            else:
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
                ft.Button(t["finish"], icon=ft.Icons.CHECK, on_click=return_from_exercise, bgcolor=INDIGO, color="white", height=54),
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
                ft.Button(t["finish"], icon=ft.Icons.CHECK, on_click=return_from_exercise, bgcolor=INDIGO, color="white", height=54),
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
            bgcolor=SCREEN_BACKGROUNDS["exercise"],
            padding=0,
            can_pop=True,
        )
        set_session_view(result_view)

    async def open_app_after_welcome():
        await asyncio.sleep(1)
        if user_stats.get("lang"):
            show_home()
        else:
            show_language_selector()

    def show_welcome_screen():
        clear_navigation_view()
        page.controls.clear()
        page.navigation_bar = None
        page.scroll = None
        page.padding = 0
        page.bgcolor = BG
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        stage_page_controls(ft.SafeArea(
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
