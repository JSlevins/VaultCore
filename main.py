from fastapi import FastAPI
from src.routers import auth, projects, techs

app = FastAPI(title="VaultCore API")

app.include_router(auth.auth_router, tags=["Auth"])
app.include_router(techs.techs_router, tags=["Techs"])
app.include_router(projects.project_router, tags=["Projects"])

