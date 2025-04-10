from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)

button_style = {
    'backgroundColor': '#444',
    'color': 'white',
    'border': '1px solid #555',
    'padding': '10px 20px',
    'margin': '5px',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'transition': 'all 0.3s ease',
    'fontWeight': 'bold'
}

button_hover_style = {
    'backgroundColor': '#666',
    'transform': 'scale(1.05)'
}

app.layout = html.Div(style={'backgroundColor': 'black', 'minHeight': '100vh'}, children=[
    html.Div(style={
        'backgroundColor': '#111',
        'padding': '20px',
        'borderBottom': '1px solid #333',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'
    }, children=[
        html.H1('Are we in deep shit?', style={
            'color': 'white', 
            'marginBottom': '20px',
            'textAlign': 'center'
        }),
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'center',
            'flexWrap': 'wrap',
            'gap': '10px'
        }, children=[
            dcc.Link(
                html.Button(
                    page['name'],
                    id=f'btn-{page["name"].lower().replace(" ", "-")}',
                    style=button_style,
                    n_clicks=0
                ),
                href=page['relative_path'],
                style={'textDecoration': 'none'}
            ) for page in dash.page_registry.values()
        ])
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run()