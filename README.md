# nhlrecs

## quick start

1. Open virtual environment
2. Install pandas(`pip install pandas`) and gradio(`pip install gradio`)
3. Run demo: `gradio gradio_demo.py`


## implementation notes

### Current season data

`https://www.nhl.com/scores/htmlreports/<yr1><yr2>/PL<szn><game#>.HTM`
- `<yr1>`-`<yr2>` season
- `<szn>`: 01=preseason, 02=regular season
- `<game#>` chronological order, all games (4 digits)
e.g. https://www.nhl.com/scores/htmlreports/20162017/PL020716.HTM

### Past season data (no longer updated after 2024)

https://github.com/danmorse314/hockeyR-data

`play_by_play_<szn>_lite.csv` headers:
- event_type
- event
- secondary_type
- event_team
- event_team_type
- description
- period
- period_seconds
- period_seconds_remaining
- game_seconds
- game_seconds_remaining
- home_score
- away_score
- event_player_1_name
- event_player_1_type
- event_player_2_name
- event_player_2_type
- event_player_3_name
- event_player_3_type
- event_goalie_name
- strength_state
- strength_code
- strength
- event_idx
- num_on
- players_on
- num_off
- players_off
- extra_attacker
- x
- y
- x_fixed
- y_fixed
- shot_distance
- shot_angle
- home_skaters
- away_skaters
- home_on_1
- home_on_2
- home_on_3
- home_on_4
- home_on_5
- home_on_6
- home_on_7
- away_on_1
- away_on_2
- away_on_3
- away_on_4
- away_on_5
- away_on_6
- away_on_7
- home_goalie
- away_goalie
- game_id
- penalty_severity
- penalty_minutes
- timeInPeriod
- timeRemaining
- situationCode
- homeTeamDefendingSide
- sortOrder
- eventOwnerTeamId
- losingPlayerId
- winningPlayerId
- zoneCode
- hittingPlayerId
- hitteePlayerId
- shotType
- shootingPlayerId
- goalieInNetId
- awaySOG
- homeSOG
- reason
- playerId
- blockingPlayerId
- typeCode
- descKey
- duration
- committedByPlayerId
- drawnByPlayerId
- scoringPlayerId
- scoringPlayerTotal
- assist1PlayerId
- assist1PlayerTotal
- assist2PlayerId
- assist2PlayerTotal
- secondaryReason
- servedByPlayerId
- event_team_id
- home_final
- away_final
- event_player_1_id
- event_player_2_id
- event_player_3_id
- event_player_4_id
- event_player_4_type
- event_goalie_id
- home_goalie_in
- away_goalie_in
- empty_net
- event_team_abbr
- event_player_4_name
- period_time
- ids_on
- ids_off
- home_on_1_id
- home_on_2_id
- home_on_3_id
- home_on_4_id
- home_on_5_id
- home_on_6_id
- home_on_7_id
- away_on_1_id
- away_on_2_id
- away_on_3_id
- away_on_4_id
- away_on_5_id
- away_on_6_id
- away_on_7_id
- season
- season_type
- game_date
- game_start
- game_state
- venue
- home_abbr
- away_abbr
- home_id
- away_id
- home_goalie_id
- away_goalie_id
- period_type
- ordinal_num
- event_id
- home_name
- away_name
- periodType
- otPeriods
- maxRegulationPeriods