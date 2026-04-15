from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from supabase import create_client, Client

app = FastAPI(
    title="Soccer Players API",
    description="A RESTful API for managing soccer players.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class PlayerCreate(BaseModel):
    name: str
    team: str
    position: str
    nationality: Optional[str] = None

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    team: Optional[str] = None
    position: Optional[str] = None
    nationality: Optional[str] = None

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

@app.get("/players", tags=["Players"])
def get_all_players():
    result = supabase.table("players").select("*").execute()
    return result.data

@app.get("/players/{player_id}", tags=["Players"])
def get_player(player_id: int):
    result = supabase.table("players").select("*").eq("id", player_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Player not found")
    return result.data[0]

@app.post("/players", status_code=201, tags=["Players"])
def create_player(player: PlayerCreate):
    result = supabase.table("players").insert(player.dict()).execute()
    return result.data[0]

@app.put("/players/{player_id}", tags=["Players"])
def update_player(player_id: int, player: PlayerUpdate):
    updates = {k: v for k, v in player.dict().items() if v is not None}
    result = supabase.table("players").update(updates).eq("id", player_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Player not found")
    return result.data[0]

@app.patch("/players/{player_id}", tags=["Players"])
def patch_player(player_id: int, player: PlayerUpdate):
    updates = {k: v for k, v in player.dict().items() if v is not None}
    result = supabase.table("players").update(updates).eq("id", player_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Player not found")
    return result.data[0]

@app.delete("/players/{player_id}", tags=["Players"])
def delete_player(player_id: int):
    result = supabase.table("players").delete().eq("id", player_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": f"Player {player_id} deleted successfully"}