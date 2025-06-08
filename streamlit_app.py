import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path
import ast
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ========================================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILO
# ========================================================================================

st.set_page_config(
    page_title="LingoApp: Estratégia de Expansão Multilíngue",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado seguindo .cursorrules (cores para daltônicos)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4A90E2 0%, #FF6B6B 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4A90E2;
    }
    .insight-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FFB000;
        margin: 1rem 0;
    }
    .stSelectbox > div > div > div {
        background-color: #f8f9fa;
    }
    .stMultiSelect > div > div > div {
        background-color: #f8f9fa;
    }
    
    /* ESTILOS PARA ABAS MAIS EVIDENTES */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 12px 24px;
        background-color: white;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4A90E2 0%, #FF6B6B 100%);
        color: white !important;
        border: 2px solid #4A90E2;
        box-shadow: 0 4px 12px rgba(74,144,226,0.3);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f8ff;
        border-color: #4A90E2;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(74,144,226,0.2);
    }
    
    .tab-header {
        background: linear-gradient(135deg, #4A90E2 0%, #FF6B6B 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 1.2em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Paleta de cores seguindo .cursorrules (colorblind-safe)
COLORS = {
    'primary': '#4A90E2',      # Azul principal
    'highlight': '#FF6B6B',    # Vermelho coral para destaque
    'benchmark': '#FFB000',    # Amarelo dourado para benchmarks
    'neutral': '#6C757D',      # Cinza neutro
    'success': '#28A745',      # Verde para sucesso (usado com parcimônia)
    'background': '#F8F9FA'    # Fundo claro
}

# ========================================================================================
# DADOS ESTRUTURADOS (Baseados no relatório original)
# ========================================================================================

@st.cache_data
def load_data():
    """Carrega e estrutura todos os dados do relatório LingoApp"""

    data_dir = Path(__file__).parent / "data"

    # Dados principais dos idiomas (corrigidos para demanda de aprendizado)
    df_languages = pd.read_csv(data_dir / "languages.csv")
    df_languages.rename(columns={
        'TAM_Milhoes': 'TAM_Milhões',
        'Complexidade_Tecnica': 'Complexidade_Técnica',
        'Competicao_Level': 'Competição_Level'
    }, inplace=True)
    df_languages['ROI_Ratio'] = df_languages['LTV_USD'] / df_languages['CAC_USD']
    df_languages['ROI_Ano2_K'] = df_languages['Ano2_Revenue_K'] - df_languages['Investimento_K']
    df_languages['Revenue_Growth'] = (df_languages['Ano2_Revenue_K'] / df_languages['Ano1_Revenue_K'] - 1) * 100

    # Dados de fases de rollout
    df_phases = pd.read_csv(data_dir / "phases.csv")
    df_phases.rename(columns={
        'Usuarios_Projetados': 'Usuários_Projetados'
    }, inplace=True)
    df_phases['Idiomas'] = df_phases['Idiomas'].apply(ast.literal_eval)

    # Análise competitiva
    df_competitors = pd.read_csv(data_dir / "competitors.csv")
    df_competitors.rename(columns={'Modelo_Negocio': 'Modelo_Negócio'}, inplace=True)

    # Projeção de receita temporal
    df_projection = pd.read_csv(data_dir / "projection.csv")
    df_projection.rename(columns={
        'Periodo': 'Período',
        'Confianca_Pct': 'Confiança_Pct'
    }, inplace=True)

    return df_languages, df_phases, df_competitors, df_projection

# ========================================================================================
# FUNÇÕES DE VISUALIZAÇÃO AVANÇADAS
# ========================================================================================

def create_interactive_tam_chart(df, selected_languages=None):
    """Gráfico TAM interativo com filtros"""
    df_filtered = df.head(8) if selected_languages is None else df[df['Idioma'].isin(selected_languages)]
    df_sorted = df_filtered.sort_values('TAM_Milhões', ascending=True)
    
    fig = go.Figure()
    
    colors = [COLORS['highlight'] if x in df_sorted['Idioma'].head(3).values 
              else COLORS['primary'] for x in df_sorted['Idioma']]
    
    fig.add_trace(go.Bar(
        y=df_sorted['Idioma'],
        x=df_sorted['TAM_Milhões'],
        orientation='h',
        marker_color=colors,
        text=[f"{x}M pessoas" for x in df_sorted['TAM_Milhões']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Demanda: %{x}M pessoas<br>Rank Global: #%{customdata}<extra></extra>',
        customdata=df_sorted['Rank_Global']
    ))
    
    fig.update_layout(
        title='🎯 TAM por Idioma: Demanda Global de Aprendizado',
        xaxis_title='Milhões de Pessoas que Querem Aprender',
        yaxis_title='',
        height=400,
        template='plotly_white',
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_advanced_roi_matrix(df):
    """Matriz ROI vs Complexidade com bubbles"""
    fig = go.Figure()
    
    # Normalizar tamanho dos bubbles
    sizes = (df['TAM_Milhões'] / df['TAM_Milhões'].max() * 50 + 10)
    
    fig.add_trace(go.Scatter(
        x=df['Complexidade_Técnica'],
        y=df['ROI_Ratio'],
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=df['Payback_Meses'],
            colorscale='RdYlBu_r',
            colorbar=dict(title="Payback (meses)"),
            line=dict(width=2, color='white')
        ),
        text=df['Idioma'],
        textposition='middle center',
        textfont=dict(size=10, color='white'),
        hovertemplate='<b>%{text}</b><br>Complexidade: %{x}/10<br>ROI: %{y:.1f}x<br>TAM: %{customdata}M<br>Payback: %{marker.color} meses<extra></extra>',
        customdata=df['TAM_Milhões']
    ))
    
    # Linhas de referência
    fig.add_hline(y=3, line_dash="dash", line_color=COLORS['benchmark'], 
                  annotation_text="ROI Mínimo Saudável (3x)")
    fig.add_vline(x=5, line_dash="dash", line_color=COLORS['highlight'], 
                  annotation_text="Complexidade Média")
    
    fig.update_layout(
        title='🔄 Matriz Estratégica: ROI vs Complexidade vs TAM',
        xaxis_title='Complexidade Técnica (1-10)',
        yaxis_title='ROI (LTV/CAC)',
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_revenue_projection_with_scenarios(df_proj, scenario_factor=1.0):
    """Projeção de receita com cenários otimista/pessimista"""
    fig = go.Figure()
    
    # Cenário base
    fig.add_trace(go.Scatter(
        x=df_proj['Período'],
        y=df_proj['Receita_Base_K'] * scenario_factor,
        mode='lines+markers',
        name='Cenário Base',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=10)
    ))
    
    # Banda de confiança
    fig.add_trace(go.Scatter(
        x=df_proj['Período'],
        y=df_proj['Receita_Max_K'] * scenario_factor,
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=df_proj['Período'],
        y=df_proj['Receita_Min_K'] * scenario_factor,
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        name='Intervalo de Confiança',
        fillcolor='rgba(74,144,226,0.2)'
    ))
    
    # Marcos importantes
    fig.add_annotation(
        x='Ano 1',
        y=df_proj[df_proj['Período'] == 'Ano 1']['Receita_Base_K'].iloc[0] * scenario_factor,
        text="Breakeven Global",
        arrowhead=2,
        arrowcolor=COLORS['benchmark']
    )
    
    fig.update_layout(
        title=f'📈 Projeção de Receita (Cenário: {scenario_factor:.1f}x)',
        xaxis_title='Período',
        yaxis_title='Receita (K USD)',
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_competitive_landscape(df_comp):
    """Análise competitiva em bubble chart"""
    fig = go.Figure()
    
    colors_map = {
        'Duolingo': COLORS['highlight'],
        'Babbel': COLORS['benchmark'], 
        'Busuu': COLORS['neutral'],
        'LingoApp (Projetado)': COLORS['primary']
    }
    
    for platform in df_comp['Plataforma']:
        data = df_comp[df_comp['Plataforma'] == platform].iloc[0]
        
        fig.add_trace(go.Scatter(
            x=[data['User_Base_Milhões']],
            y=[data['Revenue_Milhões']],
            mode='markers+text',
            marker=dict(
                size=data['Market_Share_Pct'] * 2,
                color=colors_map[platform],
                line=dict(width=2, color='white')
            ),
            text=platform,
            textposition='middle center' if platform != 'Duolingo' else 'top center',
            textfont=dict(size=10, color='white' if platform != 'Duolingo' else 'black'),
            name=platform,
            hovertemplate=f'<b>{platform}</b><br>Usuários: %{{x}}M<br>Receita: $%{{y}}M<br>Market Share: {data["Market_Share_Pct"]}%<br>Idiomas: {data["Idiomas_Count"]}<extra></extra>'
        ))
    
    fig.update_layout(
        title='🏆 Posicionamento Competitivo: Usuários vs Receita',
        xaxis_title='Base de Usuários (Milhões)',
        yaxis_title='Receita Anual (Milhões USD)',
        height=450,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def create_sensitivity_analysis():
    """Análise de sensibilidade interativa"""
    # Parâmetros base
    base_tam = 100  # Milhões
    base_conversion = 0.05  # 5%
    base_arppu = 25  # USD
    
    # Variações
    tam_variations = np.linspace(0.5, 2.0, 11)  # 50% a 200% do base
    conversion_variations = np.linspace(0.5, 2.0, 11)
    
    revenues = []
    for tam_mult in tam_variations:
        row = []
        for conv_mult in conversion_variations:
            revenue = (base_tam * tam_mult) * (base_conversion * conv_mult) * base_arppu
            row.append(revenue / 1000)  # Converter para milhões
        revenues.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=revenues,
        x=[f"{x:.1f}x" for x in conversion_variations],
        y=[f"{x:.1f}x" for x in tam_variations],
        colorscale='RdYlBu_r',
        hovertemplate='TAM: %{y}<br>Conversão: %{x}<br>Receita: $%{z:.1f}M<extra></extra>'
    ))
    
    fig.update_layout(
        title='🎯 Análise de Sensibilidade: TAM vs Taxa de Conversão',
        xaxis_title='Multiplicador da Taxa de Conversão',
        yaxis_title='Multiplicador do TAM',
        height=400
    )
    
    return fig

# ========================================================================================
# INTERFACE PRINCIPAL DO STREAMLIT
# ========================================================================================

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🌍 LingoApp: Estratégia de Expansão Multilíngue</h1>
        <h3>Análise Estratégica Avançada com IA e Simulações Interativas</h3>
        <p>Dashboard Superior com Análise de Sensibilidade em Tempo Real</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregamento de dados
    df_languages, df_phases, df_competitors, df_projection = load_data()
    
    # ========================================================================================
    # SIDEBAR COM CONTROLES INTERATIVOS
    # ========================================================================================
    
    st.sidebar.header("🎛️ Controles Interativos")
    
    # Filtros de idiomas
    selected_languages = st.sidebar.multiselect(
        "Selecionar Idiomas para Análise:",
        options=df_languages['Idioma'].tolist(),
        default=df_languages['Idioma'].head(6).tolist(),
        help="Escolha quais idiomas analisar em detalhes"
    )
    
    # Cenários de simulação
    st.sidebar.subheader("📊 Cenários de Simulação")
    scenario_factor = st.sidebar.slider(
        "Multiplicador de Cenário:",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="1.0 = Base, <1.0 = Pessimista, >1.0 = Otimista"
    )
    
    # Parâmetros de análise
    st.sidebar.subheader("⚙️ Parâmetros de Análise")
    min_roi = st.sidebar.number_input("ROI Mínimo Aceitável:", value=2.0, step=0.1)
    max_payback = st.sidebar.number_input("Payback Máximo (meses):", value=18, step=1)
    min_tam = st.sidebar.number_input("TAM Mínimo (milhões):", value=10.0, step=5.0)
    
    # Filtros aplicados
    df_filtered = df_languages[
        (df_languages['ROI_Ratio'] >= min_roi) &
        (df_languages['Payback_Meses'] <= max_payback) &
        (df_languages['TAM_Milhões'] >= min_tam)
    ]
    
    # ========================================================================================
    # MÉTRICAS PRINCIPAIS EM TEMPO REAL
    # ========================================================================================
    
    st.header("📊 Métricas Principais em Tempo Real")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_tam = df_filtered['TAM_Milhões'].sum()
        st.metric("TAM Total", f"{total_tam:.0f}M", f"+{len(df_filtered)} idiomas")
    
    with col2:
        avg_roi = df_filtered['ROI_Ratio'].mean()
        st.metric("ROI Médio", f"{avg_roi:.1f}x", f"vs {min_roi:.1f}x mín")
    
    with col3:
        total_revenue_y2 = df_filtered['Ano2_Revenue_K'].sum() * scenario_factor
        st.metric("Receita Ano 2", f"${total_revenue_y2:.0f}K", f"Cenário {scenario_factor:.1f}x")
    
    with col4:
        avg_payback = df_filtered['Payback_Meses'].mean()
        st.metric("Payback Médio", f"{avg_payback:.0f} meses", f"vs {max_payback} máx")
    
    with col5:
        total_investment = df_filtered['Investimento_K'].sum()
        total_return_y2 = df_filtered['ROI_Ano2_K'].sum() * scenario_factor
        net_profit = total_return_y2 - total_investment
        st.metric("Lucro Líquido", f"${net_profit:.0f}K", f"ROI: {total_return_y2/total_investment:.1f}x")
    
    # ========================================================================================
    # VISUALIZAÇÕES AVANÇADAS
    # ========================================================================================
    
    st.header("📈 Análise Visual Avançada")
    
    # Abas para diferentes análises - NOMES MAIS EVIDENTES
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 MERCADO & OPORTUNIDADES", 
        "💰 ANÁLISE FINANCEIRA", 
        "🔄 MATRIZ ESTRATÉGICA",
        "🏆 COMPETIÇÃO & MARKET SHARE", 
        "🔮 SIMULAÇÕES AVANÇADAS"
    ])
    
    with tab1:
        # Cabeçalho da aba
        st.markdown("""
        <div class="tab-header">
            🎯 MERCADO & OPORTUNIDADES
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_tam = create_interactive_tam_chart(df_languages, selected_languages)
            st.plotly_chart(fig_tam, use_container_width=True)
            
            # Insight box
            top_3_tam = df_filtered.nlargest(3, 'TAM_Milhões')['Idioma'].tolist()
            st.markdown(f"""
            <div class="insight-box">
                <h4>💡 Insight: Liderança em Demanda</h4>
                <p>Os top 3 idiomas por demanda são: <strong>{', '.join(top_3_tam)}</strong></p>
                <p>Representam <strong>{df_filtered.nlargest(3, 'TAM_Milhões')['TAM_Milhões'].sum():.0f}M pessoas</strong> interessadas em aprender.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gráfico de correlação TAM vs Revenue
            fig_correlation = go.Figure()
            fig_correlation.add_trace(go.Scatter(
                x=df_filtered['TAM_Milhões'],
                y=df_filtered['Ano2_Revenue_K'],
                mode='markers+text',
                text=df_filtered['Idioma'],
                textposition='top center',
                marker=dict(
                    size=12,
                    color=df_filtered['ROI_Ratio'],
                    colorscale='Viridis',
                    colorbar=dict(title="ROI")
                ),
                hovertemplate='<b>%{text}</b><br>TAM: %{x}M<br>Receita Y2: $%{y}K<extra></extra>'
            ))
            
            fig_correlation.update_layout(
                title='🔗 Correlação: TAM vs Receita Ano 2',
                xaxis_title='TAM (Milhões de Pessoas)',
                yaxis_title='Receita Ano 2 (K USD)',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_correlation, use_container_width=True)
    
    with tab2:
        # Cabeçalho da aba
        st.markdown("""
        <div class="tab-header">
            💰 ANÁLISE FINANCEIRA
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de receita por fase
            fig_phases = go.Figure()
            fig_phases.add_trace(go.Bar(
                x=df_phases['Fase'],
                y=df_phases['Investimento_K'],
                name='Investimento',
                marker_color=COLORS['highlight']
            ))
            fig_phases.add_trace(go.Bar(
                x=df_phases['Fase'],
                y=df_phases['Receita_Esperada_K'],
                name='Receita Esperada',
                marker_color=COLORS['primary']
            ))
            
            fig_phases.update_layout(
                title='💰 Investimento vs Receita por Fase',
                xaxis_title='Fases de Rollout',
                yaxis_title='Valor (K USD)',
                barmode='group',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_phases, use_container_width=True)
        
        with col2:
            # Projeção de receita com cenários
            fig_proj = create_revenue_projection_with_scenarios(df_projection, scenario_factor)
            st.plotly_chart(fig_proj, use_container_width=True)
        
        # Análise detalhada de ROI
        st.subheader("📊 Análise Detalhada de ROI por Idioma")
        df_roi_analysis = df_filtered[['Idioma', 'Investimento_K', 'Ano1_Revenue_K', 'Ano2_Revenue_K', 'ROI_Ratio', 'Payback_Meses']].copy()
        df_roi_analysis['ROI_Ano1_%'] = ((df_roi_analysis['Ano1_Revenue_K'] / df_roi_analysis['Investimento_K']) - 1) * 100
        df_roi_analysis['ROI_Ano2_%'] = ((df_roi_analysis['Ano2_Revenue_K'] / df_roi_analysis['Investimento_K']) - 1) * 100
        
        st.dataframe(
            df_roi_analysis.style.format({
                'Investimento_K': '${:,.0f}K',
                'Ano1_Revenue_K': '${:,.0f}K',
                'Ano2_Revenue_K': '${:,.0f}K',
                'ROI_Ratio': '{:.1f}x',
                'Payback_Meses': '{:.0f} meses',
                'ROI_Ano1_%': '{:.0f}%',
                'ROI_Ano2_%': '{:.0f}%'
            }).background_gradient(subset=['ROI_Ano2_%'], cmap='RdYlGn'),
            use_container_width=True
        )
    
    with tab3:
        # Cabeçalho da aba
        st.markdown("""
        <div class="tab-header">
            🔄 MATRIZ ESTRATÉGICA: ROI vs COMPLEXIDADE
        </div>
        """, unsafe_allow_html=True)
        
        # Matriz estratégica avançada
        fig_matrix = create_advanced_roi_matrix(df_filtered)
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Quadrantes estratégicos
            df_quadrants = df_filtered.copy()
            
            # Verificar se há dados suficientes para análise
            if len(df_quadrants) == 0:
                st.warning("⚠️ Nenhum idioma atende aos critérios selecionados.")
            else:
                # Definir quadrantes
                median_complexity = df_quadrants['Complexidade_Técnica'].median()
                median_roi = df_quadrants['ROI_Ratio'].median()
                
                conditions = [
                    (df_quadrants['Complexidade_Técnica'] <= median_complexity) & (df_quadrants['ROI_Ratio'] >= median_roi),
                    (df_quadrants['Complexidade_Técnica'] > median_complexity) & (df_quadrants['ROI_Ratio'] >= median_roi),
                    (df_quadrants['Complexidade_Técnica'] <= median_complexity) & (df_quadrants['ROI_Ratio'] < median_roi),
                    (df_quadrants['Complexidade_Técnica'] > median_complexity) & (df_quadrants['ROI_Ratio'] < median_roi)
                ]
                
                choices = ['🟢 Wins Fáceis', '🟡 Desafios Valiosos', '🟠 Oportunidades Rápidas', '🔴 Evitar']
                df_quadrants['Quadrante'] = np.select(conditions, choices, default='Indefinido')
                
                quadrant_summary = df_quadrants.groupby('Quadrante').agg({
                    'Idioma': 'count',
                    'TAM_Milhões': 'sum',
                    'Ano2_Revenue_K': 'sum'
                }).rename(columns={'Idioma': 'Quantidade'})
                
                st.write("📊 **Resumo por Quadrante Estratégico:**")
                st.dataframe(quadrant_summary, use_container_width=True)
        
        with col2:
            # Recomendações estratégicas
            st.markdown("""
            <div class="insight-box">
                <h4>🎯 Recomendações Estratégicas</h4>
                <ul>
                    <li><strong>🟢 Priorizar:</strong> Idiomas com alto ROI e baixa complexidade</li>
                    <li><strong>🟡 Avaliar:</strong> Alto ROI mas complexos - considerar parcerias</li>
                    <li><strong>🟠 Quick Wins:</strong> Baixa complexidade - testes rápidos</li>
                    <li><strong>🔴 Postergar:</strong> Baixo ROI e alta complexidade</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # Cabeçalho da aba
        st.markdown("""
        <div class="tab-header">
            🏆 ANÁLISE COMPETITIVA & POSICIONAMENTO DE MERCADO
        </div>
        """, unsafe_allow_html=True)
        
        # Análise competitiva
        fig_comp = create_competitive_landscape(df_competitors)
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Análise de market share
        col1, col2 = st.columns(2)
        
        with col1:
            fig_market_share = go.Figure(data=[go.Pie(
                labels=df_competitors['Plataforma'],
                values=df_competitors['Market_Share_Pct'],
                hole=0.4,
                marker_colors=[COLORS['highlight'], COLORS['benchmark'], COLORS['neutral'], COLORS['primary']]
            )])
            
            fig_market_share.update_layout(
                title='🥧 Market Share Atual',
                height=400
            )
            
            st.plotly_chart(fig_market_share, use_container_width=True)
        
        with col2:
            # Eficiência de receita
            df_competitors['Revenue_per_User'] = df_competitors['Revenue_Milhões'] / df_competitors['User_Base_Milhões']
            
            fig_efficiency = go.Figure()
            fig_efficiency.add_trace(go.Bar(
                x=df_competitors['Plataforma'],
                y=df_competitors['Revenue_per_User'],
                marker_color=[COLORS['highlight'], COLORS['benchmark'], COLORS['neutral'], COLORS['primary']]
            ))
            
            fig_efficiency.update_layout(
                title='💎 Receita por Usuário (Eficiência)',
                xaxis_title='Plataforma',
                yaxis_title='Revenue/User (USD)',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_efficiency, use_container_width=True)
    
    with tab5:
        # Cabeçalho da aba
        st.markdown("""
        <div class="tab-header">
            🔮 SIMULAÇÕES AVANÇADAS: MONTE CARLO & OTIMIZAÇÃO
        </div>
        """, unsafe_allow_html=True)
        
        # Análise de sensibilidade
        col1, col2 = st.columns(2)
        
        with col1:
            fig_sensitivity = create_sensitivity_analysis()
            st.plotly_chart(fig_sensitivity, use_container_width=True)
        
        with col2:
            # Simulador de Monte Carlo
            st.subheader("🎰 Simulação Monte Carlo")
            
            n_simulations = st.slider("Número de Simulações:", 100, 10000, 1000)
            
            if st.button("🚀 Executar Simulação"):
                with st.spinner("Executando simulações..."):
                    # Simulação Monte Carlo para receita total
                    np.random.seed(42)
                    
                    simulations = []
                    for _ in range(n_simulations):
                        total_revenue = 0
                        for _, lang in df_filtered.iterrows():
                            # Variação aleatória nos parâmetros
                            tam_variation = np.random.normal(1.0, 0.2)  # ±20%
                            conversion_variation = np.random.normal(1.0, 0.3)  # ±30%
                            arppu_variation = np.random.normal(1.0, 0.15)  # ±15%
                            
                            simulated_revenue = (lang['Ano2_Revenue_K'] * 
                                               tam_variation * 
                                               conversion_variation * 
                                               arppu_variation)
                            total_revenue += simulated_revenue
                        
                        simulations.append(total_revenue)
                    
                    # Resultados da simulação
                    simulations = np.array(simulations)
                    
                    fig_monte_carlo = go.Figure()
                    fig_monte_carlo.add_trace(go.Histogram(
                        x=simulations,
                        nbinsx=50,
                        marker_color=COLORS['primary'],
                        opacity=0.7
                    ))
                    
                    # Percentis
                    p5 = np.percentile(simulations, 5)
                    p50 = np.percentile(simulations, 50)
                    p95 = np.percentile(simulations, 95)
                    
                    fig_monte_carlo.add_vline(x=p5, line_dash="dash", line_color=COLORS['highlight'], 
                                            annotation_text=f"P5: ${p5:.0f}K")
                    fig_monte_carlo.add_vline(x=p50, line_dash="solid", line_color=COLORS['benchmark'], 
                                            annotation_text=f"Mediana: ${p50:.0f}K")
                    fig_monte_carlo.add_vline(x=p95, line_dash="dash", line_color=COLORS['primary'], 
                                            annotation_text=f"P95: ${p95:.0f}K")
                    
                    fig_monte_carlo.update_layout(
                        title='📊 Distribuição de Receita - Monte Carlo',
                        xaxis_title='Receita Total Ano 2 (K USD)',
                        yaxis_title='Frequência',
                        height=400,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig_monte_carlo, use_container_width=True)
                    
                    # Métricas da simulação
                    col_sim1, col_sim2, col_sim3 = st.columns(3)
                    with col_sim1:
                        st.metric("Receita Mediana", f"${p50:.0f}K")
                    with col_sim2:
                        st.metric("Cenário Pessimista (P5)", f"${p5:.0f}K")
                    with col_sim3:
                        st.metric("Cenário Otimista (P95)", f"${p95:.0f}K")
        
        # Otimização de portfólio
        st.subheader("🎯 Otimização de Portfólio")
        st.write("**Encontre a combinação ótima de idiomas dado um orçamento limitado**")
        
        budget_limit = st.number_input("Orçamento Total (K USD):", value=500, step=50)
        
        if st.button("🔍 Otimizar Portfólio"):
            # Algoritmo greedy simples para otimização
            df_sorted_efficiency = df_filtered.copy()
            df_sorted_efficiency['Efficiency'] = df_sorted_efficiency['Ano2_Revenue_K'] / df_sorted_efficiency['Investimento_K']
            df_sorted_efficiency = df_sorted_efficiency.sort_values('Efficiency', ascending=False)
            
            selected_portfolio = []
            total_investment = 0
            total_revenue = 0
            
            for _, lang in df_sorted_efficiency.iterrows():
                if total_investment + lang['Investimento_K'] <= budget_limit:
                    selected_portfolio.append(lang['Idioma'])
                    total_investment += lang['Investimento_K']
                    total_revenue += lang['Ano2_Revenue_K']
            
            st.success(f"**Portfólio Otimizado:**")
            st.write(f"**Idiomas selecionados:** {', '.join(selected_portfolio)}")
            st.write(f"**Investimento total:** ${total_investment:.0f}K (de ${budget_limit}K)")
            st.write(f"**Receita esperada Ano 2:** ${total_revenue:.0f}K")
            st.write(f"**ROI do portfólio:** {total_revenue/total_investment:.1f}x")
    
    # ========================================================================================
    # SEÇÃO DE INSIGHTS E RECOMENDAÇÕES
    # ========================================================================================
    
    st.header("🧠 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4>🎯 Insights Principais</h4>
            <ul>
                <li><strong>TAM vs Realidade:</strong> Espanhol lidera demanda (120M) mas alta competição</li>
                <li><strong>Sweet Spot:</strong> Francês e Alemão oferecem melhor ROI/complexidade</li>
                <li><strong>Nicho Strategy:</strong> Árabe e Turco = baixa competição, mercados especializados</li>
                <li><strong>Tech Challenge:</strong> Mandarim/Japonês = alto potencial mas complexidade técnica</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4>📋 Recomendações Estratégicas</h4>
            <ol>
                <li><strong>Fase 1:</strong> Foco em idiomas latinos (ES, FR, DE) - quick wins</li>
                <li><strong>Fase 2:</strong> Expandir para PT, IT - mercados emergentes</li>
                <li><strong>Fase 3:</strong> Investir em JA, ZH - preparação técnica</li>
                <li><strong>Diferenciação:</strong> Explorar AR, TR, ID como vantagem competitiva</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================================
    # FOOTER COM METODOLOGIA
    # ========================================================================================
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9em;">
        <p><strong>Metodologia:</strong> Análise multicritério TAM×LTV×Viabilidade | 
        <strong>Fontes:</strong> Relatório Estratégico LingoApp 2024 | 
        <strong>Atualização:</strong> Tempo real</p>
        <p><strong>Cores:</strong> Paleta otimizada para daltonismo (#4A90E2, #FF6B6B, #FFB000) | 
        <strong>Framework:</strong> Tufte + Wickham + Pica</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 