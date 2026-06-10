import { Eye, EyeOff } from 'lucide-react'
import { useState } from 'react'
import type { GameRecommendation } from '../types/games'
import { Tooltip } from './Tooltip'
import { WatchedConfirmModal } from './WatchedConfirmModal'

type GameTableProps = {
  games: GameRecommendation[]
  isLoading: boolean
  onToggleWatched: (gameId: string) => void
}

export function GameTable({
  games,
  isLoading,
  onToggleWatched,
}: GameTableProps) {
  const [pendingWatchedGame, setPendingWatchedGame] =
    useState<GameRecommendation | null>(null)

  function handleConfirmWatchedToggle() {
    if (pendingWatchedGame === null) {
      return
    }

    onToggleWatched(pendingWatchedGame.game_id)
    setPendingWatchedGame(null)
  }

  return (
    <>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Date</th>
              <th>Away</th>
              <th>Home</th>
              <th>Watched</th>
            </tr>
          </thead>
          <tbody>
            {games.map((game) => (
              <tr key={`${game.season}-${game.season_phase}-${game.game_id}`}>
                <td>{game.rank}</td>
                <td>{game.date}</td>
                <td>{game.away_team}</td>
                <td>{game.home_team}</td>
                <td>
                  <Tooltip label={game.watched ? 'Watched' : 'Unwatched'}>
                    <button
                      type="button"
                      className="watched-icon-button"
                      aria-label={game.watched ? 'Watched' : 'Unwatched'}
                      onClick={() => setPendingWatchedGame(game)}
                      disabled={isLoading}
                    >
                      {game.watched ? (
                        <Eye size={18} aria-hidden="true" />
                      ) : (
                        <EyeOff size={18} aria-hidden="true" />
                      )}
                    </button>
                  </Tooltip>
                </td>
              </tr>
            ))}
            {games.length === 0 && !isLoading && (
              <tr>
                <td colSpan={5}>No games match the current filters.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {pendingWatchedGame && (
        <WatchedConfirmModal
          game={pendingWatchedGame}
          isLoading={isLoading}
          onCancel={() => setPendingWatchedGame(null)}
          onConfirm={handleConfirmWatchedToggle}
        />
      )}
    </>
  )
}
