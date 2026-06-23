import json
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Australian Holidays API")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Data file not found: {filename}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_year_data(data: dict, year: int):
    for item in data.get("years", []):
        if item.get("year") == year:
            return item

    raise HTTPException(status_code=404, detail=f"No data found for year {year}")


@app.get("/")
def home():
    return {"message": "Australia Holidays API", "status": "running"}


@app.get("/holidays/public")
def get_public_holidays(
    state: str = Query(..., example="NT"), year: int = Query(..., example=2026)
):
    state = state.upper()

    if state != "NT":
        raise HTTPException(status_code=400, detail="Currently only NT is supported")

    data = load_json("nt_public_holidays.json")
    year_data = get_year_data(data, year)

    return {
        "state": state,
        "year": year,
        "public_holidays": year_data.get("public_holidays", []),
        "notes": year_data.get("notes"),
    }


@app.get("/holidays/school")
def get_school_holidays(
    state: str = Query(..., example="NT"), year: int = Query(..., example=2026)
):
    state = state.upper()

    if state != "NT":
        raise HTTPException(status_code=400, detail="Currently only NT is supported")

    data = load_json("nt_school_holidays.json")
    year_data = get_year_data(data, year)

    return {
        "state": state,
        "year": year,
        "school_holidays": year_data.get("school_holidays", []),
    }


@app.get("/terms/school")
def get_school_terms(
    state: str = Query(..., example="NT"), year: int = Query(..., example=2026)
):
    state = state.upper()

    if state != "NT":
        raise HTTPException(status_code=400, detail="Currently only NT is supported")

    data = load_json("nt_school_holidays.json")
    year_data = get_year_data(data, year)

    return {
        "state": state,
        "year": year,
        "school_terms": year_data.get("school_terms", []),
    }


def is_weekend(date_value: date):
    return date_value.weekday() >= 5  # 5 = Saturday, 6 = Sunday


@app.get("/holidays/check")
def check_holiday(
    state: str = Query(..., example="NT"),
    date_value: date = Query(..., alias="date", example="2026-07-03"),
):
    state = state.upper()

    if state != "NT":
        raise HTTPException(status_code=400, detail="Currently only NT is supported")

    year = date_value.year

    public_data = load_json("nt_public_holidays.json")
    school_data = load_json("nt_school_holidays.json")

    public_year_data = get_year_data(public_data, year)
    school_year_data = get_year_data(school_data, year)

    public_match = None
    school_match = None

    for holiday in public_year_data.get("public_holidays", []):
        if holiday.get("date") == str(date_value):
            public_match = holiday
            break

    for holiday in school_year_data.get("school_holidays", []):
        start_date = date.fromisoformat(holiday["start_date"])
        end_date = date.fromisoformat(holiday["end_date"])

        if start_date <= date_value <= end_date:
            school_match = holiday
            break

    return {
        "state": state,
        "date": str(date_value),
        "is_weekend": is_weekend(date_value),
        "is_public_holiday": public_match is not None,
        "is_school_holiday": school_match is not None,
        "public_holiday": public_match,
        "school_holiday": school_match,
    }
