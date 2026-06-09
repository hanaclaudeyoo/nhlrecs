import { WatchedFilter } from './WatchedFilter'

type GameFiltersProps = {
  showWatched: boolean
  showUnwatched: boolean
  isLoading: boolean
  onShowWatchedChange: (value: boolean) => void
  onShowUnwatchedChange: (value: boolean) => void
  onUpdateSeason: () => void
}

export function GameFilters({
  showWatched,
  showUnwatched,
  isLoading,
  onShowWatchedChange,
  onShowUnwatchedChange,
  onUpdateSeason,
}: GameFiltersProps) {
  return (
    <div className="game-filters">
      <section className="toolbar" aria-label="Game filters and actions">
        <h2 className="game-filters-heading">Filters</h2>
        <div className="toolbar-controls">
          <WatchedFilter
            showWatched={showWatched}
            showUnwatched={showUnwatched}
            disabled={isLoading}
            onShowWatchedChange={onShowWatchedChange}
            onShowUnwatchedChange={onShowUnwatchedChange}
          />
          <button type="button" onClick={onUpdateSeason} disabled={isLoading}>
            Load new games
          </button>
        </div>
      </section>
    </div>
  )
}
