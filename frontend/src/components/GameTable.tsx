import type { GameRecommendation } from '../types/games'

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
  return (
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
                  onClick={() => onToggleWatched(game.game_id)}
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
  )
}
