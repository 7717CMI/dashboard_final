# Comprehensive Tractor Market Analysis Dashboard

A powerful Plotly-based dashboard for analyzing tractor market data with advanced filtering capabilities and export functionality.

## Features

### 📊 Comprehensive Data Analysis
- **936 records** spanning 2+ years (2022-2024) with monthly data
- **7 major manufacturers** including Kubota, John Deere, Yanmar, and more
- **Seasonal variations** in sales data for realistic market simulation
- **Complete field coverage** with all original data fields plus Month and Year

### 🔍 Advanced Filtering System
- **Manufacturer Filter**: Filter by specific tractor manufacturers
- **Brand Filter**: Filter by brand names (dynamically updates based on manufacturer)
- **Model Filter**: Filter by specific model names (dynamically updates based on brand)
- **HP Segment Filter**: Filter by horsepower ranges
- **Price Category Filter**: Filter by price ranges (Budget, Mid-Range, Premium, etc.)
- **Sales Category Filter**: Filter by sales volume categories
- **Import Country Filter**: Filter by country of origin
- **Destination Country Filter**: Filter by destination markets
- **Year Filter**: Filter by specific years (2022, 2023, 2024)
- **Month Filter**: Filter by specific months (1-12)
- **Price Range Slider**: Interactive slider for price range filtering
- **Sales Range Slider**: Interactive slider for sales volume filtering

### 📈 Interactive Visualizations
1. **Time Series Chart**: Monthly sales trends by manufacturer
2. **Scatter Plot**: Price vs Horsepower analysis with sales volume sizing
3. **Pie Chart**: Market share by manufacturer
4. **Bar Chart**: Distribution by HP categories
5. **Sunburst Chart**: Trade flow analysis (Import → Destination)
6. **Histogram**: Price distribution analysis

### 📋 Data Display
- **Summary Cards**: Key metrics including total records, manufacturers, models, average prices, and sales
- **Interactive Data Table**: Sortable and filterable table with pagination
- **Real-time Updates**: All visualizations update dynamically based on filter selections

### 💾 Export Functionality
- **CSV Export**: Download filtered data as CSV file
- **Excel Export**: Download filtered data as Excel file
- **Timestamped Files**: Automatic filename generation with timestamps
- **Filtered Data**: Only exports data matching current filter criteria

## Data Structure

The dashboard includes the following fields:

| Field | Description | Type |
|-------|-------------|------|
| Manufacturer Name | Tractor manufacturer | String |
| Brand Name | Brand/series name | String |
| Model Name | Specific model names | String |
| HP Segment | Horsepower range | String |
| Dollar Value of Tractor | Price range in US$ | String |
| Monthly Sale Data | Sales volume range | String |
| Imported From | Country of origin | String |
| End Destination Country | Destination market | String |
| Month | Month (1-12) | Integer |
| Year | Year (2022-2024) | Integer |

### Additional Calculated Fields
- **HP_Min/Max**: Extracted numeric horsepower values
- **Price_Min/Max**: Extracted numeric price values
- **Sales_Min/Max**: Extracted numeric sales values
- **Date**: Combined year-month date field
- **HP_Category**: Categorized horsepower ranges
- **Price_Category**: Categorized price ranges
- **Sales_Category**: Categorized sales volumes

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation Steps

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:
   ```bash
   python comprehensive_dashboard.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:8050`

### Dependencies
- `dash>=2.14.0` - Web application framework
- `plotly>=5.17.0` - Interactive plotting library
- `pandas>=2.1.0` - Data manipulation library
- `openpyxl>=3.1.0` - Excel file support
- `dash-bootstrap-components>=1.5.0` - Bootstrap components for Dash
- `numpy>=1.24.0` - Numerical computing library

## Usage Guide

### 1. Filtering Data
- Use the **Advanced Filters** section to narrow down your analysis
- Filters are cascading (e.g., selecting a manufacturer updates available brands)
- Use range sliders for continuous variables like price and sales
- All filters work together to provide precise data selection

### 2. Analyzing Trends
- **Time Series Chart**: Shows sales trends over time by manufacturer
- **Scatter Plot**: Reveals relationships between price, horsepower, and sales
- **Market Share**: Understand manufacturer dominance in the market

### 3. Exporting Data
- Click **Download CSV** or **Download Excel** buttons
- Files will be automatically downloaded with timestamps
- Only filtered data matching your current selection will be exported

### 4. Data Table
- Scroll through the interactive table to see detailed records
- Use built-in sorting and filtering within the table
- Table shows up to 1000 records for performance

## Testing

Run the comprehensive test suite to verify all functionality:

```bash
python test_comprehensive_dashboard.py
```

The test suite verifies:
- ✅ Data creation and quality
- ✅ Filter functionality
- ✅ Chart creation
- ✅ Export functionality

## Data Characteristics

### Manufacturers Included
- Kubota Corporation
- Yanmar Holdings
- Mitsubishi Mahindra Agricultural Machinery
- Iseki & Co. Ltd.
- John Deere
- AGCO
- CNH Industrial (New Holland)

### Market Segments
- **HP Categories**: Compact (0-30 HP) to Ultra High (500+ HP)
- **Price Ranges**: Budget ($0-20k) to Ultra Luxury ($500k+)
- **Sales Volumes**: Low Volume (0-50) to Mass Market (1000+)

### Geographic Coverage
- **Import Countries**: Japan, USA, India, Germany, France, South Korea, Brazil, China, Turkey, UK, Austria
- **Destination Markets**: USA, EU, Australia, Latin America, Asia-Pacific

## Technical Architecture

### Frontend
- **Dash Framework**: Python-based web application
- **Bootstrap Components**: Responsive UI components
- **Font Awesome Icons**: Professional iconography
- **Plotly Charts**: Interactive visualizations

### Backend
- **Pandas**: Data processing and manipulation
- **NumPy**: Numerical computations
- **OpenPyXL**: Excel file generation
- **Base64**: File encoding for downloads

### Data Processing
- **Seasonal Modeling**: Realistic sales variations by season
- **Range Extraction**: Parsing of text-based ranges to numeric values
- **Category Creation**: Automatic categorization of continuous variables
- **Date Handling**: Proper datetime processing for time series analysis

## Performance Considerations

- **Data Limiting**: Table displays max 1000 records for performance
- **Efficient Filtering**: Optimized filter application
- **Lazy Loading**: Charts update only when filters change
- **Memory Management**: Efficient data structures and processing

## Future Enhancements

Potential improvements for future versions:
- Real-time data integration
- Advanced statistical analysis
- Custom chart configurations
- User preference saving
- Multi-language support
- Mobile-responsive optimizations

## Support

For issues or questions:
1. Check the test suite results
2. Verify all dependencies are installed
3. Ensure Python 3.8+ compatibility
4. Check browser console for any JavaScript errors

---

**Dashboard Version**: 1.0  
**Last Updated**: December 2024  
**Compatible Browsers**: Chrome, Firefox, Safari, Edge

