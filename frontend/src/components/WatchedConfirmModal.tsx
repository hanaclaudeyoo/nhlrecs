import type { GameRecommendation } from '../types/games'

type WatchedConfirmModalProps = {
  game: GameRecommendation
  isLoading: boolean
  onCancel: () => void
  onConfirm: () => void
}

export function WatchedConfirmModal({
  game,
  isLoading,
  onCancel,
  onConfirm,
}: WatchedConfirmModalProps) {
  const nextState = game.watched ? 'unwatched' : 'watched'

  return (
    <div className="modal-backdrop" role="presentation">
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="watched-modal-title"
      >
        <h2 id="watched-modal-title">Mark game {nextState}?</h2>
        <p>
          {game.away_team} at {game.home_team} on {game.date}
        </p>
        <div className="modal-actions">
          <button
            type="button"
            className="modal-cancel-button"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            type="button"
            className="modal-confirm-button"
            onClick={onConfirm}
            disabled={isLoading}
          >
            Mark {nextState}
          </button>
        </div>
      </div>
    </div>
  )
}
