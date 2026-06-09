import { useCallback, useEffect, useState } from 'react'
import './styles/app.css'
import {
  fetchGameRecommendations,
  toggleGameWatched,
  updateSeason,
} from './api/games'
import { GameFilters } from './components/GameFilters'
import { GameTable } from './components/GameTable'
import { PageHeader } from './components/PageHeader'
import { StatusBar } from './components/StatusBar'
import type { GameRecommendation } from './types/games'

function App() {
  const seasonType = '02'
  const [season, setSeason] = useState('20252026')
  const [games, setGames] = useState<GameRecommendation[]>([])
  const [showWatched, setShowWatched] = useState(true)
  const [showUnwatched, setShowUnwatched] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [status, setStatus] = useState('Ready')

  const loadGames = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const nextGames = await fetchGameRecommendations(
        season,
        seasonType,
        showWatched,
        showUnwatched,
      )
      setGames(nextGames)
      setStatus(`Loaded ${nextGames.length} game recommendations`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load games')
    } finally {
      setIsLoading(false)
    }
  }, [season, seasonType, showWatched, showUnwatched])

  useEffect(() => {
    void loadGames()
  }, [loadGames])

  async function handleToggleWatched(gameId: string) {
    setIsLoading(true)
    setError(null)

    try {
      const result = await toggleGameWatched(season, seasonType, gameId)
      setStatus(
        `${result.game_id} marked ${result.watched ? 'watched' : 'unwatched'}`,
      )
      await loadGames()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to toggle watched state',
      )
    } finally {
      setIsLoading(false)
    }
  }

  async function handleUpdateSeason() {
    setIsLoading(true)
    setError(null)

    try {
      const result = await updateSeason(season)
      setStatus(`Added ${result.num_games_added} new games`)
      await loadGames()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update season')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <PageHeader isLoading={isLoading} onRefresh={loadGames} />
      <GameFilters
        showWatched={showWatched}
        showUnwatched={showUnwatched}
        selectedSeason={season}
        isLoading={isLoading}
        onSeasonChange={setSeason}
        onShowWatchedChange={setShowWatched}
        onShowUnwatchedChange={setShowUnwatched}
        onUpdateSeason={handleUpdateSeason}
      />
      <StatusBar isLoading={isLoading} status={status} error={error} />
      <GameTable
        games={games}
        isLoading={isLoading}
        onToggleWatched={(gameId) => void handleToggleWatched(gameId)}
      />
    </main>
  )
}

export default App
