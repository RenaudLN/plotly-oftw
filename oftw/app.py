import dash_mantine_components as dmc
from dash import Dash, dcc, page_container

app = Dash(
    __name__,
    external_stylesheets=dmc.styles.ALL,
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Group(
                                [
                                    dmc.Image(src="assets/oftw-logo.png", h="2.5rem"),
                                    dmc.Text("OFTW Pledge Tracker", size="md", fw="bold"),
                                ],
                                gap="sm",
                            ),
                            href="/",
                            c="inherit",
                            underline="none",
                        ),
                        dmc.Switch(color="yellow", size="lg", checked=True),
                    ],
                    justify="space-between",
                    px="1.5rem",
                    h="100%",
                )
            ),
            dmc.AppShellMain(
                dcc.Loading(
                    page_container,
                    custom_spinner=dmc.Loader(),
                    delay_show=500,
                    parent_style={"flex": 1},
                    overlay_style={"visibility": "visible", "filter": "blur(3px)"},
                ),
                style={"display": "flex", "flexDirection": "column"},
            ),
        ],
        header={"height": "4rem"},
    ),
)


if __name__ == "__main__":
    app.run(debug=True)
