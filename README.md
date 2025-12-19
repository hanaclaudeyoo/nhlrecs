# nhlrecs

## Requirements

See `requirements.txt`.


## Updating new games

To download scoresheets of new games, from root, run:

`python -m data.scoresheet_htm_fetcher`

To parse scoresheets into game objects, from root, run:

`python -m data.scoresheet_htm_parser`

After running those two commands in that order, the new games will be available.


## Running the app

From root, run:

`python -m ui.gradio_app`


## Implementation notes

### Data source

`https://www.nhl.com/scores/htmlreports/<yr1><yr2>/PL<szn><game#>.HTM`
- `<yr1>`-`<yr2>` season
- `<szn>`: 01=preseason, 02=regular season
- `<game#>` chronological order, all games (4 digits)
e.g. https://www.nhl.com/scores/htmlreports/20162017/PL020716.HTM