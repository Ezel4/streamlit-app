# -*- coding: utf-8 -*-
"""
Dashboard interactif — Analyse Marketing iFood
Basé sur copie_de_dataviz.py (notebook Colab).
Lancer :  streamlit run app.py   ->  http://localhost:8501
"""

import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="iFood · Analyse Marketing",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# LIQUID GLASS CSS (Adapted: Dark Gray Background & White Cards)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Fond principal sombre uniquement sur l'application racine */
    .stApp {
        background-color: #111317 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Le wrapper de conteneur avec bordure de Streamlit devient blanc */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Enfant direct (zone de contenu interne) forcé en blanc */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08) !important;
        border-color: #cbd5e1 !important;
    }

    /* Textes et éléments globaux de l'application en blanc */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp span, .stApp label {
        color: #f1f5f9;
    }

    /* Textes et éléments intérieurs des blocs blancs forcés en sombre */
    div[data-testid="stVerticalBlockBorderWrapper"] *,
    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] span,
    div[data-testid="stVerticalBlockBorderWrapper"] label,
    div[data-testid="stVerticalBlockBorderWrapper"] h1,
    div[data-testid="stVerticalBlockBorderWrapper"] h2,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] h4,
    div[data-testid="stVerticalBlockBorderWrapper"] h5,
    div[data-testid="stVerticalBlockBorderWrapper"] h6 {
        color: #1e293b !important;
    }

    /* KPI Cards blanches spécifiques (au cas où stylées via HTML) */
    .kpi-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 22px !important;
        text-align: left !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03) !important;
        transition: all 0.3s ease !important;
        height: 100% !important;
    }
    .kpi-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08) !important;
        border-color: #cbd5e1 !important;
    }
    .kpi-card .kpi-icon { font-size: 28px; margin-bottom: 10px; display: inline-block; }
    .kpi-card .kpi-label {
        font-size: 11px; font-weight: 600; color: #64748b !important;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px;
    }
    .kpi-card .kpi-value { font-size: 28px; font-weight: 800; color: #0f172a !important; line-height: 1.2; margin-bottom: 4px; }
    .kpi-card .kpi-sub { font-size: 12px; font-weight: 600; color: #94a3b8 !important; }

    /* Bordures de couleur sur le dessus des KPI */
    .kpi-card.accent-blue   { border-top: 4px solid #3b82f6 !important; }
    .kpi-card.accent-purple { border-top: 4px solid #8b5cf6 !important; }
    .kpi-card.accent-pink   { border-top: 4px solid #ec4899 !important; }
    .kpi-card.accent-cyan   { border-top: 4px solid #06b6d4 !important; }
    .kpi-card.accent-green  { border-top: 4px solid #10b981 !important; }

    /* Header */
    .dashboard-header { text-align: center; padding: 35px 20px 20px; }
    .dashboard-header h1 {
        font-size: 42px; font-weight: 850;
        color: #ffffff !important;
        margin-bottom: 6px; letter-spacing: -1.2px;
    }
    .dashboard-header .subtitle { font-size: 14px; color: #94a3b8 !important; letter-spacing: 3px; text-transform: uppercase; }
    .dashboard-header .timestamp { font-size: 12px; color: #64748b !important; margin-top: 10px; }

    .section-title {
        font-size: 19px; font-weight: 700; color: #f1f5f9 !important;
        margin: 30px 0 16px 4px; display: flex; align-items: center; gap: 8px;
    }
    .section-title .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; background-color: currentColor; }

    /* Cartes Insight */
    .insight-card {
        background: #f8fafc !important; border: 1px solid #e2e8f0 !important;
        border-left: 4px solid var(--ic, #818cf8) !important; border-radius: 12px !important;
        padding: 16px !important; margin-bottom: 12px !important;
    }
    .insight-card .ic-title { font-size: 14px; font-weight: 700; color: #0f172a !important; margin-bottom: 4px; }
    .insight-card .ic-text { font-size: 13px; color: #475569 !important; line-height: 1.5; }

    .corr-badge {
        display: inline-block; padding: 5px 12px; border-radius: 8px; font-weight: 700; font-size: 12px;
        background: #f1f5f9 !important; color: #4f46e5 !important; border: 1px solid #e2e8f0 !important;
        margin-bottom: 10px;
    }

    /* Streamlit Overrides */
    .stApp > header { background: transparent !important; }
    div[data-testid="stToolbar"], div[data-testid="stDecoration"], div[data-testid="stStatusWidget"] { display: none; }
    .stMarkdown, .stMarkdown p { font-family: 'Inter', sans-serif !important; }
    div[data-testid="stHorizontalBlock"] { gap: 16px; }
    .block-container { padding-top: 1rem !important; max-width: 1280px; position: relative; z-index: 1; }
    
    /* Sidebar sombre propre */
    section[data-testid="stSidebar"] {
        background: #16171d !important;
        border-right: 1px solid #272730 !important;
        z-index: 2;
    }
    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.08); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.15); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHARGEMENT & NETTOYAGE DES DONNÉES
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Chargement du dataset iFood…")
def load_and_clean():
    """Télécharge le dataset Kaggle, le nettoie et renvoie (df, rapport_qualite)."""
    # 1. Localisation du fichier — priorité au CSV local (instantané, hors-ligne)
    here = os.path.dirname(os.path.abspath(__file__))
    csv_path = None
    candidates = [
        os.path.join(here, "ifood_df.csv"),
        "ifood_df.csv",
        os.path.expanduser(
            "~/.cache/kagglehub/datasets/jackdaoud/marketing-data/versions/3/ifood_df.csv"
        ),
        "/kaggle/input/marketing-data/ifood_df.csv",
    ]
    for cand in candidates:
        if os.path.exists(cand):
            csv_path = cand
            break

    # 2. En dernier recours seulement : téléchargement Kaggle (réseau)
    if csv_path is None:
        try:
            import kagglehub
            path = kagglehub.dataset_download("jackdaoud/marketing-data")
            csv_path = os.path.join(path, "ifood_df.csv")
        except Exception:
            csv_path = None

    if csv_path is None or not os.path.exists(csv_path):
        raise FileNotFoundError("Dataset introuvable. Place 'ifood_df.csv' à côté de app.py.")

    raw = pd.read_csv(csv_path)
    n0 = len(raw)

    rapport = {
        "lignes_brutes": n0,
        "colonnes": raw.shape[1],
        "manquantes": int(raw.isnull().sum().sum()),
        "doublons": int(raw.duplicated().sum()),
        "revenus_negatifs": int((raw["Income"] < 0).sum()) if "Income" in raw else 0,
        "regular_negatifs": int((raw["MntRegularProds"] < 0).sum()) if "MntRegularProds" in raw else 0,
    }

    df = raw.copy()

    # 2. Suppression des doublons
    df = df.drop_duplicates().reset_index(drop=True)

    # 3. Correction des valeurs aberrantes
    #    - revenus négatifs : on les retire (incohérents)
    if "Income" in df:
        df = df[df["Income"] >= 0]
    #    - MntRegularProds négatif : on retire ces lignes incohérentes
    if "MntRegularProds" in df:
        df = df[df["MntRegularProds"] >= 0]

    df = df.reset_index(drop=True)
    rapport["lignes_finales"] = len(df)
    rapport["lignes_supprimees"] = n0 - len(df)

    # 4. Reconstruction des variables catégorielles (one-hot -> libellé)
    edu_map = {
        "education_2n Cycle": "2e Cycle", "education_Basic": "Basique",
        "education_Graduation": "Licence", "education_Master": "Master",
        "education_PhD": "Doctorat",
    }
    edu_cols = [c for c in edu_map if c in df.columns]
    if edu_cols:
        df["Education"] = df[edu_cols].idxmax(axis=1).map(edu_map)

    mar_map = {
        "marital_Divorced": "Divorcé", "marital_Married": "Marié",
        "marital_Single": "Célibataire", "marital_Together": "En couple",
        "marital_Widow": "Veuf",
    }
    mar_cols = [c for c in mar_map if c in df.columns]
    if mar_cols:
        df["Statut"] = df[mar_cols].idxmax(axis=1).map(mar_map)

    # 5. Variables dérivées
    depenses = ["MntWines", "MntFruits", "MntMeatProducts",
                "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
    df["DepenseTotale"] = df[depenses].sum(axis=1)
    df["Enfants"] = df.get("Kidhome", 0) + df.get("Teenhome", 0)

    return df, rapport


try:
    data, qa = load_and_clean()
except Exception as e:
    st.error(f"❌ Impossible de charger les données : {e}")
    st.stop()


# ─────────────────────────────────────────────
# THÈME PLOTLY
# ─────────────────────────────────────────────
glass_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#334155', size=12),
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis=dict(gridcolor='#f1f5f9', zerolinecolor='#e2e8f0',
               tickfont=dict(size=11, color='#64748b')),
    yaxis=dict(gridcolor='#f1f5f9', zerolinecolor='#e2e8f0',
               tickfont=dict(size=11, color='#64748b')),
    hoverlabel=dict(bgcolor='#ffffff', bordercolor='#cbd5e1',
                    font=dict(color='#0f172a', family='Inter')),
)
PALETTE = ['#3b82f6', '#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f59e0b']


# ─────────────────────────────────────────────
# SIDEBAR — FILTRES INTERACTIFS
# ─────────────────────────────────────────────
st.sidebar.markdown("### 🎛️ Filtres")
st.sidebar.caption("Toute l'analyse se met à jour en direct.")

inc_min, inc_max = int(data["Income"].min()), int(data["Income"].max())
age_min, age_max = int(data["Age"].min()), int(data["Age"].max())

f_income = st.sidebar.slider("Revenu annuel (€)", inc_min, inc_max, (inc_min, inc_max))
f_age = st.sidebar.slider("Âge", age_min, age_max, (age_min, age_max))

edu_opts = sorted(data["Education"].dropna().unique()) if "Education" in data else []
mar_opts = sorted(data["Statut"].dropna().unique()) if "Statut" in data else []
f_edu = st.sidebar.multiselect("Niveau d'études", edu_opts, default=edu_opts)
f_mar = st.sidebar.multiselect("Situation matrimoniale", mar_opts, default=mar_opts)

mask = (
    data["Income"].between(*f_income) &
    data["Age"].between(*f_age)
)
if edu_opts:
    mask &= data["Education"].isin(f_edu if f_edu else edu_opts)
if mar_opts:
    mask &= data["Statut"].isin(f_mar if f_mar else mar_opts)

df = data[mask].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Clients sélectionnés", f"{len(df):,}".replace(",", " "),
                  f"sur {len(data):,}".replace(",", " "))

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🧹 Qualité des données")
st.sidebar.markdown(
    f"""
- Lignes brutes : **{qa['lignes_brutes']:,}**
- Doublons retirés : **{qa['doublons']:,}**
- Valeurs aberrantes (Mnt<0) : **{qa['regular_negatifs']:,}**
- Revenus négatifs : **{qa['revenus_negatifs']:,}**
- Valeurs manquantes : **{qa['manquantes']:,}**
- ✅ Lignes finales : **{qa['lignes_finales']:,}**
""".replace(",", " ")
)

if df.empty:
    st.warning("Aucun client ne correspond aux filtres. Élargis la sélection.")
    st.stop()


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dashboard-header">
    <h1>💎 iFood · Analyse Marketing</h1>
    <div class="subtitle">Comportement client · Produits · Campagnes</div>
    <div class="timestamp">Dataset nettoyé · {qa['lignes_finales']:,} clients · {qa['colonnes']} variables</div>
</div>
""".replace(",", " "), unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title"><span class="dot" style="color:#818cf8;background:#818cf8;"></span> Indicateurs Clés</div>', unsafe_allow_html=True)

ca_total = df["DepenseTotale"].sum()
panier_moyen = df["DepenseTotale"].mean()
revenu_moyen = df["Income"].mean()
taux_reponse = df["Response"].mean() * 100
recence_moy = df["Recency"].mean()

def kfmt(v):
    return f"{v/1000:.1f}K" if v >= 1000 else f"{v:.0f}"

k1, k2, k3, k4, k5 = st.columns(5)
cards = [
    (k1, "accent-blue", "👥", "Clients", f"{len(df):,}".replace(",", " "), f"{len(df)/len(data)*100:.0f}% du total"),
    (k2, "accent-green", "💰", "CA Total", f"€{kfmt(ca_total)}", "dépenses cumulées"),
    (k3, "accent-purple", "🛒", "Panier Moyen", f"€{panier_moyen:,.0f}".replace(",", " "), "par client"),
    (k4, "accent-cyan", "💵", "Revenu Moyen", f"€{revenu_moyen:,.0f}".replace(",", " "), "annuel / client"),
    (k5, "accent-pink", "🎯", "Taux Réponse", f"{taux_reponse:.1f}%", "dernière campagne"),
]
for col, acc, icon, label, val, sub in cards:
    with col:
        st.markdown(f"""
        <div class="kpi-card {acc}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Q1 — PRODUITS LES PLUS VENDUS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title"><span class="dot" style="color:#a78bfa;background:#a78bfa;"></span> Quels produits se vendent le mieux ?</div>', unsafe_allow_html=True)

prod_labels = {
    "MntWines": "Vins", "MntMeatProducts": "Viandes", "MntGoldProds": "Or/Premium",
    "MntFishProducts": "Poissons", "MntSweetProducts": "Sucreries", "MntFruits": "Fruits",
}
prod_cols = list(prod_labels.keys())
ventes = df[prod_cols].sum().sort_values(ascending=False)
ventes.index = [prod_labels[c] for c in ventes.index]

c_prod, c_chan = st.columns([3, 2])

with c_prod:
    with st.container(border=True):
        fig = go.Figure(go.Bar(
            x=ventes.index, y=ventes.values,
            marker=dict(color=ventes.values, colorscale=[[0, '#3b82f6'], [1, '#ec4899']], cornerradius=8),
            text=[f"€{v/1000:.0f}K" for v in ventes.values], textposition="outside",
            textfont=dict(color='#475569'),
            hovertemplate='<b>%{x}</b><br>€%{y:,.0f}<extra></extra>',
        ))
        fig.update_layout(**glass_layout, height=380,
                          title=dict(text="Chiffre d'affaires par catégorie de produit", font=dict(size=15, color='#1e293b')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────
# Q2 — CANAUX D'ACHAT
# ─────────────────────────────────────────────
with c_chan:
    with st.container(border=True):
        chan_labels = {"NumStorePurchases": "Magasin", "NumWebPurchases": "Web", "NumCatalogPurchases": "Catalogue"}
        chan = df[list(chan_labels.keys())].sum()
        chan.index = [chan_labels[c] for c in chan.index]
        chan = chan.sort_values(ascending=False)
        fig = go.Figure(go.Pie(
            labels=chan.index, values=chan.values, hole=0.62,
            marker=dict(colors=PALETTE, line=dict(color='#ffffff', width=3)),
            textinfo='percent', textfont=dict(size=13, color='#ffffff'),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} achats<extra></extra>',
        ))
        fig.update_layout(**glass_layout, height=380,
                          title=dict(text="Répartition par canal d'achat", font=dict(size=15, color='#1e293b')),
                          showlegend=True,
                          legend=dict(orientation='h', yanchor='top', y=-0.02, xanchor='center', x=0.5,
                                      font=dict(size=11, color='#64748b'), bgcolor='rgba(0,0,0,0)'),
                          annotations=[dict(text='<b>Canaux</b>', x=0.5, y=0.5, font=dict(size=15, color='#475569'), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ─────────────────────────────────────────────
# Q3 / Q4 — CORRÉLATIONS (revenu↔dépense, visites↔achats)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title"><span class="dot" style="color:#f472b6;background:#f472b6;"></span> Revenu, dépenses & efficacité du site</div>', unsafe_allow_html=True)

def scatter_with_trend(x, y, color, name_x, name_y, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        marker=dict(color=color, size=6, opacity=0.45, line=dict(width=0)),
        hovertemplate=f'{name_x}: %{{x:,.0f}}<br>{name_y}: %{{y:,.0f}}<extra></extra>',
        name='Clients',
    ))
    # droite de tendance (régression linéaire numpy)
    xv, yv = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(xv) & np.isfinite(yv)
    if ok.sum() > 2:
        a, b = np.polyfit(xv[ok], yv[ok], 1)
        xs = np.linspace(xv[ok].min(), xv[ok].max(), 50)
        fig.add_trace(go.Scatter(x=xs, y=a * xs + b, mode='lines',
                                 line=dict(color='#fb7185', width=2.5), name='Tendance',
                                 hoverinfo='skip'))
    fig.update_layout(**glass_layout, height=360,
                      title=dict(text=title, font=dict(size=15, color='#1e293b')),
                      showlegend=False)
    return fig

c1, c2 = st.columns(2)

with c1:
    corr1 = df["Income"].corr(df["DepenseTotale"])
    with st.container(border=True):
        st.markdown(f'<span class="corr-badge">📈 Corrélation Revenu ↔ Dépenses : {corr1:.2f}</span>', unsafe_allow_html=True)
        fig = scatter_with_trend(df["Income"], df["DepenseTotale"], '#818cf8',
                                 "Revenu", "Dépenses", "Les hauts revenus dépensent-ils plus ?")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with c2:
    corr2 = df["NumWebVisitsMonth"].corr(df["NumWebPurchases"])
    with st.container(border=True):
        st.markdown(f'<span class="corr-badge">🌐 Corrélation Visites ↔ Achats web : {corr2:.2f}</span>', unsafe_allow_html=True)
        fig = scatter_with_trend(df["NumWebVisitsMonth"], df["NumWebPurchases"], '#22d3ee',
                                 "Visites/mois", "Achats web", "Les visites se transforment-elles en achats ?")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ─────────────────────────────────────────────
# Q5 — PROFIL QUI RÉPOND AUX CAMPAGNES
# ─────────────────────────────────────────────
st.markdown('<div class="section-title"><span class="dot" style="color:#22d3ee;background:#22d3ee;"></span> Quel profil répond le mieux aux campagnes ?</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    with st.container(border=True):
        edu_resp = (df.groupby("Education")["Response"].mean() * 100).sort_values(ascending=False)
        fig = go.Figure(go.Bar(
            x=edu_resp.values, y=edu_resp.index, orientation='h',
            marker=dict(color=edu_resp.values, colorscale=[[0, '#3b82f6'], [1, '#06b6d4']], cornerradius=8),
            text=[f"{v:.1f}%" for v in edu_resp.values], textposition="outside",
            textfont=dict(color='#475569'),
            hovertemplate='<b>%{y}</b><br>Taux de réponse : %{x:.1f}%<extra></extra>',
        ))
        fig.update_layout(**glass_layout, height=330,
                          title=dict(text="Taux de réponse par niveau d'études", font=dict(size=15, color='#1e293b')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with c4:
    with st.container(border=True):
        mar_resp = (df.groupby("Statut")["Response"].mean() * 100).sort_values(ascending=False)
        fig = go.Figure(go.Bar(
            x=mar_resp.values, y=mar_resp.index, orientation='h',
            marker=dict(color=mar_resp.values, colorscale=[[0, '#8b5cf6'], [1, '#ec4899']], cornerradius=8),
            text=[f"{v:.1f}%" for v in mar_resp.values], textposition="outside",
            textfont=dict(color='#475569'),
            hovertemplate='<b>%{y}</b><br>Taux de réponse : %{x:.1f}%<extra></extra>',
        ))
        fig.update_layout(**glass_layout, height=330,
                          title=dict(text="Taux de réponse par situation matrimoniale", font=dict(size=15, color='#1e293b')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

c5, c6 = st.columns(2)

with c5:
    with st.container(border=True):
        fig = go.Figure()
        for r, col, lab in [(0, '#fb7185', "Non répondants"), (1, '#34d399', "Répondants")]:
            fig.add_trace(go.Box(y=df[df["Response"] == r]["Income"], name=lab,
                                 marker_color=col, boxmean=True, line=dict(width=1.5)))
        fig.update_layout(**glass_layout, height=330,
                          title=dict(text="Revenu selon la réponse à la campagne", font=dict(size=15, color='#1e293b')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with c6:
    with st.container(border=True):
        fig = go.Figure()
        for r, col, lab in [(0, '#fb7185', "Non répondants"), (1, '#34d399', "Répondants")]:
            fig.add_trace(go.Box(y=df[df["Response"] == r]["Age"], name=lab,
                                 marker_color=col, boxmean=True, line=dict(width=1.5)))
        fig.update_layout(**glass_layout, height=330,
                          title=dict(text="Âge selon la réponse à la campagne", font=dict(size=15, color='#1e293b')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ─────────────────────────────────────────────
# INSIGHTS AUTOMATIQUES
# ─────────────────────────────────────────────
st.markdown('<div class="section-title"><span class="dot" style="color:#34d399;background:#34d399;"></span> Insights & Recommandations</div>', unsafe_allow_html=True)

top_prod = ventes.index[0]
top_prod_share = ventes.iloc[0] / ventes.sum() * 100
top_chan = chan.index[0]
top_chan_share = chan.iloc[0] / chan.sum() * 100
best_edu = edu_resp.index[0]
best_mar = mar_resp.index[0]
rev_diff = df[df["Response"] == 1]["Income"].mean() - df[df["Response"] == 0]["Income"].mean()

insights = [
    ("#818cf8", "🍷 Produit phare",
     f"<b>{top_prod}</b> domine les ventes avec <b>{top_prod_share:.0f}%</b> du chiffre d'affaires. "
     f"C'est le moteur de revenu : à mettre en avant dans les promotions et le cross-sell."),
    ("#22d3ee", "🛒 Canal dominant",
     f"Le <b>{top_chan}</b> concentre <b>{top_chan_share:.0f}%</b> des achats. "
     f"La corrélation visites web ↔ achats n'est que de <b>{corr2:.2f}</b> : un fort trafic web "
     f"ne se convertit pas en ventes — piste d'optimisation UX/checkout."),
    ("#a855f7", "💰 Revenu = dépense",
     f"Corrélation revenu ↔ dépenses de <b>{corr1:.2f}</b> : les clients aisés dépensent nettement plus. "
     f"Un ciblage par tranche de revenu maximise le retour des campagnes."),
    ("#34d399", "🎯 Profil réactif",
     f"Les meilleurs répondants : niveau <b>{best_edu}</b> et statut <b>{best_mar}</b>. "
     f"Les répondants gagnent en moyenne <b>€{rev_diff:,.0f}</b> de plus que les non-répondants — "
     f"un segment premium à prioriser.".replace(",", " ")),
]

ic1, ic2 = st.columns(2)
for i, (color, title, text) in enumerate(insights):
    with (ic1 if i % 2 == 0 else ic2):
        st.markdown(f"""
        <div class="insight-card" style="--ic:{color};">
            <div class="ic-title">{title}</div>
            <div class="ic-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DONNÉES BRUTES (optionnel)
# ─────────────────────────────────────────────
with st.expander("🔍 Voir les données nettoyées (échantillon)"):
    st.dataframe(
        df[["Income", "Age", "Education", "Statut", "Enfants",
            "DepenseTotale", "NumWebPurchases", "NumStorePurchases",
            "NumCatalogPurchases", "Response"]].head(200),
        use_container_width=True,
    )


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:40px 0 20px; color:rgba(255,255,255,0.15); font-size:12px; letter-spacing:2px;">
    iFOOD MARKETING ANALYTICS · STREAMLIT + PLOTLY · 2026
</div>
""", unsafe_allow_html=True)
