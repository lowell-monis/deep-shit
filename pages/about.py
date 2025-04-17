from dash import dcc, html
import dash

dash.register_page(__name__, path='/about', name="About & References")

layout = html.Div(
    style={
        'backgroundColor': 'black', 
        'padding': '40px',
        'minHeight': '100vh',
        'color': 'white',
        'fontFamily': '"Garamond", serif'
    },
    children=[
        html.H1(
            "About & References",
            style={
                'textAlign': 'center',
                'fontSize': '3rem',
                'marginBottom': '40px',
                'textShadow': '2px 2px 0 #ff0050, 4px 4px 0 #00f2ea'
            }
        ),
        
        html.Div(
            style={
                'backgroundColor': '#111',
                'padding': '30px',
                'borderRadius': '10px',
                'marginBottom': '40px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.3)'
            },
            children=[
                html.H2(
                    "About This Project",
                    style={
                        'color': '#00F2EA', 
                        'borderBottom': '1px solid #333',
                        'paddingBottom': '10px'
                    }
                ),
                html.P(
                    "This dashboard analyzes TikTok content moderation patterns through interactive visualizations.",
                    style={'fontSize': '1.1rem'}
                ),
                html.Div(
                    [
                        html.P("Created by Lowell Monis", style={'marginBottom': '5px'}),
                        html.A(
                            "GitHub Profile",
                            href="https://github.com/lowell-monis",
                            target="_blank",
                            style={
                                'color': '#FF0050',  # TikTok Pink
                                'textDecoration': 'none',
                                'marginRight': '20px'
                            }
                        ),
                        html.A(
                            "[Other Website Placeholder]",
                            href="#",  # Replace with your link
                            target="_blank",
                            style={
                                'color': '#00F2EA',
                                'textDecoration': 'none'
                            }
                        )
                    ],
                    style={'marginTop': '20px'}
                )
            ]
        ),
        
        html.Div(
            style={
                'backgroundColor': '#111',
                'padding': '30px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.3)'
            },
            children=[
                html.H2(
                    "References & Sources",
                    style={
                        'color': '#FF0050',
                        'borderBottom': '1px solid #333',
                        'paddingBottom': '10px'
                    }
                ),
                html.H3("Data Sources", style={'marginTop': '20px'}),
                html.Ul([
                    html.Li("TikTok Moderation Dataset: [Source to be added]"),
                    html.Li("Content Policy Documentation: [Source to be added]")
                ]),
                
                html.H3("Design Inspiration", style={'marginTop': '20px'}),
                html.Ul([
                    html.Li("TikTok Brand Colors"),
                    html.Li("Glitch Art Aesthetics"),
                    html.Li("Modern Data Visualization Principles")
                ]),
                
                html.H3("Technical References", style={'marginTop': '20px'}),
                html.Ul([
                    html.Li("Plotly Dash Documentation"),
                    html.Li("Pandas Data Analysis"),
                    html.Li("CSS Animation Techniques")
                ])
            ]
        ),
        
        # Footer
        html.Div(
            style={
                'textAlign': 'center',
                'marginTop': '50px',
                'color': '#666'
            },
            children=[
                html.P("© 2023 TikTok Moderation Analysis Dashboard"),
                html.P("All data used for educational purposes")
            ]
        )
    ]
)