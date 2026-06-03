# nhlrecs

## Requirements

Python FastAPI backend + Vite React TypeScript frontend. See `requirements.txt`.


## Running the app (dev)

To launch backend, run:

```
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
- `<szn>`: 01=preseason, 02=regular season
- `<game#>` chronological order, all games (4 digits)
e.g. https://www.nhl.com/scores/htmlreports/20162017/PL020716.HTM


### Data processing

To re-run data fetch and/or parse, run:

`python -m data.update_pipline`