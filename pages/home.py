from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import dash

dash.register_page(__name__, path='/', name="Home")

# Load data
try:
    tiktok_clean = pd.read_csv('data/tiktok_dataset.csv')
except:
    tiktok_clean = pd.DataFrame()  # Fallback empty dataframe

def create_sankey_figure(df):
    if df.empty:
        return go.Figure()
    
    source, target, value, colors, node_labels = [], [], [], [], []
    categories = ['claim_status', 'verified_status', 'author_ban_status']
    
    # Create node mapping
    node_map = {}
    index = 0
    for col in categories:
        for label in df[col].unique():
            node_map[(col, label)] = index
            node_labels.append(f"{col}: {label}")
            index += 1
    
    # Define colors
    flow_colors = {
        'claim': '#FF6384', 
        'opinion': '#36A2EB',
        'not verified': '#4BC0C0',
        'verified': '#9966FF'
    }
    
    # Create links
    for i in range(len(categories)-1):
        col1, col2 = categories[i], categories[i+1]
        flow_data = df.groupby([col1, col2]).size().reset_index(name='count')
        
        for _, row in flow_data.iterrows():
            source.append(node_map[(col1, row[col1])])
            target.append(node_map[(col2, row[col2])])
            value.append(row['count'])
            colors.append(flow_colors.get(row[col1], '#BEC2CB'))
    
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color='#333333'
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=colors
        )
    ))
    
    fig.update_layout(
        font_size=12,
        paper_bgcolor='black',
        plot_bgcolor='black',
        font_color='white',
        height=700
    )
    
    return fig

layout = html.Div(style={'backgroundColor': 'black', 'padding': '20px'}, children=[
    html.H1("Is TikTok doing its job?", style={'color': 'white'}),
    dcc.Graph(
        id='sankey-graph',
        figure=create_sankey_figure(tiktok_clean),
        style={'height': '80vh'}
    )
])