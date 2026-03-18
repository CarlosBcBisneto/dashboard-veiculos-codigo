import streamlit as st
import pandas as pd
import plotly.express as px

#Configurações da Página
#Definindo o titulo da página, icone e layout para ocupar a largura total da página
st.set_page_config(
    page_title="Dash Board Frota por tipo de Veiculo e UF",
    page_icon="",
    layout="wide",
)

#Conteudo da Página
st.title("🚗📊Dash board com Frota por tipo de veículo e UF até Dezembro de 2025")
st.markdown("Criado por Carlos Bernardo de Castro Bisneto")



#Carregando os dados
df = pd.read_csv("https://raw.githubusercontent.com/CarlosBcBisneto/dashboard-veiculos/refs/heads/main/frota_tratada.csv")

df_long = df.melt(
    id_vars=["Estados"],
    var_name="Tipo_Veiculo",
    value_name="Quantidade"
)

#Filtro de Estado
estados_disponiveis = sorted(df_long['Estados'].unique())
estados_selecionados = st.sidebar.multiselect(
    "Estado",
    estados_disponiveis,
    default=estados_disponiveis
)

#Filtro de Tipo de Veiculo
veiculos_disponiveis = sorted(df_long['Tipo_Veiculo'].unique())
veiculos_selecionados = st.sidebar.multiselect(
    "Tipo de Veiculo",
    veiculos_disponiveis,
    default=veiculos_disponiveis
)

#Fitro do Gráfico
df_filtrado = df_long[
    (df_long["Estados"].isin(estados_selecionados)) &
    (df_long["Tipo_Veiculo"].isin(veiculos_selecionados))
]

#Pricipais estatisticas
st.subheader("Métricas Gerais")

if not df_filtrado.empty:
    total_veiculos =  df_filtrado['Quantidade'].sum()
else:
    total_veiculos = 0

col1, = st.columns(1)
col1.metric("Total de Veículos", f"{total_veiculos:,.0f}")

#Barra lateral (Filtros)
st.sidebar.header("Filtros:")

#Gráfico teste
fig = px.bar(
    df_filtrado,
    x="Estados",
    y="Quantidade",
    color="Tipo_Veiculo",
    title="Frota por tipo de veículo e estado Gráfico de Barras"
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.line(df_filtrado, x="Estados", y="Quantidade", color="Tipo_Veiculo",  title="Frota por tipo de veículo e estado Gráfico de Linhas")

st.plotly_chart(fig2, use_container_width=True)