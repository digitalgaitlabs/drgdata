from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("drg_data.csv")

app = Dash(__name__)
server = app.server  # for gunicorn

app.layout = html.Div([
    html.H1("DRG Inpatient Pricing and Rehab Mapping", style={"textAlign": "center"}),
    html.Div([
        html.Label("Filter by Rehab Category:"),
        dcc.Dropdown(
            options=[{"label": cat, "value": cat} for cat in sorted(df["Rehab Category"].dropna().unique())],
            id="category-filter",
            value=None,
            placeholder="Select a rehab category"
        ),
    ], style={"width": "50%", "margin": "auto"}),
    html.Br(),
    dash_table.DataTable(
        id="drg-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'maxWidth': '200px'},
        filter_action="native",
        sort_action="native"
    ),
    html.Br(),
    dcc.Graph(id="cost-chart")
])

@app.callback(
    [Output("drg-table", "data"),
     Output("cost-chart", "figure")],
    [Input("category-filter", "value")]
)
def update_dashboard(selected_category):
    if selected_category:
        filtered_df = df[df["Rehab Category"] == selected_category]
    else:
        filtered_df = df

    fig = px.bar(
        filtered_df.sort_values("Price (€)", ascending=False).head(20),
        x="Description",
        y="Price (€)",
        color="Rehab Category",
        title="Top 20 DRG Prices by Description",
        labels={"Price (€)": "Inpatient Price (€)", "Description": "DRG Description"}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return filtered_df.to_dict("records"), fig

if __name__ == "__main__":
    app.run_server(debug=True)