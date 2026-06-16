export type DateWindow = 'all' | 'last_week' | 'last_month' | 'last_two_months'

export type Profile = {
    id: number;
    username: string;
}

export type MetricWeightKey =
    | 'total_goals'
    | 'final_goal_diff'
    | 'lead_changes'
    | 'max_lead'
    | 'max_time_between_goals'

export type MetricWeights = Record<MetricWeightKey, number>

export type GameRecommendation = {
    rank: number;
    season: string;
    season_phase: string;
    game_id: string;
    date: string;
    away_team: string;
    home_team: string;
    watched: boolean;
}

export type GameRecommendationsPage = {
    games: GameRecommendation[]
    page: number
    page_size: number
    total: number
    total_pages: number
}

export type ToggleWatchedResponse = {
    game_id: string;
    watched: boolean;
}
