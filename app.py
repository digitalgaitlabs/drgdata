from dash import Dash, dash_table, html
import pandas as pd

# Load data (assumes drg_data.csv is in the same directory)
df = pd.read_csv("drg_data.csv")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

app = Dash(__name__)
server = app.server  # for Render deployment

app.layout = html.Div([
    html.H1("DRG Table Explorer", style={"textAlign": "center"}),
    dash_table.DataTable(
        id='drg-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=20,
        filter_action="native",
        sort_action="native",
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '120px', 'maxWidth': '300px'},
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
