import sys, os, time
import pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit_app as app
import plotly.graph_objects as go

# ========== 1. Testes de Carregamento de Dados ==========
def test_load_data_columns():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    expected_language_cols = {
        'Idioma', 'TAM_Milhões', 'ARPPU_USD', 'LTV_USD', 'CAC_USD',
        'Ano1_Revenue_K', 'Ano2_Revenue_K', 'Complexidade_Técnica',
        'Payback_Meses', 'Rank_Global', 'Investimento_K',
        'Market_Readiness', 'Competição_Level', 'ROI_Ratio',
        'ROI_Ano2_K', 'Revenue_Growth'
    }
    assert expected_language_cols.issubset(df_languages.columns), f"Colunas faltando em df_languages: {expected_language_cols - set(df_languages.columns)}"

    expected_phase_cols = {
        'Fase', 'Idiomas', 'Investimento_K', 'Receita_Esperada_K',
        'Usuários_Projetados'
    }
    assert expected_phase_cols == set(df_phases.columns), f"Colunas de fases incorretas: {set(df_phases.columns)}"

    expected_competitor_cols = {
        'Plataforma', 'Market_Share_Pct', 'User_Base_Milhões',
        'Revenue_Milhões', 'Idiomas_Count', 'Modelo_Negócio'
    }
    assert expected_competitor_cols == set(df_competitors.columns), f"Colunas de competidores incorretas: {set(df_competitors.columns)}"

    expected_projection_cols = {
        'Período', 'Receita_Base_K', 'Receita_Min_K',
        'Receita_Max_K', 'Confiança_Pct'
    }
    assert expected_projection_cols == set(df_projection.columns), f"Colunas de projeção incorretas: {set(df_projection.columns)}"

# ========== 2. Testes de Casos de Erro ==========
def test_load_data_missing(monkeypatch):
    # Simula erro de leitura de arquivo
    def fake_read_csv(*args, **kwargs):
        raise FileNotFoundError("Arquivo não encontrado")
    monkeypatch.setattr(app.pd, "read_csv", fake_read_csv)
    df1, df2, df3, df4 = app.load_data()
    assert df1.empty and df2.empty and df3.empty and df4.empty, "DataFrames não estão vazios quando arquivos faltam"

# ========== 3. Testes de Funções de Visualização ==========
def test_chart_functions_return_figures():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    figs = [
        app.create_interactive_tam_chart(df_languages),
        app.create_advanced_roi_matrix(df_languages),
        app.create_revenue_projection_with_scenarios(df_projection),
        app.create_competitive_landscape(df_competitors),
        app.create_sensitivity_analysis()
    ]
    for i, fig in enumerate(figs):
        assert isinstance(fig, go.Figure), f"Função de gráfico {i} não retornou go.Figure"

# ========== 4. Teste de Paleta de Cores Científica ==========
def test_charts_use_scientific_palette():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    figs = [
        app.create_interactive_tam_chart(df_languages),
        app.create_advanced_roi_matrix(df_languages),
        app.create_revenue_projection_with_scenarios(df_projection),
        app.create_competitive_landscape(df_competitors),
        app.create_sensitivity_analysis()
    ]
    allowed_colors = set(app.COLORS.values())
    for fig in figs:
        for trace in fig.data:
            # Verifica cor principal
            color = getattr(trace, 'marker', {}).get('color', None)
            if color is not None:
                if isinstance(color, list):
                    for c in color:
                        assert c in allowed_colors, f"Cor {c} fora da paleta científica"
                elif isinstance(color, str):
                    assert color in allowed_colors or color.startswith('rgba'), f"Cor {color} fora da paleta científica"
            # Verifica fillcolor se existir
            fillcolor = getattr(trace, 'fillcolor', None)
            if fillcolor:
                assert fillcolor in allowed_colors or fillcolor.startswith('rgba'), f"Fillcolor {fillcolor} fora da paleta"

# ========== 5. Teste de Títulos e Labels de Acessibilidade ==========
def test_charts_have_titles_and_labels():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    figs = [
        app.create_interactive_tam_chart(df_languages),
        app.create_advanced_roi_matrix(df_languages),
        app.create_revenue_projection_with_scenarios(df_projection),
        app.create_competitive_landscape(df_competitors),
        app.create_sensitivity_analysis()
    ]
    for fig in figs:
        title = fig.layout.title.text if fig.layout.title else None
        assert title and len(title) > 0, "Gráfico sem título acessível"
        # Eixos principais
        assert fig.layout.xaxis.title.text is not None, "Eixo X sem label"
        assert fig.layout.yaxis.title.text is not None, "Eixo Y sem label"

# ========== 6. Teste de Performance ==========
def test_main_functions_performance():
    df_languages, df_phases, df_competitors, df_projection = app.load_data()
    funcs = [
        lambda: app.create_interactive_tam_chart(df_languages),
        lambda: app.create_advanced_roi_matrix(df_languages),
        lambda: app.create_revenue_projection_with_scenarios(df_projection),
        lambda: app.create_competitive_landscape(df_competitors),
        lambda: app.create_sensitivity_analysis()
    ]
    for f in funcs:
        t0 = time.time()
        _ = f()
        t1 = time.time()
        assert (t1 - t0) < 1.0, f"Função {f.__name__} demorou mais de 1s para executar"

