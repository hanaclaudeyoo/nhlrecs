# nhlrecs

1. Webscraping w/ Beautiful Soup
2. Object-oriented metrics & scoring
3. RESTful FastAPI backend
4. Vite React TypeScript frontend
5. SQLite database
6. User authentication & sessions


## Running the app (dev)

To launch backend, run:

```
$ python -m backend.db.init_db
$ uvicorn backend.api.app:app --reload --port 8000
```

To launch frontend, run:

```
$ cd frontend
$ npm run dev
```


## Loading new games

To run a one-time fetch and parse of new games, run:

```
$ python -m backend.scraper.update_pipeline
```

To continuously fetch and parse new games, after running docker container, run host cron job:

```
$ 0 6 * 9-12,1-4 * docker exec nhlrecs python -m backend.scraper.update_pipeline
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


### Repository structure

- `backend/`
    - `core/`: data models and metrics scoring logic
    - `api/`: FastAPI endpoints and services
    - `scraper/`: fetch and parse scoresheets to ingest data
    - `db/`: functions to interact with the SQLite database
- `frontend/`
- `data/`: persistent SQLite database