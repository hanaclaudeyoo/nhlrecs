# nhlrecs

## Requirements

Python FastAPI backend + Vite React TypeScript frontend. See `requirements.txt`.


## Running the app (dev)

To launch backend, run:

```
python -m backend.db.init_db
uvicorn backend.api.app:app --reload --port 8000
```

To launch frontend, run:

```
cd frontend
npm run dev
```


## Implementation notes

### Data source

`https://www.nhl.com/scores/htmlreports/<yr1><yr2>/PL<szn><game#>.HTM`
- `<yr1>`-`<yr2>` season
- `<szn>`: 01=pre-season, 02=regular season, 03=post-season
- `<game#>`: 4 digit number, depends on season:
    - for 01 and 02: chronological order, all games (0001 - ~1300)
    - for 03: `<round><matchup><number>`
        - `<round>`: 1=first round, 2=division finals, 3=conference finals, 4=cup final
        - `<matchup>`: 1-8 for first round, 1-4 for second round, etc.
        - `<number>`: game # within 7-game series (01 - 07)

e.g. https://www.nhl.com/scores/htmlreports/20162017/PL020716.HTM


### Data processing

To re-run data fetch and/or parse, run:

`python -m data.update_pipline`


### Repository Structure

- `backend/`
    - `core/`
    - `api/`
    - `scraper/`: fetch and parse scoresheets to ingest data
    - `db/`: functions to interact with the SQLite database
- `frontend/`
- `data/` = persistent SQLite database