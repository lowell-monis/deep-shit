from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash

dash.register_page(__name__, name="Claim vs Verification", path='/claim-verification')

layout = html.Div(style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("Claim Status vs Creator Verification", style={'color': 'white'}),
    dcc.Graph(id='claim-verified-graph')
])

@callback(
    Output('claim-verified-graph', 'figure'),
    Input('claim-verified-graph', 'id')
)
def update_graph(_):
    data = pd.read_csv('data/tiktok_dataset.csv')
    fig = px.histogram(
        data,
        x="verified_status",
        color="claim_status",
        barmode="group",
        title="Claim Status by Creator Verification",
        template='plotly_dark'
    )
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    return fig
