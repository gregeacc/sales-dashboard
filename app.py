from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import numpy as np

# Read the CSV file and parse dates
sales_data = pd.read_csv("Sales Dataset.csv", parse_dates=['Date'])

app = Dash(__name__)

# Create the date range slider
date_slider = dcc.RangeSlider(
    id='date-range-slider',
    min=sales_data['Date'].astype(np.int64) // 10**9,
    max=sales_data['Date'].astype(np.int64) // 10**9,
    value=[
        sales_data['Date'].min().timestamp(),
        sales_data['Date'].max().timestamp()
    ],
    marks={
        str(int(timestamp)): date.strftime('%Y-%m-%d')
        for timestamp, date in zip(
            sales_data['Date'].astype(np.int64) // 10**9,
            sales_data['Date']
        )
    }
)

# Create graphs
sales_trend = dcc.Graph(
    id='sales-trend',
    figure=px.line(sales_data, x='Date', y='Total Sales', title='Sales Trend Over Time')
)

product_sales = dcc.Graph(
    id='product-sales',
    figure=px.pie(sales_data, values='Sales Amount', names='Product', title='Sales by Product')
)

status_bar = dcc.Graph(
    id='sales-status-bar',
    figure=px.bar(
        sales_data['Opportunity Status'].value_counts(),
        x=sales_data['Opportunity Status'].value_counts().index,
        y=sales_data['Opportunity Status'].value_counts().values,
        title='Sales by Status'
    )
)

# Create metrics div
metrics = html.Div([
    html.Div([
        html.H4("Total Sales"),
        html.H2(f"${sales_data['Sales Amount'].sum():,.2f}")
    ], className='metric-card'),
    html.Div([
        html.H4("Average Deal Size"),
        html.H2(f"${sales_data['Sales Amount'].mean():,.2f}")
    ], className='metric-card'),
    html.Div([
        html.H4("Win Rate"),
        html.H2(f"{(sales_data['Opportunity Status'] == 'Won').mean():.2%}")
    ], className='metric-card')
], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0'})

# Define the layout with tabs
app.layout = html.Div([
    html.H1("Sales Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    # Metrics at the top
    metrics,
    
    # Tabs
    dcc.Tabs([
        # Data View Tab
        dcc.Tab(label='Data View', children=[
            html.Div([
                html.H4("Sales Data Table", style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
                dash_table.DataTable(
                    id='sales-table',
                    columns=[{"name": i, "id": i} for i in sales_data.columns],
                    data=sales_data.to_dict('records'),
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
                    page_size=15,  # Number of rows per page
                    filter_action="native",  # Enable filtering
                    sort_action="native",    # Enable sorting
                    sort_mode="multi",       # Enable sorting by multiple columns
                    style_table={'overflowX': 'auto'}
                )
            ], style={'margin': '20px'})
        ]),
        
        # Visualizations Tab
        dcc.Tab(label='Visualizations', children=[
            html.Div([
                # Sales Trend Graph
                html.Div([
                    sales_trend
                ], style={'marginBottom': '30px'}),
                
                # Product Sales and Status Bar side by side
                html.Div([
                    html.Div([
                        product_sales
                    ], style={'width': '50%', 'display': 'inline-block'}),
                    html.Div([
                        status_bar
                    ], style={'width': '50%', 'display': 'inline-block'})
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

if __name__ == '__main__':
    app.run_server(debug=True)
