"""stage02_validate.py.

(EDIT YOUR VERSION OF THIS FILE)

Source: raw JSON object
Sink: validated JSON object

Purpose

  Inspect JSON structure and validate that the data is usable.

Analytical Questions

- What is the top-level structure of the JSON data?
- What keys are present in each record?
- What data types are associated with each field?
- Does the data meet expectations for transformation?

Edit your Python file to:
- inspect the JSON structure for your API,
- validate required keys and types,
- confirm the data is usable for your analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
from typing import Any

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    json_data: Any,
    LOG: logging.Logger,
) -> list[dict]:
    """Inspect and validate JSON structure."""
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT JSON STRUCTURE
    # ============================================================

    LOG.info("JSON STRUCTURE INSPECTION:")
    LOG.info(f"Top-level type: {type(json_data).__name__}")

    if isinstance(json_data, list) and len(json_data) > 0:
        first_record = json_data[0]

        LOG.info(f"Total records received: {len(json_data)}")

        if isinstance(first_record, dict):
            LOG.info(f"Keys in first record: {list(first_record.keys())}")

            LOG.info("Field types:")
            for key, value in first_record.items():
                LOG.info(f"{key}: {type(value).__name__}")

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    if not isinstance(json_data, list):
        raise TypeError("Expected JSON data to be a list of records.")

    if len(json_data) == 0:
        raise ValueError("Expected at least one record.")

    if not all(isinstance(record, dict) for record in json_data):
        raise ValueError("Expected each record to be a dictionary.")

    # ============================================================
    # CUSTOM MODIFICATION: VALIDATE API POST FIELDS
    # ============================================================

    required_fields = {
        "player_display_name": str,
        "team": str,
        "season": int,
        "week": int,
        "passing_yards": int,
        "rushing_yards": int,
        "receiving_yards": int,
        "passing_tds": int,
        "rushing_tds": int,
        "receiving_tds": int,
    }

    for index, record in enumerate(json_data, start=1):
        for field, expected_type in required_fields.items():
            if field not in record:
                raise ValueError(f"Record {index} is missing required field: {field}")

            if type(record[field]) is not expected_type:
                raise TypeError(
                    f"Record {index}: {field} must be {expected_type.__name__}"
                )

    LOG.info(f"Successfully validated {len(json_data)} Chiefs records.")
    LOG.info("All required fields and data types are correct.")

    LOG.info("Validation passed.")
    LOG.info("Sink: validated JSON object")

    # Return validated data for the Transform stage.
    return json_data
