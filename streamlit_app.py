import streamlit as st
import requests

BASE = "https://myapip2.onrender.com"

st.title("Soccer Players Manager")
st.markdown("A full-stack SCRUD app consuming the Soccer Players REST API")

menu = st.sidebar.selectbox("Choose Operation", [
    "Search Players",
    "Get All Players",
    "Get Player by ID",
    "Create Player",
    "Update Player (PUT)",
    "Patch Player (PATCH)",
    "Delete Player"
])

# ── SEARCH ────────────────────────────────────────────────────
if menu == "Search Players":
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

# ── GET ALL ───────────────────────────────────────────────────
elif menu == "Get All Players":
    st.header("All Players")
    if st.button("Fetch All"):
        r = requests.get(f"{BASE}/players")
        if r.status_code == 200:
            st.success("Players retrieved successfully!")
            st.json(r.json())
        else:
            st.error("Failed to fetch players.")

# ── GET ONE ───────────────────────────────────────────────────
elif menu == "Get Player by ID":
    st.header("Get Player by ID")
    player_id = st.number_input("Player ID", min_value=1, step=1)
    if st.button("Fetch"):
        r = requests.get(f"{BASE}/players/{player_id}")
        if r.status_code == 200:
            st.success("Player found!")
            st.json(r.json())
        else:
            st.error("Player not found.")

# ── CREATE ────────────────────────────────────────────────────
elif menu == "Create Player":
    st.header("Create New Player")
    name        = st.text_input("Name")
    team        = st.text_input("Team")
    position    = st.text_input("Position")
    nationality = st.text_input("Nationality")
    if st.button("Create"):
        payload = {"name": name, "team": team,
                   "position": position, "nationality": nationality}
        r = requests.post(f"{BASE}/players", json=payload)
        if r.status_code == 201:
            st.success("Player created!")
            st.json(r.json())
        else:
            st.error("Failed to create player.")

# ── PUT ───────────────────────────────────────────────────────
elif menu == "Update Player (PUT)":
    st.header("Full Update Player (PUT)")
    player_id   = st.number_input("Player ID", min_value=1, step=1)
    name        = st.text_input("Name")
    team        = st.text_input("Team")
    position    = st.text_input("Position")
    nationality = st.text_input("Nationality")
    if st.button("Full Update"):
        payload = {"name": name, "team": team,
                   "position": position, "nationality": nationality}
        r = requests.put(f"{BASE}/players/{player_id}", json=payload)
        if r.status_code == 200:
            st.success("Player updated!")
            st.json(r.json())
        else:
            st.error("Failed to update player.")

# ── PATCH ─────────────────────────────────────────────────────
elif menu == "Patch Player (PATCH)":
    st.header("Partial Update Player (PATCH)")
    player_id = st.number_input("Player ID", min_value=1, step=1)
    field     = st.selectbox("Field to update",
                             ["name", "team", "position", "nationality"])
    new_value = st.text_input("New value")
    if st.button("Patch"):
        payload = {field: new_value}
        r = requests.patch(f"{BASE}/players/{player_id}", json=payload)
        if r.status_code == 200:
            st.success("Player patched!")
            st.json(r.json())
        else:
            st.error("Failed to patch player.")

# ── DELETE ────────────────────────────────────────────────────
elif menu == "Delete Player":
    st.header("Delete Player")
    player_id = st.number_input("Player ID", min_value=1, step=1)
    if st.button("Delete", type="primary"):
        r = requests.delete(f"{BASE}/players/{player_id}")
        if r.status_code == 200:
            st.success("Player deleted!")
            st.json(r.json())
        else:
            st.error("Player not found.")