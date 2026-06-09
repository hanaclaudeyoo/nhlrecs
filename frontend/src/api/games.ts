import type {
  GameRecommendation,
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
): Promise<GameRecommendation[]> {
  const params = new URLSearchParams({
    season,
    season_phase: seasonType,
    show_watched: String(showWatched),
    show_unwatched: String(showUnwatched),
  })

  return requestJson<GameRecommendation[]>(`/api/games?${params.toString()}`)
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
