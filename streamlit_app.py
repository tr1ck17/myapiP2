import streamlit as st
import requests

BASE = "https://myapip2.onrender.com"

st.title("Soccer Players Manager")
st.markdown("A full-stack SCRUD app consuming the Soccer Players REST API")

st.divider()

# ── SEARCH ────────────────────────────────────────────────────
st.header("Search Players")
search_term = st.text_input("Search by name, team, position, or nationality")
if st.button("Search"):
    r = requests.get(f"{BASE}/players")
    if r.status_code == 200:
        players = r.json()
        results = [p for p in players if search_term.lower() in
                   (p.get("name","") + p.get("team","") +
                    p.get("position","") + p.get("nationality","")).lower()]
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
    r = requests.get(f"{BASE}/players/{get_id}")
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
    payload = {"name": new_name, "team": new_team,
               "position": new_position, "nationality": new_nationality}
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
    payload = {"name": put_name, "team": put_team,
               "position": put_position, "nationality": put_nationality}
    r = requests.put(f"{BASE}/players/{put_id}", json=payload)
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
    r = requests.patch(f"{BASE}/players/{patch_id}", json=payload)
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
    r = requests.delete(f"{BASE}/players/{del_id}")
    if r.status_code == 200:
        st.success("Player deleted!")
        st.json(r.json())
    else:
        st.error("Player not found.")