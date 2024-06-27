import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home', title='Building Maintenance')

layout = dbc.Container([
    # Title Section
    dbc.Row([
        dbc.Col([
            html.H1('Welcome!', className='display-3 text-center mb-4'),
            html.P('App Overview', className='lead text-center')
        ], width=12)
    ], className='mb-5'),
    # Guidelines Section
    dbc.Row([
        dbc.Col([
            html.P([
                html.Strong('1) Built-in dataset'),
                html.Br(),
                'The default dataset used is Building Maintenance.'
            ], className='guide'),
            html.P([
                html.Strong('2) Get in touch with the due work with this functionality'),
                html.Br(),
                'Title vs date - expected date (days delayed).'
            ], className='guide'),
            html.P([
                html.Strong('3) Determine the total as well as individual cost of each category of each floor'),
                html.Br(),
                'Cost according to different categories.'
            ], className='guide'),
            html.P([
                html.Strong('4) Determine which floor has which categories of work'),
                html.Br(),
                'Floor wise category graph.'
            ], className='guide'),
            html.P([
                html.Strong('5) Determine the completed and the pending work'),
                html.Br(),
                'Completed vs pending.'
            ], className='guide'),
            dbc.Button("Get Started", color="primary", href="/form", className="mt-4", style={'font-size': '16px', 'font-weight': 'bold', 'padding': '10px 20px'})
        ], width=8),  # Adjusted width to accommodate the image column
        # Image Column
        dbc.Col([
            html.Img(src='assets/images/image3.png', style={'width': '100%', 'height': 'auto', 'margin-right': '34rem'})
        ], width=4)
    ])
], className='py-5')
