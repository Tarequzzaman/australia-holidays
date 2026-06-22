# A

A simple Australian holidays API providing public holiday and school holiday data. The first version focuses on Northern Territory (NT) holidays, with support for other Australian states and territories planned for future releases.

## Requirements

- Python 3.12+
- [FastAPI](https://fastapi.tiangolo.com/) (with standard extras)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

```bash
fastapi dev 
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

## Endpoints

### `GET /`

Health check.

**Response:**
```json
{ "message": "Australia Holidays API", "status": "running" }
```

---

### `GET /holidays/public`

Returns public holidays for a given state and year.

| Parameter | Type   | Required | Example |
|-----------|--------|----------|---------|
| `state`   | string | Yes      | `NT`    |
| `year`    | int    | Yes      | `2026`  |

```bash
curl "http://127.0.0.1:8000/holidays/public?state=NT&year=2026"
```

---

### `GET /holidays/school`

Returns school holiday periods for a given state and year.

| Parameter | Type   | Required | Example |
|-----------|--------|----------|---------|
| `state`   | string | Yes      | `NT`    |
| `year`    | int    | Yes      | `2026`  |

```bash
curl "http://127.0.0.1:8000/holidays/school?state=NT&year=2026"
```

---

### `GET /terms/school`

Returns school terms for a given state and year.

| Parameter | Type   | Required | Example |
|-----------|--------|----------|---------|
| `state`   | string | Yes      | `NT`    |
| `year`    | int    | Yes      | `2026`  |

```bash
curl "http://127.0.0.1:8000/terms/school?state=NT&year=2026"
```

---

### `GET /holidays/check`

Checks whether a specific date is a public holiday, school holiday, or both.

| Parameter | Type   | Required | Example      |
|-----------|--------|----------|--------------|
| `state`   | string | Yes      | `NT`         |
| `date`    | string | Yes      | `2026-07-03` |

```bash
curl "http://127.0.0.1:8000/holidays/check?state=NT&date=2026-07-03"
```

**Response:**
```json
{
  "state": "NT",
  "date": "2026-07-03",
  "is_public_holiday": false,
  "is_school_holiday": true,
  "public_holiday": null,
  "school_holiday": { "name": "School Holidays", "start_date": "...", "end_date": "..." }
}
```

## Data

Holiday data is stored as JSON files under the `data/` directory:

- `data/nt_public_holidays.json` — NT public holidays
- `data/nt_school_holidays.json` — NT school holidays and terms

The holiday data has been collected from:

- https://nt.gov.au/nt-public-holidays
- https://nt.gov.au/learning/primary-and-secondary-students/school-term-dates-in-nt#future_term_dates




