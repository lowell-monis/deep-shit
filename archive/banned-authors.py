from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash

dash.register_page(__name__, name="Banned Authors", path='/banned-authors')

# Load data
df = pd.read_csv('data/tiktok_dataset.csv')

# Clean and preprocess relevant columns
df = df.dropna(subset=['author_ban_status', 'claim_status', 'video_view_count', 'verified_status'])

# Engagement metric options
engagement_options = {
    'video_view_count': 'Views',
    'video_like_count': 'Likes',
    'video_comment_count': 'Comments',
    'video_share_count': 'Shares',
    'video_download_count': 'Downloads'
}

layout = html.Div(className='main-container', children=[
    html.H1("Author Ban & Verification Analysis"),
    
    html.Div(className='filter-container', children=[
        html.Label("Group By"),
        dcc.Dropdown(
            id='group-dropdown',
            options=[
                {'label': 'Author Ban Status', 'value': 'author_ban_status'},
                {'label': 'Verified Status', 'value': 'verified_status'}
            ],
            value='author_ban_status',
            className='color-dropdown'
        ),
        html.Label("Claim Type Filter"),
        dcc.Dropdown(
            id='claim-dropdown',
            options=[
                {'label': 'Both', 'value': 'both'},
                {'label': 'Claim Only', 'value': 'claim'},
                {'label': 'Opinion Only', 'value': 'opinion'}
            ],
            value='both',
            className='filter-dropdown'
        ),
        html.Label("Engagement Metric (for Box Plot)"),
        dcc.Dropdown(
            id='engagement-dropdown',
            options=[{'label': name, 'value': col} for col, name in engagement_options.items()],
            value='video_view_count',
            className='axis-dropdown'
        ),
    ]),

    html.Div(className='plot-container', children=[
        dcc.Graph(id='bar-plot'),
        dcc.Graph(id='box-plot')
    ])
])

@callback(
    Output('bar-plot', 'figure'),
    Output('box-plot', 'figure'),
    Input('group-dropdown', 'value'),
    Input('claim-dropdown', 'value'),
    Input('engagement-dropdown', 'value')
)
def update_plots(group_col, claim_filter, engagement_metric):
    filtered = df.copy()

    if claim_filter == 'claim':
        filtered = filtered[filtered['claim_status'] == 'claim']
    elif claim_filter == 'opinion':
        filtered = filtered[filtered['claim_status'] == 'opinion']

    # Bar Plot
    bar_df = filtered.groupby([group_col, 'claim_status']).size().reset_index(name='count')

    bar_df['hover'] = bar_df.apply(
        lambda row: f"{row['count']} videos making {row['claim_status']}s have their authors under review"
        if group_col == 'author_ban_status' else
        f"{row['count']} videos making {row['claim_status']}s were uploaded by {row[group_col]} creators",
        axis=1
    )

    fig_bar = px.bar(
        bar_df,
        x=group_col,
        y='count',
        color='claim_status',
        text='count',
        hover_data={'hover': True},
        labels={group_col: 'Group', 'count': 'Number of Videos'},
        color_discrete_map={'claim': '#FF0050', 'opinion': '#00F2EA'},
        barmode='group',
        title="Claim Type Distribution by Group"
    )

    fig_bar.update_traces(hovertemplate='%{customdata[0]}<extra></extra>', customdata=bar_df[['hover']])
    fig_bar.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        title_font_color='white'
    )

    # Box Plot
    fig_box = px.box(
        filtered,
        x=group_col,
        y=engagement_metric,
        color='claim_status',
        points='all',
        labels={
            group_col: 'Group',
            engagement_metric: engagement_options[engagement_metric],
            'claim_status': 'Claim Status'
        },
        color_discrete_map={'claim': '#FF0050', 'opinion': '#00F2EA'},
        title=f"{engagement_options[engagement_metric]} by {group_col.replace('_', ' ').title()} and Claim Status"
    )

    fig_box.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        title_font_color='white',
        boxmode='group'
    )

    return fig_bar, fig_box
