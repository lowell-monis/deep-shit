from dash import Dash, dcc, html, Input, Output
import geopandas as gpd
import plotly.express as px
import pandas as pd

dropdown_values = {
    'regions': ['North East', 'South East'],
    'years': [2021, 2022, 2023],
}

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='region dropdown',
        options=[{'label': region, 'value': region} for region in dropdown_values['regions']],
        value='South East'
    ),
    dcc.Dropdown(
        id='year dropdown',
        options=[{'label': year, 'value': year} for year in dropdown_values['years']],
        value='2022'
    ),
    html.Div([
        dcc.Graph(id='plot1'),
        dcc.Graph(id='plot2'),
    ])
])

if __name__ == '__main__':
    app.run(debug=True)