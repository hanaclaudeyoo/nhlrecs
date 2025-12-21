# nhlrecs

## Requirements

See `requirements.txt`.


## Running the app

From root, run:

`python -m ui.app`


## Implementation notes

### Data source

`https://www.nhl.com/scores/htmlreports/<yr1><yr2>/PL<szn><game#>.HTM`
- `<yr1>`-`<yr2>` season
- `<szn>`: 01=preseason, 02=regular season
- `<game#>` chronological order, all games (4 digits)
e.g. https://www.nhl.com/scores/htmlreports/20162017/PL020716.HTM