from fastapi import FastAPI

from api.router_factory import create_league_router
from api.dependencies import get_brasileirao, get_premier_league

app = FastAPI(title="Football Analytics")

brasileirao_router = create_league_router(
    prefix="brasileirao",
    tags=["Brasileirao"],
    league_dependency=get_brasileirao
)

premier_league_router = create_league_router(
    prefix="premier",
    tags=["Premier League"],
    league_dependency=get_premier_league
)

# Inclua os routers gerados na sua aplicação
app.include_router(premier_league_router)
app.include_router(brasileirao_router)


@app.get("/")
def read_root():
    return {"message": "API to analyze football data"}
