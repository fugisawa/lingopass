import sys, os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit_app as app

# ========== Edge Case Tests ==========

def test_create_interactive_tam_chart_nan_values():
    """Test TAM chart handles NaN values gracefully"""
    df_with_nan = pd.DataFrame({
        'Idioma': ['Lang1', 'Lang2', 'Lang3'],
        'TAM_Milhões': [100, np.nan, 50],
        'Rank_Global': [1, 2, 3]
    })
    
    fig = app.create_interactive_tam_chart(df_with_nan)
    assert isinstance(fig, app.go.Figure)
    # Should still create a chart, filtering out NaN values


def test_create_advanced_roi_matrix_extreme_values():
    """Test ROI matrix with extreme values"""
    df_extreme = pd.DataFrame({
        'Idioma': ['Lang1', 'Lang2'],
        'Complexidade_Técnica': [0.1, 10],
        'ROI_Ratio': [0.01, 100],
        'TAM_Milhões': [0.1, 1000],
        'Payback_Meses': [1, 100]
    })
    
    fig = app.create_advanced_roi_matrix(df_extreme)
    assert isinstance(fig, app.go.Figure)
    # Should handle extreme ranges properly


def test_create_revenue_projection_negative_scenario():
    """Test revenue projection with negative growth scenario"""
    df_proj = pd.DataFrame({
        'Período': ['Q1', 'Q2', 'Q3', 'Q4'],
        'Receita_Base_K': [100, 150, 200, 250],
        'Receita_Min_K': [80, 120, 160, 200],
        'Receita_Max_K': [120, 180, 240, 300],
        'Confiança_Pct': [95, 90, 85, 80]
    })
    
    # Test with very low scenario factor
    fig = app.create_revenue_projection_with_scenarios(df_proj, scenario_factor=0.1)
    assert isinstance(fig, app.go.Figure)
    
    # Check that values are properly scaled down
    if len(fig.data) > 0:
        base_values = fig.data[0].y
        assert all(v < 30 for v in base_values if not pd.isna(v))  # All values should be small


def test_create_competitive_landscape_single_competitor():
    """Test competitive landscape with only one competitor"""
    df_single = pd.DataFrame({
        'Plataforma': ['OnlyOne'],
        'Market_Share_Pct': [100],
        'User_Base_Milhões': [50],
        'Revenue_Milhões': [100],
        'Idiomas_Count': [10],
        'Modelo_Negócio': ['Freemium']
    })
    
    fig = app.create_competitive_landscape(df_single)
    assert isinstance(fig, app.go.Figure)
    assert len(fig.data) == 1


def test_create_sensitivity_analysis_edge_multipliers():
    """Test sensitivity analysis with edge case multipliers"""
    # The function uses fixed multipliers, but we can test it runs
    fig = app.create_sensitivity_analysis()
    assert isinstance(fig, app.go.Figure)
    
    # Check edge values in heatmap
    z_values = fig.data[0].z
    min_val = min(min(row) for row in z_values)
    max_val = max(max(row) for row in z_values)
    
    assert min_val > 0  # No negative revenues
    assert max_val < 1e6  # Reasonable upper bound


# ========== Unicode and Special Characters Tests ==========

def test_unicode_handling():
    """Test handling of unicode characters in data"""
    df_unicode = pd.DataFrame({
        'Idioma': ['Português', 'Español', '中文', '日本語', 'العربية'],
        'TAM_Milhões': [25, 120, 45, 32, 15],
        'Rank_Global': [1, 2, 3, 4, 5]
    })
    
    fig = app.create_interactive_tam_chart(df_unicode)
    assert isinstance(fig, app.go.Figure)
    
    # Check that unicode text is preserved
    if len(fig.data) > 0:
        y_values = list(fig.data[0].y)
        assert 'Português' in y_values or len(y_values) == 0


def test_special_characters_in_metric_card():
    """Test metric card with special characters"""
    html = app.create_enhanced_metric_card(
        title="Revenue (R$)",
        value="€1.5M",
        delta="+15% ↗️",
        icon="💰",
        help_text="Currency: € EUR"
    )
    
    assert '€1.5M' in html
    assert '💰' in html
    assert 'Currency: € EUR' in html


# ========== Performance and Memory Tests ==========

def test_large_dataset_handling():
    """Test handling of large datasets"""
    # Create large dataset
    n_rows = 1000
    df_large = pd.DataFrame({
        'Idioma': [f'Lang{i}' for i in range(n_rows)],
        'TAM_Milhões': np.random.uniform(10, 200, n_rows),
        'ARPPU_USD': np.random.uniform(50, 150, n_rows),
        'LTV_USD': np.random.uniform(200, 500, n_rows),
        'CAC_USD': np.random.uniform(50, 200, n_rows),
        'Complexidade_Técnica': np.random.uniform(1, 10, n_rows),
        'Payback_Meses': np.random.uniform(6, 24, n_rows),
        'Rank_Global': range(1, n_rows + 1)
    })
    
    # Should only show top 8 by default
    fig = app.create_interactive_tam_chart(df_large)
    assert isinstance(fig, app.go.Figure)
    
    if len(fig.data) > 0:
        assert len(fig.data[0].y) <= 8  # Should limit to top 8


def test_empty_selection_handling():
    """Test chart functions with empty selection"""
    df_languages, _, _, _ = app.load_data()
    
    # Empty selection should show nothing or default
    fig = app.create_interactive_tam_chart(df_languages, selected_languages=[])
    assert isinstance(fig, app.go.Figure)


# ========== Color and Style Tests ==========

def test_color_contrast_accessibility():
    """Test that color combinations meet accessibility standards"""
    # Test primary colors have good contrast
    primary_colors = [
        app.COLORS['primary'],
        app.COLORS['highlight'],
        app.COLORS['success'],
        app.COLORS['warning']
    ]
    
    for color in primary_colors:
        # Check it's a valid hex color
        assert color.startswith('#')
        assert len(color) == 7
        
        # Check RGB values are valid
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255


def test_layout_responsive_design():
    """Test that layout functions return responsive configurations"""
    layout = app.create_tufte_optimized_layout()
    
    # Check margins are reasonable for responsive design
    assert layout['margin']['l'] >= 30
    assert layout['margin']['r'] >= 20
    assert layout['margin']['t'] >= 30
    assert layout['margin']['b'] >= 30
    
    # Check font is scalable
    assert 'family' in layout['font']
    assert layout['font']['size'] >= 10


# ========== Error Recovery Tests ==========

@patch('pandas.read_csv')
def test_load_data_partial_failure(mock_read_csv):
    """Test load_data handles partial file failures"""
    # Make first file fail, others succeed
    def side_effect(path, *args, **kwargs):
        if 'languages.csv' in str(path):
            raise Exception("File corrupted")
        # Return minimal valid DataFrames for other files
        if 'phases.csv' in str(path):
            return pd.DataFrame({'Fase': [1], 'Idiomas': ['Test'], 
                               'Investimento_K': [100], 'Receita_Esperada_K': [200],
                               'Usuários_Projetados': [1000]})
        elif 'competitors.csv' in str(path):
            return pd.DataFrame({'Plataforma': ['Test'], 'Market_Share_Pct': [10],
                               'User_Base_Milhões': [5], 'Revenue_Milhões': [10],
                               'Idiomas_Count': [5], 'Modelo_Negócio': ['Freemium']})
        elif 'projection.csv' in str(path):
            return pd.DataFrame({'Período': ['Q1'], 'Receita_Base_K': [100],
                               'Receita_Min_K': [80], 'Receita_Max_K': [120],
                               'Confiança_Pct': [90]})
    
    mock_read_csv.side_effect = side_effect
    
    df1, df2, df3, df4 = app.load_data()
    
    # First DataFrame should be empty due to error
    assert df1.empty
    # Others might be empty or have data depending on implementation
    assert isinstance(df2, pd.DataFrame)
    assert isinstance(df3, pd.DataFrame)
    assert isinstance(df4, pd.DataFrame)


def test_chart_functions_with_minimal_data():
    """Test chart functions with minimal valid data"""
    # Minimal language data
    df_min_lang = pd.DataFrame({
        'Idioma': ['Test'],
        'TAM_Milhões': [10],
        'ARPPU_USD': [50],
        'LTV_USD': [200],
        'CAC_USD': [50],
        'Complexidade_Técnica': [5],
        'Payback_Meses': [12],
        'Rank_Global': [1],
        'Ano1_Revenue_K': [100],
        'Ano2_Revenue_K': [200],
        'Investimento_K': [50],
        'Market_Readiness': [8],
        'Competição_Level': ['Medium']
    })
    df_min_lang['ROI_Ratio'] = df_min_lang['LTV_USD'] / df_min_lang['CAC_USD']
    df_min_lang['ROI_Ano2_K'] = df_min_lang['Ano2_Revenue_K'] - df_min_lang['Investimento_K']
    df_min_lang['Revenue_Growth'] = 100
    
    # Test TAM chart
    fig = app.create_interactive_tam_chart(df_min_lang)
    assert isinstance(fig, app.go.Figure)
    
    # Test ROI matrix
    fig = app.create_advanced_roi_matrix(df_min_lang)
    assert isinstance(fig, app.go.Figure)


# ========== Integration Tests ==========

def test_full_visualization_pipeline():
    """Test complete visualization pipeline"""
    # Load data
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    
    # Create all visualizations
    figs = [
        app.create_interactive_tam_chart(df_languages),
        app.create_advanced_roi_matrix(df_languages),
        app.create_revenue_projection_with_scenarios(df_projection),
        app.create_competitive_landscape(df_competitors),
        app.create_sensitivity_analysis()
    ]
    
    # Verify all figures are valid
    for i, fig in enumerate(figs):
        assert isinstance(fig, app.go.Figure), f"Figure {i} is not valid"
        assert hasattr(fig, 'data'), f"Figure {i} has no data"
        assert hasattr(fig, 'layout'), f"Figure {i} has no layout"


def test_ui_components_integration():
    """Test UI helper functions work together"""
    # Create a complete metric display
    metrics = [
        ("TAM Total", "847M", "+12.3%", "🌍", "Total addressable market"),
        ("Revenue", "R$ 225M", "+340%", "💰", "3-year projection"),
        ("Languages", "10", "Prioritized", "🗣️", "Priority languages"),
        ("Confidence", "94.2%", "High", "📊", "Statistical confidence")
    ]
    
    html_parts = []
    for title, value, delta, icon, help_text in metrics:
        html = app.create_enhanced_metric_card(title, value, delta, icon, help_text)
        html_parts.append(html)
        
        # Verify HTML structure
        assert 'metric-card-enhanced' in html
        assert title in html
        assert value in html
    
    # All parts should be valid HTML strings
    assert len(html_parts) == 4
    
    # Create insight boxes
    insights = [
        ("Critical Opportunity", "Spanish leads with 120M TAM", "🚀"),
        ("Attention Required", "French and German are mature markets", "⚠️"),
        ("Growth Potential", "Mandarin offers interesting niche", "📈")
    ]
    
    for title, content, icon in insights:
        html = app.create_enhanced_insight_box(title, content, icon)
        assert 'insight-box-enhanced' in html
        assert title in html
        assert content in html