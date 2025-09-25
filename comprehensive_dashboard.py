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
    
    # Generate data for each month from 2022 to 2024
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    
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
            total_factor = seasonal_factor * random_factor
            
            adjusted_sales_min = int(base_sales_min * total_factor)
            adjusted_sales_max = int(base_sales_max * total_factor)
            
            comprehensive_data.append([
                row[0],  # Manufacturer Name
                row[1],  # Brand Name
                row[2],  # Model Name
                row[3],  # HP Segment
                row[4],  # Dollar Value
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
                              labels=['Compact (0-30 HP)', 'Mid-Range (30-60 HP)', 'Standard (60-100 HP)', 
                                     'Heavy Duty (100-200 HP)', 'High Performance (200-500 HP)', 'Ultra High (500+ HP)'])
    
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
hp_categories = sorted(df['HP_Category'].dropna().unique())
price_categories = sorted(df['Price_Category'].dropna().unique())
sales_categories = sorted(df['Sales_Category'].dropna().unique())
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
                            html.Label("Brand:", className="fw-bold"),
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
                            html.Label("Price Category:", className="fw-bold"),
                            dcc.Dropdown(
                                id='price-category-filter',
                                options=[{'label': 'All Price Categories', 'value': 'All'}] + 
                                        [{'label': p, 'value': p} for p in price_categories],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("Sales Category:", className="fw-bold"),
                            dcc.Dropdown(
                                id='sales-category-filter',
                                options=[{'label': 'All Sales Categories', 'value': 'All'}] + 
                                        [{'label': s, 'value': s} for s in sales_categories],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3),
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
                        ], width=3),
                        dbc.Col([
                            html.Label("Destination Country:", className="fw-bold"),
                            dcc.Dropdown(
                                id='destination-country-filter',
                                options=[{'label': 'All Destination Countries', 'value': 'All'}] + 
                                        [{'label': c, 'value': c} for c in destination_countries],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=3)
                    ]),
                    
                    # Third row - Time filters and Range sliders
                    dbc.Row([
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
                                        [{'label': f"{m:02d}", 'value': m} for m in months],
                                value='All',
                                clearable=False,
                                className="mb-3"
                            )
                        ], width=2),
                        dbc.Col([
                            html.Label("Price Range (US$):", className="fw-bold"),
                            dcc.RangeSlider(
                                id='price-range-slider',
                                min=int(df['Price_Min'].min()),
                                max=int(df['Price_Max'].max()),
                                value=[int(df['Price_Min'].min()), int(df['Price_Max'].max())],
                                marks={int(i): f'${i:,.0f}' for i in range(int(df['Price_Min'].min()), int(df['Price_Max'].max()) + 1, 50000)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                className="mb-3"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Sales Range (Units):", className="fw-bold"),
                            dcc.RangeSlider(
                                id='sales-range-slider',
                                min=int(df['Sales_Min'].min()),
                                max=int(df['Sales_Max'].max()),
                                value=[int(df['Sales_Min'].min()), int(df['Sales_Max'].max())],
                                marks={int(i): f'{i:,.0f}' for i in range(int(df['Sales_Min'].min()), int(df['Sales_Max'].max()) + 1, 100)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                className="mb-3"
                            )
                        ], width=4)
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
     Input("price-category-filter", "value"),
     Input("sales-category-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value"),
     Input("price-range-slider", "value"),
     Input("sales-range-slider", "value")]
)
def update_summary_cards(manufacturer, brand, model, hp_segment, price_category, sales_category, 
                        import_country, destination_country, year, month, price_range, sales_range):
    """Update summary cards based on filter selections"""
    
    # Apply filters
    filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, price_category, 
                              sales_category, import_country, destination_country, year, month, 
                              price_range, sales_range)
    
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
                    html.I(className="fas fa-database fa-2x text-primary mb-3"),
                    html.H4(f"{total_records:,}", className="text-primary mb-2"),
                    html.P("Total Records", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"}),
        
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
                    html.P("Unique Models", className="mb-0 text-muted")
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
                    html.P("Avg Monthly Sales", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className="fas fa-shopping-cart fa-2x text-secondary mb-3"),
                    html.H4(f"{total_sales_min:,.0f} - {total_sales_max:,.0f}", className="text-secondary mb-2"),
                    html.P("Total Sales Range", className="mb-0 text-muted")
                ], className="text-center")
            ])
        ], className="text-center shadow-sm border-0", style={"border-radius": "15px"})
    ]
    
    return dbc.Row([
        dbc.Col(card, width=2, className="mb-3") for card in cards
    ], justify="center")

# Callback to update charts
@app.callback(
    Output("charts-container", "children"),
    [Input("manufacturer-filter", "value"),
     Input("brand-filter", "value"),
     Input("model-filter", "value"),
     Input("hp-segment-filter", "value"),
     Input("price-category-filter", "value"),
     Input("sales-category-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value"),
     Input("price-range-slider", "value"),
     Input("sales-range-slider", "value")]
)
def update_charts(manufacturer, brand, model, hp_segment, price_category, sales_category, 
                 import_country, destination_country, year, month, price_range, sales_range):
    """Update charts based on filter selections"""
    
    # Apply filters
    filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, price_category, 
                              sales_category, import_country, destination_country, year, month, 
                              price_range, sales_range)
    
    if filtered_df.empty:
        return html.Div([
            dbc.Alert("No data matches the selected filters. Please adjust your filter criteria.", color="warning")
        ])
    
    charts = []
    
    # 1. Time Series Chart - Sales over time
    time_series_data = filtered_df.groupby(['Date', 'Manufacturer Name'])['Sales_Min'].sum().reset_index()
    fig_time = px.line(
        time_series_data,
        x='Date',
        y='Sales_Min',
        color='Manufacturer Name',
        title="Monthly Sales Trends by Manufacturer",
        labels={'Sales_Min': 'Monthly Sales (Units)', 'Date': 'Date'},
        template="plotly_white"
    )
    fig_time.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
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
        title="Price vs Horsepower Analysis",
        labels={'HP_Min': 'Horsepower (HP)', 'Price_Min': 'Price (US$)'},
        template="plotly_white"
    )
    fig_price_hp.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
    )
    charts.append(dcc.Graph(figure=fig_price_hp, className="shadow-sm"))
    
    # 3. Manufacturer Market Share
    manufacturer_sales = filtered_df.groupby('Manufacturer Name')['Sales_Min'].sum().sort_values(ascending=False)
    fig_manufacturer = px.pie(
        values=manufacturer_sales.values,
        names=manufacturer_sales.index,
        title="Market Share by Manufacturer (Total Sales)",
        template="plotly_white"
    )
    fig_manufacturer.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
    )
    charts.append(dcc.Graph(figure=fig_manufacturer, className="shadow-sm"))
    
    # 4. HP Category Distribution
    hp_category_counts = filtered_df['HP_Category'].value_counts()
    fig_hp_category = px.bar(
        x=hp_category_counts.index,
        y=hp_category_counts.values,
        title="Distribution by HP Category",
        labels={'x': 'HP Category', 'y': 'Number of Records'},
        template="plotly_white"
    )
    fig_hp_category.update_layout(
        height=400,
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
    )
    charts.append(dcc.Graph(figure=fig_hp_category, className="shadow-sm"))
    
    # 5. Trade Flow Analysis
    trade_flow = filtered_df.groupby(['Imported From (Country Name)', 'End Destination Country']).size().reset_index(name='Count')
    fig_trade = px.sunburst(
        trade_flow,
        path=['Imported From (Country Name)', 'End Destination Country'],
        values='Count',
        title="Trade Flow Analysis",
        template="plotly_white"
    )
    fig_trade.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
    )
    charts.append(dcc.Graph(figure=fig_trade, className="shadow-sm"))
    
    # 6. Price Distribution Histogram
    fig_price_dist = px.histogram(
        filtered_df,
        x='Price_Min',
        nbins=20,
        title="Price Distribution",
        labels={'Price_Min': 'Price (US$)', 'count': 'Number of Records'},
        template="plotly_white"
    )
    fig_price_dist.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
    )
    charts.append(dcc.Graph(figure=fig_price_dist, className="shadow-sm"))
    
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
     Input("price-category-filter", "value"),
     Input("sales-category-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value"),
     Input("price-range-slider", "value"),
     Input("sales-range-slider", "value")]
)
def update_data_table(manufacturer, brand, model, hp_segment, price_category, sales_category, 
                      import_country, destination_country, year, month, price_range, sales_range):
    """Update data table based on filter selections"""
    
    # Apply filters
    filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, price_category, 
                              sales_category, import_country, destination_country, year, month, 
                              price_range, sales_range)
    
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
     Input("price-category-filter", "value"),
     Input("sales-category-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value"),
     Input("price-range-slider", "value"),
     Input("sales-range-slider", "value")]
)
def download_csv(n_clicks, manufacturer, brand, model, hp_segment, price_category, sales_category, 
                import_country, destination_country, year, month, price_range, sales_range):
    """Handle CSV download"""
    if n_clicks:
        # Apply filters
        filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, price_category, 
                                  sales_category, import_country, destination_country, year, month, 
                                  price_range, sales_range)
        
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
     Input("price-category-filter", "value"),
     Input("sales-category-filter", "value"),
     Input("import-country-filter", "value"),
     Input("destination-country-filter", "value"),
     Input("year-filter", "value"),
     Input("month-filter", "value"),
     Input("price-range-slider", "value"),
     Input("sales-range-slider", "value")]
)
def download_excel(n_clicks, manufacturer, brand, model, hp_segment, price_category, sales_category, 
                  import_country, destination_country, year, month, price_range, sales_range):
    """Handle Excel download"""
    if n_clicks:
        # Apply filters
        filtered_df = apply_filters(df, manufacturer, brand, model, hp_segment, price_category, 
                                  sales_category, import_country, destination_country, year, month, 
                                  price_range, sales_range)
        
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

def apply_filters(df, manufacturer, brand, model, hp_segment, price_category, sales_category, 
                 import_country, destination_country, year, month, price_range, sales_range):
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
    if price_category != 'All':
        filtered_df = filtered_df[filtered_df['Price_Category'] == price_category]
    if sales_category != 'All':
        filtered_df = filtered_df[filtered_df['Sales_Category'] == sales_category]
    if import_country != 'All':
        filtered_df = filtered_df[filtered_df['Imported From (Country Name)'] == import_country]
    if destination_country != 'All':
        filtered_df = filtered_df[filtered_df['End Destination Country'] == destination_country]
    if year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == year]
    if month != 'All':
        filtered_df = filtered_df[filtered_df['Month'] == month]
    
    # Apply range filters
    if price_range:
        filtered_df = filtered_df[
            (filtered_df['Price_Min'] >= price_range[0]) & 
            (filtered_df['Price_Max'] <= price_range[1])
        ]
    if sales_range:
        filtered_df = filtered_df[
            (filtered_df['Sales_Min'] >= sales_range[0]) & 
            (filtered_df['Sales_Max'] <= sales_range[1])
        ]
    
    return filtered_df

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8051)))
