import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Sample geospatial data
data = {
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Lat': [40.712776, 34.052235, 41.878113, 29.760427, 33.448376],
    'Lon': [-74.005974, -118.243683, -87.629799, -95.369804, -112.074036],
    'Population': [8398748, 3980802, 2716000, 2320259, 1680992]
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Geospatial Dashboard"),
    dcc.Graph(id='map-graph'),
    html.Div([
        html.Label("Select minimum population:"),
        dcc.Input(id='population-input', type='number', value=2000000)
    ]),
])

# Define callback to update the map based on the population input
@app.callback(
    Output('map-graph', 'figure'),
    [Input('population-input', 'value')]
)
def update_map(min_population):
    filtered_df = df[df['Population'] >= min_population]

    fig = px.scatter_mapbox(
        filtered_df,
        lat='Lat',
        lon='Lon',
        hover_name='City',
        size='Population',
        mapbox_style='carto-positron',
        zoom=3,
        size_max=40
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)