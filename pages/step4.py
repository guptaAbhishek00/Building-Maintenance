import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# Load the Building Maintenance data
df_building = pd.read_csv('data/Building_Maintenance.csv')

# Register the page
dash.register_page(__name__, name='Work Done Dashboard', title='Category Analysis')

# Helper function to generate pie chart for work done status by category
def generate_work_done_by_category_pie_chart(category):
    df_category = df_building[df_building['Category'] == category]
    work_done_counts = df_category['Is Done'].value_counts()
    colors = ['red', 'green']  # Define custom colors for 'No' and 'Yes'
    fig = go.Figure(data=[go.Pie(labels=work_done_counts.index, values=work_done_counts.values, marker=dict(colors=colors))])
    fig.update_layout(title=f'Work Done Status for Category {category}')
    return fig

# Helper function to generate pie chart for isDone status
def generate_isdone_pie_chart(floor):
    df_floor = df_building[df_building['Floor'] == floor]
    isdone_counts = df_floor['Is Done'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=isdone_counts.index, values=isdone_counts.values)])
    fig.update_layout(title=f'Work Completion Status for Floor {floor}', title_x=0.5)
    return fig


# Helper function to generate bar chart for category-wise work done
def generate_category_work_done_bar_chart(floor):
    df_floor = df_building[df_building['Floor'] == floor]
    category_status = df_floor.groupby(['Category', 'Is Done']).size().unstack(fill_value=0)
    
    if 'Yes' not in category_status.columns:
        category_status['Yes'] = 0
    
    fig = go.Figure(data=[
        go.Bar(name='Done', x=category_status.index, y=category_status['Yes']),
        go.Bar(name='Not Done', x=category_status.index, y=category_status['No'])
    ])
    fig.update_layout(barmode='stack', title=f'Category-wise Work Done for Floor {floor}', title_x=0.5)
    return fig

# Helper function to generate table for pending items in each floor
def generate_pending_items_table(floor):
    df_floor = df_building[(df_building['Floor'] == floor)]
    table = dbc.Table.from_dataframe(df_floor[['Description', 'Category', 'Class/Lab No']], striped=True, bordered=True, dark= True, hover=True, style={'background-color': 'black'})
    return table

# Define layout for the page
layout = dbc.Container([
  # Section 1: Header with Padding
    dbc.Row([
        dbc.Col(html.H3('Category-wise Work Done Dashboard', style={'text-align': 'center', 'padding-top': '20px', 'padding-bottom': '20px'}))
    ]),
    # Section 2: Category Dropdown
    dbc.Row([
        dbc.Col([
            html.Label('Select Category:', style={'padding-top': '20px'}),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': category, 'value': category} for category in sorted(df_building['Category'].unique())],
                value=df_building['Category'].iloc[0],  # Default to the first category
                clearable=False,
                style={'width': '100%'}  # Shorten the input bar
            )
        ], width=6)
    ], style={'padding-bottom': '20px'}),  # Add padding between dropdown and pie charts


    # Section 4: Work Done Status by Category Pie Chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='work-done-by-category-pie-chart')
        ])
    ]),

    # Section 1: Header with Padding
    dbc.Row([
        dbc.Col(html.H3('Floor-wise Work Done Dashboard', style={'text-align': 'center', 'padding-top': '30px', 'padding-bottom': '20px'}))
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
    ], style={'padding-bottom': '20px'}),  # Add padding between input and graphs

    # Section 3: isDone Status Pie Chart with Padding
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='isdone-pie-chart', className='my-graph')
        ])
    ], style={'padding-top': '20px', 'padding-bottom': '20px'}),  # Add padding between sections


    # Section 5: Category-wise Work Done Bar Chart with Padding
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='category-work-done-bar-chart', className='my-graph')
        ])
    ], style={'padding-bottom': '20px'}),  # Add padding between graphs

    # Section 6: Pending Items Table with Padding
    dbc.Row([
        dbc.Col([
            html.H3('Pending Items', style={'padding-top': '20px'}),
            html.Div(id='pending-items-table', style={'color': 'black'}),
            # Change the font colors
        ])
                
    ], style={'padding-bottom': '20px'}),  # Add padding between table and footer
])

# Define callback to update work done status pie chart based on selected category
@callback(
    Output('work-done-by-category-pie-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_work_done_pie_chart(selected_category):
    return generate_work_done_by_category_pie_chart(selected_category)

# Define callback to update category dropdown based on selected floor
@callback(
    Output('category-dropdown', 'options'),
    [Input('floor-dropdown', 'value')]
)
def update_category_dropdown(selected_floor):
    categories = df_building[df_building['Floor'] == selected_floor]['Category'].unique()
    options = [{'label': category, 'value': category} for category in categories]
    return options

# Define callbacks to update charts and table based on user selection
@callback(
    [Output('isdone-pie-chart', 'figure'),
     Output('category-work-done-bar-chart', 'figure'),
     Output('pending-items-table', 'children')],
    [Input('floor-dropdown', 'value')]
)
def update_charts_and_table(selected_floor):
    return (generate_isdone_pie_chart(selected_floor),
            generate_category_work_done_bar_chart(selected_floor),
            generate_pending_items_table(selected_floor))


