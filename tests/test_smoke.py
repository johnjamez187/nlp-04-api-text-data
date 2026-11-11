"""Offline smoke tests for the JSON API EVTL stages."""

import json
import logging
from types import SimpleNamespace

import polars as pl
import pytest
import requests

from nlp.stage01_extract import run_extract
from nlp.stage02_validate import run_validate
from nlp.stage03_transform import run_transform
from nlp.stage04_load import run_load


def test_json_stages_write_expected_csv(monkeypatch, tmp_path):
    """Run extraction through loading with a controlled API response."""
    # Sample 2024 Kansas City Chiefs player statistics.
    rows = [
        {
            "player_display_name": "Patrick Mahomes",
            "team": "KC",
            "season": 2024,
            "week": 1,
            "opponent_team": "BAL",
            "position": "QB",
            "passing_yards": 291,
            "rushing_yards": 3,
            "receiving_yards": 0,
            "passing_tds": 1,
            "rushing_tds": 0,
            "receiving_tds": 0,
        },
        {
            "player_display_name": "Travis Kelce",
            "team": "KC",
            "season": 2024,
            "week": 1,
            "opponent_team": "BAL",
            "position": "TE",
            "passing_yards": 0,
            "rushing_yards": 0,
            "receiving_yards": 34,
            "passing_tds": 0,
            "rushing_tds": 0,
            "receiving_tds": 0,
        },
    ]

    # Convert sample records to CSV to simulate the NFLverse download.
    payload = pl.DataFrame(rows).write_csv()

    def fake_get(url, *, headers, timeout):
        assert url == (
            "https://github.com/nflverse/nflverse-data/releases/"
            "download/stats_player/stats_player_week_2024.csv"
        )
        assert headers["Accept"] == "text/csv"
        assert timeout == 30

        return SimpleNamespace(
            text=payload,
            raise_for_status=lambda: None,
        )

    monkeypatch.setattr(requests, "get", fake_get)
    log = logging.getLogger(__name__)
    raw_path = tmp_path / "raw.json"
    csv_path = tmp_path / "processed.csv"

    extracted = run_extract(
        "https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2024.csv",
        {"Accept": "text/csv"},
        raw_path,
        log,
    )
    df = run_transform(run_validate(extracted, log), log)
    run_load(df, csv_path, log)

    assert json.loads(raw_path.read_text(encoding="utf-8")) == rows
    assert csv_path.stat().st_size > 0
    saved = pl.read_csv(csv_path)
    # Verify the Chiefs player statistics.
    assert saved["player_name"].to_list() == [
        "Patrick Mahomes",
        "Travis Kelce",
    ]
    assert saved["team"].to_list() == ["KC", "KC"]
    assert saved["passing_yards"].to_list() == [291, 0]
    assert saved["receiving_yards"].to_list() == [0, 34]
    assert saved["total_offensive_yards"].to_list() == [294, 34]
    assert saved["total_touchdowns"].to_list() == [1, 0]


def test_validation_rejects_empty_records():
    """Reject an empty API response instead of creating an empty dataset."""
    with pytest.raises(ValueError, match="at least one record"):
        run_validate([], logging.getLogger(__name__))
