"""config.py.

(EDIT YOUR VERSION OF THIS FILE)

Purpose

  Store configuration values for the EVTL pipeline.

Analytical Questions

- What API endpoint should be used as the data source?
- What HTTP request headers are required?
- Where should raw and processed data be stored?

Edit your Python file to change:
- API URL (source of the JSON data),
- the HTTP Request Headers (to show your app name in the user-agent header)
- customize your output file name.
"""

from pathlib import Path

# ============================================================
# API CONFIGURATION
# ============================================================

# CUSTOM: Download 2024 NFL weekly player statistics from NFLverse (CSV).
API_URL: str = "https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2024.csv"

# TODO: In your custom app, change the header user-agent value
# to something that represents your app or project.
HTTP_REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": "chiefs-2024-nfl-analysis/1.0",
    "Accept": "text/csv",
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

# TODO: In your custom app, change the output file names from case_
# to something that represents YOUR custom project.
RAW_JSON_PATH: Path = RAW_PATH / "chiefs_2024_raw.json"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "chiefs_2024_processed.csv"
