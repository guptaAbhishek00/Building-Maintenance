import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import csv
import requests
import base64
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go


dash.register_page(__name__, name='Project Management', title='Form')
df_building = pd.read_csv('data/Building_Maintenance.csv')

def get_descriptions():
    descriptions = []
    with open('./data/Building_Maintenance.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            descriptions.append(row['Description'])
    return descriptions

def get_bill_url(description):
    with open('./data/Building_Maintenance.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Description'] == description:
                return row['Bill URL']
    return []


def generate_cost_by_category_bar(df_building):
    # df = df_building.copy()  # create a copy to avoid modifying the original DataFrame
    df = pd.read_csv('data/Building_Maintenance.csv')
    df_grouped = df.groupby('Category')['Expected Cost (INR)'].sum().reset_index()  # group by category and sum the cost
    fig = go.Figure(data=[
        go.Bar(name='Expected Cost (INR)', x=df_grouped['Category'], y=df_grouped['Expected Cost (INR)'])
    ])
    fig.update_layout(title='Cost by Category', title_x=0.5)
    return fig

fig2 = generate_cost_by_category_bar(df_building)
# fig = generate_date_vs_expected_date_scatter(df_building)

def generate_completed_vs_pending_bar(df_building):
    df = df_building.copy()  # create a copy to avoid modifying the original DataFrame
    df_grouped = df.groupby('Is Done').size().reset_index(name='Count')  # group by status and count the tasks
    fig = go.Figure(data=[
        go.Bar(name='Count', x=df_grouped['Is Done'], y=df_grouped['Count'])
    ])
    fig.update_layout(title='Completed vs Pending Tasks', title_x=0.5)
    return fig
fig4 = generate_completed_vs_pending_bar(df_building)

def generate_floor_wise_category_bar(df_building):
    df = df_building.copy()  # create a copy to avoid modifying the original DataFrame
    df_grouped = df.groupby(['Floor', 'Category']).size().reset_index(name='Count')  # group by floor and category and count the tasks
    # print(df_grouped)
    floors = df_grouped['Floor'].unique()
    categories = df_grouped['Category'].unique()

    fig = go.Figure(data=[
        go.Bar(name=category, x=floors, y=df_grouped[df_grouped['Category'] == category]['Count'])
        for category in categories
    ])

    fig.update_layout(barmode='stack', title='Floor wise Category Distribution', title_x=0.5)
    return fig

fig3 = generate_floor_wise_category_bar(df_building)


def generate_date_expected_date_line(df_building):
    df = df_building.copy()  

    # Fill NaN values
    df['Date'] = df['Date'].fillna(method='ffill')
    df['Expected Date'] = df['Expected Date'].fillna(method='ffill')

    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Expected Date'] = pd.to_datetime(df['Expected Date'], format='%d-%m-%Y')

    # Calculate the delay
    df['Delay'] = df['Date'] - df['Expected Date']

    # Filter delayed points
    delayed_points = df[df['Delay'] > pd.Timedelta(0)]

    fig = go.Figure()

    # Add traces for original and expected dates
    fig.add_trace(go.Scatter(y=df['Date'], x=df['Description'], mode='lines', name='Date'))
    fig.add_trace(go.Scatter(y=df['Expected Date'], x=df['Description'], mode='lines', name='Expected Date'))

    # Add delayed points to the plot
    if not delayed_points.empty:
        fig.add_trace(go.Scatter(y=delayed_points['Expected Date'], x=delayed_points['Description'],
                                 mode='markers', name='Delayed Date', marker=dict(color='red', size=10)))

    fig.update_layout(title='Date vs Expected Date', title_x=0.5)
    return fig

fig = generate_date_expected_date_line(df_building)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([   
            html.H3(['Project Management'], className='row-titles'),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Create Project', id='create-project-btn', className='my-button'),
                ],  
                 style={
                        "display": "flex",
                        "justify-content": "center",
                       }
                
                  ),
                dbc.Col([
                    dbc.Button('Edit Project', id='edit-project-btn', className='my-button'),
                ],style={
                        "display": "flex",
                        "justify-content": "center",
                       } ),
                dbc.Col([
                    dbc.Button('Bill View/Upload', id='bill-upload-btn', className='my-button'),
                ], style={
                        "display": "flex",
                        "justify-content": "center",
                       }),
            ],
            
            style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "space-between",
                       }
            ),
            html.Br(),
            html.Div(id='update-success-message'),
            html.Div(id='content-section')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Loading(id='p2-2-loading', type='circle', children=dcc.Graph(id='fig-transformed', className='my-graph',figure=fig)),
            # dbc.Button("Button 1", color="primary", className="mt-2")
        ], width=6, className='multi-graph'),
        dbc.Col([
            dcc.Loading(id='p2-2-loading', type='circle', children=dcc.Graph(id='fig-acf', className='my-graph',figure=fig2)),
            # dbc.Button("Button 2", color="primary", className="mt-2")
        ], width=6, className='multi-graph')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Loading(id='p2-2-loading', type='circle', children=dcc.Graph(id='fig-boxcox', className='my-graph',figure=fig3)),
            # dbc.Button("Button 3", color="primary", className="mt-2")
        ], width=6, className='multi-graph'),
        dbc.Col([
            dcc.Loading(id='p2-2-loading', type='circle', children=dcc.Graph(id='fig-pacf', className='my-graph',figure=fig4)),
            # dbc.Button("Button 4", color="primary", className="mt-2")
        ], width=6, className='multi-graph')
    ])
],
style={
    "margin-left": "5rem",
    "margin-right": "5rem",
    "width": "90%"
}
)

# call backs for updating the graphs
@callback(
    Output('fig-acf', 'figure'),
    [Input('fig-acf', 'figure')],
)
def update_cost_by_category_graph(_):
    df = pd.read_csv('data/Building_Maintenance.csv')  # Load CSV data dynamically
    return generate_cost_by_category_bar(df)

@callback(
    Output('fig-boxcox', 'figure'),
    [Input('fig-boxcox', 'figure')],
)
def update_floor_wise_category_graph(_):
    df = pd.read_csv('data/Building_Maintenance.csv')
    return generate_floor_wise_category_bar(df)

@callback(
    Output('fig-pacf', 'figure'),
    [Input('fig-pacf', 'figure')],
)
def update_completed_vs_pending_graph(_):
    df = pd.read_csv('data/Building_Maintenance.csv')
    return generate_completed_vs_pending_bar(df)

@callback(
    Output('content-section', 'children'),
    [Input('create-project-btn', 'n_clicks'),
     Input('edit-project-btn', 'n_clicks'),
     Input('bill-upload-btn', 'n_clicks')]
)


def update_content(create_clicks, edit_clicks, bill_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'create-project-btn':
            return create_project_form()
        elif button_id == 'edit-project-btn':
            return edit_project_form()
        elif button_id == 'bill-upload-btn':
            return bill_upload_section()

def create_project_form():
    return html.Form(id='maintenance-form', children=[
                html.Label('Description'),
                dbc.Input(id='description', type='text', className='input-text',
                            style={'background-color': '#f0f0f0', 'color': 'black'}
                          ),
                html.Label('Date'),
                dbc.Input(id='date', type='date', className='input-text'),
                html.Label('Expected Date'),
                dbc.Input(id='expected_date', type='date', className='input-text'),
                html.Label('Category'),
                dbc.Input(id='category', type='text', className='input-text'),
                html.Label('Expected Cost (INR)'),
                dbc.Input(id='expected_cost', type='number', className='input-text'),
                html.Label('Floor'),
                dbc.Input(id='floor', type='number', className='input-text'),
                html.Label('Class/Lab No'),
                dbc.Input(id='class_lab', type='text', className='input-text'),

                html.Br(),
                html.Button('Submit', id='submit-button', type='submit', className='my-button')
            ])

def edit_project_form():
    return html.Div([
        html.Label('Select Description'),
        dcc.Dropdown(
            id='description-dropdown',
            options=[{'label': desc, 'value': desc} for desc in get_descriptions()],
            value=get_descriptions()[0],
            className='input-text'
        ),
        html.Div(id='edit-form-content'),
        html.Br(),
    ])

@callback(
    Output('edit-form-content', 'children'),
    [Input('description-dropdown', 'value')]
)
def load_edit_form_data(description):
    if description:
        with open('./data/Building_Maintenance.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Description'] == description:
                    return create_project_form_with_data(row)

def create_project_form_with_data(data):
    # print("update data", data)
    return html.Div([
        html.Form(id='maintenance-form-update', children=[
             html.Label('Description'),
        dbc.Input(id='description', type='text', value=data['Description'], className='input-text', style={'background-color': '#f0f0f0', 'color': 'black'}),  
        html.Label('Date'),
        html.Label('Date'),
        dbc.Input(id='date', type='date', value=datetime.strptime(data['Date'], '%d-%m-%Y').strftime('%Y-%m-%d'), className='input-text'),  
        html.Label('Expected Date'),
        dbc.Input(id='expected_date', type='date', value=datetime.strptime(data['Expected Date'], '%d-%m-%Y').strftime('%Y-%m-%d'), className='input-text'),  
        html.Label('Category'),
        dbc.Input(id='category', type='text', value=data['Category'], className='input-text'),  
        html.Label('Expected Cost (INR)'),
        dbc.Input(id='expected_cost', type='number', value=data['Expected Cost (INR)'], className='input-text'),  
        html.Label('Floor'),
        dbc.Input(id='floor', type='number', value=data['Floor'], className='input-text'),  
        html.Label('Class/Lab No'),
        dbc.Input(id='class_lab', type='text', value=data['Class/Lab No'], className='input-text'),  
        html.Br(),
        # a check box to mark the task as done, initial value is set to the value in the csv called Is Done which is a strin "Yes" or "No"
        dcc.Checklist(
            id='is-done',
            options=[
                {'label': 'Mark as Done', 'value': 'Yes'}
            ],
            value=[data['Is Done']]
        ),
        html.Br(),
        html.Button('Update', id='update-button', type='submit', className='my-button', style={'font-size': '16px', 'padding': '10px 20px'}),
        html.Br(),
        ])
    ])

@callback(
    [Output('maintenance-form-update', 'reset'),
     Output('update-success-message', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('description', 'value'),
     State('date', 'value'),
     State('expected_date', 'value'),
     State('category', 'value'),
     State('expected_cost', 'value'),
     State('floor', 'value'),
     State('class_lab', 'value'),
    State('is-done', 'value')
     ]
)
def update_form(n_clicks, description, date, expected_date, category, expected_cost, floor, class_lab, is_done):
    if n_clicks:
        with open('./data/Building_Maintenance.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            for index, row in enumerate(rows):
                if row['Description'] == description:
                    # print('is_done', is_done)
                    rows[index] = {
                        'Description': description,
                        # 'Date': date,
                        'Date': datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y'),
                        # 'Expected Date': expected_date,
                        'Expected Date': datetime.strptime(expected_date, '%Y-%m-%d').strftime('%d-%m-%Y'),
                        'Category': category,
                        'Expected Cost (INR)': expected_cost,
                        'Floor': floor,
                        'Class/Lab No': class_lab,
                        'Bill URL': row['Bill URL'],
                        'Is Done': is_done[-1] if is_done else "No"
                    }
        with open('./data/Building_Maintenance.csv', 'w', newline='') as csvfile:
            fieldnames = ['Description', 'Date', 'Expected Date', 'Category', 'Expected Cost (INR)', 'Floor', 'Class/Lab No', 'Bill URL', 'Is Done']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True, dbc.Alert("Update successful!", color="success")
    return None, None

def bill_upload_section():
    return html.Div([
        dcc.Dropdown(
            id='description-dropdown',
            options=[{'label': desc, 'value': desc} for desc in get_descriptions()],
            placeholder='Select a description...'
        ),
        html.Div(id='output-bill-images'),
        dcc.Upload(
            id='upload-bill',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px 0'
            },
            multiple=False
        ),
        html.Div(id='output-bill-upload')
    ])

@callback(
    Output('output-bill-images', 'children', allow_duplicate=True),
    [Input('description-dropdown', 'value')],
    prevent_initial_call=True
)
def update_bill_images(description):
    if description:
        urls = get_bill_url(description)
        if urls:
            urls = urls.split('|')
            if len(urls) == 1:
                return html.Div(html.Img(src=urls[0], style={'width': '100%'}), style={"margin": '10px'})
            else:
                return html.Div(
                    [
                        html.Div(html.Img(src=url, style={'width': '100%', }), style={'display': 'inline-block', "margin": '10px'})
                        for url in urls
                    ]
                )
        else:
            return html.Div([html.P('No bills available for this description.')])

@callback(
    [
    Output('output-bill-upload', 'reset'),
     Output('output-bill-images', 'children', allow_duplicate=True),
     ],  
    [Input('upload-bill', 'contents'),
     Input('upload-bill', 'filename'),
     Input('description-dropdown', 'value')],
    prevent_initial_call=True
)
def update_output(contents, filename, selected_description):
    if contents is not None and selected_description:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        url = upload_bill_to_api(decoded, filename)
        if url:
            append_url_to_csv(selected_description, url)
            updated_images = update_bill_images(selected_description)
            return (
                html.Div([
                    html.P('Bill uploaded successfully!')
                ]),
                updated_images,
            )
        else:
            return html.Div([
                html.P('Error uploading bill!')
            ])
    return None, None

def upload_bill_to_api(contents, filename):
    try:
        api = 'http://127.0.0.1:3001/upload_bill'
        files = {'image': (filename, contents)}
        response = requests.post(api, files=files)
        return response.json()['url']
    except Exception as e:
        print(e)
        return None

def append_url_to_csv(description, url):
    # print("append_url_to_csv")
    with open('./data/Building_Maintenance.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        for index, row in enumerate(rows):
            if row['Description'] == description:
                # print("match found desc")
                if row['Bill URL']:
                    row['Bill URL'] = row['Bill URL'] + '|' + url
                else:
                    row['Bill URL'] = url
                break
    with open('./data/Building_Maintenance.csv', 'w', newline='') as csvfile:
        fieldnames = ['Description', 'Date', 'Expected Date', 'Category', 'Expected Cost (INR)', 'Floor', 'Class/Lab No', 'Bill URL', 'Is Done']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

@callback(
    Output('maintenance-form', 'reset'),
    [Input('submit-button', 'n_clicks')],
    [State('description', 'value'),
     State('date', 'value'),
     State('expected_date', 'value'),
     State('category', 'value'),
     State('expected_cost', 'value'),
     State('floor', 'value'),
     State('class_lab', 'value')]
)
def submit_form(n_clicks, description, date, expected_date, category, expected_cost, floor, class_lab):
    if not n_clicks:
        return None
    if not all([description, date, expected_date, category, expected_cost, floor, class_lab]):
        return False
    with open('./data/Building_Maintenance.csv', 'a', newline='') as csvfile:
        fieldnames = ['Description', 'Date', 'Expected Date', 'Category', 'Expected Cost (INR)', 'Floor', 'Class/Lab No', 'Bill URL', 'Is Done']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'Description': description,
            # 'Date': date,
            'Date': datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y'),
            # 'Expected Date': expected_date,
            'Expected Date': datetime.strptime(expected_date, '%Y-%m-%d').strftime('%d-%m-%Y'),
            'Category': category,
            'Expected Cost (INR)': expected_cost,
            'Floor': floor,
            'Class/Lab No': class_lab,
            'Bill URL': '',
            'Is Done': "No"
        })
    return True

