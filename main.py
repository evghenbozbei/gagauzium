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
        "next": "Понял, дальше",
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
        "skip": "Пропустить →",
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
        "confirm_reset_all": "Обнулить весь прогресс? Все выученные слова станут невыученными."
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
        "next": "Am înțeles, mai departe",
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
        "skip": "Sari peste →",
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
        "confirm_reset_all": "Resetăm tot progresul? Toate cuvintele învățate vor deveni neînvățate."
    }
}

PHASE1_TEXT = {
    "RU": {
        "nav_home": "Главная", "nav_learn": "Учить", "nav_review": "Повторять",
        "gagauz_language": "Гагаузский язык", "settings": "Настройки",
        "your_progress": "ВАШ ПРОГРЕСС", "words": "слов", "beginner": "Начальный",
        "today": "Сегодня", "daily_review": "Ежедневное повторение",
        "ready_review": "20 слов готовы к повторению", "daily_in_progress": "Продолжить: {0} / 20",
        "daily_complete": "Повторение на сегодня завершено", "daily_locked": "Откроется после изучения 20 слов",
        "start_daily": "Начать повторение", "continue_daily": "Продолжить повторение",
        "continue_learning": "ПРОДОЛЖИТЬ ОБУЧЕНИЕ", "choose_category": "Выбрать категорию",
        "continue": "Продолжить", "no_category": "Выберите первую категорию в разделе «Учить».",
        "day_streak": "дн. подряд", "streak_hint": "Завершите занятие сегодня, чтобы продолжить серию.",
        "learn_title": "Что вы хотите изучить?", "learn_subtitle": "Выберите тему и учитесь в своём темпе.",
        "conversational": "Разговорный", "advanced": "Продвинутый", "expert": "Эксперт", "locked": "Скоро",
        "back": "Назад", "words_learned": "слов изучено", "learn_new": "Учить новые слова",
        "words_remaining": "слов осталось", "start_learning": "Начать обучение",
        "difficult_words": "Сложные слова", "need_attention": "слов требуют внимания", "review_action": "Повторить",
        "learned_words": "Изученные слова", "view_words": "Посмотреть слова",
        "review_title": "Повторение", "review_subtitle": "Закрепляйте слова короткими тренировками.",
        "daily_desc": "Персональная подборка на сегодня.", "difficult_desc": "Слова, в которых вы чаще ошибаетесь.",
        "quick_review": "Быстрое повторение", "quick_desc": "Тренировка на скорость с тремя жизнями.",
        "quiz": "Тест", "quiz_desc": "Проверьте себя в формате «Правда или ложь».",
        "start_session": "Начать", "global_review": "Выбор слов", "true_false_short": "Правда / Ложь", "no_difficult": "Пока нет сложных слов",
        "language": "Язык обучения", "russian": "Русский", "romanian": "Румынский",
        "reset_progress": "Сброс прогресса", "reset_category_label": "Сбросить категорию",
        "select_category": "Выберите категорию", "reset_all_hint": "Изученные слова станут неизученными. Статистика ответов сохранится.",
        "open_settings": "Открыть настройки", "all_words_learned": "Все слова изучены",
    },
    "RO": {
        "nav_home": "Acasă", "nav_learn": "Învață", "nav_review": "Repetă",
        "gagauz_language": "Limba găgăuză", "settings": "Setări",
        "your_progress": "PROGRESUL TĂU", "words": "cuvinte", "beginner": "Începător",
        "today": "Astăzi", "daily_review": "Repetare zilnică",
        "ready_review": "20 de cuvinte sunt gata de repetat", "daily_in_progress": "Continuă: {0} / 20",
        "daily_complete": "Repetarea de astăzi este finalizată", "daily_locked": "Disponibilă după 20 de cuvinte învățate",
        "start_daily": "Începe repetarea", "continue_daily": "Continuă repetarea",
        "continue_learning": "CONTINUĂ ÎNVĂȚAREA", "choose_category": "Alege categoria",
        "continue": "Continuă", "no_category": "Alege prima categorie din secțiunea „Învață”.",
        "day_streak": "zile la rând", "streak_hint": "Finalizează o sesiune astăzi pentru a continua seria.",
        "learn_title": "Ce vrei să înveți?", "learn_subtitle": "Alege o temă și învață în ritmul tău.",
        "conversational": "Conversațional", "advanced": "Avansat", "expert": "Expert", "locked": "În curând",
        "back": "Înapoi", "words_learned": "cuvinte învățate", "learn_new": "Învață cuvinte noi",
        "words_remaining": "cuvinte rămase", "start_learning": "Începe învățarea",
        "difficult_words": "Cuvinte dificile", "need_attention": "cuvinte necesită atenție", "review_action": "Repetă",
        "learned_words": "Cuvinte învățate", "view_words": "Vezi cuvintele",
        "review_title": "Repetare", "review_subtitle": "Consolidează vocabularul prin sesiuni scurte.",
        "daily_desc": "Selecția personalizată pentru astăzi.", "difficult_desc": "Cuvintele la care greșești mai des.",
        "quick_review": "Repetare rapidă", "quick_desc": "Antrenament contra cronometru cu trei vieți.",
        "quiz": "Test", "quiz_desc": "Verifică-te în formatul Adevărat sau Fals.",
        "start_session": "Începe", "global_review": "Alegere de cuvinte", "true_false_short": "Adevărat / Fals", "no_difficult": "Nu există încă cuvinte dificile",
        "language": "Limba de învățare", "russian": "Rusă", "romanian": "Română",
        "reset_progress": "Resetarea progresului", "reset_category_label": "Resetează categoria",
        "select_category": "Alege categoria", "reset_all_hint": "Cuvintele învățate vor deveni neînvățate. Statisticile răspunsurilor se păstrează.",
        "open_settings": "Deschide setările", "all_words_learned": "Toate cuvintele sunt învățate",
    },
}

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
    page.window_width = 450
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.assets_dir = "assets"
    
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
        "session_completion_recorded": False,
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
            ft.Container(
                content=ft.Text("G", size=19, weight=ft.FontWeight.BOLD, color=INDIGO),
                width=38, height=38, alignment=ft.Alignment.CENTER,
                bgcolor="#EEF2FF", border_radius=12,
            ),
            ft.Column([
                ft.Text("Gagauzium", size=19, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(t["gagauz_language"], size=11, color=MUTED),
            ], spacing=0, expand=True),
            ft.Container(
                content=ft.Text(app_state["lang"], size=11, weight=ft.FontWeight.BOLD, color=INDIGO),
                padding=ft.Padding.symmetric(horizontal=10, vertical=7),
                bgcolor="#EEF2FF", border_radius=12,
            ),
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
        page.scroll = ft.ScrollMode.AUTO
        page.bgcolor = BG
        page.padding = ft.Padding.only(left=16, right=16, top=14, bottom=18)
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
        page.scroll = ft.ScrollMode.AUTO
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
                    ft.Container(content=ft.Text("G", size=34, weight=ft.FontWeight.BOLD, color="white"), width=76, height=76, alignment=ft.Alignment.CENTER, bgcolor=INDIGO, border_radius=24),
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
                ft.Row([
                    ft.Text(str(learned_count), size=38, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(f"/ {total_count} {t['words']}", size=14, color="#C9CEDD"),
                ], vertical_alignment=ft.CrossAxisAlignment.END, spacing=7),
                ft.ProgressBar(value=learned_count / total_count if total_count else 0, color="#75D3C7", bgcolor="#394269", height=10),
                ft.Text(f"Level 1 · {t['beginner']}", size=11, color="#A9E7DF"),
            ], spacing=10), padding=20, bgcolor=INDIGO_DARK, border_radius=24,
        )

        attention = sum(1 for w in all_words if w["learned"] and app_state["stats"]["words"].get(str(w["id"]), {}).get("wrong_answers", 0) > 0)
        daily_card = rounded_card(ft.Column([
            ft.Row([ft.Text("✨", size=24), ft.Column([ft.Text(t["today"], size=17, weight=ft.FontWeight.BOLD, color=INK), ft.Text(t["daily_review"], size=11, color=MUTED)], spacing=0)], spacing=10),
            ft.Text(daily_status, size=14, weight=ft.FontWeight.W_600, color=INK),
            ft.Text(f"⚠ {min(5, attention)} {t['need_attention']}", size=12, color="#B54747"),
            ft.ElevatedButton(daily_cta, icon=ft.Icons.PLAY_ARROW, on_click=lambda _: start_session("ALL", "daily"), disabled=daily_disabled, bgcolor=INDIGO, color="white", height=46),
        ], spacing=10))

        last_category = app_state["stats"].get("last_active_category")
        actual_categories = {w["category"] for w in all_words}
        if last_category in actual_categories:
            learned, total, _ = category_counts(last_category)
            continue_content = ft.Column([
                ft.Row([ft.Text(t["continue_learning"], size=11, weight=ft.FontWeight.BOLD, color=MUTED), ft.TextButton(t["choose_category"], on_click=lambda _: show_learn())], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([category_visual(last_category, 62), ft.Column([ft.Text(localized_category_name(last_category, app_state["lang"]), size=18, weight=ft.FontWeight.BOLD, color=INK), ft.Text(get_category_meta(last_category).get("gag") or "", size=11, color=INDIGO), ft.Text(f"{learned} / {total} {t['words']}", size=12, color=MUTED)], spacing=2, expand=True)], spacing=14),
                ft.ProgressBar(value=learned / total if total else 0, color=INDIGO, bgcolor="#E8EAF2", height=8),
                ft.ElevatedButton(t["continue"], icon=ft.Icons.ARROW_FORWARD, on_click=lambda _, c=last_category: open_category_detail(c), bgcolor="#20283D", color="white", height=46),
            ], spacing=10)
        else:
            continue_content = ft.Column([
                ft.Text(t["continue_learning"], size=11, weight=ft.FontWeight.BOLD, color=MUTED),
                ft.Text(t["no_category"], size=14, color=MUTED),
                ft.ElevatedButton(t["choose_category"], icon=ft.Icons.MENU_BOOK, on_click=lambda _: show_learn(), bgcolor=INDIGO, color="white"),
            ], spacing=12)

        streak = displayed_streak()
        streak_card = rounded_card(ft.Row([
            ft.Container(content=ft.Text("🔥", size=24), width=46, height=46, alignment=ft.Alignment.CENTER, bgcolor="#FFF0D9", border_radius=15),
            ft.Column([ft.Text(f"{streak} {t['day_streak']}", size=15, weight=ft.FontWeight.BOLD, color="#8B4513"), ft.Text(t["streak_hint"], size=11, color="#9A633A")], spacing=2, expand=True),
        ], spacing=12), padding=14, bgcolor="#FFF8EC")

        page.add(ft.Container(height=4), progress_card, daily_card, rounded_card(continue_content), streak_card, ft.Container(height=8))
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
                    ], scroll=ft.ScrollMode.AUTO, spacing=7),
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
        t = phase_text()
        learned, total, difficult = category_counts(source_name)
        remaining = total - learned
        meta = get_category_meta(source_name)
        page.add(
            ft.Row([ft.TextButton(t["back"], icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_learn()), ft.Container(expand=True), ft.Text(meta.get("gag") or "", size=11, color=INDIGO)], spacing=5),
            rounded_card(ft.Column([
                ft.Row([category_visual(source_name, 82), ft.Column([ft.Text(localized_category_name(source_name, app_state["lang"]), size=24, weight=ft.FontWeight.BOLD, color=INK), ft.Text(meta.get("gag") or "", size=12, color=INDIGO)], spacing=3, expand=True)], spacing=15),
                ft.Row([ft.Text(f"{learned} / {total} {t['words_learned']}", size=12, weight=ft.FontWeight.BOLD, color=INK), ft.Text(f"{round(learned / total * 100) if total else 0}%", size=12, weight=ft.FontWeight.BOLD, color=INDIGO)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=learned / total if total else 0, color=INDIGO, bgcolor="#E8EAF2", height=9),
            ], spacing=12)),
            rounded_card(ft.Column([
                ft.Text("✨ " + t["learn_new"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(f"{remaining} {t['words_remaining']}", size=12, color=MUTED),
                ft.ElevatedButton(t["start_learning"] if remaining else t["all_words_learned"], icon=ft.Icons.PLAY_ARROW, on_click=lambda _: start_session(source_name, "new"), disabled=remaining == 0, bgcolor=INDIGO, color="white"),
            ], spacing=9)),
            rounded_card(ft.Column([
                ft.Text("⚠️ " + t["difficult_words"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(f"{difficult} {t['need_attention']}" if difficult else t["no_difficult"], size=12, color=MUTED),
                ft.ElevatedButton(t["review_action"], icon=ft.Icons.REPLAY, on_click=lambda _: start_session(source_name, "difficult"), disabled=difficult == 0, bgcolor="#D34A5B", color="white"),
            ], spacing=9)),
            rounded_card(ft.Column([
                ft.Text("📖 " + t["learned_words"], size=17, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(f"{learned} {t['words']}", size=12, color=MUTED),
                ft.ElevatedButton(t["view_words"], icon=ft.Icons.LIST_ALT, on_click=lambda _: show_word_list(source_name, learned_only=True), disabled=learned == 0, bgcolor="#16847A", color="white"),
            ], spacing=9)),
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

        def review_card(icon, title, description, badge, action, color, disabled=False, secondary=None):
            actions = [ft.ElevatedButton(t["start_session"] if secondary is None else t["global_review"], icon=ft.Icons.PLAY_ARROW, on_click=action, disabled=disabled, bgcolor=color, color="white", height=44, expand=True)]
            if secondary is not None:
                actions.append(ft.OutlinedButton(t["true_false_short"], on_click=secondary, disabled=disabled, height=44, expand=True))
            return rounded_card(ft.Column([
                ft.Row([ft.Text(icon, size=28), ft.Column([ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=INK), ft.Text(badge, size=11, color=color)], spacing=1, expand=True)], spacing=11),
                ft.Text(description, size=12, color=MUTED),
                ft.Row(actions, spacing=8),
            ], spacing=10))

        page.add(
            ft.Container(height=4), ft.Text(t["review_title"], size=24, weight=ft.FontWeight.BOLD, color=INK), ft.Text(t["review_subtitle"], size=12, color=MUTED),
            review_card("✨", t["daily_review"], t["daily_desc"], t["daily_complete"] if daily_done else (t["ready_review"] if learned_count >= 20 else t["daily_locked"]), lambda _: start_session("ALL", "daily"), INDIGO, learned_count < 20 or daily_done),
            review_card("⚠️", t["difficult_words"], t["difficult_desc"], f"{difficult_count} {t['need_attention']}" if difficult_count else t["no_difficult"], lambda _: start_session("ALL", "difficult"), "#D34A5B", difficult_count == 0),
            review_card("⚡", t["quick_review"], t["quick_desc"], f"{learned_count} {t['words']}", lambda _: start_session("ALL", "fast"), "#5C55C8", learned_count < 4),
            review_card("✓", t["quiz"], t["quiz_desc"], "10 / 15", lambda _: start_session("ALL", "review"), "#16847A", learned_count < 4, secondary=lambda _: start_session("ALL", "true_false")),
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
            ], spacing=10)),
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
            for w in all_words:
                w["learned"] = False
                app_state["stats"]["words"][str(w["id"])]["learned"] = False
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

        list_view = ft.ListView(controls=rows, expand=True, spacing=0)

        page.add(
            ft.Container(height=30),
            ft.Row([ft.TextButton(content=ft.Text(phase_text()["back"], size=17, weight="bold"), icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_category_detail(category))], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=10),
            ft.Text(f"{txt['dictionary']}{cat_display}", size=20, weight="bold", color="black"),
            ft.Container(height=10),
            list_view,
        )
        page.update()

    def return_from_exercise():
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

    def start_session(category, mode):
        if app_state.get("current_screen") != "exercise":
            app_state["exercise_return_screen"] = app_state.get("current_screen", "home")
            app_state["exercise_return_category"] = (
                category if app_state["exercise_return_screen"] == "category" and category != "ALL" else None
            )
        app_state["current_screen"] = "exercise"
        page.navigation_bar = None
        if category != "ALL":
            persist_last_category(category)
        app_state["mode"] = mode
        app_state["last_word_id"] = None
        app_state["session_completion_recorded"] = False
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
            app_state["current_batch"] = weighted_sample(
                words, app_state["stats"], today, k=10 if category == "ALL" else 6
            )
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
        elif mode == "daily":
            app_state["is_quiz"] = True
            daily = app_state["stats"].get("daily_review")
            if not daily or daily.get("date") != today_iso:
                learned = [w for w in all_words if w["learned"]]
                word_ids = build_daily_set(learned, app_state["stats"], today)
                daily = {
                    "date": today_iso,
                    "word_ids": word_ids,
                    "index": 0,
                    "correct_count": 0
                }
                app_state["stats"]["daily_review"] = daily
                save_stats(app_state["stats"])
            word_map = {w["id"]: w for w in all_words}
            app_state["current_batch"] = [word_map[wid] for wid in daily["word_ids"] if wid in word_map]
            app_state["index"] = daily.get("index", 0)
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
        else:
            if app_state["is_quiz"]: show_quiz_card()
            else: show_study_card()

    def continue_new_session():
        start_session(app_state["last_category"], "new")

    def show_study_card():
        page.clean()
        page.navigation_bar = None
        page.scroll = None
        page.padding = 0
        page.bgcolor = "#F5DEB3"
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        if app_state["index"] >= len(app_state["current_batch"]):
            app_state["is_quiz"] = True
            app_state["index"] = 0
            show_quiz_card()
            return
        word = app_state["current_batch"][app_state["index"]]
        native_word = word.get(lang.lower(), word.get("ru", "---"))
        progress_val = (app_state["index"] + 1) / len(app_state["current_batch"])

        page.add(
            ft.Container(height=30),
            ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: return_from_exercise())], alignment=ft.MainAxisAlignment.START),
            ft.ProgressBar(value=progress_val, color="#449C4A", bgcolor="#eeeeee", width=380),
            ft.Container(height=30),
            ft.Container(
                content=ft.Column([
                    ft.Text(txt["remember"], size=16, color="grey"),
                    ft.Text(native_word, size=35, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color="transparent"),
                    ft.Text(word["gag"], size=30, color="blue", italic=True, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40, bgcolor="#B0E0E6", border=ft.Border.all(2, "blue"), border_radius=20, width=380,
            ),
            ft.Container(height=50),
            ft.ElevatedButton(txt["next"], on_click=lambda _: next_study_word(), width=300, height=50)
        )
        page.update()

    def next_study_word():
        app_state["index"] += 1
        show_study_card()

    def skip_word():
        word = app_state["current_batch"][app_state["index"]]
        word_stats = app_state["stats"]["words"][str(word["id"])]
        word_stats["wrong_answers"] = word_stats.get("wrong_answers", 0) + 1
        word_stats["last_seen"] = datetime.date.today().isoformat()
        save_stats(app_state["stats"])
        app_state["index"] += 1
        app_state["feedback_text"] = ""
        show_quiz_card()

    def show_quiz_card():
        page.clean()
        page.navigation_bar = None
        page.scroll = None
        page.padding = 0
        page.bgcolor = "#FFE4B5"
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        is_fast = app_state["mode"] == "fast"
        is_tf = app_state["mode"] == "true_false"

        if is_fast and app_state.get("lives", 0) <= 0:
            page.add(
                ft.Container(height=100), ft.Text("💔", size=80),
                ft.Text(txt["fast_review_fail"], size=20, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(txt["to_menu"], on_click=lambda _: return_from_exercise(), width=200)
            )
            page.update()
            return

        if app_state["index"] >= len(app_state["current_batch"]):
            record_completed_session()
            if app_state["mode"] == "new":
                unlearned_left = len([w for w in all_words if w["category"] == app_state["last_category"] and not w["learned"]])
                if unlearned_left == 0:
                    page.add(
                        ft.Container(height=100), ft.Text("🎉", size=80),
                        ft.Text(txt["finished"], size=25, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                        ft.Text(txt["all_learned"], size=20, weight="bold", color="green", text_align=ft.TextAlign.CENTER),
                        ft.Container(height=20),
                        ft.ElevatedButton(txt["to_menu"], on_click=lambda _: return_from_exercise(), width=200)
                    )
                else:
                    # Предложить продолжить изучение новых слов
                    page.add(
                        ft.Container(height=100), ft.Text("✅", size=80),
                        ft.Text(txt["finished"], size=25, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                        ft.Text(txt["continue_question"], size=18, color="black", text_align=ft.TextAlign.CENTER),
                        ft.Row([
                            ft.ElevatedButton(txt["continue_yes"], on_click=lambda _: continue_new_session(), width=150),
                            ft.ElevatedButton(txt["continue_no"], on_click=lambda _: return_from_exercise(), width=150)
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    )
            elif app_state["mode"] == "daily":
                daily = app_state["stats"].get("daily_review", {})
                correct = daily.get("correct_count", 0)
                total = len(app_state["current_batch"])
                pct = int(round(correct / total * 100)) if total > 0 else 0
                page.add(
                    ft.Container(height=100), ft.Text("🎉", size=80),
                    ft.Text(txt["daily_review_score"].format(correct, total, pct), size=22, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    ft.Text(txt["daily_review_locked"], size=18, color="grey", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    ft.ElevatedButton(txt["to_menu"], on_click=lambda _: return_from_exercise(), width=200)
                )
            else:
                msg = txt["fast_review_success"] if (is_fast or is_tf) else txt["finished"]
                page.add(
                    ft.Container(height=100), ft.Text("✅", size=80),
                    ft.Text(msg, size=25, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(txt["to_menu"], on_click=lambda _: return_from_exercise(), width=200)
                )
            page.update()
            return

        word = app_state["current_batch"][app_state["index"]]
        if app_state["last_word_id"] != word["id"]:
            if app_state["mode"] == "new":
                direction = "forward"
            else:
                direction = random.choice(["forward", "reverse"])
            app_state["direction"] = direction

            if direction == "forward":
                prompt_word = word.get(lang.lower(), word.get("ru", "---"))
                correct = word["gag"]
                others = list({w["gag"] for w in all_words if w["gag"] != correct})
            else:
                prompt_word = word["gag"]
                correct = word.get(lang.lower(), word.get("ru", "---"))
                others = list({w.get(lang.lower(), w.get("ru", "---")) for w in all_words if w.get(lang.lower(), w.get("ru", "---")) != correct})

            if is_tf:
                is_truth = random.choice([True, False])
                if is_truth:
                    app_state["tf_displayed"] = correct
                    app_state["tf_is_truth"] = True
                else:
                    app_state["tf_displayed"] = random.choice(others) if others else correct
                    app_state["tf_is_truth"] = False
            else:
                distractors = random.sample(others, min(len(others), 3))
                options = distractors + [correct]
                random.shuffle(options)
                app_state["current_options"] = options
            app_state["prompt_word"] = prompt_word
            app_state["correct_answer"] = correct
            app_state["last_word_id"] = word["id"]
            app_state["feedback_text"] = ""

        prompt_word = app_state["prompt_word"]
        direction = app_state.get("direction", "forward")
        prompt_color = "blue" if direction == "reverse" else "black"
        prompt_italic = direction == "reverse"
        tf_displayed_color = "black" if direction == "reverse" else "blue"
        tf_displayed_italic = direction == "forward"

        btns_column = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        if is_tf:
            btns_column.controls.append(ft.ElevatedButton(txt["true_btn"], width=350, height=65, bgcolor="#dcedc8", color="black", on_click=lambda e: check_answer(e, True, word)))
            btns_column.controls.append(ft.ElevatedButton(txt["false_btn"], width=350, height=65, bgcolor="#ffcdd2", color="black", on_click=lambda e: check_answer(e, False, word)))
            progress_val = (app_state["index"] + 1) / len(app_state["current_batch"])
            page.add(
                ft.Container(height=30),
                ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: return_from_exercise())], alignment=ft.MainAxisAlignment.START),
                ft.ProgressBar(value=progress_val, color="#449C4A", bgcolor="#eeeeee", width=350),
                ft.Container(height=10),
                ft.Text(txt["quiz_title"], size=16, color="grey"),
                ft.Container(height=20), ft.Text(prompt_word, size=35, weight="bold", color=prompt_color, italic=prompt_italic, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10), ft.Text(app_state["tf_displayed"], size=30, weight="bold", color=tf_displayed_color, italic=tf_displayed_italic, text_align=ft.TextAlign.CENTER),
                ft.Container(height=20), btns_column, ft.Container(height=20),
                ft.Text(app_state["feedback_text"], size=20, weight="bold", color="black")
            )
            page.update()
        else:
            app_state["option_buttons"] = {}
            for opt in app_state["current_options"]:
                option_btn = ft.ElevatedButton(opt, width=350, height=55, on_click=lambda e, s=opt: check_answer(e, s, word))
                app_state["option_buttons"][opt] = option_btn
                btns_column.controls.append(option_btn)

            if is_fast:
                app_state["question_id"] = app_state.get("question_id", 0) + 1
                current_q_id = app_state["question_id"]
                progress_bar = ft.ProgressBar(value=1.0, color="red", bgcolor="#eeeeee", width=350)
                lives_text = ft.Text("❤️" * app_state.get("lives", 3), size=20)
                counter_text = ft.Text(str(app_state.get("score", 0)), size=24, weight="bold", color="black")
                
                page.add(
                    ft.Container(height=30),
                    ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: return_from_exercise())], alignment=ft.MainAxisAlignment.START),
                    lives_text,
                    progress_bar,
                    counter_text,
                    ft.Container(height=10),
                    ft.Text(txt["quiz_title"], size=16, color="grey"),
                    ft.Container(height=20), ft.Text(prompt_word, size=35, weight="bold", color=prompt_color, italic=prompt_italic),
                    ft.Container(height=20), btns_column, ft.Container(height=20),
                    ft.Text(app_state["feedback_text"], size=20, weight="bold", color="black")
                )
                page.update()

                async def run_timer():
                    steps = 70
                    for i in range(steps):
                        await asyncio.sleep(0.1)
                        if app_state.get("question_id") != current_q_id:
                            return
                        progress_bar.value = 1.0 - (i + 1) / steps
                        page.update()
                    
                    if app_state.get("question_id") == current_q_id:
                        app_state["lives"] -= 1
                        app_state["index"] += 1
                        app_state["feedback_text"] = UI_TEXT[lang]["wrong"]
                        page.update()
                        await asyncio.sleep(0.8)
                        app_state["feedback_text"] = ""
                        show_quiz_card()

                page.run_task(run_timer)
            else:
                progress_val = (app_state["index"] + 1) / len(app_state["current_batch"])
                title_text = txt["daily_review_title"] if app_state["mode"] == "daily" else txt["quiz_title"]
                page.add(
                    ft.Container(height=30),
                    ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: return_from_exercise())], alignment=ft.MainAxisAlignment.START),
                    ft.ProgressBar(value=progress_val, color="#449C4A", bgcolor="#eeeeee", width=350),
                    ft.Container(height=10),
                    ft.Text(title_text, size=16, color="grey"),
                    ft.Container(height=20), ft.Text(prompt_word, size=35, weight="bold", color=prompt_color, italic=prompt_italic),
                    ft.Container(height=20), btns_column, ft.Container(height=20),
                    ft.Text(app_state["feedback_text"], size=20, weight="bold", color="black"),
                    *( [ft.TextButton(content=ft.Text(txt["skip"], size=14, color="grey"), on_click=lambda _: skip_word())] if app_state["mode"] == "review" else [] )
                )
                page.update()

    def check_answer(e, selected, correct_word):
        lang = app_state["lang"]
        btn = e.control
        is_tf = app_state["mode"] == "true_false"
        is_daily = app_state["mode"] == "daily"
        today_iso = datetime.date.today().isoformat()

        if app_state["mode"] == "fast":
            app_state["question_id"] += 1

        if is_tf:
            is_correct = (selected == app_state["tf_is_truth"])
        else:
            is_correct = (selected == app_state.get("correct_answer", correct_word["gag"]))

        word_stats = app_state["stats"]["words"][str(correct_word["id"])]
        word_stats["last_seen"] = today_iso

        if is_correct:
            word_stats["correct_answers"] += 1

            if app_state["mode"] == "fast" or is_tf:
                app_state["score"] = app_state.get("score", 0) + 1
            if app_state["mode"] == "new":
                for w in all_words:
                    if w["id"] == correct_word["id"]:
                        w["learned"] = True
                        word_stats["learned"] = True
                        break
            if is_daily:
                app_state["stats"]["daily_review"]["correct_count"] = app_state["stats"]["daily_review"].get("correct_count", 0) + 1
                app_state["stats"]["daily_review"]["index"] = app_state["index"] + 1

            save_stats(app_state["stats"])
            btn.bgcolor = "green"
            btn.color = "white"
            app_state["feedback_text"] = UI_TEXT[lang]["correct"]
            page.update()
            async def go_next():
                await asyncio.sleep(0.8)
                btn.bgcolor = None
                btn.color = None
                app_state["index"] += 1
                show_quiz_card()
            page.run_task(go_next)
        else:
            word_stats["wrong_answers"] += 1

            if is_daily:
                app_state["stats"]["daily_review"]["index"] = app_state["index"] + 1

            save_stats(app_state["stats"])
            if app_state["mode"] == "fast":
                app_state["lives"] -= 1
            btn.bgcolor = "red"
            btn.color = "white"
            correct_btn = None
            if is_daily:
                correct_btn = app_state.get("option_buttons", {}).get(app_state.get("correct_answer"))
                if correct_btn is not None:
                    correct_btn.bgcolor = "green"
                    correct_btn.color = "white"
            app_state["feedback_text"] = UI_TEXT[lang]["wrong"]
            page.update()
            async def reset_btn():
                await asyncio.sleep(1.2 if is_daily else 0.8)
                btn.bgcolor = None
                btn.color = None
                if correct_btn is not None:
                    correct_btn.bgcolor = None
                    correct_btn.color = None
                app_state["feedback_text"] = ""
                if app_state["mode"] == "fast" or is_tf or is_daily:
                    app_state["index"] += 1
                    show_quiz_card()
                else:
                    page.update()
            page.run_task(reset_btn)

    if user_stats.get("lang"):
        show_main_menu(reset_scroll=True)
    else:
        show_language_selector()

if __name__ == "__main__":
    ft.run(main)
