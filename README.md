# 📊 Dashboard des Ventes - E-commerce

Ce projet présente un tableau de bord interactif développé avec **Streamlit**, permettant d’analyser des fichiers de ventes CSV (années ou mois) téléchargés dynamiquement par l’utilisateur.

## 🔍 Fonctionnalités :
- Téléversement de **plusieurs fichiers CSV**
- Calcul automatique du :
  - Chiffre d’affaires total
  - Nombre de commandes
  - Panier moyen
- Graphique de l’évolution mensuelle du CA
- Top 5 produits
- Top 5 clients

## 📁 Données attendues
Les fichiers doivent contenir les colonnes suivantes :
- `Date` (format date)
- `Client`
- `Produit`
- `Quantité`
- `Prix_Unitaire`
- `Montant` (ou laisser l'app le recalculer automatiquement si besoin)

## 🧠 Auteur
Développé par **Josias Nteme** — Statisticien, Data Analyst & Data Scientist passionné.

## 🚀 Lancer l’application en local
```bash
pip install -r requirements.txt
streamlit run app.py
