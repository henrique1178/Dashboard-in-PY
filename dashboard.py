import streamlit as st #criar dashboard em python
import pandas as pd #manipular planilhas
import plotly.express as px #construir os graficos

st.set_page_config(layout="wide")

#com uma visao mensal
#faturamento por unidade
#tipo de produto mais vendido, contribuição por filial
#desempenho das formas de pagamento
#como estao as avaliacoes das filiais?

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Date", y="Total", title="Faturamento por dia")
col1.plotly_chart(fig_date)