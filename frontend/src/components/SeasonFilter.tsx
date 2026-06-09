import {
  SingleSelectFilterDropdown,
  type SingleSelectFilterOption,
} from './SingleSelectFilterDropdown'

type SeasonFilterProps = {
  selectedSeason: string
  disabled: boolean
  onSeasonChange: (value: string) => void
}

const seasonOptions: SingleSelectFilterOption<string>[] = [
  { value: '20252026', label: '2025-2026' },
]

export function SeasonFilter({
  selectedSeason,
  disabled,
  onSeasonChange,
}: SeasonFilterProps) {
  return (
    <SingleSelectFilterDropdown
      value={selectedSeason}
      options={seasonOptions}
      disabled={disabled}
      fallbackLabel="Season"
      onChange={onSeasonChange}
    />
  )
}
