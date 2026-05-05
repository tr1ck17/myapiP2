import streamlit as st
import requests

BASE = "https://myapip2.onrender.com"

st.set_page_config(page_title="Soccer Players Manager", page_icon="⚽", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --pitch: #1a472a;
    --grass: #2d6a4f;
    --accent: #f4d03f;
    --card-bg: #0f2417;
    --border: #2e7d52;
    --text: #e8f5e9;
    --muted: #81c784;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--pitch) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

[data-testid="stAppViewContainer"] > .main {
    background-color: var(--pitch) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

h1 { font-family: 'Bebas Neue', sans-serif; font-size: 3rem; color: var(--accent); letter-spacing: 2px; margin-bottom: 0; }
h2 { font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: var(--accent); letter-spacing: 1px; margin-bottom: 0.25rem; }

hr { border-color: var(--border) !important; margin: 1.5rem 0; }

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background-color: #0f2417 !important;
    color: #e8f5e9 !important;
    border: 2px solid #2e7d52 !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(244, 208, 63, 0.2) !important;
    outline: none !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stNumberInput"] input::placeholder {
    color: #4caf50 !important;
    opacity: 0.7;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background-color: #0f2417 !important;
    border: 2px solid #2e7d52 !important;
    border-radius: 6px !important;
    color: #e8f5e9 !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #e8f5e9 !important;
    background-color: #0f2417 !important;
}

div[data-baseweb="popover"] {
    background-color: #0f2417 !important;
    border: 1px solid #2e7d52 !important;
    border-radius: 6px !important;
}

div[data-baseweb="popover"] li {
    color: #e8f5e9 !important;
    background-color: #0f2417 !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #2d6a4f !important;
}

/* ── Buttons ── */
div[data-testid="stButton"] button {
    background-color: var(--accent) !important;
    color: #0f2417 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
    padding: 0.4rem 1.2rem !important;
    transition: opacity 0.2s;
}

div[data-testid="stButton"] button:hover {
    opacity: 0.85 !important;
}

div[data-testid="stButton"] button[kind="primary"] {
    background-color: #e53935 !important;
    color: #fff !important;
}

/* ── Alerts ── */
div[data-testid="stSuccess"] { background-color: #1b5e20 !important; border-left: 4px solid #66bb6a !important; color: #e8f5e9 !important; border-radius: 6px; }
div[data-testid="stError"]   { background-color: #7f0000 !important; border-left: 4px solid #ef5350 !important; color: #ffcdd2 !important; border-radius: 6px; }
div[data-testid="stWarning"] { background-color: #e65100 !important; border-left: 4px solid #ffa726 !important; color: #fff3e0 !important; border-radius: 6px; }

/* ── JSON viewer ── */
div[data-testid="stJson"] {
    background-color: #0a1a10 !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.5rem !important;
}

/* ── Markdown text ── */
p, .stMarkdown p { color: var(--muted) !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Soccer Players Manager")
st.markdown("A full-stack SCRUD app consuming the Soccer Players REST API")
st.divider()

# ── SEARCH ────────────────────────────────────────────────────
st.header("Search Players")
search_term = st.text_input("Search by name, team, position, or nationality")
if st.button("Search", disabled=not search_term.strip()):
    r = requests.get(f"{BASE}/players")
    if r.status_code == 200:
        players = r.json()
        results = [p for p in players if search_term.lower() in
                   (p.get("name", "") + p.get("team", "") +
                    p.get("position", "") + p.get("nationality", "")).lower()]
        if results:
            st.success(f"Found {len(results)} result(s)")
            st.json(results)
        else:
            st.warning("No players matched your search.")
    else:
        st.error("Failed to fetch players.")

st.divider()

# ── GET ALL ───────────────────────────────────────────────────
st.header("Get All Players")
if st.button("Fetch All"):
    r = requests.get(f"{BASE}/players")
    if r.status_code == 200:
        st.success("Players retrieved successfully!")
        st.json(r.json())
    else:
        st.error("Failed to fetch players.")

st.divider()

# ── GET ONE ───────────────────────────────────────────────────
st.header("Get Player by ID")
get_id = st.number_input("Player ID", min_value=1, step=1, key="get_id")
if st.button("Fetch Player"):
    r = requests.get(f"{BASE}/players/{int(get_id)}")
    if r.status_code == 200:
        st.success("Player found!")
        st.json(r.json())
    else:
        st.error("Player not found.")

st.divider()

# ── CREATE ────────────────────────────────────────────────────
st.header("Create Player")
new_name        = st.text_input("Name",        key="new_name")
new_team        = st.text_input("Team",        key="new_team")
new_position    = st.text_input("Position",    key="new_position")
new_nationality = st.text_input("Nationality", key="new_nationality")
if st.button("Create Player"):
    payload = {
        "name": new_name,
        "team": new_team,
        "position": new_position,
        "nationality": new_nationality,
    }
    r = requests.post(f"{BASE}/players", json=payload)
    if r.status_code == 201:
        st.success("Player created!")
        st.json(r.json())
    else:
        st.error("Failed to create player.")

st.divider()

# ── PUT ───────────────────────────────────────────────────────
st.header("Full Update Player (PUT)")
put_id          = st.number_input("Player ID", min_value=1, step=1, key="put_id")
put_name        = st.text_input("Name",        key="put_name")
put_team        = st.text_input("Team",        key="put_team")
put_position    = st.text_input("Position",    key="put_position")
put_nationality = st.text_input("Nationality", key="put_nationality")
if st.button("Full Update"):
    payload = {
        "name": put_name,
        "team": put_team,
        "position": put_position,
        "nationality": put_nationality,
    }
    r = requests.put(f"{BASE}/players/{int(put_id)}", json=payload)
    if r.status_code == 200:
        st.success("Player updated!")
        st.json(r.json())
    else:
        st.error("Failed to update player.")

st.divider()

# ── PATCH ─────────────────────────────────────────────────────
st.header("Partial Update Player (PATCH)")
patch_id    = st.number_input("Player ID", min_value=1, step=1, key="patch_id")
patch_field = st.selectbox("Field to update", ["name", "team", "position", "nationality"])
patch_value = st.text_input("New value", key="patch_value")
if st.button("Patch Player"):
    payload = {patch_field: patch_value}
    r = requests.patch(f"{BASE}/players/{int(patch_id)}", json=payload)
    if r.status_code == 200:
        st.success("Player patched!")
        st.json(r.json())
    else:
        st.error("Failed to patch player.")

st.divider()

# ── DELETE ────────────────────────────────────────────────────
st.header("Delete Player")
del_id = st.number_input("Player ID", min_value=1, step=1, key="del_id")
if st.button("Delete Player", type="primary"):
    r = requests.delete(f"{BASE}/players/{int(del_id)}")
    if r.status_code == 200:
        st.success("Player deleted!")
        st.json(r.json())
    else:
        st.error("Player not found.")
