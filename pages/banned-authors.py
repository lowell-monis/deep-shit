from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash

dash.register_page(__name__, name="Banned Authors", path='/banned-authors')

layout = html.Div(style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("Author Ban Status Analysis", style={'color': 'white'}),
    dcc.Graph(id='ban-claims'),
    dcc.Graph(id='ban-views')
])

@callback(
    [Output('ban-claims', 'figure'),
     Output('ban-views', 'figure')],
    Input('ban-claims', 'id')
)
def update_ban_graphs(_):
    df = pd.read_csv('data/tiktok_dataset.csv').dropna(subset=['author_ban_status', 'claim_status', 'video_view_count'])

    fig1 = px.histogram(df, x="author_ban_status", color="claim_status", barmode="group", title="Claim Status by Author Ban Status", template='plotly_dark')
    fig2 = px.box(df, x="author_ban_status", y="video_view_count", color="claim_status", title="Views by Author Ban Status", template='plotly_dark')

    for fig in [fig1, fig2]:
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

    return fig1, fig2
