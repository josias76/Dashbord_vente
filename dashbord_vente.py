import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Tableau de Bord des Ventes - Josias Nteme")

# 📥 Upload des fichiers CSV ou excel
st.sidebar.header("Téléversement des fichiers")
uploaded_files = st.sidebar.file_uploader(
    "Téléversez un ou plusieurs fichiers CSV de ventes",
    type="csv",
    accept_multiple_files=True
)

# Traitement des fichiers
if uploaded_files:
    # Lecture et concaténation
    df_list = [pd.read_excel(file, parse_dates=["Date"]) for file in uploaded_files]
    df = pd.concat(df_list)

    # Filtres de dates
    st.sidebar.header("Filtres")
    date_range = st.sidebar.date_input("Période", [df["Date"].min(), df["Date"].max()])
    df_filtered = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

    # 🧮 KPIs
    st.metric("Chiffre d'affaires", f"${df_filtered['Montant'].sum():,.2f}")
    st.metric("Nombre de commandes", len(df_filtered))
    st.metric("Panier moyen", f"${df_filtered['Montant'].mean():.2f}")

    # 📈 Évolution mensuelle
    df_monthly = df_filtered.resample("M", on="Date").sum(numeric_only=True)
    fig = px.line(df_monthly, y="Montant", title="Évolution Mensuelle du CA")
    st.plotly_chart(fig)

    # 🏆 Top produits
    st.subheader("Top 5 Produits")
    top_produits = df_filtered.groupby("Produit")["Montant"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_produits)

    # 🧑‍💼 Top clients
    st.subheader("Top 5 Clients")
    top_clients = df_filtered.groupby("Client")["Montant"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_clients)

else:
    st.info("Veuillez téléverser un ou plusieurs fichiers CSV pour commencer.")
