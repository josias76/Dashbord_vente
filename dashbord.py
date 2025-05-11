import streamlit as st
import pandas as pd
import plotly.express as px




st.image("logo.jpeg", width=120)

# === 🎨 CSS personnalisé avec image de fond, animation, logo ===
st.markdown("""
    <style>
        .main {
            background-image: url("background.jpg");
            background-size: cover;
            background-attachment: fixed;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            box-shadow: 0 0 12px rgba(0,0,0,0.05);
        }
        h1 {
            color: #1a1a2e;
            animation: fadeIn 2s ease-in;
        }
        .stMetric {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        }
        .stMetric > div > div:nth-child(1) {
            color: #00bcd4;
            font-weight: bold;
            font-size: 20px;
        }
        .stMetric > div > div:nth-child(2) {
            color: #ff5722;
            font-size: 26px;
            font-weight: bold;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        #logo {
            width: 120px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# === Logo ===
st.sidebar.image("logo.jpeg", caption="SDA Academy", use_container_width=True)

# === Titre animé ===
st.markdown("<h1 style='text-align: center;'>📊 Tableau de Bord des Ventes</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Bienvenue dans votre outil interactif d’analyse des ventes 💡</p>", unsafe_allow_html=True)

# === Upload CSV ===
st.sidebar.header("🗂️ Téléversement des fichiers")
uploaded_files = st.sidebar.file_uploader(
    "📎 Importez vos fichiers CSV",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    df_list = [pd.read_csv(file, parse_dates=["Date"]) for file in uploaded_files]
    df = pd.concat(df_list)

    # Filtres
    st.sidebar.header("🗓️ Filtrer par période")
    date_range = st.sidebar.date_input("Période", [df["Date"].min(), df["Date"].max()])
    df_filtered = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

    # KPIs
    st.subheader("📈 Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Chiffre d'affaires", f"${df_filtered['Montant'].sum():,.2f}")
    with col2:
        st.metric("🧾 Nombre de commandes", len(df_filtered))
    with col3:
        st.metric("🛒 Panier moyen", f"${df_filtered['Montant'].mean():.2f}")

    st.markdown("---")

    # Graphique mensuel
    st.subheader("📆 Évolution Mensuelle du CA")
    df_monthly = df_filtered.resample("M", on="Date").sum(numeric_only=True)
    fig = px.line(df_monthly, y="Montant", title="Chiffre d'affaires mensuel",
                  markers=True, template="plotly_white",
                  color_discrete_sequence=["#673ab7"])
    fig.update_layout(title_font_color="#1a1a2e")
    st.plotly_chart(fig, use_container_width=True)

    # Top Produits
    st.subheader("🥇 Top 5 Produits")
    top_produits = df_filtered.groupby("Produit")["Montant"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_produits)

    # Top Clients
    st.subheader("👤 Top 5 Clients")
    top_clients = df_filtered.groupby("Client")["Montant"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_clients)

    st.success("✅ Visualisation terminée avec succès !")

else:
    st.info("📤 Veuillez téléverser un ou plusieurs fichiers CSV pour démarrer votre analyse.")
