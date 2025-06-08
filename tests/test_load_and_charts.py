import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit_app as app
import plotly.graph_objects as go


def test_load_data_columns():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    expected_language_cols = {
        'Idioma', 'TAM_Milhões', 'ARPPU_USD', 'LTV_USD', 'CAC_USD',
        'Ano1_Revenue_K', 'Ano2_Revenue_K', 'Complexidade_Técnica',
        'Payback_Meses', 'Rank_Global', 'Investimento_K',
        'Market_Readiness', 'Competição_Level', 'ROI_Ratio',
        'ROI_Ano2_K', 'Revenue_Growth'
    }
    assert expected_language_cols.issubset(df_languages.columns)

    expected_phase_cols = {
        'Fase', 'Idiomas', 'Investimento_K', 'Receita_Esperada_K',
        'Usuários_Projetados'
    }
    assert expected_phase_cols == set(df_phases.columns)

    expected_competitor_cols = {
        'Plataforma', 'Market_Share_Pct', 'User_Base_Milhões',
        'Revenue_Milhões', 'Idiomas_Count', 'Modelo_Negócio'
    }
    assert expected_competitor_cols == set(df_competitors.columns)

    expected_projection_cols = {
        'Período', 'Receita_Base_K', 'Receita_Min_K',
        'Receita_Max_K', 'Confiança_Pct'
    }
    assert expected_projection_cols == set(df_projection.columns)


def test_chart_functions_return_figures():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()

    fig1 = app.create_interactive_tam_chart(df_languages)
    assert isinstance(fig1, go.Figure)

    fig2 = app.create_advanced_roi_matrix(df_languages)
    assert isinstance(fig2, go.Figure)

    fig3 = app.create_revenue_projection_with_scenarios(df_projection)
    assert isinstance(fig3, go.Figure)

    fig4 = app.create_competitive_landscape(df_competitors)
    assert isinstance(fig4, go.Figure)

    fig5 = app.create_sensitivity_analysis()
    assert isinstance(fig5, go.Figure)

