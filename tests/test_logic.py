"""Unit tests for the pure learning logic in main.py."""

import datetime
import json
import random

import pytest

import main

TODAY = datetime.date(2026, 9, 30)


def word(word_id, ru, gag, ro=None, category="Семья", learned=False):
    return {"id": word_id, "ru": ru, "ro": ro or ru, "gag": gag, "category": category, "learned": learned}


# --- text helpers

@pytest.mark.parametrize("count, expected", [
    (1, "слово"), (2, "слова"), (5, "слов"), (11, "слов"), (21, "слово"), (22, "слова"), (112, "слов"),
])
def test_russian_plural(count, expected):
    assert main.russian_plural(count, "слово", "слова", "слов") == expected


def test_localized_counters():
    assert main.learned_of_total_text(1, 20, "RU") == "1 слово изучено из 20"
    assert main.learned_of_total_text(1, 20, "RO") == "1 cuvânt învățat din 20"
    assert main.streak_days_text(3, "RU") == "3 дня подряд"
    assert main.attention_word_count_text(1, "RU") == "1 слово требует внимания"


def test_display_letter_keeps_dotted_and_dotless_i_apart():
    assert main.display_letter("i") == "İ"
    assert main.display_letter("ı") == "I"
    assert main.display_letter("ä") == "Ä"
    assert main.display_letter("ş") == "Ş"


def test_answer_variants():
    assert main.answer_variants("büük / büyük") == {"büük", "büyük"}
    assert main.answer_variants("Eni yıl") == {"eni yıl"}


@pytest.mark.parametrize("gag, target", [
    ("furkuliţa / vilka / çatall", "furkuliţa"),
    ("mezä (içeceklerä)", "mezä"),
    ("Eni yıl", "Eni yıl"),
    ("arada-sırada", "arada-sırada"),
])
def test_word_build_target(gag, target):
    assert main.word_build_target({"gag": gag}) == target


def test_word_build_characters_keep_separators():
    assert main.word_build_characters("Eni yıl") == list("Eni yıl")
    assert main.word_build_characters("a(b)") == ["a", "b"]


@pytest.mark.parametrize("template, expected_count", [
    ("ay", 0), ("kitap", 0), ("kardaş", 1), ("üürenici", 1), ("kaybetmää", 2), ("eni yıl", 2),
])
def test_word_build_hint_count(template, expected_count):
    hints = main.word_build_hint_positions(list(template))
    assert len(hints) == expected_count
    assert all(template[i].isalpha() for i in hints)


def test_hints_are_placed_in_both_parts_of_a_phrase():
    first, second = main.word_build_hint_positions(list("eni yıl"))
    assert first < 3 < second


# --- valid and wrong answers

HOMONYM_WORDS = [
    word(165, "луна", "ay", ro="lună"),
    word(315, "месяц", "ay", ro="lună"),
    word(131, "плохой", "bet / fena", ro="rău"),
    word(24, "плохо", "bet", ro="rău"),
    word(132, "большой", "büük / büyük", ro="mare"),
    word(324, "море", "deniz", ro="mare"),
    word(1, "я", "bän", ro="eu"),
    word(2, "ты", "sän", ro="tu"),
]


def test_homonyms_accept_every_translation():
    assert main.valid_answers(HOMONYM_WORDS[0], "reverse", HOMONYM_WORDS, "RU") == {"луна", "месяц"}
    assert main.valid_answers(HOMONYM_WORDS[0], "forward", HOMONYM_WORDS, "RU") == {"ay"}


def test_shared_romanian_translation_accepts_both_words():
    assert main.valid_answers(HOMONYM_WORDS[4], "forward", HOMONYM_WORDS, "RO") == {"büük / büyük", "deniz"}


def test_partially_overlapping_variants_are_valid():
    assert main.valid_answers(HOMONYM_WORDS[3], "reverse", HOMONYM_WORDS, "RU") == {"плохо", "плохой"}


@pytest.mark.parametrize("lang", ["RU", "RO"])
@pytest.mark.parametrize("direction", ["forward", "reverse"])
def test_wrong_answers_never_contain_a_valid_translation(lang, direction):
    for entry in HOMONYM_WORDS:
        acceptable = main.valid_answers(entry, direction, HOMONYM_WORDS, lang)
        acceptable_variants = set().union(*(main.answer_variants(a) for a in acceptable))
        for option in main.wrong_answers(direction, acceptable, HOMONYM_WORDS, lang):
            assert not main.answer_variants(option) & acceptable_variants


def test_matching_accepts_homonym_pairs():
    grandson, granddaughter = word(582, "внук", "unuka / torun"), word(583, "внучка", "unuka / torun")
    assert main.entries_are_equivalent(grandson, granddaughter, "RU")
    assert not main.entries_are_equivalent(HOMONYM_WORDS[6], HOMONYM_WORDS[7], "RU")


# --- progress tracking

def fresh_stats():
    return {"correct_answers": 0, "wrong_answers": 0, "last_seen": "1970-01-01",
            "needs_attention": False, "difficult_correct_streak": 0}


def test_wrong_answer_marks_word_for_attention():
    stats = fresh_stats()
    main.update_word_performance(stats, False, "review", TODAY)
    assert stats["wrong_answers"] == 1
    assert stats["needs_attention"] is True
    assert stats["last_seen"] == TODAY.isoformat()


def test_two_correct_difficult_answers_resolve_a_word():
    stats = fresh_stats()
    main.update_word_performance(stats, False, "review", TODAY)
    main.update_word_performance(stats, True, "difficult", TODAY)
    assert stats["needs_attention"] is True
    main.update_word_performance(stats, True, "difficult", TODAY)
    assert stats["needs_attention"] is False


def test_correct_answers_outside_difficult_mode_do_not_resolve():
    stats = fresh_stats()
    main.update_word_performance(stats, False, "review", TODAY)
    for _ in range(3):
        main.update_word_performance(stats, True, "review", TODAY)
    assert stats["needs_attention"] is True


def test_legacy_stats_without_flag_use_error_count():
    assert main.requires_attention({"wrong_answers": 2}) is True
    assert main.requires_attention({"wrong_answers": 0}) is False


def test_register_learning_day_streak():
    stats = {"streak_days": 0}
    assert main.register_learning_day(stats, TODAY) is True
    assert stats["streak_days"] == 1
    assert main.register_learning_day(stats, TODAY) is False
    assert main.register_learning_day(stats, TODAY + datetime.timedelta(days=1)) is True
    assert stats["streak_days"] == 2
    assert main.register_learning_day(stats, TODAY + datetime.timedelta(days=5)) is True
    assert stats["streak_days"] == 1


# --- word selection

def test_weighted_sample_returns_unique_words():
    words = [word(i, f"w{i}", f"g{i}") for i in range(1, 31)]
    stats = {"words": {}}
    sample = main.weighted_sample(words, stats, TODAY, k=10)
    assert len(sample) == 10 and len({w["id"] for w in sample}) == 10
    assert len(main.weighted_sample(words[:3], stats, TODAY, k=10)) == 3
    assert main.weighted_sample([], stats, TODAY, k=5) == []


def test_word_weight_prefers_errors_and_old_words():
    stats = {"words": {
        "1": {"correct_answers": 5, "wrong_answers": 0, "last_seen": TODAY.isoformat()},
        "2": {"correct_answers": 0, "wrong_answers": 5, "last_seen": TODAY.isoformat()},
        "3": {"correct_answers": 5, "wrong_answers": 0, "last_seen": "2026-01-01"},
    }}
    weights = {i: main.word_weight({"id": i}, stats, TODAY) for i in (1, 2, 3)}
    assert weights[2] > weights[1]
    assert weights[3] > weights[1]


def test_number_category_starts_in_counting_order():
    numbers = [word(i, str(i), f"n{i}", category="Цифры") for i in range(36, 60)]
    first = main.select_new_learning_batch(numbers, "Цифры")
    assert [w["id"] for w in first] == [36, 37, 38, 39, 40]
    for entry in first:
        entry["learned"] = True
    assert [w["id"] for w in main.select_new_learning_batch(numbers, "Цифры")] == [41, 42, 43, 44, 45]


def test_other_categories_take_up_to_six_unlearned_words():
    words = [word(i, f"w{i}", f"g{i}", learned=i <= 3) for i in range(1, 12)]
    batch = main.select_new_learning_batch(words, "Семья")
    assert len(batch) == 6
    assert all(not w["learned"] for w in batch)


def test_daily_set_includes_most_mistaken_words():
    random.seed(1)
    words = [word(i, f"w{i}", f"g{i}", learned=True) for i in range(1, 41)]
    stats = {"words": {str(i): {"wrong_answers": 10 if i <= 5 else 0} for i in range(1, 41)}}
    daily = main.build_daily_set(words, stats, TODAY)
    assert len(daily) == 20 and len(set(daily)) == 20
    assert {1, 2, 3, 4, 5} <= set(daily)
    assert main.build_daily_set(words[:19], stats, TODAY) == []


# --- persistence

def test_merge_creates_progress_for_new_words(isolated_stats_file):
    words = [word(1, "я", "bän", learned=True)]
    stats = {"words": {}}
    main.merge_data_and_stats(words, stats)
    assert words[0]["learned"] is False
    assert stats["words"]["1"]["learned"] is False
    assert isolated_stats_file.exists()


def test_merge_adds_missing_fields_and_keeps_progress():
    words = [word(1, "я", "bän")]
    stats = {"words": {"1": {"learned": True, "wrong_answers": 1}}}
    main.merge_data_and_stats(words, stats)
    assert words[0]["learned"] is True
    assert stats["words"]["1"]["needs_attention"] is True
    assert stats["words"]["1"]["difficult_correct_streak"] == 0


def test_save_and_load_round_trip(isolated_stats_file):
    main.save_stats({"lang": "RO", "words": {"1": {"learned": True}}})
    assert not isolated_stats_file.with_name("user_stats.json.tmp").exists()
    stats = main.load_stats()
    assert stats["lang"] == "RO"
    assert stats["streak_days"] == 0


@pytest.mark.parametrize("content", ['{"words": {"1": {"lea', "[1, 2]", "\udcff"])
def test_unreadable_stats_do_not_crash(isolated_stats_file, content):
    isolated_stats_file.write_bytes(content.encode("utf-8", "surrogateescape"))
    stats = main.load_stats()
    assert stats["words"] == {}
    assert not isolated_stats_file.exists()
    assert list(isolated_stats_file.parent.glob("user_stats.corrupt-*.json"))


def test_missing_stats_file_starts_fresh():
    stats = main.load_stats()
    assert stats == {"streak_days": 0, "last_login": "", "milestone_50_completed": False, "words": {}}
    assert json.dumps(stats)


# --- category reset

def test_reset_forgets_progress_and_upcoming_daily_words():
    stats = {
        "words": {str(i): {"learned": True, "correct_answers": 3, "wrong_answers": 2,
                           "last_seen": TODAY.isoformat(), "needs_attention": True,
                           "difficult_correct_streak": 1} for i in range(1, 7)},
        "daily_review": {"date": TODAY.isoformat(), "word_ids": [1, 2, 3, 4, 5, 6], "index": 2},
    }
    main.reset_words_progress(stats, [1, 4, 5])
    assert stats["words"]["4"] == main.new_word_stats()
    assert stats["words"]["2"]["learned"] is True
    # Word 1 was already answered today and stays counted; 4 and 5 are dropped.
    assert stats["daily_review"]["word_ids"] == [1, 2, 3, 6]
    assert main.daily_review_length(stats["daily_review"]) == 4


def test_daily_review_length_without_a_set():
    assert main.daily_review_length(None) == 0
    assert main.daily_review_length({}) == 0


# --- choosing wrong options

POS_WORDS = (
    [dict(word(100 + i, f"глагол{i}", f"fiil{i}", category="Глаголы"), part_of_speech=["verb"]) for i in range(6)]
    + [dict(word(200 + i, f"цифра{i}", f"sayı{i}", category="Цифры"), part_of_speech=["numeral"]) for i in range(6)]
    + [dict(word(300 + i, f"еда{i}", f"iimäk{i}", category="Еда"), part_of_speech=["noun"]) for i in range(6)]
    + [dict(word(400 + i, f"дом{i}", f"ev{i}", category="Дом и Предметы"), part_of_speech=["noun"]) for i in range(6)]
)


@pytest.mark.parametrize("direction", ["forward", "reverse"])
def test_two_of_three_wrong_options_resemble_the_word(direction):
    asked = POS_WORDS[0]
    same_kind = {main.answer_text(w, direction, "RU") for w in POS_WORDS if w["category"] == "Глаголы"}
    for seed in range(50):
        acceptable = main.valid_answers(asked, direction, POS_WORDS, "RU")
        options = main.pick_wrong_answers(asked, direction, acceptable, POS_WORDS, "RU", 3, rng=random.Random(seed))
        assert len(options) == len(set(options)) == 3
        assert not set(options) & acceptable
        assert len(set(options) & same_kind) >= 2


def test_similar_options_prefer_the_same_category():
    asked = POS_WORDS[12]  # noun from «Еда»; nouns also exist in «Дом и Предметы»
    same_topic, same_kind = main.similar_wrong_answers(
        asked, "forward", {main.answer_text(w, "forward", "RU") for w in POS_WORDS}, POS_WORDS, "RU")
    assert same_topic == sorted(f"iimäk{i}" for i in range(6))
    assert same_kind == sorted(f"ev{i}" for i in range(6))
    options = main.pick_wrong_answers(asked, "forward", {"iimäk0"}, POS_WORDS, "RU", 3, rng=random.Random(3))
    assert sum(option.startswith("iimäk") for option in options) >= 2


def test_rare_parts_of_speech_fall_back_to_any_words():
    lonely = dict(word(999, "и", "hem", category="Союзы и Связки"), part_of_speech=["conjunction"])
    words = POS_WORDS + [lonely]
    options = main.pick_wrong_answers(lonely, "forward", {"hem"}, words, "RU", 3, rng=random.Random(1))
    assert len(options) == 3 and "hem" not in options


def test_single_option_respects_exclusions():
    asked = POS_WORDS[0]
    for seed in range(30):
        options = main.pick_wrong_answers(asked, "forward", {"fiil0"}, POS_WORDS, "RU", 1,
                                          exclude=["FIIL1"], rng=random.Random(seed))
        assert len(options) == 1 and options[0] not in {"fiil0", "fiil1"}
