import { useState } from 'react'

type SeasonOption = {
  value: string
  label: string
}

type SeasonFilterProps = {
  selectedSeason: string
  disabled: boolean
  onSeasonChange: (value: string) => void
}

const seasonOptions: SeasonOption[] = [
  { value: '20252026', label: '2025-2026' },
]

export function SeasonFilter({
  selectedSeason,
  disabled,
  onSeasonChange,
}: SeasonFilterProps) {
  const [isOpen, setIsOpen] = useState(false)
  const selectedLabel =
    seasonOptions.find((season) => season.value === selectedSeason)?.label ??
    'Season'

  return (
    <div className="filter-dropdown season-filter" onMouseLeave={() => setIsOpen(false)}>
      <button
        type="button"
        className={
          isOpen
            ? 'filter-dropdown-button is-open'
            : 'filter-dropdown-button'
        }
        disabled={disabled}
        onClick={() => setIsOpen((isOpen) => !isOpen)}
      >
        <span>{selectedLabel}</span>
        <span className="dropdown-caret" aria-hidden="true" />
      </button>

      {isOpen && (
        <div className="filter-menu">
          {seasonOptions.map((season) => (
            <button
              type="button"
              className="filter-menu-option"
              key={season.value}
              disabled={disabled}
              onClick={() => {
                onSeasonChange(season.value)
                setIsOpen(false)
              }}
            >
              {season.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
