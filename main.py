from fastapi import FastAPI
from src.routers import techs, projects

app = FastAPI(title="VaultCore API")

app.include_router(techs.router, tags=["Techs"])
app.include_router(projects.router, tags=["Projects"])
