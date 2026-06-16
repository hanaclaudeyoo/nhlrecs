import { DateFilter } from './DateFilter'
import { SeasonFilter } from './SeasonFilter'
import { TeamFilter } from './TeamFilter'
import { WatchedFilter } from './WatchedFilter'
import type { DateWindow } from '../types/games'

type GameFiltersProps = {
  showWatched: boolean
  showUnwatched: boolean
  selectedSeason: string
  selectedTeam: string | null
  selectedDateWindow: DateWindow
  isLoading: boolean
  onSeasonChange: (value: string) => void
  onTeamChange: (value: string | null) => void
  onDateWindowChange: (value: DateWindow) => void
  onShowWatchedChange: (value: boolean) => void
  onShowUnwatchedChange: (value: boolean) => void
}

export function GameFilters({
  showWatched,
  showUnwatched,
  selectedSeason,
  selectedTeam,
  selectedDateWindow,
  isLoading,
  onSeasonChange,
  onTeamChange,
  onDateWindowChange,
  onShowWatchedChange,
  onShowUnwatchedChange,
}: GameFiltersProps) {
  return (
    <div className="game-filters">
      <section className="toolbar" aria-label="Game filters and actions">
        <h2 className="game-filters-heading">Filters</h2>
        <div className="toolbar-controls">
          <div className="toolbar-filter-controls">
            <SeasonFilter
              selectedSeason={selectedSeason}
              disabled={isLoading}
              onSeasonChange={onSeasonChange}
            />
            <DateFilter
              selectedDateWindow={selectedDateWindow}
              disabled={isLoading}
              onDateWindowChange={onDateWindowChange}
            />
            <TeamFilter
              selectedTeam={selectedTeam}
              disabled={isLoading}
              onTeamChange={onTeamChange}
            />
            <WatchedFilter
              showWatched={showWatched}
              showUnwatched={showUnwatched}
              disabled={isLoading}
              onShowWatchedChange={onShowWatchedChange}
              onShowUnwatchedChange={onShowUnwatchedChange}
            />
          </div>
        </div>
      </section>
    </div>
  )
}
