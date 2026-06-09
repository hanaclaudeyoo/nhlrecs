import { useState } from 'react'

type TeamOption = {
  value: string | null
  label: string
}

type TeamFilterProps = {
  selectedTeam: string | null
  disabled: boolean
  onTeamChange: (value: string | null) => void
}

const teamOptions: TeamOption[] = [
  { value: null, label: 'All Teams' },
  { value: 'ANA', label: 'ANA' },
  { value: 'ARI', label: 'ARI' },
  { value: 'BOS', label: 'BOS' },
  { value: 'BUF', label: 'BUF' },
  { value: 'CAR', label: 'CAR' },
  { value: 'CBJ', label: 'CBJ' },
  { value: 'CGY', label: 'CGY' },
  { value: 'CHI', label: 'CHI' },
  { value: 'COL', label: 'COL' },
  { value: 'DAL', label: 'DAL' },
  { value: 'DET', label: 'DET' },
  { value: 'EDM', label: 'EDM' },
  { value: 'FLA', label: 'FLA' },
  { value: 'LAK', label: 'LAK' },
  { value: 'MIN', label: 'MIN' },
  { value: 'MTL', label: 'MTL' },
  { value: 'NJD', label: 'NJD' },
  { value: 'NSH', label: 'NSH' },
  { value: 'NYI', label: 'NYI' },
  { value: 'NYR', label: 'NYR' },
  { value: 'OTT', label: 'OTT' },
  { value: 'PHI', label: 'PHI' },
  { value: 'PIT', label: 'PIT' },
  { value: 'SEA', label: 'SEA' },
  { value: 'SJS', label: 'SJS' },
  { value: 'STL', label: 'STL' },
  { value: 'TBL', label: 'TBL' },
  { value: 'TOR', label: 'TOR' },
  { value: 'UTA', label: 'UTA' },
  { value: 'VAN', label: 'VAN' },
  { value: 'VGK', label: 'VGK' },
  { value: 'WPG', label: 'WPG' },
  { value: 'WSH', label: 'WSH' },
]

export function TeamFilter({
  selectedTeam,
  disabled,
  onTeamChange,
}: TeamFilterProps) {
  const [isOpen, setIsOpen] = useState(false)
  const selectedLabel =
    teamOptions.find((team) => team.value === selectedTeam)?.label ??
    'All Teams'

  return (
    <div className="filter-dropdown team-filter" onMouseLeave={() => setIsOpen(false)}>
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
        <div className="filter-menu team-filter-menu">
          {teamOptions.map((team) => (
            <button
              type="button"
              className="filter-menu-option"
              key={team.value ?? 'all'}
              disabled={disabled}
              onClick={() => {
                onTeamChange(team.value)
                setIsOpen(false)
              }}
            >
              {team.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
