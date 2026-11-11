"""stage03_transform.py.

(EDIT YOUR VERSION OF THIS FILE)

Source: validated JSON object
Sink: Polars DataFrame

Purpose

  Transform validated JSON data into a structured format.

Analytical Questions

- Which fields are needed from the JSON data?
- How can records be normalized into tabular form?
- What derived fields would support analysis?

Edit your Python file to:
- extract the fields needed for your analysis,
- normalize records into a consistent structure,
- create any derived fields required.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
from typing import Any

import polars as pl

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    json_data: list[dict[str, Any]],
    LOG: logging.Logger,
) -> pl.DataFrame:
    """Transform JSON into a structured DataFrame.

    Args:
        json_data (list[dict[str, Any]]): Validated JSON data.
        LOG (logging.Logger): The logger instance.

    Returns:
        pl.DataFrame: The transformed dataset.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    # CUSTOM MODIFICATION: 2024 CHIEFS PLAYER STATISTICS
    records: list[dict[str, Any]] = []

    for record in json_data:
        records.append(
            {
                "player_name": record["player_display_name"],
                "team": record["team"],
                "season": record["season"],
                "week": record["week"],
                "opponent": record["opponent_team"],
                "position": record["position"],
                "passing_yards": record["passing_yards"],
                "rushing_yards": record["rushing_yards"],
                "receiving_yards": record["receiving_yards"],
                "passing_tds": record["passing_tds"],
                "rushing_tds": record["rushing_tds"],
                "receiving_tds": record["receiving_tds"],
            }
        )

    df: pl.DataFrame = pl.DataFrame(records)

    # Calculate combined player statistical categories.
    df = df.with_columns(
        [
            (
                pl.col("passing_yards")
                + pl.col("rushing_yards")
                + pl.col("receiving_yards")
            ).alias("total_offensive_yards"),
            (
                pl.col("passing_tds") + pl.col("rushing_tds") + pl.col("receiving_tds")
            ).alias("total_touchdowns"),
        ]
    )

    LOG.info("Chiefs player statistics transformation completed.")
    LOG.info(f"Total player-game records: {df.height}")
    LOG.info(f"Total passing yards: {df['passing_yards'].sum()}")
    LOG.info(f"Total rushing yards: {df['rushing_yards'].sum()}")
    LOG.info(f"Total receiving yards: {df['receiving_yards'].sum()}")
    LOG.info(f"Total player statistical touchdowns: {df['total_touchdowns'].sum()}")
    LOG.info("Transformation complete.")
    LOG.info(f"DataFrame preview:\n{df.head()}")
    LOG.info("Sink: Polars DataFrame created")

    # Return the transformed DataFrame for use in the next stage.
    return df
