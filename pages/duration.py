from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash

dash.register_page(__name__, name="Duration Dynamics", path="/duration")

df = pd.read_csv('data/tiktok_dataset.csv')
df = df[df['video_duration_sec'].notna() & df['claim_status'].isin(['claim', 'opinion'])]

fig_density = px.histogram(
    df,
    x="video_duration_sec",
    color="claim_status",
    marginal="rug",
    nbins=50,
    histnorm="probability density",
    opacity=0.6,
    barmode="overlay",
    labels={
        "video_duration_sec": "Video Duration (seconds)",
        "claim_status": "Content Type"
    },
    title="Distribution of Video Duration by Claim Status",
    color_discrete_map={'claim': '#FF0050', 'opinion': '#00F2EA'}
)

fig_density.update_layout(
    template="plotly_dark",
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white'
)

layout = html.Div(className='main-container', children=[
    html.H1("Duration Density Analysis"),
    dcc.Graph(figure=fig_density, className='point-plot-graph')
])
