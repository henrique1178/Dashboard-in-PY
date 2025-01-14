import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")

# Título do Dashboard
st.title("Dashboard de Vendas - Supermercado")

# Leitura e preparação dos dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Criando coluna de mês formatada
df["Month"] = df["Date"].dt.strftime("%Y-%m")

# Filtro de mês na barra lateral
st.sidebar.header("Filtros")
month = st.sidebar.selectbox("Selecione o Mês", df["Month"].unique())

# Filtrando dados pelo mês selecionado
df_filtered = df[df["Month"] == month]

# Criando layout com colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico 1: Faturamento por dia
fig_date = px.bar(
    df_filtered, 
    x="Date", 
    y="Total", 
    title="Faturamento por Dia",
    labels={"Date": "Data", "Total": "Faturamento (R$)"}
)
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico 2: Faturamento por filial
fig_branch = px.bar(
    df_filtered, 
    x="Branch", 
    y="Total", 
    title="Faturamento por Filial",
    labels={"Branch": "Filial", "Total": "Faturamento (R$)"}
)
col2.plotly_chart(fig_branch, use_container_width=True)

# Gráfico 3: Produtos mais vendidos
products_sales = df_filtered.groupby("Product line")["Total"].sum().sort_values(ascending=True)
fig_products = px.bar(
    products_sales,
    orientation="h",
    title="Faturamento por Categoria de Produto",
    labels={"value": "Faturamento (R$)", "Product line": "Categoria"}
)
col3.plotly_chart(fig_products, use_container_width=True)

# Gráfico 4: Formas de pagamento
payment_data = df_filtered["Payment"].value_counts()
fig_payment = px.pie(
    values=payment_data.values,
    names=payment_data.index,
    title="Distribuição de Formas de Pagamento"
)
col4.plotly_chart(fig_payment, use_container_width=True)

# Gráfico 5: Avaliações por filial
fig_rating = px.box(
    df_filtered,
    x="Branch",
    y="Rating",
    title="Avaliações por Filial",
    labels={"Branch": "Filial", "Rating": "Avaliação"}
)
col5.plotly_chart(fig_rating, use_container_width=True)

# Métricas gerais
st.markdown("### Métricas do Mês Selecionado")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

total_sales = df_filtered["Total"].sum()
avg_rating = df_filtered["Rating"].mean()
total_products = df_filtered["Quantity"].sum()
avg_ticket = df_filtered["Total"].mean()

metric_col1.metric("Faturamento Total", f"R$ {total_sales:,.2f}")
metric_col2.metric("Avaliação Média", f"{avg_rating:.1f} ⭐")
metric_col3.metric("Produtos Vendidos", f"{total_products:,.0f}")
metric_col4.metric("Ticket Médio", f"R$ {avg_ticket:.2f}")