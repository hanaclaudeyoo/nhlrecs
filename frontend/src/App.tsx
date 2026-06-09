import { useCallback, useEffect, useState } from 'react'
import './styles/app.css'
import {
  fetchGameRecommendations,
  toggleGameWatched,
  updateCurrentSeason,
} from './api/games'
import type { GameRecommendation } from './types/games'

function App() {
  const season = '20252026'
  const seasonType = '02'
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
      const result = await updateCurrentSeason()
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
      <header className="page-header">
        <div>
          <h1>🏒 NHL Game Recommender</h1>
          <p>Find fun games without getting spoiled!</p>
        </div>
        <button type="button" onClick={loadGames} disabled={isLoading}>
          Refresh
        </button>
      </header>

      <section className="toolbar" aria-label="Game filters and actions">
        <label>
          <input
            type="checkbox"
            checked={showWatched}
            onChange={(event) => setShowWatched(event.target.checked)}
          />
          Show watched
        </label>
        <label>
          <input
            type="checkbox"
            checked={showUnwatched}
            onChange={(event) => setShowUnwatched(event.target.checked)}
          />
          Show unwatched
        </label>
        <button type="button" onClick={handleUpdateSeason} disabled={isLoading}>
          Load new games
        </button>
      </section>

      <section className="status-bar" aria-live="polite">
        <span>{isLoading ? 'Loading...' : status}</span>
        {error && <strong>{error}</strong>}
      </section>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Date</th>
              <th>Away</th>
              <th>Home</th>
              <th>Watched</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {games.map((game) => (
              <tr key={`${game.season}-${game.season_phase}-${game.game_id}`}>
                <td>{game.rank}</td>
                <td>{game.date}</td>
                <td>{game.away_team}</td>
                <td>{game.home_team}</td>
                <td>{game.watched ? 'Yes' : 'No'}</td>
                <td>
                  <button
                    type="button"
                    onClick={() => void handleToggleWatched(game.game_id)}
                    disabled={isLoading}
                  >
                    Toggle
                  </button>
                </td>
              </tr>
            ))}
            {games.length === 0 && !isLoading && (
              <tr>
                <td colSpan={6}>No games match the current filters.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  )
}

export default App
