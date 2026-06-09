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
    <section className="toolbar" aria-label="Game filters and actions">
      <label>
        <input
          type="checkbox"
          checked={showWatched}
          onChange={(event) => onShowWatchedChange(event.target.checked)}
        />
        Show watched
      </label>
      <label>
        <input
          type="checkbox"
          checked={showUnwatched}
          onChange={(event) => onShowUnwatchedChange(event.target.checked)}
        />
        Show unwatched
      </label>
      <button type="button" onClick={onUpdateSeason} disabled={isLoading}>
        Load new games
      </button>
    </section>
  )
}
