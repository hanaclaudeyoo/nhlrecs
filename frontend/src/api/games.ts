import type {
  DateWindow,
  GameRecommendationsPage,
  ToggleWatchedResponse,
  UpdateSeasonResponse,
} from '../types/games'

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init)

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(errorText || `${response.status} ${response.statusText}`)
  }

  return response.json() as Promise<T>
}

export function fetchGameRecommendations(
  season: string,
  seasonType: string,
  showWatched: boolean,
  showUnwatched: boolean,
  team: string | null,
  dateWindow: DateWindow,
  page: number,
  pageSize: number,
): Promise<GameRecommendationsPage> {
  const params = new URLSearchParams({
    season,
    season_phase: seasonType,
    show_watched: String(showWatched),
    show_unwatched: String(showUnwatched),
    date_window: dateWindow,
    page: String(page),
    page_size: String(pageSize)
  })

  if (team !== null) {
    params.set('team', team)
  }

  return requestJson<GameRecommendationsPage>(`/api/games?${params.toString()}`)
}

export function toggleGameWatched(
  season: string,
  seasonType: string,
  gameId: string,
): Promise<ToggleWatchedResponse> {
  return requestJson<ToggleWatchedResponse>(
    `/api/games/${encodeURIComponent(season)}/${encodeURIComponent(seasonType)}/${encodeURIComponent(gameId)}/watched/toggle`,
    { method: 'POST' },
  )
}

export function updateSeason(season: string): Promise<UpdateSeasonResponse> {
  return requestJson<UpdateSeasonResponse>(
    `/api/seasons/${encodeURIComponent(season)}/update`,
    {
      method: 'POST',
    },
  )
}
