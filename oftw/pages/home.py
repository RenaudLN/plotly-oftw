import dash_mantine_components as dmc
import polars as pl
from dash import register_page
from dash_pydantic_utils import Quantity

from oftw.data import PledgeStatus, get_pledges

register_page(__name__, path="/", title="OFTW Pledge Tracker")


def metric_card(label: str, value: str | int | float):
    """A simple metric card."""
    return dmc.Card(
        dmc.Stack(
            [
                dmc.Text(value, size="xl", fw="bold"),
                dmc.Text(label),
            ],
            align="center",
            gap="sm",
        ),
        withBorder=True,
        radius="md",
        p="md",
        shadow="lg",
    )


def layout():
    """The layout for the home page."""
    pledges = get_pledges()
    active_pledges = pledges.filter(pl.col(PledgeStatus._column).is_in(PledgeStatus.active_statuses()))

    ongoing_donations = (
        active_pledges.group_by("currency")
        .agg(pl.sum("contribution_amount"))
        .map_rows(lambda row: (Quantity(row[1], row[0]).to("USD").value,))
        .sum()
        .item()
    )
    return dmc.Box(
        [
            dmc.Title("Pledges", order=3, mb="1rem"),
            dmc.SimpleGrid(
                cols=3,
                children=[
                    metric_card(
                        "Active Pledges",
                        active_pledges.n_unique("pledge_id"),
                    ),
                    metric_card(
                        "Ongoing Donations",
                        f"US${ongoing_donations:,.0f}",
                    ),
                ],
            ),
        ],
        p="1rem 1.5rem",
    )
