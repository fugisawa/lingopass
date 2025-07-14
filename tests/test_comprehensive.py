import sys, os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit_app as app

# ========== Test Helper Functions ==========

def test_create_tufte_optimized_layout():
    """Test that Tufte layout returns proper structure"""
    layout = app.create_tufte_optimized_layout()
    
    # Check required keys
    assert 'plot_bgcolor' in layout
    assert 'paper_bgcolor' in layout
    assert 'font' in layout
    assert 'margin' in layout
    assert 'xaxis' in layout
    assert 'yaxis' in layout
    
    # Check transparent backgrounds (Tufte principle)
    assert layout['plot_bgcolor'] == 'rgba(0,0,0,0)'
    assert layout['paper_bgcolor'] == 'rgba(0,0,0,0)'
    
    # Check minimal gridlines
    assert layout['xaxis']['showgrid'] == False
    assert layout['yaxis']['showgrid'] == True
    assert layout['yaxis']['gridwidth'] == 0.5


def test_add_accessibility_attrs():
    """Test accessibility attributes are added correctly"""
    mock_fig = MagicMock()
    mock_fig.update_layout = MagicMock()
    
    title = "Test Chart Title"
    description = "Test description"
    
    result = app.add_accessibility_attrs(mock_fig, title, description)
    
    # Check that update_layout was called
    mock_fig.update_layout.assert_called_once()
    
    # Get the args passed to update_layout
    layout_args = mock_fig.update_layout.call_args[1]
    
    # Check title structure
    assert 'title' in layout_args
    assert title in layout_args['title']['text']
    assert layout_args['title']['x'] == 0.02  # Left-aligned
    assert layout_args['title']['font']['size'] == 16


def test_show_loading_state():
    """Test loading state HTML generation"""
    message = "Test loading message"
    html = app.show_loading_state(message)
    
    # Check it's a streamlit markdown object
    assert hasattr(html, '_repr_html_')
    
    # The function returns st.markdown which we can't directly test
    # But we can verify the message would be in the HTML
    # by checking the function parameters


def test_create_enhanced_metric_card():
    """Test metric card HTML generation"""
    title = "Test Metric"
    value = "100K"
    delta = "+10%"
    icon = "📊"
    help_text = "This is a test metric"
    
    html = app.create_enhanced_metric_card(title, value, delta, icon, help_text)
    
    # Check HTML structure
    assert 'metric-card-enhanced' in html
    assert title in html
    assert value in html
    assert delta in html
    assert icon in html
    assert help_text in html
    
    # Check delta styling
    assert '↗️' in html  # Positive delta icon
    assert '#059669' in html  # Positive color


def test_create_enhanced_metric_card_negative_delta():
    """Test metric card with negative delta"""
    html = app.create_enhanced_metric_card("Test", "50K", "-5%")
    
    assert '↘️' in html  # Negative delta icon
    assert '#dc2626' in html  # Negative color


def test_create_enhanced_insight_box():
    """Test insight box HTML generation"""
    title = "Key Insight"
    content = "This is an important insight about the data"
    icon = "💡"
    
    html = app.create_enhanced_insight_box(title, content, icon)
    
    # Check HTML structure
    assert 'insight-box-enhanced' in html
    assert title in html
    assert content in html
    assert icon in html
    assert '<h4' in html
    assert '#1e293b' in html  # Title color


@patch('streamlit.download_button')
def test_create_export_button_dataframe(mock_download_button):
    """Test export button creation for DataFrame"""
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    filename = "test_data"
    
    app.create_export_button(df, filename)
    
    # Check download_button was called
    mock_download_button.assert_called_once()
    
    # Check parameters
    call_args = mock_download_button.call_args
    assert call_args[1]['label'] == "📥 Exportar Dados"
    assert call_args[1]['file_name'] == "test_data.csv"
    assert call_args[1]['mime'] == "text/csv"
    
    # Check CSV data
    csv_data = call_args[1]['data']
    assert 'A,B' in csv_data
    assert '1,4' in csv_data


@patch('streamlit.download_button')
def test_create_export_button_dict(mock_download_button):
    """Test export button creation for dictionary/JSON"""
    data = {'key1': 'value1', 'key2': 'value2'}
    filename = "test_json"
    
    app.create_export_button(data, filename)
    
    # Check download_button was called
    mock_download_button.assert_called_once()
    
    # Check parameters
    call_args = mock_download_button.call_args
    assert call_args[1]['file_name'] == "test_json.json"
    assert call_args[1]['mime'] == "application/json"
    
    # Check JSON data
    json_data = call_args[1]['data']
    assert 'key1' in json_data
    assert 'value1' in json_data


# ========== Test Chart Functions with Edge Cases ==========

def test_create_interactive_tam_chart_empty_data():
    """Test TAM chart with empty DataFrame"""
    df_empty = pd.DataFrame()
    fig = app.create_interactive_tam_chart(df_empty)
    
    assert isinstance(fig, app.go.Figure)
    assert len(fig.data) == 0 or (len(fig.data) == 1 and len(fig.data[0].x) == 0)


def test_create_interactive_tam_chart_with_selection():
    """Test TAM chart with language selection"""
    df_languages, _, _, _ = app.load_data()
    selected = ['Espanhol', 'Francês']
    
    fig = app.create_interactive_tam_chart(df_languages, selected_languages=selected)
    
    assert isinstance(fig, app.go.Figure)
    # Should only show selected languages
    if len(fig.data) > 0:
        y_values = list(fig.data[0].y)
        for lang in selected:
            assert lang in y_values or len(y_values) == 0


def test_create_advanced_roi_matrix_data_types():
    """Test ROI matrix handles different data types correctly"""
    df_languages, _, _, _ = app.load_data()
    fig = app.create_advanced_roi_matrix(df_languages)
    
    assert isinstance(fig, app.go.Figure)
    # Check scatter plot data
    if len(fig.data) > 0:
        assert hasattr(fig.data[0], 'x')
        assert hasattr(fig.data[0], 'y')
        assert hasattr(fig.data[0], 'marker')


def test_create_revenue_projection_scenarios():
    """Test revenue projection with different scenario factors"""
    _, _, _, df_projection = app.load_data()
    
    # Test different scenarios
    for factor in [0.5, 1.0, 1.5, 2.0]:
        fig = app.create_revenue_projection_with_scenarios(df_projection, scenario_factor=factor)
        assert isinstance(fig, app.go.Figure)
        
        # Check that values are scaled by factor
        if len(fig.data) > 0:
            base_trace = fig.data[0]
            if hasattr(base_trace, 'y') and len(base_trace.y) > 0:
                # Values should be scaled
                assert all(y > 0 for y in base_trace.y if not pd.isna(y))


def test_create_competitive_landscape_error_handling():
    """Test competitive landscape handles missing columns gracefully"""
    # Create DataFrame with missing columns
    df_bad = pd.DataFrame({
        'Plataforma': ['Test1', 'Test2'],
        'Market_Share_Pct': [10, 20]
        # Missing other required columns
    })
    
    fig = app.create_competitive_landscape(df_bad)
    assert isinstance(fig, app.go.Figure)
    # Should return error figure
    assert 'annotations' in fig.layout


def test_create_competitive_landscape_empty_data():
    """Test competitive landscape with empty DataFrame"""
    df_empty = pd.DataFrame()
    fig = app.create_competitive_landscape(df_empty)
    
    assert isinstance(fig, app.go.Figure)
    # Should show warning/error message
    if hasattr(fig.layout, 'title'):
        assert 'não disponíve' in str(fig.layout.title.text) or 'annotations' in fig.layout


def test_create_sensitivity_analysis_calculations():
    """Test sensitivity analysis calculations"""
    fig = app.create_sensitivity_analysis()
    
    assert isinstance(fig, app.go.Figure)
    assert len(fig.data) > 0
    
    # Check heatmap data
    heatmap = fig.data[0]
    assert hasattr(heatmap, 'z')
    assert len(heatmap.z) == 11  # 11 TAM variations
    assert len(heatmap.z[0]) == 11  # 11 conversion variations
    
    # Check that revenues increase with multipliers
    z_values = heatmap.z
    assert z_values[0][0] < z_values[-1][-1]  # Bottom-left < Top-right


# ========== Test Data Processing Functions ==========

def test_load_data_calculations():
    """Test that load_data performs calculations correctly"""
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    
    # Check calculated columns exist
    assert 'ROI_Ratio' in df_languages.columns
    assert 'ROI_Ano2_K' in df_languages.columns
    assert 'Revenue_Growth' in df_languages.columns
    
    # Verify calculations
    for idx, row in df_languages.iterrows():
        expected_roi = row['LTV_USD'] / row['CAC_USD']
        assert abs(row['ROI_Ratio'] - expected_roi) < 0.01
        
        expected_roi_ano2 = row['Ano2_Revenue_K'] - row['Investimento_K']
        assert abs(row['ROI_Ano2_K'] - expected_roi_ano2) < 0.01


def test_colors_dictionary():
    """Test COLORS dictionary has all required colors"""
    required_colors = [
        'primary', 'highlight', 'benchmark', 'neutral', 'success',
        'background', 'secondary', 'tertiary', 'quaternary', 'info',
        'warning_bg', 'axis_light', 'axis_medium', 'text_secondary',
        'insight_primary', 'insight_secondary', 'data_focus', 'warning'
    ]
    
    for color in required_colors:
        assert color in app.COLORS
        assert app.COLORS[color].startswith('#')
        assert len(app.COLORS[color]) == 7  # #RRGGBB format


# ========== Test Main Function Components ==========

@patch('streamlit.set_page_config')
@patch('streamlit.markdown')
@patch('streamlit.tabs')
@patch('streamlit.container')
@patch('streamlit.spinner')
@patch('streamlit.columns')
@patch('streamlit.plotly_chart')
@patch('streamlit.metric')
@patch('streamlit.success')
@patch('streamlit.warning')
@patch('streamlit.info')
@patch('streamlit.divider')
@patch('streamlit.slider')
@patch('streamlit.selectbox')
def test_main_function_executes(*mocks):
    """Test that main function executes without errors"""
    # Mock tabs to return mock objects
    mock_tab1 = MagicMock()
    mock_tab2 = MagicMock()
    mock_tab3 = MagicMock()
    mocks[3].return_value = [mock_tab1, mock_tab2, mock_tab3]  # st.tabs
    
    # Mock columns to return mock objects
    mock_cols = [MagicMock() for _ in range(4)]
    mocks[5].return_value = mock_cols  # st.columns
    
    # Call main function
    app.main()
    
    # Check that page config was set
    mocks[0].assert_called_once()  # set_page_config
    
    # Check that some content was rendered
    assert mocks[1].call_count > 0  # markdown called multiple times


# ========== Test Data Validation ==========

def test_data_files_exist():
    """Test that required data files exist"""
    data_dir = app.Path(__file__).parent.parent / "data"
    
    required_files = [
        "languages.csv",
        "phases.csv", 
        "competitors.csv",
        "projection.csv"
    ]
    
    for filename in required_files:
        filepath = data_dir / filename
        assert filepath.exists(), f"Data file {filename} not found"


def test_data_consistency():
    """Test data consistency across files"""
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    
    # Check that all DataFrames have data
    assert len(df_languages) > 0
    assert len(df_phases) > 0
    assert len(df_competitors) > 0
    assert len(df_projection) > 0
    
    # Check data types
    assert df_languages['TAM_Milhões'].dtype in ['float64', 'int64']
    assert df_languages['ROI_Ratio'].dtype == 'float64'
    assert df_projection['Confiança_Pct'].dtype in ['float64', 'int64']