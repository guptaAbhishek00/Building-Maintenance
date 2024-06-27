# import dash
# from dash import html, dcc, callback, Input, Output
# import plotly.graph_objects as go
# import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
# import plotly.express as px

# # Load the Building Maintenance data
# df_building = pd.read_csv('data/Building_Maintenance.csv')

# # Register the page
# dash.register_page(__name__, name='Category-wise Analysis', title='Category Analysis')

# # Helper function to generate pie chart for cost breakdown by category
# def generate_cost_by_category_pie_chart():
#     category_cost = df_building.groupby('Category')['Expected Cost (INR)'].sum().reset_index()
#     fig = go.Figure(data=[go.Pie(labels=category_cost['Category'], values=category_cost['Expected Cost (INR)'])])
#     fig.update_layout(title='Cost Breakdown by Category')
#     return fig

# # Helper function to generate pie chart for work done status by category
# def generate_work_done_by_category_pie_chart(category):
#     df_category = df_building[df_building['Category'] == category]
#     work_done_counts = df_category['Is Done'].value_counts()
#     colors = ['red', 'green']  # Define custom colors for 'No' and 'Yes'
#     fig = go.Figure(data=[go.Pie(labels=work_done_counts.index, values=work_done_counts.values, marker=dict(colors=colors))])
#     fig.update_layout(title=f'Work Done Status for Category {category}')
#     return fig

# # Define layout for the page
# layout = dbc.Container([
#     # Section 1: Header with Padding
#     dbc.Row([
#         dbc.Col(html.H3('Category-wise Analysis', style={'text-align': 'center', 'padding-top': '20px', 'padding-bottom': '20px'}))
#     ]),

#     # Section 2: Category Dropdown
#     dbc.Row([
#         dbc.Col([
#             html.Label('Select Category:', style={'padding-top': '20px'}),
#             dcc.Dropdown(
#                 id='category-dropdown',
#                 options=[{'label': category, 'value': category} for category in sorted(df_building['Category'].unique())],
#                 value=df_building['Category'].iloc[0],  # Default to the first category
#                 clearable=False,
#                 style={'width': '100%'}  # Shorten the input bar
#             )
#         ], width=6)
#     ], style={'padding-bottom': '20px'}),  # Add padding between dropdown and pie charts

#     # Section 3: Cost Breakdown by Category Pie Chart
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='cost-by-category-pie-chart')
#         ])
#     ], style={'padding-bottom': '20px'}),  # Add padding between charts

#     # Section 4: Work Done Status by Category Pie Chart
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='work-done-by-category-pie-chart')
#         ])
#     ])
# ])

# # Define callback to update work done status pie chart based on selected category
# @callback(
#     Output('work-done-by-category-pie-chart', 'figure'),
#     [Input('category-dropdown', 'value')]
# )
# def update_work_done_pie_chart(selected_category):
#     return generate_work_done_by_category_pie_chart(selected_category)

# # Define callback to update cost breakdown pie chart based on selected category
# @callback(
#     Output('cost-by-category-pie-chart', 'figure'),
#     [Input('category-dropdown', 'value')]
# )
# def update_cost_pie_chart(selected_category):
#     return generate_cost_by_category_pie_chart()
