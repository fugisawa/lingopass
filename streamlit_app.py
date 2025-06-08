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
    page_title="LingoDash: Estratégia de Expansão Multilíngue com Análise Científica",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design system
st.markdown("""
<style>
    /* CSS Variables for Design System - Professional High-Contrast Palette */
    :root {
        --color-primary: #1e293b;        /* Slate 800 - Professional dark blue-gray */
        --color-secondary: #3b82f6;      /* Blue 500 - Clean modern blue */
        --color-success: #059669;        /* Emerald 600 - High contrast green */
        --color-warning: #d97706;        /* Amber 600 - Readable orange */
        --color-error: #dc2626;          /* Red 600 - Clear error red */
        --color-neutral: #374151;        /* Gray 700 - Professional neutral */
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8FAFC;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --space-sm: 0.5rem;
        --space-md: 1rem;
        --space-lg: 1.5rem;
        --space-xl: 2rem;
        --transition: 250ms ease-in-out;
    }

    /* Enhanced Main Header with Professional High-Contrast Design */
    .main-header-enhanced {
        background: #f8fafc;
        padding: var(--space-xl);
        border-radius: var(--radius-xl);
        color: #0f172a;
        margin-bottom: var(--space-xl);
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    
    /* LingoDash Logo Styling */
    .lingodash-logo {
        transition: transform 0.3s ease, filter 0.3s ease;
    }
    
    .lingodash-logo:hover {
        transform: scale(1.05);
        filter: drop-shadow(0 4px 8px rgba(103, 58, 183, 0.3));
    }
    
    .main-header-enhanced::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header-enhanced h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: var(--space-sm);
        color: #0f172a;
        position: relative;
        z-index: 1;
    }
    
    .main-header-enhanced h3 {
        font-size: 1.25rem;
        font-weight: 400;
        color: #334155;
        margin-bottom: var(--space-sm);
        position: relative;
        z-index: 1;
    }
    
    .main-header-enhanced p {
        font-size: 1rem;
        color: #64748b;
        position: relative;
        z-index: 1;
    }

    /* Enhanced Metric Cards - Modern 2025 Design */
    .metric-card-enhanced {
        background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.6);
        border-top: 3px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 100%;
        backdrop-filter: blur(8px);
    }
    
    .metric-card-enhanced:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
        border-color: rgba(68, 119, 170, 0.4);
        border-top-color: var(--color-primary);
    }
    
    .metric-card-enhanced::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-secondary) 50%, var(--color-success) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card-enhanced:hover::before {
        opacity: 1;
    }
    
    .metric-card-enhanced::after {
        content: '';
        position: absolute;
        top: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: radial-gradient(circle, rgba(68, 119, 170, 0.08) 0%, transparent 70%);
        border-radius: 50%;
        z-index: 0;
    }

    /* Enhanced Insight Boxes - Modern Progressive Disclosure */
    .insight-box-enhanced {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid rgba(226, 232, 240, 0.6);
        border-left: 4px solid var(--color-warning);
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        backdrop-filter: blur(8px);
    }
    
    .insight-box-enhanced:hover {
        transform: translateX(8px) translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        border-left-color: var(--color-primary);
    }
    
    .insight-box-enhanced h4 {
        color: var(--color-neutral);
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        position: relative;
        z-index: 1;
    }
    
    .insight-box-enhanced p {
        position: relative;
        z-index: 1;
        line-height: 1.6;
        color: #64748b;
    }
    
    /* Progressive Cards */
    .progressive-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        backdrop-filter: blur(10px);
    }
    
    .progressive-card:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        transform: translateY(-4px);
        border-color: rgba(68, 119, 170, 0.3);
    }
    
    .progressive-card-header {
        padding: 20px 24px 16px;
        border-bottom: 1px solid rgba(241, 245, 249, 0.8);
        background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(255,255,255,0.9) 100%);
        position: relative;
    }
    
    .progressive-card-header::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 24px;
        right: 24px;
        height: 2px;
        background: linear-gradient(90deg, var(--color-primary), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .progressive-card:hover .progressive-card-header::before {
        opacity: 1;
    }
    
    .progressive-card-content {
        padding: 20px 24px;
    }

    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-sm);
        background: var(--bg-secondary);
        padding: var(--space-sm);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-sm);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: var(--space-md) var(--space-lg);
        background: var(--bg-primary);
        border-radius: var(--radius-lg);
        border: 2px solid transparent;
        font-weight: 600;
        font-size: 16px;
        transition: all var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        border-color: var(--color-primary);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
        color: white !important;
        border: 2px solid var(--color-primary);
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }

    /* Tab Headers */
    .tab-header-enhanced {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
        color: white;
        padding: var(--space-lg);
        border-radius: var(--radius-lg);
        text-align: center;
        margin-bottom: var(--space-xl);
        font-size: 1.25rem;
        font-weight: 700;
        box-shadow: var(--shadow-md);
        position: relative;
    }
    
    .tab-header-enhanced::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 4px;
        background: var(--color-warning);
        border-radius: 2px;
    }

    /* Advanced Loading States - Modern Skeleton UI */
    .loading-skeleton {
        background: linear-gradient(
            90deg,
            rgba(248, 250, 252, 0.8) 25%,
            rgba(241, 245, 249, 0.8) 50%,
            rgba(248, 250, 252, 0.8) 75%
        );
        background-size: 200% 100%;
        animation: skeleton-loading 1.8s ease-in-out infinite;
        border-radius: 12px;
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64748b;
        font-weight: 500;
        position: relative;
        overflow: hidden;
    }
    
    .loading-skeleton::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(255, 255, 255, 0.6) 50%,
            transparent 100%
        );
        animation: shimmer 2s infinite;
    }
    
    @keyframes skeleton-loading {
        0%, 100% { 
            background-position: 200% 0;
            opacity: 1;
        }
        50% { 
            background-position: -200% 0;
            opacity: 0.7;
        }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Modern Grid Layouts */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
        margin: 24px 0;
    }
    
    .dashboard-grid-2 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 24px;
        margin: 24px 0;
    }
    
    .dashboard-grid-3 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 24px 0;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-indicator.success {
        background: rgba(5, 150, 105, 0.1);
        color: #065f46;
        border: 1px solid rgba(5, 150, 105, 0.3);
    }
    
    .status-indicator.warning {
        background: rgba(217, 119, 6, 0.1);
        color: #92400e;
        border: 1px solid rgba(217, 119, 6, 0.3);
    }
    
    .status-indicator.error {
        background: rgba(238, 102, 119, 0.1);
        color: var(--color-highlight);
        border: 1px solid rgba(238, 102, 119, 0.2);
    }
    
    .status-indicator::before {
        content: '';
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Chart Container Enhancements */
    .chart-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.6);
        backdrop-filter: blur(8px);
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--color-primary), var(--color-secondary), var(--color-success));
        opacity: 0.7;
    }
    
    /* Enhanced Tooltips */
    .custom-tooltip {
        background: rgba(30, 41, 59, 0.95);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(71, 85, 105, 0.3);
        backdrop-filter: blur(16px);
        font-size: 13px;
        line-height: 1.4;
        max-width: 250px;
    }

    /* Enhanced Form Controls */
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
        border: 1px solid #e5e7eb;
        transition: all 150ms ease-in-out;
    }
    
    .stSelectbox > div > div > div:hover,
    .stMultiSelect > div > div > div:hover {
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
    }

    /* Enhanced Buttons with Micro-interactions */
    .stButton > button {
        background: linear-gradient(135deg, var(--color-primary) 0%, #357ABD 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #357ABD 0%, var(--color-primary) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Modern Typography Scale */
    .dashboard-title {
        font-size: clamp(2.5rem, 5vw, 3.5rem);
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        font-size: 1.25rem;
        font-weight: 500;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Enhanced Data Metrics */
    .metric-value {
        font-size: clamp(2rem, 4vw, 2.5rem);
        font-weight: 700;
        line-height: 1;
        color: #0f172a;
        font-variant-numeric: tabular-nums;
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .metric-delta.positive {
        background: rgba(34, 136, 51, 0.1);
        color: var(--color-success);
    }
    
    .metric-delta.negative {
        background: rgba(238, 102, 119, 0.1);
        color: var(--color-highlight);
    }
    
    /* Micro-interactions for Cards */
    .interactive-card {
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .interactive-card:hover {
        transform: translateY(-4px) scale(1.02);
    }
    
    .interactive-card:active {
        transform: translateY(-2px) scale(1.01);
        transition: all 0.1s ease;
    }

    /* Enhanced Status Messages */
    .stWarning {
        background: linear-gradient(135deg, #fef3cd 0%, #fde68a 100%);
        border-left: 4px solid var(--color-warning);
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid var(--color-success);
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid var(--color-error);
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
        border-left: 4px solid var(--color-primary);
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }

    /* Export Button Styling */
    .export-button {
        display: inline-flex;
        align-items: center;
        gap: var(--space-sm);
        background: linear-gradient(135deg, var(--color-success) 0%, #059669 100%);
        color: white;
        padding: var(--space-sm) var(--space-md);
        border-radius: var(--radius-md);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all var(--transition);
        box-shadow: var(--shadow-sm);
        border: none;
        cursor: pointer;
    }
    
    .export-button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        text-decoration: none;
        color: white;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header-enhanced {
            padding: var(--space-lg);
            margin-bottom: var(--space-lg);
        }
        
        .main-header-enhanced h1 {
            font-size: 2rem;
        }
        
        .metric-card-enhanced {
            padding: var(--space-md);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: var(--space-sm) var(--space-md);
            font-size: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

# =================================================================================
# PALETA DE CORES CIENTIFICAMENTE OTIMIZADA - BASEADA EM PESQUISA ONLINE
# =================================================================================
# Baseada em pesquisas de:
# • Paul Tol (2021): Scientific colour schemes for accessible visualization
# • Edward Tufte: Data-ink ratio and minimalist design principles  
# • Hadley Wickham: Grammar of Graphics color mapping best practices
# • Lea Pica: Strategic color use for data storytelling and insight highlighting
#
# MELHORIAS IMPLEMENTADAS:
# ✅ Substituição por palette "Paul Tol Bright" (100% colorblind-safe)
# ✅ Adição de cores científicas para hierarquia visual clara
# ✅ Cores Tufte-inspired para elementos de suporte (grids, eixos)
# ✅ Cores Lea Pica para destaque estratégico de insights
# ✅ Colorscales customizadas baseadas na nova paleta científica
# ✅ Acessibilidade aprimorada para usuários com daltonismo
# =================================================================================
COLORS = {
    # Core palette - Professional High-Contrast (WCAG AA/AAA compliant)
    'primary': '#1e293b',      # Slate 800 - Professional dark blue-gray
    'highlight': '#dc2626',    # Red 600 - High contrast red
    'benchmark': '#d97706',    # Amber 600 - Professional orange
    'neutral': '#64748b',      # Slate 500 - Readable neutral
    'success': '#059669',      # Emerald 600 - High contrast green
    'background': '#f8fafc',   # Slate 50 - Professional light background
    
    # Extended palette for complex visualizations
    'secondary': '#3b82f6',    # Blue 500 - Modern blue for secondary elements
    'tertiary': '#10b981',     # Emerald 500 - Professional teal
    'quaternary': '#f1f5f9',   # Slate 100 - Light background
    
    # Professional grays for supporting elements (high contrast)
    'axis_light': '#e2e8f0',   # Slate 200 - Subtle grid lines
    'axis_medium': '#cbd5e1',  # Slate 300 - Main axes
    'text_secondary': '#475569', # Slate 600 - Readable secondary text
    
    # Strategic emphasis colors (WCAG AA compliant)
    'insight_primary': '#dc2626',    # Red 600 - Primary insights
    'insight_secondary': '#1e293b',  # Slate 800 - Supporting data
    'warning': '#d97706',           # Amber 600 - Important alerts
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
    df_competitors.rename(columns={
        'Modelo_Negocio': 'Modelo_Negócio',
        'User_Base_Milhoes': 'User_Base_Milhões',
        'Revenue_Milhoes': 'Revenue_Milhões'
    }, inplace=True)

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
            colorscale=[[0.0, COLORS['success']], [0.5, COLORS['benchmark']], [1.0, COLORS['highlight']]],
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
        fillcolor='rgba(68,119,170,0.2)'
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
        'LingoDash (Projetado)': COLORS['primary']
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
        colorscale=[[0.0, COLORS['quaternary']], [0.3, COLORS['primary']], [0.7, COLORS['benchmark']], [1.0, COLORS['highlight']]],
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
# ENHANCED UI HELPER FUNCTIONS
# ========================================================================================

def show_loading_state(message="Carregando dados..."):
    """Display enhanced loading state with animation"""
    return st.markdown(f"""
    <div class="loading-skeleton">
        <div style="text-align: center;">
            <div style="font-size: 1.2rem; margin-bottom: 1rem;">⏳ {message}</div>
            <div style="font-size: 0.9rem; opacity: 0.7;">Por favor, aguarde...</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_metric_card(title, value, delta, icon="📊", help_text=""):
    """Create modern metric card with enhanced typography and professional high-contrast colors"""
    delta_color = "#059669" if str(delta).startswith("+") else "#dc2626" if str(delta).startswith("-") else "#374151"
    delta_icon = "↗️" if str(delta).startswith("+") else "↘️" if str(delta).startswith("-") else "➡️"
    delta_class = "positive" if str(delta).startswith("+") else "negative" if str(delta).startswith("-") else ""
    
    return f"""
    <div class="metric-card-enhanced interactive-card" title="{help_text}">
        <div style="font-size: 14px; color: #64748b; font-weight: 600; margin-bottom: 8px;">
            {icon} {title}
        </div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #0f172a; line-height: 1; margin-bottom: 4px;">
            {value}
        </div>
        <div style="font-size: 13px; color: {delta_color}; font-weight: 600;">
            {delta_icon} {delta}
        </div>
    </div>
    """

def create_enhanced_insight_box(title, content, icon="💡"):
    """Create enhanced insight box with professional high-contrast styling"""
    return f"""
    <div class="insight-box-enhanced">
        <h4 style="color: #1e293b; font-weight: 700; margin-bottom: 8px; font-size: 16px;">{icon} {title}</h4>
        <div style="color: #475569; line-height: 1.6;">{content}</div>
    </div>
    """

def create_export_button(data, filename, button_text="📥 Exportar Dados"):
    """Create enhanced export button for data"""
    import io
    import json
    
    if isinstance(data, pd.DataFrame):
        csv = data.to_csv(index=False)
        return st.download_button(
            label=button_text,
            data=csv,
            file_name=f"{filename}.csv",
            mime="text/csv",
            help="Baixar dados em formato CSV"
        )
    else:
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        return st.download_button(
            label=button_text,
            data=json_data,
            file_name=f"{filename}.json",
            mime="application/json",
            help="Baixar dados em formato JSON"
        )

# ========================================================================================
# INTERFACE PRINCIPAL DO STREAMLIT
# ========================================================================================

def main():
    # Enhanced Header with modern typography and high-contrast professional colors
    st.markdown("""
    <div class="main-header-enhanced">
        <div style="display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 16px;">
            <div style="font-size: 48px;">🌐</div>
            <div>
                <div class="dashboard-title">LingoDash</div>
            </div>
        </div>
        <div class="dashboard-subtitle">Estratégia de Expansão Multilíngue com Análise Científica</div>
        <div style="display: flex; align-items: center; gap: 12px; margin-top: 16px;">
            <div class="status-indicator success">Sistema Online</div>
            <div class="status-indicator warning">Dados Atualizados</div>
        </div>
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
    # MÉTRICAS PRINCIPAIS EM TEMPO REAL - ENHANCED
    # ========================================================================================
    
    st.header("📊 Métricas Principais em Tempo Real")
    
    # Show loading state briefly for better UX
    with st.spinner("Calculando métricas..."):
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Calculate metrics
        total_tam = df_filtered['TAM_Milhões'].sum()
        avg_roi = df_filtered['ROI_Ratio'].mean() if len(df_filtered) > 0 else 0
        total_revenue_y2 = df_filtered['Ano2_Revenue_K'].sum() * scenario_factor
        avg_payback = df_filtered['Payback_Meses'].mean() if len(df_filtered) > 0 else 0
        total_investment = df_filtered['Investimento_K'].sum()
        total_return_y2 = df_filtered['ROI_Ano2_K'].sum() * scenario_factor
        net_profit = total_return_y2 - total_investment
        roi_text = f"ROI: {total_return_y2/total_investment:.1f}x" if total_investment > 0 else "ROI: N/A"
        
        with col1:
            st.markdown(create_enhanced_metric_card(
                "TAM Total", 
                f"{total_tam:.0f}M",
                f"+{len(df_filtered)} idiomas",
                "🎯",
                "Total Addressable Market dos idiomas selecionados"
            ), unsafe_allow_html=True)
        
        with col2:
            roi_delta = f"+{avg_roi-min_roi:.1f}x vs mínimo" if avg_roi > min_roi else f"{avg_roi-min_roi:.1f}x vs mínimo"
            st.markdown(create_enhanced_metric_card(
                "ROI Médio",
                f"{avg_roi:.1f}x",
                roi_delta,
                "💰",
                "Return on Investment médio dos idiomas filtrados"
            ), unsafe_allow_html=True)
        
        with col3:
            scenario_text = f"Cenário {scenario_factor:.1f}x"
            st.markdown(create_enhanced_metric_card(
                "Receita Ano 2",
                f"${total_revenue_y2:.0f}K",
                scenario_text,
                "📈",
                "Projeção de receita para o segundo ano"
            ), unsafe_allow_html=True)
        
        with col4:
            payback_delta = f"{avg_payback - max_payback:.0f} vs máximo" if avg_payback < max_payback else f"+{avg_payback - max_payback:.0f} vs máximo"
            st.markdown(create_enhanced_metric_card(
                "Payback Médio",
                f"{avg_payback:.0f} meses",
                payback_delta,
                "⏱️",
                "Tempo médio para recuperar o investimento"
            ), unsafe_allow_html=True)
        
        with col5:
            profit_delta = f"+${net_profit:.0f}K lucro" if net_profit > 0 else f"${abs(net_profit):.0f}K prejuízo"
            st.markdown(create_enhanced_metric_card(
                "Lucro Líquido",
                f"${net_profit:.0f}K",
                roi_text,
                "💵",
                "Lucro líquido projetado após investimentos"
            ), unsafe_allow_html=True)
    
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
        # Enhanced tab header
        st.markdown("""
        <div class="tab-header-enhanced">
            🎯 MERCADO & OPORTUNIDADES
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_tam = create_interactive_tam_chart(df_languages, selected_languages)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_tam, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Insight box
            if len(df_filtered) > 0:
                top_n = min(3, len(df_filtered))
                top_tam = df_filtered.nlargest(top_n, 'TAM_Milhões')
                top_tam_languages = top_tam['Idioma'].tolist()
                top_tam_sum = top_tam['TAM_Milhões'].sum()
                
                st.markdown(create_enhanced_insight_box(
                    "Insight: Liderança em Demanda",
                    f"""<p>Os top {top_n} idiomas por demanda são: <strong>{', '.join(top_tam_languages)}</strong></p>
                    <p>Representam <strong>{top_tam_sum:.0f}M pessoas</strong> interessadas em aprender.</p>
                    <p><em>Estes idiomas oferecem o maior potencial de mercado para expansão inicial.</em></p>""",
                    "🎯"
                ), unsafe_allow_html=True)
            else:
                st.warning("⚠️ Nenhum idioma atende aos critérios selecionados. Ajuste os filtros.")
        
        with col2:
            # Gráfico de correlação TAM vs Revenue
            if len(df_filtered) > 0:
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
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(fig_correlation, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("📊 Gráfico indisponível - nenhum idioma atende aos critérios.")
    
    with tab2:
        # Enhanced tab header
        st.markdown("""
        <div class="tab-header-enhanced">
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
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_phases, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Projeção de receita com cenários
            fig_proj = create_revenue_projection_with_scenarios(df_projection, scenario_factor)
            st.plotly_chart(fig_proj, use_container_width=True)
        
        # Análise detalhada de ROI com exportação
        col_header, col_export = st.columns([3, 1])
        
        with col_header:
            st.subheader("📊 Análise Detalhada de ROI por Idioma")
        
        if len(df_filtered) > 0:
            df_roi_analysis = df_filtered[['Idioma', 'Investimento_K', 'Ano1_Revenue_K', 'Ano2_Revenue_K', 'ROI_Ratio', 'Payback_Meses']].copy()
            df_roi_analysis['ROI_Ano1_%'] = ((df_roi_analysis['Ano1_Revenue_K'] / df_roi_analysis['Investimento_K']) - 1) * 100
            df_roi_analysis['ROI_Ano2_%'] = ((df_roi_analysis['Ano2_Revenue_K'] / df_roi_analysis['Investimento_K']) - 1) * 100
            
            with col_export:
                create_export_button(df_roi_analysis, "roi_analysis", "📥 Exportar ROI")
            
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
            
            # Enhanced insight
            best_roi = df_roi_analysis.loc[df_roi_analysis['ROI_Ratio'].idxmax()]
            st.markdown(create_enhanced_insight_box(
                "Insight: Melhor ROI",
                f"""<p><strong>{best_roi['Idioma']}</strong> oferece o melhor ROI de <strong>{best_roi['ROI_Ratio']:.1f}x</strong></p>
                <p>Com payback em apenas <strong>{best_roi['Payback_Meses']:.0f} meses</strong> e ROI no segundo ano de <strong>{best_roi['ROI_Ano2_%']:.0f}%</strong></p>""",
                "🏆"
            ), unsafe_allow_html=True)
        else:
            st.info("📊 Tabela indisponível - nenhum idioma atende aos critérios selecionados.")
    
    with tab3:
        # Enhanced tab header
        st.markdown("""
        <div class="tab-header-enhanced">
            🔄 MATRIZ ESTRATÉGICA: ROI vs COMPLEXIDADE
        </div>
        """, unsafe_allow_html=True)
        
        # Matriz estratégica avançada
        if len(df_filtered) > 0:
            fig_matrix = create_advanced_roi_matrix(df_filtered)
            st.plotly_chart(fig_matrix, use_container_width=True)
        else:
            st.info("📊 Matriz indisponível - nenhum idioma atende aos critérios selecionados.")
        
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
            # Enhanced strategic recommendations
            st.markdown(create_enhanced_insight_box(
                "Recomendações Estratégicas",
                """<ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>🟢 Priorizar:</strong> Idiomas com alto ROI e baixa complexidade</li>
                    <li><strong>🟡 Avaliar:</strong> Alto ROI mas complexos - considerar parcerias</li>
                    <li><strong>🟠 Quick Wins:</strong> Baixa complexidade - testes rápidos</li>
                    <li><strong>🔴 Postergar:</strong> Baixo ROI e alta complexidade</li>
                </ul>
                <p style="margin-top: 1rem; font-style: italic; color: #6B7280;">
                    💡 <strong>Dica:</strong> Foque nos quadrantes superiores esquerdos para máximo retorno com menor risco.
                </p>""",
                "🎯"
            ), unsafe_allow_html=True)
    
    with tab4:
        # Enhanced tab header
        st.markdown("""
        <div class="tab-header-enhanced">
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
        # Enhanced tab header
        st.markdown("""
        <div class="tab-header-enhanced">
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
                if len(df_filtered) > 0:
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
                else:
                    st.warning("⚠️ Simulação indisponível - nenhum idioma atende aos critérios selecionados.")
        
        # Otimização de portfólio
        st.subheader("🎯 Otimização de Portfólio")
        st.write("**Encontre a combinação ótima de idiomas dado um orçamento limitado**")
        
        budget_limit = st.number_input("Orçamento Total (K USD):", value=500, step=50)
        
        if st.button("🔍 Otimizar Portfólio"):
            if len(df_filtered) > 0:
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
                
                if selected_portfolio:
                    st.success(f"**Portfólio Otimizado:**")
                    st.write(f"**Idiomas selecionados:** {', '.join(selected_portfolio)}")
                    st.write(f"**Investimento total:** ${total_investment:.0f}K (de ${budget_limit}K)")
                    st.write(f"**Receita esperada Ano 2:** ${total_revenue:.0f}K")
                    roi_portfolio = total_revenue/total_investment if total_investment > 0 else 0
                    st.write(f"**ROI do portfólio:** {roi_portfolio:.1f}x")
                else:
                    st.warning("⚠️ Nenhum idioma se encaixa no orçamento especificado.")
            else:
                st.warning("⚠️ Nenhum idioma disponível para otimização. Ajuste os filtros.")
    
    # ========================================================================================
    # SEÇÃO DE INSIGHTS E RECOMENDAÇÕES ENHANCED
    # ========================================================================================
    
    st.header("🧠 Insights Estratégicos e Recomendações")
    
    # Calculate dynamic insights based on filtered data
    if len(df_filtered) > 0:
        top_tam_language = df_filtered.nlargest(1, 'TAM_Milhões').iloc[0]
        best_roi_language = df_filtered.nlargest(1, 'ROI_Ratio').iloc[0]
        fastest_payback = df_filtered.nsmallest(1, 'Payback_Meses').iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(create_enhanced_insight_box(
                "Insights Principais Baseados em Dados",
                f"""<ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>🎯 Maior TAM:</strong> {top_tam_language['Idioma']} com {top_tam_language['TAM_Milhões']:.0f}M pessoas</li>
                    <li><strong>💰 Melhor ROI:</strong> {best_roi_language['Idioma']} com {best_roi_language['ROI_Ratio']:.1f}x retorno</li>
                    <li><strong>⚡ Payback Rápido:</strong> {fastest_payback['Idioma']} em apenas {fastest_payback['Payback_Meses']:.0f} meses</li>
                    <li><strong>📊 Portfolio:</strong> {len(df_filtered)} idiomas atendem aos critérios selecionados</li>
                </ul>
                <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(74, 144, 226, 0.1); border-radius: 0.5rem; border-left: 3px solid var(--color-primary);">
                    <strong>💡 Insight Chave:</strong> Balanceie TAM alto com ROI sustentável para maximizar retornos.
                </div>""",
                "🎯"
            ), unsafe_allow_html=True)
        
        with col2:
            # Calculate phase-based recommendations
            high_roi_languages = df_filtered[df_filtered['ROI_Ratio'] >= 3.0]['Idioma'].tolist()
            low_complexity = df_filtered[df_filtered['Complexidade_Técnica'] <= 3]['Idioma'].tolist()
            quick_wins = list(set(high_roi_languages) & set(low_complexity))
            
            st.markdown(create_enhanced_insight_box(
                "Recomendações Estratégicas Personalizadas",
                f"""<ol style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>🚀 Quick Wins:</strong> {', '.join(quick_wins[:3]) if quick_wins else 'Ajustar filtros para identificar'}</li>
                    <li><strong>🎯 Foco Imediato:</strong> Priorizar {top_tam_language['Idioma']} pelo TAM e {best_roi_language['Idioma']} pelo ROI</li>
                    <li><strong>⏱️ Timing:</strong> Começar com {fastest_payback['Idioma']} para cashflow rápido</li>
                    <li><strong>💼 Portfolio:</strong> Diversificar entre {len(df_filtered)} idiomas selecionados</li>
                </ol>
                <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 0.5rem; border-left: 3px solid var(--color-success);">
                    <strong>✅ Próximos Passos:</strong> Execute análise detalhada dos top 3 idiomas identificados.
                </div>""",
                "📋"
            ), unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(create_enhanced_insight_box(
                "Ajuste os Filtros",
                """<p>Nenhum idioma atende aos critérios atuais.</p>
                <p><strong>Sugestões:</strong></p>
                <ul>
                    <li>Reduzir ROI mínimo para valores mais realistas</li>
                    <li>Aumentar prazo de payback aceitável</li>
                    <li>Diminuir TAM mínimo para incluir nichos</li>
                </ul>""",
                "⚠️"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_enhanced_insight_box(
                "Valores Recomendados",
                """<ul>
                    <li><strong>ROI Mínimo:</strong> 2.0x - 3.0x (realista)</li>
                    <li><strong>Payback Máximo:</strong> 12-24 meses</li>
                    <li><strong>TAM Mínimo:</strong> 5-20M pessoas</li>
                </ul>
                <p><em>Ajuste gradualmente para encontrar o equilíbrio ideal.</em></p>""",
                "💡"
            ), unsafe_allow_html=True)
    
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