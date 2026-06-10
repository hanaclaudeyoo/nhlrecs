import {
  SingleSelectFilterDropdown,
  type SingleSelectFilterOption,
} from './SingleSelectFilterDropdown'
import type { DateWindow } from '../types/games'

type DateFilterProps = {
  selectedDateWindow: DateWindow
  disabled: boolean
  onDateWindowChange: (value: DateWindow) => void
}

const dateWindowOptions: SingleSelectFilterOption<DateWindow>[] = [
  { value: 'all', label: 'Any Date' },
  { value: 'last_week', label: 'Last Week' },
  { value: 'last_month', label: 'Last Month' },
  { value: 'last_two_months', label: 'Last 2 Months' },
]

export function DateFilter({
  selectedDateWindow,
  disabled,
  onDateWindowChange,
}: DateFilterProps) {
  return (
    <SingleSelectFilterDropdown
      value={selectedDateWindow}
      options={dateWindowOptions}
      disabled={disabled}
      fallbackLabel="Any Date"
      onChange={onDateWindowChange}
    />
  )
}
