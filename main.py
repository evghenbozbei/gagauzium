import flet as ft
import json
import random
import asyncio
import datetime
import os

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
        "streak": "Дней подряд: ",
        "hard_words": "Самые сложные слова (ошибок):",
        "category_title": "Изучения и повторения по категориям",
        "true_false_btn": "Правда или Ложь",
        "true_btn": "✅ Правда",
        "false_btn": "❌ Ложь",
        "continue_question": "Продолжить изучение новых слов?",
        "continue_yes": "Да",
        "continue_no": "Нет"
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
        "streak": "Zile la rând: ",
        "hard_words": "Cele mai grele cuvinte (erori):",
        "category_title": "Studiu și repetare pe categorii",
        "true_false_btn": "Adevărat sau Fals",
        "true_btn": "✅ Adevărat",
        "false_btn": "❌ Fals",
        "continue_question": "Continuați învățarea cuvintelor noi?",
        "continue_yes": "Da",
        "continue_no": "Nu"
    }
}

# --- СЛОВАРЬ КАТЕГОРИЙ ---
category_map = {
    "Местоимения": {"ro": "Pronume", "gag": "Adıllar"},
    "Вопросы": {"ro": "Întrebări", "gag": "Sormalar"},
    "Базовые": {"ro": "Cuvinte de bază", "gag": "Temel laflar"},
    "Время": {"ro": "Timpul", "gag": "Vakıt"},
    "Цифры": {"ro": "Numere", "gag": "Sayılar"},
    "Семья": {"ro": "Familia", "gag": "Aylä"},
    "Еда": {"ro": "Mâncare", "gag": "İimäk"},
    "Глаголы": {"ro": "Verbe", "gag": "İşliklär"},
    "Прилагательные": {"ro": "Adjective", "gag": "Nışannar"},
    "Анатомия": {"ro": "Anatomia", "gag": "Anatomiya"},
    "Природа": {"ro": "Natura", "gag": "Tabiat"},
    "Животные": {"ro": "Animale", "gag": "Hayvannar"},
    "Дом и Предметы": {"ro": "Casă și obiecte", "gag": "Ev hem nesnelär"},
    "Профессии": {"ro": "Profesii", "gag": "Zanaatlar"},
    "Цвета": {"ro": "Culori", "gag": "Renklär"},
    "Транспорт и Город": {"ro": "Transport și oraș", "gag": "Transport hem Kasaba"},
    "Одежда": {"ro": "Haine", "gag": "Giiyim"},
    "Действия": {"ro": "Acțiuni", "gag": "İşlär"},
    "Качества": {"ro": "Calități", "gag": "Kallitälär"},
    "Места": {"ro": "Locuri", "gag": "Erler"}
}

def load_data():
    try:
        with open("words_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open("words_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_stats():
    try:
        with open("user_stats.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"streak_days": 0, "last_login": "", "words": {}}

def save_stats(stats):
    with open("user_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def merge_data_and_stats(all_words, stats):
    needs_save = False
    for w in all_words:
        w_id = str(w["id"])
        if w_id not in stats["words"]:
            stats["words"][w_id] = {
                "learned": w.get("learned", False),
                "correct_answers": 0,
                "wrong_answers": 0,
                "interval": 0,
                "next_review": "1970-01-01"
            }
            needs_save = True
        else:
            # Миграция для старых записей
            if "interval" not in stats["words"][w_id]:
                stats["words"][w_id]["interval"] = 0
                needs_save = True
            if "next_review" not in stats["words"][w_id]:
                stats["words"][w_id]["next_review"] = "1970-01-01"
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
    
    today_str = datetime.date.today().isoformat()
    if user_stats.get("last_login") != today_str:
        if user_stats.get("last_login"):
            last_date = datetime.date.fromisoformat(user_stats["last_login"])
            if (datetime.date.today() - last_date).days == 1:
                user_stats["streak_days"] = user_stats.get("streak_days", 0) + 1
            else:
                user_stats["streak_days"] = 1
        else:
            user_stats["streak_days"] = 1
        user_stats["last_login"] = today_str
        save_stats(user_stats)

    all_words = merge_data_and_stats(raw_words, user_stats)

    app_state = {
        "lang": "RU",
        "current_batch": [],
        "index": 0,
        "is_quiz": False, 
        "mode": "new", 
        "current_options": [],
        "feedback_text": "",
        "last_word_id": None,
        "last_category": None,
        "saved_scroll": 0.0,
        "stats": user_stats
    }

    def on_scroll(e):
        if app_state.get("tracking_scroll", False):
            app_state["saved_scroll"] = e.pixels

    page.on_scroll = on_scroll

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
            ft.Row([
                ft.Text("🔥", size=40),
                ft.Text(f"{txt['streak']}{app_state['stats'].get('streak_days', 0)}", size=20, weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
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
        page.scroll = None
        page.bgcolor = "white"
        page.add(
            ft.Container(height=100),
            ft.Text("Gagauzium", size=45, weight="bold", color="#00008B"),
            ft.Text("Выберите язык / Alegeți limba", size=16, color="grey"),
            ft.Container(height=40),
            ft.ElevatedButton(
                content=ft.Row([ft.Text("РУССКИЙ", size=20, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
                width=300, height=70, on_click=lambda _: set_language("RU")
            ),
            ft.Container(height=20),
            ft.ElevatedButton(
                content=ft.Row([ft.Text("ROMÂNĂ", size=20, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
                width=300, height=70, on_click=lambda _: set_language("RO")
            )
        )
        page.update()

    def set_language(lang):
        app_state["lang"] = lang
        show_main_menu(reset_scroll=True)

    def show_main_menu(reset_scroll=False):
        app_state["question_id"] = -1  # Отменяем все запущенные таймеры
        app_state["tracking_scroll"] = False  # Пауза трекинга на время построения
        if reset_scroll:
            app_state["saved_scroll"] = 0.0
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        page.bgcolor = "#E0FFFF"
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        nonlocal all_words
        all_words = merge_data_and_stats(load_data(), app_state["stats"])
        
        categories = sorted(list(set(w["category"] for w in all_words)))
        category_column = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        total_learned_count = len([w for w in all_words if w["learned"]])
        
        today = datetime.date.today().isoformat()
        due_global = [w for w in all_words if w["learned"] and app_state["stats"]["words"][str(w["id"])].get("next_review", "1970-01-01") <= today]
        due_count = len(due_global)

        page.add(
            ft.Container(height=30),
            ft.Row([
                ft.Row([ft.Text("🔥", size=20, color="orange"), ft.Text(f"{app_state['stats'].get('streak_days', 0)}", size=20, weight="bold", color="orange")]),
                ft.TextButton("🌐 Сменить язык / Schimbă limba", on_click=lambda _: show_language_selector())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text(txt["title"], size=25, weight="bold", color="#00008B"),
            ft.Container(height=20),
            ft.Text(txt["global_title"], size=18, weight="bold", color="black"),
            ft.ElevatedButton(content=ft.Text(f"{txt['global_btn']} ({due_count})", size=16, weight="bold"), bgcolor="#bbdefb", color="black", width=350, height=60, on_click=lambda _: start_session("ALL", "review"), disabled=due_count == 0),
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Image(src="fast_check.png", width=24, height=24),
                        ft.Text(txt["fast_review_btn"], size=16, weight="bold")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                bgcolor="#ffcdd2", color="black", width=350, height=60,
                on_click=lambda _: start_session("ALL", "fast"), disabled=total_learned_count < 4),
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Text(txt["true_false_btn"], size=16, weight="bold"),
                bgcolor="#ffe082", color="black", width=350, height=60,
                on_click=lambda _: start_session("ALL", "true_false"), disabled=total_learned_count < 4),
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Text(txt["statistics"], size=16, weight="bold"),
                bgcolor="#e1bee7", color="black", width=350, height=60,
                on_click=lambda _: show_statistics()),
            ft.Container(height=20),
            ft.Divider(height=1, color="#eeeeee"),
            ft.Container(height=10),
            ft.Text(txt["category_title"], size=18, weight="bold", color="black"),
            ft.Container(height=10)
        )

        for cat in categories:
            unlearned = [w for w in all_words if w["category"] == cat and not w["learned"]]
            learned = [w for w in all_words if w["category"] == cat and w["learned"]]
            
            cat_info = category_map.get(cat, {})
            base_name = cat_info.get(lang.lower(), cat)
            gag_name = cat_info.get("gag", "")
            display_name = f"{base_name} / {gag_name}" if gag_name else base_name

            cat_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(display_name, size=18, weight="bold", color="black", expand=True),
                        ft.TextButton(content=ft.Text(txt["reset"], size=11, color="red"), on_click=lambda e, c=cat: reset_category(c))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=10),
                    ft.Row([
                        ft.ElevatedButton(content=ft.Text(txt["learn"], size=13, color="black", text_align=ft.TextAlign.CENTER), on_click=lambda e, c=cat: start_session(c, "new"), disabled=len(unlearned) == 0, bgcolor="#FFD700", width=165),
                        
                        ft.ElevatedButton(
                            content=ft.Text(f"{txt['review']} ({len([w for w in learned if app_state['stats']['words'][str(w['id'])].get('next_review', '1970-01-01') <= today])})", size=13, text_align=ft.TextAlign.CENTER), 
                            on_click=lambda e, c=cat: start_session(c, "review"), 
                            disabled=len([w for w in learned if app_state['stats']['words'][str(w['id'])].get('next_review', '1970-01-01') <= today]) == 0, 
                            width=165
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.TextButton(content=ft.Text(txt["view_all"], size=14, color="blue"), on_click=lambda e, c=cat: show_word_list(c), width=340)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=15, width=400, bgcolor="#FFFFE0", border=ft.Border.all(1, "#dddddd"), border_radius=15,
                key=cat
            )
            category_column.controls.append(cat_card)
        
        page.add(category_column)
        page.add(
            ft.Container(height=30), ft.Divider(height=1, color="#eeeeee"), ft.Container(height=20),
            ft.TextButton(content=ft.Text(txt["reset_all"], size=15, color="red"), on_click=lambda _: reset_all_progress()),
            ft.Container(height=40)
        )
        page.update()
        
        saved = app_state["saved_scroll"]
        if saved > 0:
            async def restore_scroll():
                await asyncio.sleep(0.05)
                await page.scroll_to(offset=saved, duration=400)
            page.run_task(restore_scroll)
        
        app_state["tracking_scroll"] = True
        app_state["last_category"] = None

    def reset_category(category_name):
        for w in all_words:
            if w["category"] == category_name:
                w["learned"] = False
                app_state["stats"]["words"][str(w["id"])]["learned"] = False
        save_stats(app_state["stats"])
        show_main_menu()

    def reset_all_progress():
        for w in all_words:
            w["learned"] = False
            app_state["stats"]["words"][str(w["id"])]["learned"] = False
        save_stats(app_state["stats"])
        show_main_menu()

    def show_word_list(category):
        app_state["tracking_scroll"] = False
        app_state["last_category"] = category
        page.clean()
        page.scroll = None
        page.bgcolor = "#E0FFFF"
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        words = [w for w in all_words if w["category"] == category]
        cat_info = category_map.get(category, {})
        cat_display = cat_info.get(lang.lower(), category)

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
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "#eeeeee"))
                )
            )

        list_view = ft.ListView(controls=rows, expand=True, spacing=0)

        page.add(
            ft.Container(height=30),
            ft.Row([ft.TextButton(content=ft.Text(txt["back"], size=17, weight="bold"), on_click=lambda _: show_main_menu())], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=10),
            ft.Text(f"{txt['dictionary']}{cat_display}", size=20, weight="bold", color="black"),
            ft.Container(height=10),
            list_view,
        )
        page.update()

    def start_session(category, mode):
        if category != "ALL":
            app_state["last_category"] = category
        app_state["mode"] = mode
        batch_size = 6
        today = datetime.date.today().isoformat()

        if mode == "fast":
            words = [w for w in all_words if w["learned"]]
            app_state["is_quiz"] = True
            app_state["lives"] = 3
            app_state["score"] = 0
            batch_size = len(words)
            app_state["question_id"] = 0
        elif mode == "true_false":
            words = [w for w in all_words if w["learned"]]
            app_state["is_quiz"] = True
            batch_size = 10
            app_state["score"] = 0
        elif category == "ALL":
            # SRS mode for global review
            words = [w for w in all_words if w["learned"] and app_state["stats"]["words"][str(w["id"])].get("next_review", "1970-01-01") <= today]
            app_state["is_quiz"] = True
            batch_size = 10
        elif mode == "new":
            words = [w for w in all_words if w["category"] == category and not w["learned"]]
            app_state["is_quiz"] = False
        else:
            # SRS mode for category review
            words = [w for w in all_words if w["category"] == category and w["learned"] and app_state["stats"]["words"][str(w["id"])].get("next_review", "1970-01-01") <= today]
            app_state["is_quiz"] = True

        random.shuffle(words)
        app_state["current_batch"] = words[:batch_size]
        app_state["index"] = 0
        
        if not app_state["current_batch"]:
            show_main_menu()
        else:
            if app_state["is_quiz"]: show_quiz_card()
            else: show_study_card()

    def continue_new_session():
        start_session(app_state["last_category"], "new")

    def show_study_card():
        page.clean()
        page.scroll = None
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
            ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: show_main_menu())], alignment=ft.MainAxisAlignment.START),
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

    def show_quiz_card():
        page.clean()
        page.scroll = None
        page.bgcolor = "#FFE4B5"
        lang = app_state["lang"]
        txt = UI_TEXT[lang]
        is_fast = app_state["mode"] == "fast"
        is_tf = app_state["mode"] == "true_false"

        if is_fast and app_state.get("lives", 0) <= 0:
            page.add(
                ft.Container(height=100), ft.Text("💔", size=80),
                ft.Text(txt["fast_review_fail"], size=20, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(txt["to_menu"], on_click=lambda _: show_main_menu(), width=200)
            )
            page.update()
            return

        if app_state["index"] >= len(app_state["current_batch"]):
            if app_state["mode"] == "new":
                # Предложить продолжить изучение новых слов
                page.add(
                    ft.Container(height=100), ft.Text("✅", size=80),
                    ft.Text(txt["finished"], size=25, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                    ft.Text(txt["continue_question"], size=18, color="black", text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        ft.ElevatedButton(txt["continue_yes"], on_click=lambda _: continue_new_session(), width=150),
                        ft.ElevatedButton(txt["continue_no"], on_click=lambda _: show_main_menu(), width=150)
                    ], alignment=ft.MainAxisAlignment.CENTER)
                )
            else:
                msg = txt["fast_review_success"] if (is_fast or is_tf) else txt["finished"]
                page.add(
                    ft.Container(height=100), ft.Text("✅", size=80),
                    ft.Text(msg, size=25, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(txt["to_menu"], on_click=lambda _: show_main_menu(), width=200)
                )
            page.update()
            return

        word = app_state["current_batch"][app_state["index"]]
        native_word = word.get(lang.lower(), word.get("ru", "---"))
        if app_state["last_word_id"] != word["id"]:
            correct = word["gag"]
            others = [w["gag"] for w in all_words if w["gag"] != correct]
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
            app_state["last_word_id"] = word["id"]
            app_state["feedback_text"] = ""

        btns_column = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        if is_tf:
            btns_column.controls.append(ft.ElevatedButton(txt["true_btn"], width=350, height=65, bgcolor="#dcedc8", color="black", on_click=lambda e: check_answer(e, True, word)))
            btns_column.controls.append(ft.ElevatedButton(txt["false_btn"], width=350, height=65, bgcolor="#ffcdd2", color="black", on_click=lambda e: check_answer(e, False, word)))
            progress_val = (app_state["index"] + 1) / len(app_state["current_batch"])
            page.add(
                ft.Container(height=30),
                ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: show_main_menu())], alignment=ft.MainAxisAlignment.START),
                ft.ProgressBar(value=progress_val, color="#449C4A", bgcolor="#eeeeee", width=350),
                ft.Container(height=10),
                ft.Text(txt["quiz_title"], size=16, color="grey"),
                ft.Container(height=20), ft.Text(native_word, size=35, weight="bold", color="black", text_align=ft.TextAlign.CENTER),
                ft.Container(height=10), ft.Text(app_state["tf_displayed"], size=30, weight="bold", color="blue", italic=True, text_align=ft.TextAlign.CENTER),
                ft.Container(height=20), btns_column, ft.Container(height=20),
                ft.Text(app_state["feedback_text"], size=20, weight="bold", color="black")
            )
            page.update()
        else:
            for opt in app_state["current_options"]:
                btns_column.controls.append(ft.ElevatedButton(opt, width=350, height=55, on_click=lambda e, s=opt: check_answer(e, s, word)))

            if is_fast:
                app_state["question_id"] = app_state.get("question_id", 0) + 1
                current_q_id = app_state["question_id"]
                progress_bar = ft.ProgressBar(value=1.0, color="red", bgcolor="#eeeeee", width=350)
                lives_text = ft.Text("❤️" * app_state.get("lives", 3), size=20)
                counter_text = ft.Text(str(app_state.get("score", 0)), size=24, weight="bold", color="black")
                
                page.add(
                    ft.Container(height=30),
                    ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: show_main_menu())], alignment=ft.MainAxisAlignment.START),
                    lives_text,
                    progress_bar,
                    counter_text,
                    ft.Container(height=10),
                    ft.Text(txt["quiz_title"], size=16, color="grey"),
                    ft.Container(height=20), ft.Text(native_word, size=35, weight="bold", color="black"),
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
                page.add(
                    ft.Container(height=30),
                    ft.Row([ft.TextButton(content=ft.Text(txt["to_menu"], size=17, weight="bold"), on_click=lambda _: show_main_menu())], alignment=ft.MainAxisAlignment.START),
                    ft.ProgressBar(value=progress_val, color="#449C4A", bgcolor="#eeeeee", width=350),
                    ft.Container(height=10),
                    ft.Text(txt["quiz_title"], size=16, color="grey"),
                    ft.Container(height=20), ft.Text(native_word, size=35, weight="bold", color="black"),
                    ft.Container(height=20), btns_column, ft.Container(height=20),
                    ft.Text(app_state["feedback_text"], size=20, weight="bold", color="black")
                )
                page.update()

    def check_answer(e, selected, correct_word):
        lang = app_state["lang"]
        btn = e.control
        is_tf = app_state["mode"] == "true_false"
        
        if app_state["mode"] == "fast":
            app_state["question_id"] += 1

        is_correct = False
        if is_tf:
            is_correct = (selected == app_state["tf_is_truth"])
        else:
            is_correct = (selected == correct_word["gag"])

        if is_correct:
            app_state["stats"]["words"][str(correct_word["id"])]["correct_answers"] += 1
            
            # SRS Обновление
            if app_state["mode"] == "review" or (app_state["mode"] == "new"):
                word_stats = app_state["stats"]["words"][str(correct_word["id"])]
                if app_state["mode"] == "new":
                    # Для новых слов: interval=0, next_review=сегодня (чтобы можно было повторять сразу)
                    word_stats["interval"] = 0
                    word_stats["next_review"] = datetime.date.today().isoformat()
                else:
                    # Для review: стандартная SRS логика
                    intervals = [1, 3, 7, 14, 30]
                    current_int = word_stats.get("interval", 0)
                    new_int = 1
                    for i in intervals:
                        if i > current_int:
                            new_int = i
                            break
                    else:
                        new_int = 30
                    
                    word_stats["interval"] = new_int
                    word_stats["next_review"] = (datetime.date.today() + datetime.timedelta(days=new_int)).isoformat()

            if app_state["mode"] == "fast" or is_tf:
                app_state["score"] = app_state.get("score", 0) + 1
            if app_state["mode"] == "new":
                for w in all_words:
                    if w["id"] == correct_word["id"]:
                        w["learned"] = True
                        app_state["stats"]["words"][str(correct_word["id"])]["learned"] = True
                        break
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
            app_state["stats"]["words"][str(correct_word["id"])]["wrong_answers"] += 1
            
            # SRS Сброс при ошибке
            if app_state["mode"] == "review":
                word_stats = app_state["stats"]["words"][str(correct_word["id"])]
                word_stats["interval"] = 0
                word_stats["next_review"] = datetime.date.today().isoformat()

            save_stats(app_state["stats"])
            if app_state["mode"] == "fast":
                app_state["lives"] -= 1
            btn.bgcolor = "red"
            btn.color = "white"
            app_state["feedback_text"] = UI_TEXT[lang]["wrong"]
            page.update()
            async def reset_btn():
                await asyncio.sleep(0.8)
                btn.bgcolor = None
                btn.color = None
                app_state["feedback_text"] = ""
                if app_state["mode"] == "fast" or is_tf:
                    app_state["index"] += 1
                    show_quiz_card()
                else:
                    page.update()
            page.run_task(reset_btn)

    show_language_selector()

if __name__ == "__main__":
    ft.run(main)