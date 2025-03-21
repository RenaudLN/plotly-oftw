from enum import Enum
from functools import lru_cache
from io import StringIO

import polars as pl
import requests

pledges_path = "https://storage.googleapis.com/plotly-app-challenge/one-for-the-world-pledges.json"
payments_path = "https://storage.googleapis.com/plotly-app-challenge/one-for-the-world-payments.json"


class PledgeStatus(str, Enum):
    """Donor status enum."""

    ACTIVE_DONOR = "Active donor"
    PAYMENT_FAILURE = "Payment failure"
    CHURNED_DONOR = "Churned donor"
    ONE_TIME = "One-Time"
    PLEDGED_DONOR = "Pledged donor"
    UPDATED = "Updated"
    ERROR = "ERROR"

    _column = "pledge_status"

    @classmethod
    def active_statuses(cls):
        """Return list of active statuses."""
        return [cls.ACTIVE_DONOR.value, cls.PLEDGED_DONOR.value]


@lru_cache
def get_pledges():
    """Retrieve pledges data and sanitise it."""
    pledges_data = pl.read_json(StringIO(requests.get(pledges_path, timeout=30).text))
    str_cols = [col for col, dtype in pledges_data.schema.items() if dtype == pl.String]
    date_cols = ["pledge_created_at", "pledge_starts_at", "pledge_ended_at"]
    pledges_data = pledges_data.with_columns(pl.col(col).replace("", None) for col in str_cols).with_columns(
        pl.col(col).str.to_date("%Y-%m-%d") for col in date_cols
    )
    return pledges_data


@lru_cache
def get_payments():
    """Retrieve payments data and sanitise it."""
    payments_data = pl.read_json(StringIO(requests.get(payments_path, timeout=30).text))
    str_cols = [col for col, dtype in payments_data.schema.items() if dtype == pl.String]
    date_cols = ["date"]
    payments_data = payments_data.with_columns(pl.col(col).replace("", None) for col in str_cols).with_columns(
        pl.col(col).str.to_date("%Y-%m-%d") for col in date_cols
    )
    return payments_data
