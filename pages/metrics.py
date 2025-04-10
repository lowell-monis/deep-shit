from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash

metric_mapping = {
    'Likes': 'video_like_count',
    'Views': 'video_view_count', 
    'Shares': 'video_share_count'
}

# Changed path to '/metrics' since home.py will be at '/'
dash.register_page(__name__, name="Engagement Metrics", path='/metrics')

layout = html.Div(style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("Engagement Metrics Dashboard", style={'color': 'white'}),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[{'label': key, 'value': key} for key in metric_mapping.keys()],
        value='Likes',
        style={'color': 'black', 'width': '50%', 'marginBottom': '20px'}
    ),
    html.Div([
        dcc.Graph(id='plot1', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='plot2', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ])
])

@callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure')],
    Input('metric-dropdown', 'value')
)
def update_figures(selected_metric):
    try:
        data = pd.read_csv('data/tiktok_dataset.csv')
        column_name = metric_mapping[selected_metric]
        filtered_data = data[['claim_status', column_name]]
        
        fig1 = px.bar(filtered_data, x='claim_status', y=column_name, 
                     title=f'{selected_metric} by Claim Status',
                     template='plotly_dark')
        
        fig2 = px.histogram(filtered_data, x=column_name, color='claim_status',
                           title=f'Distribution of {selected_metric}',
                           template='plotly_dark')
        
        for fig in [fig1, fig2]:
            fig.update_layout(
                paper_bgcolor='black',
                plot_bgcolor='black',
                font_color='white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
        
        return fig1, fig2
    except Exception as e:
        print(f"Error loading data: {e}")
        return px.scatter(title="Error loading data"), px.scatter(title="Error loading data")