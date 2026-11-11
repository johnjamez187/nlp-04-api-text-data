"""stage01_extract.py - Stage 01: Extract.

CUSTOMIZED: Extract 2024 Kansas City Chiefs player statistics.

Source: API
Sink: raw JSON object + raw JSON file

The Extract stage is responsible for retrieving data
from the source (in this case, an API)
and saving it to a file.
It also returns the extracted data as a Python object
for use in subsequent stages.

Notes:
- This file should not require modification.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

from io import StringIO
import json
import logging
from pathlib import Path
from typing import Any

from datafun_toolkit.logger import log_path
import polars as pl
import requests

# ============================================================
# Section 2. Define Run Extract Function
# ============================================================


def run_extract(
    source_api_url: str,
    http_request_headers: dict[str, str],
    raw_json_path: Path,
    LOG: logging.Logger,
) -> Any:
    """Extract NFL CSV data and save Chiefs records as JSON.

    Args:
        source_api_url (str): The URL of the API endpoint.
        http_request_headers (dict[str, str]): The HTTP request headers.
        raw_json_path (Path): The path to save the raw JSON file.
        LOG (logging.Logger): The logger instance.

    Returns:
        Any: The extracted JSON data as a Python object (e.g., a list or dictionary).

    Raises:
        requests.HTTPError: If the HTTP request to the API fails.
        requests.RequestException: For other types of request exceptions.
        ValueError: If the response content cannot be parsed as JSON.
    """
    LOG.info("========================")
    LOG.info("STAGE 01: EXTRACT starting... ")
    LOG.info("========================")

    # Use the requests.get() function to make an HTTP GET request
    # to the source_api_url with the provided headers.
    response = requests.get(source_api_url, headers=http_request_headers, timeout=30)

    # Use the raise_for_status() method to check for HTTP errors
    # and raise an exception if the request was unsuccessful.
    response.raise_for_status()

    # Read the NFLverse CSV response and convert Chiefs records to JSON.

    # ============================================================
    # CUSTOM MODIFICATION: EXTRACT CHIEFS NFL STATISTICS
    # ============================================================

    # Read the NFL statistics CSV from the API response.
    df = pl.read_csv(
        StringIO(response.text),
        infer_schema_length=None,
    )

    # Filter for Kansas City Chiefs players.
    # Keep Chiefs records that identify an individual player.
    chiefs_df = df.filter(
        (pl.col("team") == "KC")
        & pl.col("player_display_name").is_not_null()
        & (pl.col("player_display_name").str.strip_chars() != "")
    )

    # Convert the filtered records into JSON-compatible dictionaries.
    json_data: Any = chiefs_df.to_dicts()
    # Save the Chiefs records as JSON for the Validate stage.
    raw_json_path.write_text(
        json.dumps(json_data, indent=2),
        encoding="utf-8",
    )

    LOG.info(f"Total NFL records retrieved: {df.height}")
    LOG.info(f"Chiefs player-game records extracted: {chiefs_df.height}")

    # Use log.info() to log the source API URL (a string).
    # Use a formatted string (f-string) to include the variable in the log message.
    LOG.info(f"SOURCE PATH = {source_api_url}")

    # Use the privacy-conscious
    # log_path function to log the sink path.
    log_path(LOG, "SINK PATH", raw_json_path)

    # Return the extracted JSON data as a Python object (e.g., a list or dictionary).
    return json_data
