import { useState } from 'react'

export type SingleSelectFilterOption<T extends string | null> = {
  value: T
  label: string
}

type SingleSelectFilterDropdownProps<T extends string | null> = {
  value: T
  options: SingleSelectFilterOption<T>[]
  disabled: boolean
  fallbackLabel: string
  menuClassName?: string
  onChange: (value: T) => void
}

export function SingleSelectFilterDropdown<T extends string | null>({
  value,
  options,
  disabled,
  fallbackLabel,
  menuClassName,
  onChange,
}: SingleSelectFilterDropdownProps<T>) {
  const [isOpen, setIsOpen] = useState(false)
  const selectedLabel =
    options.find((option) => option.value === value)?.label ?? fallbackLabel

  return (
    <div className="filter-dropdown" onMouseLeave={() => setIsOpen(false)}>
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
        <div
          className={
            menuClassName ? `filter-menu ${menuClassName}` : 'filter-menu'
          }
        >
          {options.map((option) => (
            <button
              type="button"
              className={
                option.value === value
                  ? 'filter-menu-option is-selected'
                  : 'filter-menu-option'
              }
              key={option.value ?? 'none'}
              disabled={disabled}
              aria-pressed={option.value === value}
              onClick={() => {
                onChange(option.value)
                setIsOpen(false)
              }}
            >
              {option.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
