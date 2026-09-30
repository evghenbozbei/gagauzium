"""Every interface text used in main.py must exist in both languages."""

import re
from pathlib import Path

import main

SOURCE = (Path(main.__file__)).read_text(encoding="utf-8")


def referenced_keys(pattern):
    return set(re.findall(pattern, SOURCE))


def test_both_languages_have_the_same_keys():
    for table in (main.UI_TEXT, main.PHASE1_TEXT):
        assert set(table["RU"]) == set(table["RO"])


def test_phase_texts_used_in_code_exist():
    keys = referenced_keys(r'(?:\bt|phase_text\(\))\["(\w+)"\]')
    keys |= referenced_keys(r'"(result_\w+)"')
    assert keys - set(main.PHASE1_TEXT["RU"]) == set()


def test_legacy_texts_used_in_code_exist():
    keys = referenced_keys(r'(?:\btxt|UI_TEXT\[[^\]]+\])\["(\w+)"\]')
    assert keys - set(main.UI_TEXT["RU"]) == set()


def test_format_placeholders_match_between_languages():
    for table in (main.UI_TEXT, main.PHASE1_TEXT):
        for key, text in table["RU"].items():
            assert re.findall(r"\{\d\}", text) == re.findall(r"\{\d\}", table["RO"][key]), key
