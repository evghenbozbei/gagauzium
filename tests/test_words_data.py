"""Integrity checks for words_data.json and category_metadata.py."""

import pytest

import main
from category_metadata import CATEGORY_METADATA, CATEGORIES_BY_SOURCE

REQUIRED_TEXT_FIELDS = ("ru", "ro", "gag")
LEVELS = {"beginner", "conversational"}

# Official Gagauz Latin alphabet (ţ and ş with cedilla).
GAGAUZ_LETTERS = set("aäbcçdeêfgğhıijklmnoöprsştţuüvyz")
GAGAUZ_ALLOWED = GAGAUZ_LETTERS | {c.upper() for c in GAGAUZ_LETTERS} | {"İ"} | set(" /-()")
# Romanian uses ș and ț with a comma below.
ROMANIAN_LETTERS = set("aăâbcdefghiîjklmnopqrsștțuvwxyz")
ROMANIAN_ALLOWED = ROMANIAN_LETTERS | {c.upper() for c in ROMANIAN_LETTERS} | set(" /-()")
RUSSIAN_LETTERS = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
RUSSIAN_ALLOWED = RUSSIAN_LETTERS | {c.upper() for c in RUSSIAN_LETTERS} | set(" /-()")

# Entries with characters outside the alphabet that still await a check by a
# Gagauz speaker. Remove an ID once the entry is confirmed or corrected.
UNVERIFIED_GAGAUZ_CHARACTERS = {
    700: {"ó"},  # kósa / tırpan
}


def test_ids_are_unique_positive_integers(words):
    ids = [word["id"] for word in words]
    assert all(isinstance(word_id, int) and word_id > 0 for word_id in ids)
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("field", REQUIRED_TEXT_FIELDS)
def test_text_fields_are_clean(words, field):
    problems = [
        (word["id"], word.get(field))
        for word in words
        if not isinstance(word.get(field), str)
        or not word[field].strip()
        or word[field] != word[field].strip()
        or "  " in word[field]
    ]
    assert problems == []


def test_gagauz_uses_gagauz_alphabet(words):
    problems = {}
    for word in words:
        unexpected = set(word["gag"]) - GAGAUZ_ALLOWED
        if unexpected and unexpected != UNVERIFIED_GAGAUZ_CHARACTERS.get(word["id"]):
            problems[word["id"]] = (word["gag"], sorted(unexpected))
    assert problems == {}


def test_romanian_uses_comma_below_letters(words):
    problems = {
        word["id"]: (word["ro"], sorted(set(word["ro"]) - ROMANIAN_ALLOWED))
        for word in words
        if set(word["ro"]) - ROMANIAN_ALLOWED
    }
    assert problems == {}


def test_russian_has_no_latin_lookalikes(words):
    problems = {
        word["id"]: (word["ru"], sorted(set(word["ru"]) - RUSSIAN_ALLOWED))
        for word in words
        if set(word["ru"]) - RUSSIAN_ALLOWED
    }
    assert problems == {}


def test_categories_match_metadata(words):
    used = {word["category"] for word in words}
    assert used - set(CATEGORIES_BY_SOURCE) == set()
    assert set(CATEGORIES_BY_SOURCE) - used == set()


def test_metadata_is_consistent():
    for field in ("key", "source_name", "order"):
        values = [item[field] for item in CATEGORY_METADATA]
        assert len(values) == len(set(values)), field
    for item in CATEGORY_METADATA:
        assert item["ru"] and item["ro"]


def test_levels_and_parts_of_speech(words):
    assert {word["level"] for word in words} <= LEVELS
    for word in words:
        pos = word["part_of_speech"]
        assert isinstance(pos, list) and pos and all(isinstance(p, str) and p for p in pos), word["id"]


def test_dictionary_holds_no_progress(words):
    assert all(word["learned"] is False for word in words)


def test_number_foundation_batches_exist(words):
    by_id = {word["id"]: word for word in words}
    for batch in main.NUMBER_FOUNDATION_BATCH_IDS:
        for word_id in batch:
            assert CATEGORIES_BY_SOURCE[by_id[word_id]["category"]]["key"] == "numbers"


def test_every_word_can_be_built(words):
    for word in words:
        template = main.word_build_characters(main.word_build_target(word))
        hints = set(main.word_build_hint_positions(template))
        to_build = [i for i, char in enumerate(template) if char.isalpha() and i not in hints]
        assert to_build, word["id"]


@pytest.mark.parametrize("lang", ["RU", "RO"])
@pytest.mark.parametrize("direction", ["forward", "reverse"])
def test_every_question_has_enough_wrong_options(words, lang, direction):
    for word in words:
        acceptable = main.valid_answers(word, direction, words, lang)
        assert len(main.wrong_answers(direction, acceptable, words, lang)) >= 3, word["id"]
