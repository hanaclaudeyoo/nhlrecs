export type GameRecommendation = {
    rank: number;
    game_id: string;
    date: string;
    away_team: string;
    home_team: string;
    watched: boolean;
}

export type ToggleWatchedResponse = {
    game_id: string;
    watched: boolean;
}

export type UpdateSeasonResponse = {
    num_games_added: number;
}
