import flet as ft
import json
import random
import asyncio

# --- ЛОГИКА ДАННЫХ ---
def load_data():
    try:
        with open("words_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open("words_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- ГЛАВНОЕ ПРИЛОЖЕНИЕ ---
def main(page: ft.Page):
    page.title = "Gagauzium"
    page.theme_mode = "light" 
    page.window_width = 450
    page.window_height = 800
    page.horizontal_alignment = "center"
    page.bgcolor = "white"
    page.scroll = "auto" 
    
    all_words = load_data()
    app_state = {
        "current_batch": [],
        "index": 0,
        "is_quiz": False, 
        "mode": "new", 
        "current_options": [],
        "feedback_text": "",
        "last_word_id": None
    }

    def show_main_menu():
        page.clean()
        nonlocal all_words
        all_words = load_data()
        
        page.add(
            ft.Container(height=20),
            ft.Text("ГЛАВНОЕ МЕНЮ", size=25, weight="bold", color="black"),
            ft.Container(height=10)
        )
        
        categories = sorted(list(set(w["category"] for w in all_words)))
        category_column = ft.Column(spacing=20, horizontal_alignment="center")
        
        total_learned_count = len([w for w in all_words if w["learned"]])

        for cat in categories:
            unlearned = [w for w in all_words if w["category"] == cat and not w["learned"]]
            learned = [w for w in all_words if w["category"] == cat and w["learned"]]
            
            # Функция сброса прогресса для конкретной категории
            def reset_category(e, category_name=cat):
                for w in all_words:
                    if w["category"] == category_name:
                        w["learned"] = False
                save_data(all_words)
                show_main_menu()

            cat_card = ft.Container(
                content=ft.Column([
                    # Заголовок: Название + Кнопка сброса
                    ft.Row([
                        ft.Text(cat, size=20, weight="bold", color="black", expand=True),
                        ft.TextButton(
                            content=ft.Text("Обнулить прогресс", size=12, color="red"),
                            on_click=reset_category
                        )
                    ], alignment="spaceBetween"),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            content=ft.Text(f"Учить ({len(unlearned)})", size=13),
                            on_click=lambda e, c=cat: start_session(c, "new"),
                            disabled=len(unlearned) == 0,
                            width=165
                        ),
                        ft.ElevatedButton(
                            content=ft.Text(f"Повторить ({len(learned)})", size=13),
                            on_click=lambda e, c=cat: start_session(c, "review"),
                            disabled=len(learned) == 0,
                            width=165
                        ),
                    ], alignment="center", spacing=10),
                    
                    ft.TextButton(
                        content=ft.Text("Просмотреть все слова", size=14, color="blue"),
                        on_click=lambda e, c=cat: show_word_list(c),
                        width=340
                    )
                ], horizontal_alignment="center", spacing=5),
                padding=15,
                width=400,
                border=ft.border.all(1, "#dddddd"),
                border_radius=15
            )
            category_column.controls.append(cat_card)
        
        page.add(category_column)

        # Секция общего прогресса
        page.add(
            ft.Container(height=30),
            ft.Divider(height=1, color="#eeeeee"),
            ft.Container(height=20),
            ft.Text("ОБЩИЙ ПРОГРЕСС", size=18, weight="bold", color="black"),
            ft.ElevatedButton(
                content=ft.Text(f"Глобальное повторение ({total_learned_count})", size=16, weight="bold"),
                bgcolor="#bbdefb",
                color="black",
                width=350,
                height=60,
                on_click=lambda _: start_session("ALL", "review"),
                disabled=total_learned_count < 4
            ),
            ft.Container(height=40)
        )
        page.update()

    def show_word_list(category):
        page.clean()
        words = [w for w in all_words if w["category"] == category]
        
        page.add(
            ft.Row([ft.TextButton("< Назад", on_click=lambda _: show_main_menu())], alignment="start"),
            ft.Container(height=10),
            ft.Text(f"Словарь: {category}", size=22, weight="bold", color="black"),
            ft.Container(height=10)
        )

        page.add(
            ft.Container(
                content=ft.Row([
                    ft.Text("Русский", size=14, weight="bold", color="grey", width=150),
                    ft.Text("Гагаузский", size=14, weight="bold", color="grey", expand=True),
                    ft.Container(width=30)
                ]),
                padding=ft.padding.only(left=10, right=10, bottom=5),
                border=ft.border.only(bottom=ft.border.BorderSide(1, "#cccccc"))
            )
        )

        word_list_column = ft.Column(spacing=0)
        for i, w in enumerate(words):
            word_list_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(content=ft.Text(w["ru"], size=16, weight="bold", color="black"), width=150),
                        ft.Text(w["gag"], size=16, color="blue", italic=True, expand=True),
                        ft.Text("✅" if w["learned"] else "⭕", size=14)
                    ], alignment="start"),
                    padding=12,
                    bgcolor="#ffffff" if i % 2 == 0 else "#f9f9f9",
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "#eeeeee"))
                )
            )
        
        page.add(word_list_column)
        page.add(ft.Container(height=30))
        page.update()

    def start_session(category, mode):
        app_state["mode"] = mode
        if category == "ALL":
            words = [w for w in all_words if w["learned"]]
            app_state["is_quiz"] = True
        elif mode == "new":
            words = [w for w in all_words if w["category"] == category and not w["learned"]]
            app_state["is_quiz"] = False
        else:
            words = [w for w in all_words if w["category"] == category and w["learned"]]
            app_state["is_quiz"] = True

        random.shuffle(words)
        app_state["current_batch"] = words[:6]
        app_state["index"] = 0
        
        if not app_state["current_batch"]:
            show_main_menu()
        else:
            if app_state["is_quiz"]:
                show_quiz_card()
            else:
                show_study_card()

    def show_study_card():
        page.clean()
        if app_state["index"] >= len(app_state["current_batch"]):
            app_state["is_quiz"] = True
            app_state["index"] = 0
            show_quiz_card()
            return

        word = app_state["current_batch"][app_state["index"]]
        back_btn = ft.TextButton("< В меню", on_click=lambda _: show_main_menu())

        page.add(
            ft.Row([back_btn], alignment="start"),
            ft.Container(height=50),
            ft.Container(
                content=ft.Column([
                    ft.Text("ЗАПОМНИТЕ СЛОВО", size=16, color="grey"),
                    ft.Text(word["ru"], size=35, weight="bold", color="black", text_align="center"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Text(word["gag"], size=30, color="blue", italic=True, text_align="center"),
                ], horizontal_alignment="center"),
                padding=40,
                border=ft.border.all(2, "blue"),
                border_radius=20,
                width=380,
            ),
            ft.Container(height=50),
            ft.ElevatedButton("Понял, дальше", on_click=lambda _: next_study_word(), width=300, height=50)
        )
        page.update()

    def next_study_word():
        app_state["index"] += 1
        show_study_card()

    def show_quiz_card():
        page.clean()
        if app_state["index"] >= len(app_state["current_batch"]):
            page.add(
                ft.Container(height=100),
                ft.Text("✅", size=80),
                ft.Text("Сессия завершена!", size=25, weight="bold", color="black"),
                ft.ElevatedButton("В меню", on_click=lambda _: show_main_menu(), width=200)
            )
            page.update()
            return

        word = app_state["current_batch"][app_state["index"]]
        
        if app_state["last_word_id"] != word["id"]:
            correct = word["gag"]
            others = [w["gag"] for w in all_words if w["gag"] != correct]
            distractors = random.sample(others, min(len(others), 3))
            options = distractors + [correct]
            random.shuffle(options)
            app_state["current_options"] = options
            app_state["last_word_id"] = word["id"]
            app_state["feedback_text"] = ""

        btns_column = ft.Column(spacing=10, horizontal_alignment="center")
        for opt in app_state["current_options"]:
            btns_column.controls.append(
                ft.ElevatedButton(opt, width=350, height=55, on_click=lambda e, s=opt: check_answer(e, s, word))
            )

        page.add(
            ft.Row([ft.TextButton("< В меню", on_click=lambda _: show_main_menu())], alignment="start"),
            ft.Text("ПРОВЕРКА ЗНАНИЙ", size=16, color="grey"),
            ft.Text(f"Слово {app_state['index']+1} из {len(app_state['current_batch'])}", color="black", weight="bold"),
            ft.Container(height=20),
            ft.Text(word["ru"], size=35, weight="bold", color="black"),
            ft.Container(height=20),
            btns_column,
            ft.Container(height=20),
            ft.Text(app_state["feedback_text"], size=20, weight="bold", color="black")
        )
        page.update()

    def check_answer(e, selected, correct_word):
        if selected == correct_word["gag"]:
            if app_state["mode"] == "new":
                for w in all_words:
                    if w["id"] == correct_word["id"]:
                        w["learned"] = True
                        break
                save_data(all_words)
            
            e.control.bgcolor = "green"
            e.control.color = "white"
            app_state["feedback_text"] = "Верно! ✅"
            page.update()
            
            async def go_next():
                await asyncio.sleep(1.0)
                app_state["index"] += 1
                show_quiz_card()
            
            page.run_task(go_next)
        else:
            e.control.bgcolor = "red"
            e.control.color = "white"
            app_state["feedback_text"] = "Ошибка! ❌"
            page.update()

    show_main_menu()

if __name__ == "__main__":
    ft.run(main)