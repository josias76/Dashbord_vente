import streamlit as st
import pandas as pd
import plotly.express as px

# 🔵 Mise en forme CSS
st.markdown("""
    <style>
        .main { background-color: #f7f9fc; }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
        .metric-label {
            font-weight: bold;
            font-size: 18px;
            color: #2c3e50;
        }
        .stMetric {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 Titre principal avec icône
st.title("📊 Tableau de Bord des Ventes")
st.markdown("Bienvenue dans votre espace de suivi des ventes. Personnalisez, explorez et impressionnez 🚀")

# 📥 Upload
st.sidebar.header("🗂️ Téléversement des fichiers")
uploaded_files = st.sidebar.file_uploader(
    "📎 Téléversez un ou plusieurs fichiers CSV de ventes",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    df_list = [pd.read_csv(file, parse_dates=["Date"]) for file in uploaded_files]
    df = pd.concat(df_list)

    # 📅 Filtres de date
    st.sidebar.header("🗓️ Filtres")
    date_range = st.sidebar.date_input("Période", [df["Date"].min(), df["Date"].max()])
    df_filtered = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

    # 📊 KPIs
    st.subheader("📈 Indicateurs Clés de Performance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Chiffre d'affaires", f"${df_filtered['Montant'].sum():,.2f}")
    with col2:
        st.metric("🧾 Nombre de commandes", len(df_filtered))
    with col3:
        st.metric("🛒 Panier moyen", f"${df_filtered['Montant'].mean():.2f}")

    st.markdown("---")

    # 📈 Évolution mensuelle
    st.subheader("📆 Évolution Mensuelle du Chiffre d'Affaires")
    df_monthly = df_filtered.resample("M", on="Date").sum(numeric_only=True)
    fig = px.line(df_monthly, y="Montant", title="Évolution Mensuelle du CA", markers=True,
                  template="plotly_white", color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(fig, use_container_width=True)

    # 🏆 Top Produits
    st.subheader("🥇 Top 5 Produits")
    top_produits = df_filtered.groupby("Produit")["Montant"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_produits)

    # 🧑‍💼 Top Clients
    st.subheader("👤 Top 5 Clients")
    top_clients = df_filtered.groupby("Client")["Montant"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_clients)

    st.success("✅ Analyse terminée. N'hésitez pas à explorer les graphiques !")

else:
    st.info("📤 Veuillez téléverser un ou plusieurs fichiers CSV pour commencer votre analyse.")
