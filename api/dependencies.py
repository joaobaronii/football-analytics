from fastapi import HTTPException
from model.brasileirao import Brasileirao
from model.premier import Premier
import services.data_loader as dl


def get_brasileirao() -> Brasileirao:
    try:
        df = dl.load_brasileirao()
        return Brasileirao(df)
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Brasileirao file not found.")


def get_premier_league() -> Premier:
    try:
        df = dl.load_premier_25_26()
        return Premier(df)
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Premier League file not found.")