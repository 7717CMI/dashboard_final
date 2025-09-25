#!/usr/bin/env python3
"""
Test script to verify comprehensive dashboard components work correctly
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

def test_comprehensive_data_creation():
    """Test creating comprehensive dummy data"""
    print("Testing comprehensive dummy data creation...")
    
    try:
        # Import the dashboard module
        from comprehensive_dashboard import create_comprehensive_dummy_data
        
        # Create the data
        df = create_comprehensive_dummy_data()
        
        print(f"✓ Data created successfully: {df.shape}")
        print(f"✓ Columns: {df.columns.tolist()}")
        print(f"✓ Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"✓ Manufacturers: {df['Manufacturer Name'].nunique()}")
        print(f"✓ Total records: {len(df):,}")
        
        # Test data quality
        assert len(df) > 0, "Data should not be empty"
        assert 'Month' in df.columns, "Month column should exist"
        assert 'Year' in df.columns, "Year column should exist"
        assert 'Date' in df.columns, "Date column should exist"
        assert df['Price_Min'].min() > 0, "Price should be positive"
        assert df['Sales_Min'].min() > 0, "Sales should be positive"
        
        print("✓ Data quality checks passed")
        return True
        
    except Exception as e:
        print(f"✗ Error creating comprehensive data: {e}")
        return False

def test_filter_functionality():
    """Test filter functionality"""
    print("\nTesting filter functionality...")
    
    try:
        from comprehensive_dashboard import create_comprehensive_dummy_data, apply_filters
        
        df = create_comprehensive_dummy_data()
        
        # Test manufacturer filter
        filtered_df = apply_filters(df, 'Kubota Corporation', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', None, None)
        assert len(filtered_df) > 0, "Manufacturer filter should return data"
        assert all(filtered_df['Manufacturer Name'] == 'Kubota Corporation'), "All records should be Kubota"
        
        # Test year filter
        filtered_df = apply_filters(df, 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 2023, 'All', None, None)
        assert len(filtered_df) > 0, "Year filter should return data"
        assert all(filtered_df['Year'] == 2023), "All records should be from 2023"
        
        # Test month filter
        filtered_df = apply_filters(df, 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 6, None, None)
        assert len(filtered_df) > 0, "Month filter should return data"
        assert all(filtered_df['Month'] == 6), "All records should be from June"
        
        # Test price range filter
        filtered_df = apply_filters(df, 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', [20000, 50000], None)
        assert len(filtered_df) > 0, "Price range filter should return data"
        assert all(filtered_df['Price_Min'] >= 20000), "All prices should be >= 20000"
        assert all(filtered_df['Price_Max'] <= 50000), "All prices should be <= 50000"
        
        print("✓ All filter tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Error testing filters: {e}")
        return False

def test_chart_creation():
    """Test creating charts with the data"""
    print("\nTesting chart creation...")
    
    try:
        from comprehensive_dashboard import create_comprehensive_dummy_data
        
        df = create_comprehensive_dummy_data()
        
        # Test time series chart
        time_data = df.groupby(['Date', 'Manufacturer Name'])['Sales_Min'].sum().reset_index()
        fig_time = px.line(
            time_data,
            x='Date',
            y='Sales_Min',
            color='Manufacturer Name',
            title="Monthly Sales Trends by Manufacturer"
        )
        print("✓ Time series chart created")
        
        # Test scatter plot
        fig_scatter = px.scatter(
            df.head(100),  # Use subset for testing
            x='HP_Min',
            y='Price_Min',
            size='Sales_Min',
            color='Manufacturer Name',
            title="Price vs Horsepower Analysis"
        )
        print("✓ Scatter plot created")
        
        # Test pie chart
        manufacturer_sales = df.groupby('Manufacturer Name')['Sales_Min'].sum()
        fig_pie = px.pie(
            values=manufacturer_sales.values,
            names=manufacturer_sales.index,
            title="Market Share by Manufacturer"
        )
        print("✓ Pie chart created")
        
        # Test bar chart
        hp_counts = df['HP_Category'].value_counts()
        fig_bar = px.bar(
            x=hp_counts.index,
            y=hp_counts.values,
            title="HP Category Distribution"
        )
        print("✓ Bar chart created")
        
        # Test histogram
        fig_hist = px.histogram(
            df,
            x='Price_Min',
            nbins=20,
            title="Price Distribution"
        )
        print("✓ Histogram created")
        
        # Test sunburst chart
        trade_flow = df.groupby(['Imported From (Country Name)', 'End Destination Country']).size().reset_index(name='Count')
        fig_sunburst = px.sunburst(
            trade_flow,
            path=['Imported From (Country Name)', 'End Destination Country'],
            values='Count',
            title="Trade Flow Analysis"
        )
        print("✓ Sunburst chart created")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating charts: {e}")
        return False

def test_export_functionality():
    """Test export functionality"""
    print("\nTesting export functionality...")
    
    try:
        from comprehensive_dashboard import create_comprehensive_dummy_data, apply_filters
        import base64
        import io
        
        df = create_comprehensive_dummy_data()
        
        # Test CSV export
        filtered_df = apply_filters(df, 'John Deere', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', None, None)
        csv_string = filtered_df.to_csv(index=False)
        assert len(csv_string) > 0, "CSV export should not be empty"
        print("✓ CSV export test passed")
        
        # Test Excel export
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='Filtered Data', index=False)
        excel_data = output.getvalue()
        assert len(excel_data) > 0, "Excel export should not be empty"
        print("✓ Excel export test passed")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing exports: {e}")
        return False

if __name__ == "__main__":
    print("Comprehensive Tractor Dashboard - Component Test")
    print("=" * 60)
    
    # Run all tests
    data_test = test_comprehensive_data_creation()
    filter_test = test_filter_functionality()
    chart_test = test_chart_creation()
    export_test = test_export_functionality()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"Data Creation: {'✓ PASS' if data_test else '✗ FAIL'}")
    print(f"Filter Functionality: {'✓ PASS' if filter_test else '✗ FAIL'}")
    print(f"Chart Creation: {'✓ PASS' if chart_test else '✗ FAIL'}")
    print(f"Export Functionality: {'✓ PASS' if export_test else '✗ FAIL'}")
    
    if all([data_test, filter_test, chart_test, export_test]):
        print("\n🎉 All tests passed! Comprehensive dashboard is ready to run.")
        print("Run 'python comprehensive_dashboard.py' to start the dashboard.")
        print("Dashboard will be available at: http://localhost:8050")
        print("\nFeatures included:")
        print("• Comprehensive dummy data with 2+ years of monthly data")
        print("• Advanced filtering for all data fields")
        print("• Monthly and yearly tenure filters")
        print("• Multiple chart types (line, scatter, pie, bar, histogram, sunburst)")
        print("• Export functionality (CSV and Excel)")
        print("• Interactive data table")
        print("• Summary cards with key metrics")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
