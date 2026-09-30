import json
import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

import main  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_stats_file(tmp_path, monkeypatch):
    """Never let a test touch the real user_stats.json."""
    stats_file = tmp_path / "user_stats.json"
    monkeypatch.setattr(main, "USER_STATS_FILE", stats_file)
    return stats_file


@pytest.fixture(scope="session")
def words():
    with (PROJECT_DIR / "words_data.json").open(encoding="utf-8") as f:
        return json.load(f)
