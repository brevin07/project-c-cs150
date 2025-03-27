import dash_bootstrap_components as dbc
from dash import dcc

# =============================================================================
# Define Individual Cards for the Play Tab Controls
# =============================================================================

info_card = dbc.Card(
    dbc.CardBody(
        dcc.Markdown(
            """
            **Cost of Living**  
            Explore how living expenses compare with median incomes across different counties.
            Adjust the salary (or choose a career) to see how combined expenses stack up over time.
            """
        )
    ),
    className="mt-4"
)

county_card = dbc.Card(
    [
        dbc.CardHeader("Select a County"),
        dbc.CardBody(
            dcc.RadioItems(
                id="county_radio",
                options=[
                    {"label": "Los Angeles County", "value": "LA"},
                    {"label": "Orange County", "value": "OC"},
                    {"label": "Ventura County", "value": "Ventura"}
                ],
                value="LA",
                className="mb-2"
            )
        ),
    ],
    className="mt-4"
)

salary_slider_card = dbc.Card(
    [
        dbc.CardHeader("Choose Your Salary"),
        dbc.CardBody(
            dcc.Slider(
                id="salary_slider",
                min=35000,
                max=300000,
                step=5000,
                value=35000,
                marks={
                    35000: "35k",
                    60000: "60k",
                    90000: "90k",
                    120000: "120k",
                    150000: "150k",
                    180000: "180k",
                    210000: "210k",
                    240000: "240k",
                    270000: "270k",
                    300000: "300k"
                },
                className="mb-2"
            )
        ),
    ],
    className="mt-4"
)

career_card = dbc.Card(
    [
        dbc.CardHeader("OR Pick a Career"),
        dbc.CardBody(
            dcc.Dropdown(
                id="career_dropdown",
                options=[
                    {"label": "Data Scientist", "value": "Data Scientist"},
                    {"label": "Web Developer", "value": "Web Developer"},
                    {"label": "Full Stack Developer", "value": "Full Stack Developer"},
                    {"label": "Data Analyst", "value": "Data Analyst"},
                    {"label": "Computer Systems Analyst", "value": "Computer Systems Analyst"}
                ],
                placeholder="Select a career",
                className="mb-2"
            )
        ),
    ],
    className="mt-4"
)

buttons_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Button("Combine Expenses", id="combine_button", color="primary", n_clicks=0, className="mr-2"),
            dbc.Button("Reset Graph", id="reset_button", color="secondary", n_clicks=0, className="mt-2")
        ]
    ),
    className="mt-4"
)
