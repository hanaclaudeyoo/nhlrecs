import {
  SingleSelectFilterDropdown,
  type SingleSelectFilterOption,
} from './SingleSelectFilterDropdown'

type TeamFilterProps = {
  selectedTeam: string | null
  disabled: boolean
  onTeamChange: (value: string | null) => void
}

const teamOptions: SingleSelectFilterOption<string | null>[] = [
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
  return (
    <SingleSelectFilterDropdown
      value={selectedTeam}
      options={teamOptions}
      disabled={disabled}
      fallbackLabel="All Teams"
      menuClassName="team-filter-menu"
      onChange={onTeamChange}
    />
  )
}
