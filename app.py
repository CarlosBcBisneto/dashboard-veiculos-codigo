import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da Página
st.set_page_config(
    page_title="Dashboard Frota por tipo de Veiculo e UF",
    page_icon="🚗",
    layout="wide",
)

# Cache para carregar os dados (Aumenta muito a velocidade do app)
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/CarlosBcBisneto/dashboard-veiculos/refs/heads/main/frota_tratada.csv"
    return pd.read_csv(url)

df = carregar_dados()

# Transformação dos dados
df_long = df.melt(
    id_vars=["Estados"],
    var_name="Tipo_Veiculo",
    value_name="Quantidade"
)

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros:")

estados_disponiveis = sorted(df_long['Estados'].unique())
estados_selecionados = st.sidebar.multiselect(
    "Selecione o Estado",
    estados_disponiveis,
    default=estados_disponiveis
)

veiculos_disponiveis = sorted(df_long['Tipo_Veiculo'].unique())
veiculos_selecionados = st.sidebar.multiselect(
    "Selecione o Tipo de Veículo",
    veiculos_disponiveis,
    default=veiculos_disponiveis
)

# Aplicando os Filtros
df_filtrado = df_long[
    (df_long["Estados"].isin(estados_selecionados)) &
    (df_long["Tipo_Veiculo"].isin(veiculos_selecionados))
]

# --- CONTEÚDO PRINCIPAL ---
st.title("🚗📊 Dashboard de Frota por Veículo e UF")
st.markdown("Criado por **Carlos Bernardo de Castro Bisneto**")

st.divider() # Linha visual para organizar

# Métricas
st.subheader("Estatísticas Gerais")
total_veiculos = df_filtrado['Quantidade'].sum() if not df_filtrado.empty else 0
st.metric("Total de Veículos Filtrados", f"{total_veiculos:,.0f}".replace(",", "."))

# Gráficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    fig = px.bar(
        df_filtrado,
        x="Estados",
        y="Quantidade",
        color="Tipo_Veiculo",
        title="Distribuição por Estado (Barras)"
    )
    st.plotly_chart(fig, use_container_width=True)

with col_graf2:
    fig2 = px.line(
        df_filtrado, 
        x="Estados", 
        y="Quantidade", 
        color="Tipo_Veiculo",  
        title="Tendência por Estado (Linhas)"
    )
    st.plotly_chart(fig2, use_container_width=True)
