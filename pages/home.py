from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import dash

dash.register_page(__name__, path='/', name="Home")

try:
    tiktok_clean = pd.read_csv('data/tiktok_dataset.csv')
except:
    tiktok_clean = pd.DataFrame()

def create_sankey_figure(df):
    if df.empty:
        return go.Figure()
    
    source, target, value, colors, node_labels = [], [], [], [], []
    categories = ['claim_status', 'verified_status', 'author_ban_status']
    
    # TikTok color palette
    tiktok_pink = '#FF0050'
    tiktok_aqua = '#00F2EA'
    tiktok_black = '#000000'
    tiktok_gray = '#333333'
    tiktok_white = '#FFFFFF'
    tiktok_magenta = '#de8c9d'
    tiktok_blue = '#397684'
    
    flow_colors = {
        'claim': tiktok_magenta,
        'opinion': tiktok_blue,
        'not verified': tiktok_pink,
        'verified': tiktok_aqua
    }
    
    # Node labels (simplified formatting)
    node_map = {}
    index = 0
    for col in categories:
        for label in df[col].unique():
            node_map[(col, label)] = index
            # Cleaner label formatting (removes "status" redundancy)
            clean_col = col.replace('_status', '')
            node_labels.append(f"{clean_col}: {label}")
            index += 1
    
    # Build flow data
    for i in range(len(categories)-1):
        col1, col2 = categories[i], categories[i+1]
        flow_data = df.groupby([col1, col2]).size().reset_index(name='count')
        
        for _, row in flow_data.iterrows():
            source.append(node_map[(col1, row[col1])])
            target.append(node_map[(col2, row[col2])])
            value.append(row['count'])
            colors.append(flow_colors.get(row[col1], tiktok_gray))
    
    # Create Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color=tiktok_black, width=0.8),
            label=node_labels,
            color=tiktok_gray,  # Node color
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=colors,
            hovertemplate='From %{source.label}<br>To %{target.label}<br>Count: %{value}<extra></extra>'
        )
    ))
    
    # TikTok-styled layout
    fig.update_layout(
        font_family='Garamond, serif',
        font_size=14,
        font_color=tiktok_white,
        paper_bgcolor=tiktok_black,
        plot_bgcolor=tiktok_black,
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        hoverlabel=dict(
            font_family='Garamond',
            bgcolor=tiktok_black,
            font_color=tiktok_white
        )
    )
    
    return fig

layout = html.Div(
    style={
        'backgroundColor': 'black', 
        'padding': '20px',
        'display': 'flex',          # Enables flexible container
        'flexDirection': 'column',  # Stacks children vertically
        'alignItems': 'flex-end'    # Right-aligns children (including graph)
    }, 
    children=[
        html.H1(
            "Is TikTok doing its job?", 
            style={
                'fontFamily': '"Garamond", sans-serif', 
                'color': 'white',
                'marginRight': '20px'  # Aligns text with right-aligned graph
            }
        ),
        dcc.Graph(
            id='sankey-graph',
            figure=create_sankey_figure(tiktok_clean),
            style={
                'height': '60vh',       # Reduced from 80vh
                'width': '50%',        # Constrains width
                'marginLeft': 'auto'    # Pushes graph to right
            }
        )
    ]
)