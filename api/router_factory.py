from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

import services.api_handlers as handler
from model.league import League


def create_league_router(prefix: str, tags: list[str], league_dependency):
    router = APIRouter(
        prefix=f"/{prefix}",
        tags=tags,
    )

    @router.get("/teams")
    def get_all_teams(league: League = Depends(league_dependency)):
        return {"teams": league.team_list}

    @router.get("/teams/{team}/{stat}")
    def get_team_stat(
        team: str,
        stat: str,
        threshold: float = None,
        mode: str = None,
        house_odd: float = None,
        league: League = Depends(league_dependency),
    ):
        calculator_status = bool(house_odd and threshold and mode)

        try:
            data, status_code = handler.handle_team(
                league, team, stat, calculator_status, threshold, mode, house_odd
            )
            return JSONResponse(content=data, status_code=status_code)
        except Exception as e:
            error = {"error": "An internal server error occurred", "details": str(e)}
            return JSONResponse(content=error, status_code=500)

    @router.get("/h2h/{team1}/{team2}")
    def get_team_summary(
        team1: str,
        team2: str,
        only_home: bool = None,
        year_start: int = None,
        year_end: int = None,
        league: League = Depends(league_dependency),
    ):
        try:
            data, status_code = handler.handle_h2h(
                league, team1, team2, only_home, year_start, year_end
            )
            return JSONResponse(content=data, status_code=status_code)
        except Exception as e:
            error = {"error": "An internal server error occurred", "details": str(e)}
            return JSONResponse(content=error, status_code=500)

    @router.get("/stat")
    def get_all_stats(league: League = Depends(league_dependency)):
        stats = list(league.stat_map.keys())
        if league.name == "Premier League":
            stats.extend(["cards", "second half goals"])
        return {"stats": stats}

    @router.get("/league/{stat}")
    def get_league_stat(
        stat: str,
        start_year: int = None,
        end_year: int = None,
        league: League = Depends(league_dependency),
    ):
        try:
            data, status_code = handler.handle_league(
                league, stat, start_year, end_year
            )
            return JSONResponse(content=data, status_code=status_code)
        except Exception as e:
            error = {"error": "An internal server error occurred", "details": str(e)}
            return JSONResponse(content=error, status_code=500)

    return router
