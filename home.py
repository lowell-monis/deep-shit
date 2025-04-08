from dash import Dash, dcc, html, Input, Output
import geopandas as gpd
import plotly.express as px
import pandas as pd

metric_mapping = {
    'Likes': 'video_like_count',
    'Views': 'video_view_count', 
    'Shares': 'video_share_count'
}

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='metric-dropdown',
        options=[{'label': key, 'value': key} for key in metric_mapping.keys()],
        value='Likes'
    ),
    html.Div([
        dcc.Graph(id='plot1'),
        dcc.Graph(id='plot2'),
    ])
])

@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure')],
     [Input('metric-dropdown', 'value')]
)
def update_figures(selected_metric):
    csv_file_path = 'data/tiktok_dataset.csv'
    data = pd.read_csv(csv_file_path)
    
    column_name = metric_mapping[selected_metric]
    
    filtered_data = data[['claim_status', column_name]]
    
    fig1 = px.bar(filtered_data, x='claim_status', y=column_name, 
                 title=f'{selected_metric} by Claim Status')
    
    fig2 = px.histogram(filtered_data, x=column_name, color='claim_status',
                       title=f'Distribution of {selected_metric}')
    
    return fig1, fig2

if __name__ == '__main__':
    app.run(debug=True)