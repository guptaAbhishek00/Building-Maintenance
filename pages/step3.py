import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import warnings
import plotly.express as px

# Load the Building Maintenance data
df_building = pd.read_csv('data/Building_Maintenance.csv')

# Register the page
dash.register_page(__name__, name='Category-Cost Analysis', title='Category-cost')

# Helper function to generate bar chart for category cost breakdown within selected floor
def generate_category_cost_bar_chart(floor):
    df_floor = df_building[df_building['Floor'] == floor]
    category_cost = df_floor.groupby('Category')['Expected Cost (INR)'].sum().reset_index()
    fig = px.bar(category_cost, x='Category', y='Expected Cost (INR)', title=f'Category-wise Expected Cost Breakdown for Floor {floor}')
    fig.update_layout(title_x=0.5)
    return fig

# Helper function to generate pie chart for overall category cost breakdown
def generate_overall_cost_pie_chart():
    overall_category_cost = df_building.groupby('Category')['Expected Cost (INR)'].sum().reset_index()
    fig = px.pie(overall_category_cost, values='Expected Cost (INR)', names='Category', title='Overall Category-wise Expected Cost Breakdown')
    fig.update_layout(title_x=0.5)
    return fig


# Define layout for the page
layout = dbc.Container([
    # Section 1: Header with Padding
    dbc.Row([
        dbc.Col(html.H3('Category-Cost Analysis', style={'text-align': 'center', 'padding-top': '20px', 'padding-bottom': '20px'}))
    ]),

    # Section 2: User Inputs with Padding
    dbc.Row([
        dbc.Col([
            html.Label('Select Floor:', style={'padding-top': '20px'}),
            dcc.Dropdown(
                id='floor-dropdown',
                options=[{'label': floor, 'value': floor} for floor in sorted(df_building['Floor'].unique())],
                value=df_building['Floor'].iloc[0],  # Default to the first floor
                clearable=False,
                style={'width': '100%'}  # Shorten the input bar
            )
        ], width=6)
    ], style={'padding-bottom': '20px', 'margin-left': ''}),  # Add padding between input and graphs

    # Section 3: Overall Category Cost Breakdown Bar Chart and Category Cost Breakdown Bar Chart side by side
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='category-cost-bar-chart', className='my-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='overall-category-cost-bar-chart', className='my-graph')
        ], width=6)
    ], style={'padding-bottom': '20px'}),  # Add padding between graphs
])


# Define callbacks to update charts based on user selection
@callback(
    [
     Output('overall-category-cost-bar-chart', 'figure'),
     Output('category-cost-bar-chart', 'figure'),
    ],
    [Input('floor-dropdown', 'value')]
)
def update_charts(selected_floor):
    return (
            generate_overall_cost_pie_chart(),  # Use pie chart for overall breakdown
            generate_category_cost_bar_chart(selected_floor),
            )
