import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

from cards import (info_card, county_card, career_card, buttons_card, salary_slider_card)
from variables_and_helper_methods import (INTEREST_RATE_MONTHLY, INTEREST_RATE_ANNUAL, INSURANCE, MILES_PER_MONTH,
                                          PROPERTY_TAX, MONTHS, MPG, KWH_PER_MONTH, monthly_mortgage, monthly_gas_cost,
                                          monthly_elec_cost, monthly_healthcare_cost, load_csv)

# Create the app variable
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

# =============================================================================
# Job Salary Data (2020 to 2023)
# =============================================================================
job_salary_data = {
    "Data Scientist": {2020: 136000, 2021: 136000, 2022: 140000, 2023: 128000},
    "Web Developer": {2020: 104000, 2021: 105000, 2022: 101000, 2023: 99000},
    "Full Stack Developer": {2020: 105000, 2021: 119000, 2022: 105000, 2023: 137000},
    "Data Analyst": {2020: 82000, 2021: 88000, 2022: 94000, 2023: 100000},
    "Computer Systems Analyst": {2020: 93000, 2021: 98000, 2022: 93000, 2023: 103000}
}


# =============================================================================
# CSV Paths
# =============================================================================

PATH_MEDIAN_INCOME_LA = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\median_income\median_income_LA_county.csv"
PATH_MEDIAN_INCOME_OC = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\median_income\median_income_OC.csv"
PATH_MEDIAN_INCOME_VC = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\median_income\median_income_ventura_county.csv"

PATH_LISTING_LA = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\housing\avg_house_listing_price_LA_county.csv"
PATH_LISTING_OC = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\housing\avg_house_listing_price_OC.csv"
PATH_LISTING_VC = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\housing\avg_housing_listing_ventura_county.csv"

PATH_ELEC_LA = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\household_goods_services_etc\electricity\avg_elec_price_LA_LB_ANHM.csv"
PATH_GAS_LA = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\household_goods_services_etc\gas\avg_price_gas_LA_LB_ANHM_reg.csv"

PATH_HEALTHCARE = r"C:\Users\brevi\PycharmProjects\CS150\project-c-cs150\data\household_goods_services_etc\healthcare\healthcare_dataset.csv"


def load_county_data(county):
    if county == "LA":
        income_df = load_csv(PATH_MEDIAN_INCOME_LA)
        listing_df = load_csv(PATH_LISTING_LA)
        elec_df = load_csv(PATH_ELEC_LA)
        gas_df = load_csv(PATH_GAS_LA)
    elif county == "OC":
        income_df = load_csv(PATH_MEDIAN_INCOME_OC)
        listing_df = load_csv(PATH_LISTING_OC)
        elec_df = load_csv(PATH_ELEC_LA)  # fallback to LA
        gas_df = load_csv(PATH_GAS_LA)
    elif county == "Ventura":
        income_df = load_csv(PATH_MEDIAN_INCOME_VC)
        listing_df = load_csv(PATH_LISTING_VC)
        elec_df = load_csv(PATH_ELEC_LA)  # fallback to LA
        gas_df = load_csv(PATH_GAS_LA)
    else:
        raise ValueError(f"Unknown county: {county}")

    # Load healthcare data, rename columns, and average duplicate dates
    healthcare_df = pd.read_csv(PATH_HEALTHCARE)
    healthcare_df.rename(
        columns={"Discharge Date": "observation_date", "Billing Amount": "healthcare_cost"},
        inplace=True
    )
    healthcare_df["observation_date"] = pd.to_datetime(healthcare_df["observation_date"])
    healthcare_df = healthcare_df.groupby("observation_date", as_index=False).agg({"healthcare_cost": "mean"})

    # Merge datasets on observation_date (inner join ensures common dates)
    df = pd.merge(income_df, listing_df, on="observation_date", how="inner")
    df = pd.merge(df, elec_df, on="observation_date", how="inner")
    df = pd.merge(df, gas_df, on="observation_date", how="inner")
    df = pd.merge(df, healthcare_df, on="observation_date", how="inner")

    # Convert monthly values to annual by multiplying by 12
    df["annual_mortgage"] = monthly_mortgage(df["listing_price"]) * 12
    df["annual_gas"] = monthly_gas_cost(df["gas_price"]) * 12
    df["annual_elec"] = monthly_elec_cost(df["elec_price"]) * 12
    df["annual_healthcare"] = monthly_healthcare_cost(df["healthcare_cost"]) * 12

    df = df[[
        "observation_date",
        "median_income",  # assumed annual
        "annual_mortgage",
        "annual_gas",
        "annual_elec",
        "annual_healthcare"
    ]].copy()
    df.sort_values("observation_date", inplace=True)
    return df


def create_data_card(title, df):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                dash_table.DataTable(
                    columns=[{"name": col, "id": col} for col in df.columns],
                    data=df.to_dict("records"),
                    page_size=5,
                    style_table={"overflowX": "auto"}
                )
            )
        ],
        className="mb-4"
    )


# =============================================================================
# Create Year Slider & Bar Graph for Yearly Summary
# =============================================================================
# Use LA data as reference for year range.
df_la = load_county_data("LA")
min_year = int(df_la["observation_date"].dt.year.min())
max_year = int(df_la["observation_date"].dt.year.max())
year_marks = {year: str(year) for year in range(min_year, max_year + 1)}

yearly_bar_card = dbc.Card(
    [
        dbc.CardHeader("Yearly Summary"),
        dbc.CardBody(
            [
                dcc.Slider(
                    id="year_slider",
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=min_year,
                    marks=year_marks,
                    className="mb-3"
                ),
                dcc.Graph(id="bar_graph", style={"height": "50vh"})
            ]
        )
    ],
    className="mt-4"
)


# =============================================================================
# Define Tabs for the App
# =============================================================================

learn_card = dbc.Card(
    [
        dbc.CardHeader("Introduction"),
        dbc.CardBody(
            dcc.Markdown(
                """
                Understanding how the cost of living and median income change over time
                is crucial for financial planning and policy-making. This dashboard allows you
                to explore these trends across different counties.

                **How to Use:**
                - In the **Play** tab, use the controls to select a county and adjust your salary (or choose a career).
                - Click **Combine Expenses** to see a single trace of combined expenses along with the selected salary.
                  In this mode, the y‑axis will use the natural data range (e.g. starting around 30k).
                - Click **Reset Graph** to return to the individual expense view, forcing the y‑axis to start at 0.
                - The **Yearly Summary** shows a bar graph for a selected year, comparing data salary, user-selected salary, and combined expenses.
                - In the **Raw Data** tab, view the source datasets.
                """
            )
        ),
    ],
    className="mt-4"
)

play_tab = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        info_card,
                        county_card,
                        salary_slider_card,
                        career_card,
                        buttons_card
                    ],
                    width=3
                ),
                dbc.Col(
                    # The main line graph is outside of any Card.
                    dcc.Graph(id="cost_graph", style={"height": "70vh"}),
                    width=9
                )
            ]
        ),
        dbc.Row(
            dbc.Col(yearly_bar_card, width=12)
        )
    ],
    fluid=True
)

raw_data_card = dbc.Card(
    [
        dbc.CardHeader("Raw Data"),
        dbc.CardBody(
            html.Div(
                [
                    create_data_card("Median Income - Los Angeles County", load_csv(PATH_MEDIAN_INCOME_LA)),
                    create_data_card("Median Income - Orange County", load_csv(PATH_MEDIAN_INCOME_OC)),
                    create_data_card("Median Income - Ventura County", load_csv(PATH_MEDIAN_INCOME_VC)),
                    create_data_card("House Listing Price - Los Angeles County", load_csv(PATH_LISTING_LA)),
                    create_data_card("House Listing Price - Orange County", load_csv(PATH_LISTING_OC)),
                    create_data_card("House Listing Price - Ventura County", load_csv(PATH_LISTING_VC)),
                    create_data_card("Electricity Price - LA", load_csv(PATH_ELEC_LA)),
                    create_data_card("Gas Price - LA", load_csv(PATH_GAS_LA)),
                    create_data_card("Healthcare Dataset", pd.read_csv(PATH_HEALTHCARE))
                ]
            )
        )
    ],
    className="mt-4"
)

tabs = dbc.Tabs(
    [
        dbc.Tab(learn_card, tab_id="tab1", label="Learn"),
        dbc.Tab(play_tab, tab_id="tab2", label="Play"),
        dbc.Tab(raw_data_card, tab_id="tab3", label="Raw Data"),
    ],
    id="tabs",
    active_tab="tab2",
    className="mt-2"
)

# =============================================================================
# Main Layout
# =============================================================================
app.layout = dbc.Container(
    [
        dcc.Store(id="mode_store", data="individual"),
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Cost of Living Dashboard", className="text-center bg-primary text-white p-2"),
                    html.H5("Brevin Tating - CS150", className="text-center text-secondary p-2")
                ]
            )
        ),
        dbc.Row(
            dbc.Col(tabs, width=12, className="mt-4")
        ),
        # Footer row
        dbc.Row(
            dbc.Col(
                html.Footer(
                    html.P("9 datasets used: 8 from FRED and 1 from Kaggle", className="text-center text-muted p-2")
                ),
                width=12,
                className="mt-4"
            )
        )
    ],
    fluid=True
)


# =============================================================================
# Callbacks
# =============================================================================

# Synchronize salary slider and career dropdown:
@app.callback(
    [Output("salary_slider", "value"), Output("career_dropdown", "value")],
    [Input("salary_slider", "value"), Input("career_dropdown", "value")],
    prevent_initial_call=True
)
def sync_salary(slider_val, dropdown_val):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    triggered_id = ctx.triggered[0]["prop_id"].split('.')[0]
    if triggered_id == "salary_slider":
        return slider_val, None
    elif triggered_id == "career_dropdown":
        return 0, dropdown_val
    else:
        raise dash.exceptions.PreventUpdate


# Update graph mode (combined vs. individual) based on button clicks:
@app.callback(
    Output("mode_store", "data"),
    [Input("combine_button", "n_clicks"), Input("reset_button", "n_clicks")],
    State("mode_store", "data")
)
def update_mode(combine_n, reset_n, current_mode):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_mode or "individual"
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "combine_button":
        return "combined"
    elif button_id == "reset_button":
        return "individual"
    return current_mode


# Update the main cost graph (line graph):
@app.callback(
    Output("cost_graph", "figure"),
    [Input("county_radio", "value"),
     Input("salary_slider", "value"),
     Input("career_dropdown", "value"),
     Input("mode_store", "data")]
)
def update_line_graph(county, slider_salary, dropdown_val, mode):
    df = load_county_data(county)
    ctx = dash.callback_context

    # Determine the user's salary series: if a career is selected, build a time series; else, constant.
    if dropdown_val is not None:
        # Build a time series for the selected job using job_salary_data
        user_salary_series = []
        for date in df["observation_date"]:
            year = date.year
            salary = job_salary_data[dropdown_val].get(year, job_salary_data[dropdown_val][2023])
            user_salary_series.append(salary)
    else:
        user_salary_series = [slider_salary] * len(df["observation_date"])

    # For the constant average in combined mode (if no dropdown), compute the average:
    avg_salary = sum(user_salary_series) / len(user_salary_series)

    fig = go.Figure()

    def create_trace(x, y, name, line_style=dict(), mode="lines+markers", hover_format="${:,.2f}"):
        hover_text = []
        for val in y:
            if pd.isna(val):
                hover_text.append("No data for this date")
            else:
                hover_text.append(hover_format.format(val))
        return go.Scatter(
            x=x,
            y=y,
            mode=mode,
            name=name,
            line=line_style,
            hovertext=hover_text,
            hoverinfo="text+x"
        )

    if mode == "combined":
        combined_expenses = df["annual_mortgage"] + df["annual_gas"] + df["annual_elec"] + df["annual_healthcare"]
        fig.add_trace(create_trace(df["observation_date"], combined_expenses, "Combined Expenses"))
        fig.add_trace(create_trace(df["observation_date"], df["median_income"], "Median Income"))
        # In combined mode, if a career is selected, show the time series; otherwise, show a constant trace.
        if dropdown_val is not None:
            fig.add_trace(create_trace(df["observation_date"], user_salary_series, "Selected Salary",
                                       line_style=dict(dash="dash")))
        else:
            salary_x = [df["observation_date"].min(), df["observation_date"].max()]
            salary_y = [slider_salary, slider_salary]
            fig.add_trace(go.Scatter(
                x=salary_x,
                y=salary_y,
                mode="lines",
                name="Selected Salary",
                line=dict(dash="dash"),
                hovertemplate="Salary: ${:,.2f}".format(slider_salary)
            ))
        # In combined mode, let y-axis auto-scale (it may start near 30k)
    else:
        fig.add_trace(create_trace(df["observation_date"], df["annual_mortgage"], "Annual Mortgage"))
        fig.add_trace(create_trace(df["observation_date"], df["annual_gas"], "Annual Gas"))
        fig.add_trace(create_trace(df["observation_date"], df["annual_elec"], "Annual Electricity"))
        fig.add_trace(create_trace(df["observation_date"], df["annual_healthcare"], "Annual Healthcare"))
        fig.add_trace(create_trace(df["observation_date"], df["median_income"], "Median Income"))
        if dropdown_val is not None:
            fig.add_trace(create_trace(df["observation_date"], user_salary_series, "Selected Salary",
                                       line_style=dict(dash="dash")))
        else:
            salary_x = [df["observation_date"].min(), df["observation_date"].max()]
            salary_y = [slider_salary, slider_salary]
            fig.add_trace(go.Scatter(
                x=salary_x,
                y=salary_y,
                mode="lines",
                name="Selected Salary",
                line=dict(dash="dash"),
                hovertemplate="Salary: ${:,.2f}".format(slider_salary)
            ))
        max_val = max(
            df["annual_mortgage"].max(),
            df["annual_gas"].max(),
            df["annual_elec"].max(),
            df["annual_healthcare"].max(),
            df["median_income"].max(),
            avg_salary
        )
        fig.update_layout(yaxis_range=[0, max_val * 1.1])

    fig.update_layout(
        title=f"Annual Costs & Income in {county} County",
        xaxis=dict(title="Date", tickformat="%b %d, %Y", tickmode="auto"),
        yaxis_title="Annual Amount (USD)",
        legend=dict(x=0, y=1.05, orientation="h"),
        hovermode="closest"
    )
    return fig


# Update the bar graph (yearly summary visualization):
@app.callback(
    Output("bar_graph", "figure"),
    [Input("county_radio", "value"),
     Input("salary_slider", "value"),
     Input("career_dropdown", "value"),
     Input("year_slider", "value")]
)
def update_bar_graph(county, slider_salary, dropdown_val, selected_year):
    df = load_county_data(county)
    ctx = dash.callback_context
    if dropdown_val is not None:
        user_salary = job_salary_data[dropdown_val].get(selected_year, job_salary_data[dropdown_val][2023])
        categories = ["Median Salary", dropdown_val, "Combined Expenses"]

    else:
        user_salary = slider_salary
        categories = ["Median Salary", "User Selected Salary", "Combined Expenses"]

    df_year = df[df["observation_date"].dt.year == selected_year]
    if df_year.empty:
        data_salary = 0
        combined_expenses = 0
    else:
        data_salary = df_year["median_income"].mean()
        combined_expenses = (df_year["annual_mortgage"] + df_year["annual_gas"] +
                             df_year["annual_elec"] + df_year["annual_healthcare"]).mean()
    values = [data_salary, user_salary, combined_expenses]
    bar_fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        text=[f"${v:,.2f}" for v in values],
        textposition='auto'
    )])
    bar_fig.update_layout(title=f"Yearly Summary for {selected_year}",
                          yaxis_title="Annual Amount (USD)",
                          xaxis_title="")
    return bar_fig


if __name__ == "__main__":
    app.run(debug=True)
