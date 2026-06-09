import { SeasonFilter } from './SeasonFilter'
import { WatchedFilter } from './WatchedFilter'

type GameFiltersProps = {
  showWatched: boolean
  showUnwatched: boolean
  selectedSeason: string
  isLoading: boolean
  onSeasonChange: (value: string) => void
  onShowWatchedChange: (value: boolean) => void
  onShowUnwatchedChange: (value: boolean) => void
  onUpdateSeason: () => void
}

export function GameFilters({
  showWatched,
  showUnwatched,
  selectedSeason,
  isLoading,
  onSeasonChange,
  onShowWatchedChange,
  onShowUnwatchedChange,
  onUpdateSeason,
}: GameFiltersProps) {
  return (
    <div className="game-filters">
      <section className="toolbar" aria-label="Game filters and actions">
        <h2 className="game-filters-heading">Filters</h2>
        <div className="toolbar-controls">
          <SeasonFilter
            selectedSeason={selectedSeason}
            disabled={isLoading}
            onSeasonChange={onSeasonChange}
          />
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
