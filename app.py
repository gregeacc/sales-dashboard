from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3
import base64
import io
import calendar
from datetime import datetime, date

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('sales.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,
            Product TEXT,
            Sales_Amount REAL,
            Opportunity_Status TEXT,
            Total_Sales REAL
        )
    ''')
    conn.close()

def get_data():
    try:
        conn = sqlite3.connect('sales.db')
        df = pd.read_sql_query('SELECT * FROM sales', conn)
        conn.close()
        if len(df) > 0:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return pd.DataFrame()  # Return empty DataFrame if no data exists

def save_to_db(df):
    conn = sqlite3.connect('sales.db')
    df.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()

# Initialize database
init_db()
sales_data = pd.DataFrame()  # Start with empty DataFrame

app = Dash(__name__)

# File Upload Component
upload_component = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a CSV File')
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
    html.Div(id='upload-output')
])

# Dropdown for selecting metrics
metric_selectors = html.Div([
    html.Div([
        html.Label('Select Metric 1:'),
        dcc.Dropdown(id='metric1-column', clearable=False)
    ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
    
    html.Div([
        html.Label('Select Metric 2:'),
        dcc.Dropdown(id='metric2-column', clearable=False)
    ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
    
    html.Div([
        html.Label('Select Metric 3:'),
        dcc.Dropdown(id='metric3-column', clearable=False)
    ], style={'width': '30%', 'display': 'inline-block'})
], style={'margin': '20px 0', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

# Visualization controls
viz_controls = html.Div([
    # First row: Time Series and Date Range blocks side by side
    html.Div([
        # Time Series Controls Block
        html.Div([
            html.H3("Time Series Settings", style={
                'marginBottom': '20px',
                'color': '#2c3e50',
                'borderBottom': '2px solid #3498db',
                'paddingBottom': '10px'
            }),
            html.Div([
                html.Div([
                    html.Label('Time Series Variable:', style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='timeseries-column', clearable=False)
                ], style={'width': '65%', 'display': 'inline-block', 'marginRight': '5%'}),
                
                html.Div([
                    html.Label('Plot Type:', style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='plot-type',
                        options=[
                            {'label': 'Line Plot', 'value': 'line'},
                            {'label': 'Scatter Plot', 'value': 'scatter'},
                            {'label': 'Bar Plot', 'value': 'bar'}
                        ],
                        value='line',
                        clearable=False
                    )
                ], style={'width': '30%', 'display': 'inline-block'})
            ])
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginRight': '4%'
        }),
        
        # Date Range Block
        html.Div([
            html.H3("Date Range Selection", style={
                'marginBottom': '15px',
                'color': '#2c3e50',
                'borderBottom': '2px solid #3498db',
                'paddingBottom': '10px'
            }),
            html.Div([
                # Start Date
                html.Div([
                    html.Label('Start Date:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
                    html.Div([
                        dcc.Dropdown(id='start-year', placeholder='Year', style={'width': '110px', 'display': 'inline-block', 'marginRight': '10px'}),
                        dcc.Dropdown(id='start-month', placeholder='Month', style={'width': '110px', 'display': 'inline-block', 'marginRight': '10px'}),
                        dcc.Dropdown(id='start-day', placeholder='Day', style={'width': '90px', 'display': 'inline-block'}),
                    ])
                ], style={'marginBottom': '10px'}),
                
                # End Date
                html.Div([
                    html.Label('End Date:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
                    html.Div([
                        dcc.Dropdown(id='end-year', placeholder='Year', style={'width': '110px', 'display': 'inline-block', 'marginRight': '10px'}),
                        dcc.Dropdown(id='end-month', placeholder='Month', style={'width': '110px', 'display': 'inline-block', 'marginRight': '10px'}),
                        dcc.Dropdown(id='end-day', placeholder='Day', style={'width': '90px', 'display': 'inline-block'}),
                    ])
                ])
            ])
        ], style={
            'width': '42%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': 'white',
            'padding': '15px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
    ], style={'marginBottom': '20px', 'whiteSpace': 'nowrap', 'width': '100%'}),
    
    # Category and Pie Chart Block
    html.Div([
        html.H3("Category and Pie Chart Settings", style={
            'marginBottom': '20px',
            'color': '#2c3e50',
            'borderBottom': '2px solid #3498db',
            'paddingBottom': '10px'
        }),
        html.Div([
            html.Div([
                html.Label('Category Variable:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='category-column', clearable=False)
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
            
            html.Div([
                html.Label('Pie Chart Value:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='pie-column', clearable=False)
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
], style={'margin': '20px 0'})

# Create the layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    # File upload at the top
    upload_component,
    
    # Tabs
    dcc.Tabs([
        # Data View Tab
        dcc.Tab(label='Data View', children=[
            html.Div([
                # Metric selectors
                metric_selectors,
                # Metrics div
                html.Div(id='metrics-container', style={'margin': '20px 0'}),
                # Data table
                html.H4("Data Table", style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
                dash_table.DataTable(
                    id='sales-table',
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_header={
                        'backgroundColor': '#3498db',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    style_data={
                        'backgroundColor': 'white',
                        'color': '#2c3e50'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f9f9f9'
                        }
                    ],
                    page_size=15,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    style_table={'overflowX': 'auto'}
                )
            ], style={'margin': '20px'})
        ]),
        
        # Visualizations Tab
        dcc.Tab(label='Visualizations', children=[
            html.Div([
                # Visualization controls at the top
                viz_controls,
                # Graphs
                html.Div(id='sales-trend-container', style={'marginBottom': '30px'}),
                html.Div([
                    html.Div(id='product-sales-container', style={'width': '50%', 'display': 'inline-block'}),
                    html.Div(id='sales-status-container', style={'width': '50%', 'display': 'inline-block'})
                ])
            ], style={'padding': '20px'})
        ])
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'margin': '20px'
    })
], style={
    'fontFamily': 'Arial, sans-serif',
    'margin': '0 auto',
    'maxWidth': '1200px',
    'padding': '20px'
})

# Callback for file upload (modify to include new metric dropdowns)
@app.callback(
    [Output('upload-output', 'children'),
     Output('sales-table', 'data'),
     Output('sales-table', 'columns'),
     Output('timeseries-column', 'options'),
     Output('timeseries-column', 'value'),
     Output('pie-column', 'options'),
     Output('pie-column', 'value'),
     Output('category-column', 'options'),
     Output('category-column', 'value'),
     Output('metric1-column', 'options'),
     Output('metric1-column', 'value'),
     Output('metric2-column', 'options'),
     Output('metric2-column', 'value'),
     Output('metric3-column', 'options'),
     Output('metric3-column', 'value'),
     Output('start-year', 'value'),
     Output('start-month', 'value'),
     Output('start-day', 'value'),
     Output('end-year', 'value'),
     Output('end-month', 'value'),
     Output('end-day', 'value')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        df = get_data()
        if df.empty:
            return ['No data uploaded yet.'] + [[], []] + [[], None] * 6 + [None] * 6
        
        columns = [{"name": i, "id": i} for i in df.columns]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_options = [{'label': col, 'value': col} for col in numeric_cols]
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col != 'Date']
        categorical_options = [{'label': col, 'value': col} for col in categorical_cols]
        
        # Get min and max dates for initialization
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        
        return ('', df.to_dict('records'), columns,
                numeric_options, numeric_cols[0],
                numeric_options, numeric_cols[0],
                categorical_options, categorical_cols[0],
                numeric_options, numeric_cols[0],
                numeric_options, numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0],
                numeric_options, numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[0],
                min_date.year, min_date.month, min_date.day,
                max_date.year, max_date.month, max_date.day)

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df['Date'] = pd.to_datetime(df['Date'])
            save_to_db(df)
            
            columns = [{"name": i, "id": i} for i in df.columns]
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            numeric_options = [{'label': col, 'value': col} for col in numeric_cols]
            categorical_cols = df.select_dtypes(include=['object']).columns
            categorical_cols = [col for col in categorical_cols if col != 'Date']
            categorical_options = [{'label': col, 'value': col} for col in categorical_cols]
            
            # Get min and max dates for initialization
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            
            return (html.Div(['Upload successful!']), df.to_dict('records'), columns,
                    numeric_options, numeric_cols[0],
                    numeric_options, numeric_cols[0],
                    categorical_options, categorical_cols[0],
                    numeric_options, numeric_cols[0],
                    numeric_options, numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0],
                    numeric_options, numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[0],
                    min_date.year, min_date.month, min_date.day,
                    max_date.year, max_date.month, max_date.day)
    except Exception as e:
        return ['Error processing file.'] + [[], []] + [[], None] * 6 + [None] * 6

# Callback for updating metrics
@app.callback(
    Output('metrics-container', 'children'),
    [Input('sales-table', 'data'),
     Input('metric1-column', 'value'),
     Input('metric2-column', 'value'),
     Input('metric3-column', 'value')]
)
def update_metrics(data, metric1, metric2, metric3):
    if not data or not metric1 or not metric2 or not metric3:
        return html.Div()
        
    df = pd.DataFrame(data)
    
    return html.Div([
        html.Div([
            html.H4(f"{metric1}"),
            html.H2(f"{df[metric1].sum():,.2f}")
        ], className='metric-card'),
        html.Div([
            html.H4(f"{metric2}"),
            html.H2(f"{df[metric2].mean():,.2f}")
        ], className='metric-card'),
        html.Div([
            html.H4(f"{metric3}"),
            html.H2(f"{df[metric3].sum():,.2f}")
        ], className='metric-card')
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0'})

# Callback for updating visualizations
@app.callback(
    [Output('sales-trend-container', 'children'),
     Output('product-sales-container', 'children'),
     Output('sales-status-container', 'children')],
    [Input('sales-table', 'data'),
     Input('timeseries-column', 'value'),
     Input('pie-column', 'value'),
     Input('category-column', 'value'),
     Input('plot-type', 'value'),
     Input('start-year', 'value'),
     Input('start-month', 'value'),
     Input('start-day', 'value'),
     Input('end-year', 'value'),
     Input('end-month', 'value'),
     Input('end-day', 'value')]
)
def update_graphs(data, timeseries_col, pie_col, category_col, plot_type,
                 start_year, start_month, start_day, end_year, end_month, end_day):
    if not data or not timeseries_col or not pie_col or not category_col:
        return html.Div(), html.Div(), html.Div()
        
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter data by date range if dates are selected
    if all([start_year, start_month, start_day]) and all([end_year, end_month, end_day]):
        start_date = pd.Timestamp(year=start_year, month=start_month, day=start_day)
        end_date = pd.Timestamp(year=end_year, month=end_month, day=end_day)
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        df = df.loc[mask]
    
    # Aggregate data by date
    daily_data = df.groupby('Date')[timeseries_col].sum().reset_index()
    
    # Time series plot based on selected plot type
    if plot_type == 'line':
        trend_fig = px.line(daily_data, x='Date', y=timeseries_col, 
                          title=f'Daily {timeseries_col} Over Time')
    elif plot_type == 'scatter':
        trend_fig = px.scatter(daily_data, x='Date', y=timeseries_col,
                             title=f'Daily {timeseries_col} Over Time')
    else:  # bar plot
        trend_fig = px.bar(daily_data, x='Date', y=timeseries_col,
                          title=f'Daily {timeseries_col} Over Time')
    
    # Update layout for better date display
    trend_fig.update_xaxes(
        tickformat='%Y-%m-%d',
        tickangle=45,
        title_text='Date'
    )
    trend_fig.update_yaxes(title_text=f'Total {timeseries_col}')
    
    # Pie chart
    pie_fig = px.pie(df, values=pie_col, names=category_col,
                     title=f'{pie_col} by {category_col}')
    
    # Bar chart
    status_counts = df[category_col].value_counts()
    bar_fig = px.bar(
        x=status_counts.index,
        y=status_counts.values,
        title=f'Count by {category_col}'
    )
    
    return (
        dcc.Graph(figure=trend_fig),
        dcc.Graph(figure=pie_fig),
        dcc.Graph(figure=bar_fig)
    )

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Sales Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            .metric-card {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
                min-width: 200px;
            }
            .metric-card h4 {
                color: #7f8c8d;
                margin: 0;
                font-size: 16px;
            }
            .metric-card h2 {
                color: #2c3e50;
                margin: 10px 0 0 0;
                font-size: 24px;
            }
            body {
                background-color: #f5f6fa;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

@app.callback(
    [Output('start-year', 'options'),
     Output('start-month', 'options'),
     Output('start-day', 'options'),
     Output('end-year', 'options'),
     Output('end-month', 'options'),
     Output('end-day', 'options')],
    [Input('sales-table', 'data'),
     Input('start-year', 'value'),
     Input('start-month', 'value'),
     Input('end-year', 'value'),
     Input('end-month', 'value')]
)
def update_date_dropdowns(data, start_year, start_month, end_year, end_month):
    if not data:
        return [[]] * 6
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Get min and max dates from data
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    # Create year options
    years = list(range(min_date.year, max_date.year + 1))
    year_options = [{'label': str(year), 'value': year} for year in years]
    
    # Create month options
    month_options = [{'label': calendar.month_abbr[m], 'value': m} for m in range(1, 13)]
    
    # Create day options based on selected year and month
    def get_days_in_month(year, month):
        if not year or not month:
            return []
        days = calendar.monthrange(year, month)[1]
        return [{'label': str(d), 'value': d} for d in range(1, days + 1)]
    
    start_day_options = get_days_in_month(start_year, start_month) if start_year and start_month else []
    end_day_options = get_days_in_month(end_year, end_month) if end_year and end_month else []
    
    return (
        year_options, month_options, start_day_options,
        year_options, month_options, end_day_options
    )

if __name__ == '__main__':
    app.run_server(debug=True)
