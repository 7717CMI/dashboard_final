import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import os
import numpy as np
import base64
import io

# Initialize the Dash app with Bootstrap theme and Font Awesome
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
])
app.title = "Dashboard – Japan Agricultural Tractor Tracker"

# Add health check endpoint for deployment monitoring
@app.server.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'japan-tractor-tracker'}, 200

def create_comprehensive_dummy_data():
    """Create comprehensive dummy data based on the provided tractor data structure"""
    
    # Base data from the provided CSV
    base_data = [
        # Kubota Corporation
        ["Kubota Corporation", "BX Series", "BX1880, BX2380, BX2680", "16.6 - 24.8 HP", "$12,000 - $26,900", "300-450", "Japan", "USA"],
        ["Kubota Corporation", "MX Series", "MX5400, MX6000", "55 - 63 HP", "$24,900 - $65,000", "180-260", "USA (assembly)", "USA"],
        ["Kubota Corporation", "M4 Series", "M4062, M4073", "66 - 74 HP", "$45,000 - $70,000", "120-180", "Japan", "Australia"],
        ["Kubota Corporation", "M5 Series", "M5091, M5112", "95 - 115 HP", "$45,000 - $87,500", "70-110", "USA (assembly)", "USA"],
        ["Kubota Corporation", "M6 Series", "M6-101, M6-141", "104 - 163 HP", "$44,900 - $130,000", "100-150", "France", "USA"],
        ["Kubota Corporation", "M7 Series", "M7-131, M7-171", "130 - 170 HP", "$65,000 - $120,000+", "120-180", "Japan / USA (final assembly USA)", "USA"],
        
        # Yanmar Holdings
        ["Yanmar Holdings", "AF Series", "AF118, AF30, AF33", "18 - 33 HP", "$16,000 - $30,000", "80-140", "Japan", "USA"],
        ["Yanmar Holdings", "YM Series", "YM347, YM359", "47 - 59 HP", "$27,800 - $57,700", "60-100", "Japan", "EU (Germany/France)"],
        ["Yanmar Holdings", "GA series", "GA series (GA28, GA30, GA36, GA41, GA46, GA50, GA55)", "28HP", "$4,300 - $22,000", "30-60", "Japan", "EU (Benelux)"],
        ["Yanmar Holdings", "MTU Series", "MT180", "30HP", "$5,200 - $10,200", "20-40", "Japan", "Australia/NZ"],
        
        # Mitsubishi Mahindra Agricultural Machinery
        ["Mitsubishi Mahindra Agricultural Machinery", "GCR Series", "MT226HE", "36HP", "$19,999 - $26,768", "140-220", "India", "USA"],
        ["Mitsubishi Mahindra Agricultural Machinery", "GOE", "265 DI XP PLUS", "41HP", "$26,100 - $30,400", "180-260", "South Korea", "USA"],
        ["Mitsubishi Mahindra Agricultural Machinery", "GM", "275 DI XP PLUS", "46HP", "$6,600 - $7,600", "1,200-1,800", "India", "India"],
        
        # Iseki & Co. Ltd.
        ["Iseki & Co. Ltd.", "AT Series", "AT23, AT25, AT33, AT46, AT50", "22 - 50 HP", "$20,000 - $30,000", "25-45", "Japan", "Australia"],
        ["Iseki & Co. Ltd.", "TM4 Series", "TM4230, TM4270", "20 - 25 HP", "$20,000 - $25,000", "20-35", "Japan", "UK"],
        ["Iseki & Co. Ltd.", "TG/TJ/TJW/TJV Series", "TG6, T97, TJW123, TJV95", "40 - 123 HP", "$40,000 - $52,000", "15-30", "Japan", "Thailand/Vietnam"],
        
        # John Deere
        ["John Deere", "5E Series", "5050E, 5075E, 5100E", "50 - 100 HP", "$32,000 - $47,000", "350-500", "India/Mexico", "USA"],
        ["John Deere", "5M Series", "5075M, 5100M, 5130M", "75 - 130 HP", "$35,000 - $108,000", "120-200", "Germany", "USA"],
        ["John Deere", "6M Series", "6100M, 6145M, 6175M", "100 - 175 HP", "$69,000 - $230,000", "60-100", "USA", "USA"],
        ["John Deere", "7R Series", "7200R, 7270R, 7310R", "200 - 310 HP", "$219,000 - $416,700", "60-100", "China/France", "USA"],
        ["John Deere", "9R Series", "9R 390, 9R 540, 9RX 640", "390 - 830 HP", "$375,000 - $715,000+", "60-100", "China/France", "USA"],
        
        # AGCO
        ["AGCO", "GT Series", "GT45, GT55, GT65", "52 - 71 HP", "$40,000 - $60,000", "70-120", "Brazil/China", "Latin America"],
        ["AGCO", "DT Series", "DT250B, DT275B", "290 - 320 HP", "$100,000 - $200,000", "30-60", "France", "USA/EU"],
        
        # CNH Industrial (New Holland)
        ["CNH Industrial (New Holland)", "T4 Series", "T4.55, T4.75, T4.90", "55 - 99 HP", "$18,500 - $60,000", "150-250", "Turkey", "EU"],
        ["CNH Industrial (New Holland)", "T6 Series", "T6.145, T6.160, T6.180", "145 - 180 HP", "$62,900 - $228,900", "80-130", "UK", "USA/EU"],
        ["CNH Industrial (New Holland)", "Puma Series", "Puma 150, Puma 175, Puma 200", "150 - 240 HP", "$60,600 - $279,000", "50-90", "Austria", "USA/EU"]
    ]
    
    # Create comprehensive dataset with monthly data for 2 years
    comprehensive_data = []
    
    # Generate data for each month from 2024 to 2025
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        month = current_date.month
        year = current_date.year
        
        for row in base_data:
            # Add some variation to sales data based on seasonality
            base_sales_min, base_sales_max = row[5].split('-')
            base_sales_min = int(base_sales_min.replace(',', '').strip())
            base_sales_max = int(base_sales_max.replace(',', '').strip())
            
            # Seasonal variation (higher sales in spring and fall)
            if month in [3, 4, 5, 9, 10, 11]:  # Spring and Fall
                seasonal_factor = np.random.uniform(1.1, 1.3)
            elif month in [6, 7, 8]:  # Summer
                seasonal_factor = np.random.uniform(0.8, 1.0)
            else:  # Winter
                seasonal_factor = np.random.uniform(0.7, 0.9)
            
            # Add some random variation
            random_factor = np.random.uniform(0.9, 1.1)
            
            # Add growth factor for 2025 (extrapolation)
            if year == 2025:
                # Assume 5-15% growth for 2025 based on market trends
                growth_factor = np.random.uniform(1.05, 1.15)
            else:
                growth_factor = 1.0
            
            total_factor = seasonal_factor * random_factor * growth_factor
            
            adjusted_sales_min = int(base_sales_min * total_factor)
            adjusted_sales_max = int(base_sales_max * total_factor)
            
            # Add price variation between years
            base_price = row[4]  # Original price range
            if year == 2025:
                # Extract price range and apply inflation/growth
                price_min_str = base_price.split('-')[0].replace('$', '').replace(',', '').strip()
                price_max_str = base_price.split('-')[1].replace('$', '').replace(',', '').replace('+', '').strip()
                
                price_min = float(price_min_str)
                price_max = float(price_max_str)
                
                # Apply 3-8% price increase for 2025
                price_inflation = np.random.uniform(1.03, 1.08)
                adjusted_price_min = int(price_min * price_inflation)
                adjusted_price_max = int(price_max * price_inflation)
                
                adjusted_price = f"${adjusted_price_min:,} - ${adjusted_price_max:,}"
            else:
                adjusted_price = base_price
            
            comprehensive_data.append([
                row[0],  # Manufacturer Name
                row[1],  # Brand Name
                row[2],  # Model Name
                row[3],  # HP Segment
                adjusted_price,  # Dollar Value (adjusted for year)
                f"{adjusted_sales_min}-{adjusted_sales_max}",  # Monthly Sales
                row[6],  # Imported From
                row[7],  # End Destination Country
                month,   # Month
                year     # Year
            ])
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Create DataFrame
    df = pd.DataFrame(comprehensive_data, columns=[
        'Manufacturer Name', 'Brand Name', 'Model Name', 'HP Segment',
        'Dollar Value of Tractor (ASP Range in US$)', 'Monthly Sale Data (Units)',
        'Imported From (Country Name)', 'End Destination Country', 'Month', 'Year'
    ])
    
    # Process numeric fields for better analysis
    # Extract HP values
    df['HP_Min'] = df['HP Segment'].str.extract(r'(\d+(?:\.\d+)?)').astype(float)
    df['HP_Max'] = df['HP Segment'].str.extract(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)')[1].astype(float)
    df['HP_Max'] = df['HP_Max'].fillna(df['HP_Min'])
    
    # Extract price values
    df['Price_Min'] = df['Dollar Value of Tractor (ASP Range in US$)'].str.extract(r'\$([\d,]+)')
    df['Price_Min'] = df['Price_Min'].str.replace(',', '').astype(float)
    df['Price_Max'] = df['Dollar Value of Tractor (ASP Range in US$)'].str.extract(r'\$([\d,]+)\s*-\s*\$([\d,]+)')[1]
    df['Price_Max'] = df['Price_Max'].str.replace(',', '').astype(float)
    df['Price_Max'] = df['Price_Max'].fillna(df['Price_Min'])
    
    # Extract sales values
    df['Sales_Min'] = df['Monthly Sale Data (Units)'].str.extract(r'(\d+(?:,\d+)?)')
    df['Sales_Min'] = df['Sales_Min'].str.replace(',', '').astype(float)
    df['Sales_Max'] = df['Monthly Sale Data (Units)'].str.extract(r'(\d+(?:,\d+)?)\s*[–\-]\s*(\d+(?:,\d+)?)')[1]
    df['Sales_Max'] = df['Sales_Max'].str.replace(',', '').astype(float)
    df['Sales_Max'] = df['Sales_Max'].fillna(df['Sales_Min'])
    
    # Create date field for time series analysis
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
    
    # Create categories for better filtering
    df['HP_Category'] = pd.cut(df['HP_Min'], 
                              bins=[0, 30, 60, 100, 200, 500, 1000], 
                              labels=['0-30 HP', '30-60 HP', '60-100 HP', 
                                     '100-200 HP', '200-500 HP', '500+ HP'])
    
    df['Price_Category'] = pd.cut(df['Price_Min'], 
                                 bins=[0, 20000, 50000, 100000, 200000, 500000, 1000000], 
                                 labels=['Budget ($0-20k)', 'Mid-Range ($20-50k)', 'Premium ($50-100k)', 
                                        'High-End ($100-200k)', 'Luxury ($200-500k)', 'Ultra Luxury ($500k+)'])
    
    df['Sales_Category'] = pd.cut(df['Sales_Min'], 
                                 bins=[0, 50, 100, 200, 500, 1000, 2000], 
                                 labels=['Low Volume (0-50)', 'Moderate (50-100)', 'Good (100-200)', 
                                        'High (200-500)', 'Very High (500-1000)', 'Mass Market (1000+)'])
    
    return df

# Load comprehensive data
df = create_comprehensive_dummy_data()

# Get unique values for filters
manufacturers = sorted(df['Manufacturer Name'].unique())
brands = sorted(df['Brand Name'].unique())
models = sorted(df['Model Name'].unique())
hp_segments = sorted(df['HP Segment'].unique())
import_countries = sorted(df['Imported From (Country Name)'].unique())
destination_countries = sorted(df['End Destination Country'].unique())
months = sorted(df['Month'].unique())
years = sorted(df['Year'].unique())

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="fas fa-tractor me-3 text-primary"),
                    "Dashboard – Japan Agricultural Tractor Tracker"
                ], className="text-center text-primary mb-3 fw-bold"),
                html.P([
                    html.I(className="fas fa-chart-line me-2 text-info"),
                    "Complete Market Intelligence with Advanced Filtering & Export"
                ], className="text-center text-muted mb-4 fs-5"),
                html.Hr(className="border-primary border-2")
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Disclaimer at top
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                html.Strong("Note: This dataset is for illustration purposes only. It does not represent actual data and has no association with real-world datasets.")
            ], color="danger", className="text-center fst-italic")
        ], width=12)
    ], className="mb-4"),
    
    # Filters Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-filter me-2"),
                        "Advanced Filters"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    # First row of filters
                    dbc.Row([
                        dbc.Col([
                            html.Label("Manufacturer:", className="fw-bold"),
                            dcc.Dropdown(
                                id='manufacturer-filter',
                                options=[{'label': 'All Manufacturers', 'value': 'All'}] + 
                                        [{'label': m, 'value': m} for m in manufacturers],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("Brand/Series Name:", className="fw-bold"),
                            dcc.Dropdown(
                                id='brand-filter',
                                options=[{'label': 'All Brands', 'value': 'All'}],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("Model:", className="fw-bold"),
                            dcc.Dropdown(
                                id='model-filter',
                                options=[{'label': 'All Models', 'value': 'All'}],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("HP Segment:", className="fw-bold"),
                            dcc.Dropdown(
                                id='hp-segment-filter',
                                options=[{'label': 'All HP Segments', 'value': 'All'}] + 
                                        [{'label': h, 'value': h} for h in hp_segments],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3)
                    ]),
                    
                    # Second row of filters
                    dbc.Row([
                        dbc.Col([
                            html.Label("Imported From:", className="fw-bold"),
                            dcc.Dropdown(
                                id='import-country-filter',
                                options=[{'label': 'All Import Countries', 'value': 'All'}] + 
                                        [{'label': c, 'value': c} for c in import_countries],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("End Destination Country:", className="fw-bold"),
                            dcc.Dropdown(
                                id='destination-country-filter',
                                options=[{'label': 'End Destination Countries', 'value': 'All'}] + 
                                        [{'label': c, 'value': c} for c in destination_countries],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Year:", className="fw-bold"),
                            dcc.Dropdown(
                                id='year-filter',
                                options=[{'label': 'All Years', 'value': 'All'}] + 
                                        [{'label': str(y), 'value': y} for y in years],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=2),
                        dbc.Col([
                            html.Label("Month:", className="fw-bold"),
                            dcc.Dropdown(
                                id='month-filter',
                                options=[{'label': 'All Months', 'value': 'All'}] + 
                                        [{'label': datetime(2024, m, 1).strftime('%B'), 'value': m} for m in months],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=2)
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Summary Cards
    dbc.Row([
        dbc.Col([
            html.Div(id="summary-cards")
        ], width=12)
    ], className="mb-4"),
    
    # Export Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5([
                        html.I(className="fas fa-download me-2"),
                        "Export Filtered Data"
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-file-csv me-2"),
                                "Download CSV"
                            ], id="download-csv-btn", color="success", className="me-2"),
                            dbc.Button([
                                html.I(className="fas fa-file-excel me-2"),
                                "Download Excel"
                            ], id="download-excel-btn", color="primary")
                        ], width=6),
                        dbc.Col([
                            html.Div(id="download-status", className="text-muted")
                        ], width=6)
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Charts Section
    dbc.Row([
        dbc.Col([
            html.Div(id="charts-container")
        ], width=12)
    ]),
    
    # Data Table Section
    dbc.Row([
        dbc.Col([
            html.Div(id="data-table-container")
        ], width=12)
    ], className="mt-4"),
    
    # Hidden divs for downloads
    html.Div(id="download-csv", style={"display": "none"}),
    html.Div(id="download-excel", style={"display": "none"}),
    
    # Disclaimer at bottom
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                html.Strong("Note: This dataset is for illustration purposes only. It does not represent actual data and has no association with real-world datasets.")
            ], color="danger", className="text-center fst-italic")
        ], width=12)
    ], className="mt-4")
    
], fluid=True)

# Callback to update brand dropdown based on manufacturer selection
@app.callback(
    Output('brand-filter', 'options'),
    [Input('manufacturer-filter', 'value')]
)
def update_brand_dropdown(selected_manufacturer):
    if selected_manufacturer == 'All':
        filtered_brands = brands
    else:
        filtered_brands = sorted(df[df['Manufacturer Name'] == selected_manufacturer]['Brand Name'].unique())
    
    return [{'label': 'All Brands', 'value': 'All'}] + [{'label': b, 'value': b} for b in filtered_brands]

# Callback to update model dropdown based on brand selection
@app.callback(
    Output('model-filter', 'options'),
    [Input('manufacturer-filter', 'value'),
     Input('brand-filter', 'value')]
)
def update_model_dropdown(selected_manufacturer, selected_brand):
    filtered_df = df.copy()
    
    if selected_manufacturer != 'All':
        filtered_df = filtered_df[filtered_df['Manufacturer Name'] == selected_manufacturer]
    
    if selected_brand != 'All':
        filtered_df = filtered_df[filtered_df['Brand Name'] == selected_brand]
    
    filtered_models = sorted(filtered_df['Model Name'].unique())
    return [{'label': 'All Models', 'value': 'All'}] + [{'label': m, 'value': m} for m in filtered_models]

# Callback to update summary cards
@app.callback(
    Output("summary-cards", "children"),
    [Input("manufacturer-filter", "value"),
     Input("brand-filter", "value"),
     Input("model-filter", "value"),
     Input("hp-segment-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value")]
)
def update_summary_cards(manufacturer, brand, model, hp_segment, 
                        import_country, destination_country, year, month):
    """Update summary cards based on filter selections"""
    
    # Apply filters
    filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, 
                              import_country, destination_country, year, month)
    
    if filtered_df.empty:
        return html.Div([
            dbc.Alert("No data matches the selected filters. Please adjust your filter criteria.", color="warning")
        ])
    
    # Calculate summary metrics
    total_records = len(filtered_df)
    unique_manufacturers = filtered_df['Manufacturer Name'].nunique()
    unique_models = filtered_df['Model Name'].nunique()
    avg_price_min = filtered_df['Price_Min'].mean()
    avg_price_max = filtered_df['Price_Max'].mean()
    avg_sales_min = filtered_df['Sales_Min'].mean()
    avg_sales_max = filtered_df['Sales_Max'].mean()
    total_sales_min = filtered_df['Sales_Min'].sum()
    total_sales_max = filtered_df['Sales_Max'].sum()
    
    cards = [
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className="fas fa-industry fa-2x text-success mb-3"),
                    html.H4(f"{unique_manufacturers}", className="text-success mb-2"),
                    html.P("Manufacturers", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className="fas fa-tractor fa-2x text-info mb-3"),
                    html.H4(f"{unique_models}", className="text-info mb-2"),
                    html.P("Tractor Models", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className="fas fa-dollar-sign fa-2x text-warning mb-3"),
                    html.H4(f"${avg_price_min:,.0f} - ${avg_price_max:,.0f}", className="text-warning mb-2"),
                    html.P("Avg Price Range", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className="fas fa-chart-line fa-2x text-danger mb-3"),
                    html.H4(f"{avg_sales_min:,.0f} - {avg_sales_max:,.0f}", className="text-danger mb-2"),
                    html.P("Avg Tractor Unit Monthly Sales", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"})
    ]
    
    return dbc.Row([
        dbc.Col(card, width=3, className="mb-3") for card in cards
    ], justify="center")

# Callback to update charts
@app.callback(
    Output("charts-container", "children"),
    [Input("manufacturer-filter", "value"),
     Input("brand-filter", "value"),
     Input("model-filter", "value"),
     Input("hp-segment-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value")]
)
def update_charts(manufacturer, brand, model, hp_segment, 
                 import_country, destination_country, year, month):
    """Update charts based on filter selections"""
    
    # Apply filters
    filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, 
                              import_country, destination_country, year, month)
    
    if filtered_df.empty:
        return html.Div([
            dbc.Alert("No data matches the selected filters. Please adjust your filter criteria.", color="warning")
        ])
    
    charts = []
    
    # 1. Monthly Sales Chart - Sales by month
    monthly_data = filtered_df.groupby(['Month', 'Manufacturer Name'])['Sales_Min'].sum().reset_index()
    # Convert month numbers to month names
    monthly_data['Month_Name'] = monthly_data['Month'].apply(lambda x: datetime(2024, x, 1).strftime('%B'))
    
    # Handle month filtering logic
    if month == 'All':
        # Show all months - ensure we have data for all months
        all_months = list(range(1, 13))
        manufacturers = monthly_data['Manufacturer Name'].unique()
        complete_data = []
        
        for manufacturer in manufacturers:
            manufacturer_data = monthly_data[monthly_data['Manufacturer Name'] == manufacturer]
            for m in all_months:
                month_name = datetime(2024, m, 1).strftime('%B')
                existing_data = manufacturer_data[manufacturer_data['Month'] == m]
                if len(existing_data) > 0:
                    complete_data.append({
                        'Month': m,
                        'Manufacturer Name': manufacturer,
                        'Sales_Min': existing_data['Sales_Min'].iloc[0],
                        'Month_Name': month_name
                    })
                else:
                    # Add zero sales for missing months
                    complete_data.append({
                        'Month': m,
                        'Manufacturer Name': manufacturer,
                        'Sales_Min': 0,
                        'Month_Name': month_name
                    })
        
        monthly_data = pd.DataFrame(complete_data)
    else:
        # Show only the selected month - filter the data to show only that month
        selected_month = int(month)
        monthly_data = monthly_data[monthly_data['Month'] == selected_month]
        
        # If no data for the selected month, create empty data structure
        if monthly_data.empty:
            manufacturers = filtered_df['Manufacturer Name'].unique()
            month_name = datetime(2024, selected_month, 1).strftime('%B')
            monthly_data = pd.DataFrame([{
                'Month': selected_month,
                'Manufacturer Name': manufacturer,
                'Sales_Min': 0,
                'Month_Name': month_name
            } for manufacturer in manufacturers])
    
    # Determine chart type, title and configuration based on month filter
    if month == 'All':
        chart_title = "Monthly Tractor Sales (in units)"
        xaxis_config = {'categoryorder': 'array', 'categoryarray': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}
        
        # Create line chart for all months
        fig_time = px.line(
            monthly_data,
            x='Month_Name',
            y='Sales_Min',
            color='Manufacturer Name',
            title=chart_title,
            labels={'Sales_Min': 'Monthly Tractor Sales Volume (in units)', 'Month_Name': 'Month'},
            template="plotly_white"
        )
    else:
        selected_month_name = datetime(2024, int(month), 1).strftime('%B')
        chart_title = f"Sales by Manufacturer - {selected_month_name}"
        
        # Create bar chart for specific month - show manufacturers on x-axis
        fig_time = px.bar(
            monthly_data,
            x='Manufacturer Name',
            y='Sales_Min',
            color='Manufacturer Name',
            title=chart_title,
            labels={'Sales_Min': f'Tractor Sales Volume in {selected_month_name} (units)', 'Manufacturer Name': 'Manufacturer'},
            template="plotly_white"
        )
        xaxis_config = {}
    
    fig_time.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=10),
        title_font_size=16,
        xaxis=dict(**xaxis_config, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9)),
        showlegend=True if month == 'All' else False  # Hide legend for single month bar chart
    )
    charts.append(dcc.Graph(figure=fig_time, className="shadow-sm"))
    
    # 2. Price vs HP Scatter Plot
    fig_price_hp = px.scatter(
        filtered_df,
        x='HP_Min',
        y='Price_Min',
        size='Sales_Min',
        color='Manufacturer Name',
        hover_name='Model Name',
        hover_data=['Brand Name', 'Price_Max', 'Sales_Max'],
        title="Tractor Price vs Tractor Horsepower Analysis",
        labels={'HP_Min': 'Horsepower (HP)', 'Price_Min': 'Price (US$)'},
        template="plotly_white"
    )
    fig_price_hp.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=10),
        title_font_size=16,
        xaxis=dict(tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9))
    )
    charts.append(dcc.Graph(figure=fig_price_hp, className="shadow-sm"))
    
    # 3. Manufacturer Market Share
    manufacturer_sales = filtered_df.groupby('Manufacturer Name')['Sales_Min'].sum().sort_values(ascending=False)
    fig_manufacturer = px.pie(
        values=manufacturer_sales.values,
        names=manufacturer_sales.index,
        title="Market Share by Tractor Manufacturers (Units, Percentage)",
        template="plotly_white"
    )
    fig_manufacturer.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=10),
        title_font_size=16
    )
    charts.append(dcc.Graph(figure=fig_manufacturer, className="shadow-sm"))
    
    # 4. HP Category Distribution
    hp_category_counts = filtered_df['HP_Category'].value_counts()
    fig_hp_category = px.bar(
        x=hp_category_counts.index,
        y=hp_category_counts.values,
        title="Distribution by HP Category",
        labels={'x': 'HP Category', 'y': 'Number of Tractor Sold (Unit)'},
        template="plotly_white"
    )
    fig_hp_category.update_layout(
        height=400,
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=10),
        title_font_size=16,
        xaxis=dict(tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9))
    )
    charts.append(dcc.Graph(figure=fig_hp_category, className="shadow-sm"))
    
    return dbc.Row([
        dbc.Col(chart, width=6, className="mb-4") for chart in charts
    ], justify="center")

# Callback to update data table
@app.callback(
    Output("data-table-container", "children"),
    [Input("manufacturer-filter", "value"),
     Input("brand-filter", "value"),
     Input("model-filter", "value"),
     Input("hp-segment-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value")]
)
def update_data_table(manufacturer, brand, model, hp_segment, 
                      import_country, destination_country, year, month):
    """Update data table based on filter selections"""
    
    # Apply filters
    filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, 
                              import_country, destination_country, year, month)
    
    if filtered_df.empty:
        return html.Div([
            dbc.Alert("No data matches the selected filters. Please adjust your filter criteria.", color="warning")
        ])
    
    # Prepare data for table (limit to first 1000 records for performance)
    display_df = filtered_df.head(1000)
    
    # Select columns to display
    table_columns = [
        'Manufacturer Name', 'Brand Name', 'Model Name', 'HP Segment',
        'Dollar Value of Tractor (ASP Range in US$)', 'Monthly Sale Data (Units)',
        'Imported From (Country Name)', 'End Destination Country', 'Month', 'Year'
    ]
    
    table_data = display_df[table_columns].to_dict('records')
    
    table = dash_table.DataTable(
        data=table_data,
        columns=[{"name": col, "id": col} for col in table_columns],
        style_cell={'textAlign': 'left', 'fontSize': 12},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=20,
        sort_action="native",
        filter_action="native",
        export_format="csv"
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-table me-2"),
                f"Filtered Data Table ({len(display_df):,} records shown)"
            ], className="mb-0")
        ]),
        dbc.CardBody([table])
    ], className="shadow-sm")

# Callback for CSV download
@app.callback(
    Output("download-csv", "children"),
    [Input("download-csv-btn", "n_clicks"),
     Input("manufacturer-filter", "value"),
     Input("brand-filter", "value"),
     Input("model-filter", "value"),
     Input("hp-segment-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value")]
)
def download_csv(n_clicks, manufacturer, brand, model, hp_segment, 
                import_country, destination_country, year, month):
    """Handle CSV download"""
    if n_clicks:
        # Apply filters
        filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, 
                                  import_country, destination_country, year, month)
        
        # Convert to CSV
        csv_string = filtered_df.to_csv(index=False)
        csv_b64 = base64.b64encode(csv_string.encode()).decode()
        
        return dcc.Download(
            id="download-csv-file",
            data=dict(content=csv_string, filename=f"tractor_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        )
    return ""

# Callback for Excel download
@app.callback(
    Output("download-excel", "children"),
    [Input("download-excel-btn", "n_clicks"),
     Input("manufacturer-filter", "value"),
     Input("brand-filter", "value"),
     Input("model-filter", "value"),
     Input("hp-segment-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value")]
)
def download_excel(n_clicks, manufacturer, brand, model, hp_segment, 
                  import_country, destination_country, year, month):
    """Handle Excel download"""
    if n_clicks:
        # Apply filters
        filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, 
                                  import_country, destination_country, year, month)
        
        # Convert to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='Filtered Data', index=False)
        
        excel_data = output.getvalue()
        excel_b64 = base64.b64encode(excel_data).decode()
        
        return dcc.Download(
            id="download-excel-file",
            data=dict(content=excel_b64, filename=f"tractor_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        )
    return ""

def apply_filters(df, manufacturer, brand, model, hp_segment, 
                 import_country, destination_country, year, month):
    """Apply all filters to the dataframe"""
    filtered_df = df.copy()
    
    if manufacturer != 'All':
        filtered_df = filtered_df[filtered_df['Manufacturer Name'] == manufacturer]
    if brand != 'All':
        filtered_df = filtered_df[filtered_df['Brand Name'] == brand]
    if model != 'All':
        filtered_df = filtered_df[filtered_df['Model Name'] == model]
    if hp_segment != 'All':
        filtered_df = filtered_df[filtered_df['HP Segment'] == hp_segment]
    if import_country != 'All':
        filtered_df = filtered_df[filtered_df['Imported From (Country Name)'] == import_country]
    if destination_country != 'All':
        filtered_df = filtered_df[filtered_df['End Destination Country'] == destination_country]
    if year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == year]
    if month != 'All':
        filtered_df = filtered_df[filtered_df['Month'] == month]
    
    return filtered_df

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8055)))
