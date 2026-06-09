import { useState } from 'react'

type WatchedFilterProps = {
    showWatched: boolean
    showUnwatched: boolean
    disabled: boolean
    onShowWatchedChange: (value: boolean) => void
    onShowUnwatchedChange: (value: boolean) => void
}

export function WatchedFilter({
    showWatched,
    showUnwatched,
    disabled,
    onShowWatchedChange,
    onShowUnwatchedChange
}: WatchedFilterProps)
{
    const [isOpen, setIsOpen] = useState(false)
    return (
        <div className="filter-dropdown watched-filter" onMouseLeave={() => setIsOpen(false)}>
            <button 
                type="button"
                className={isOpen ? 'filter-dropdown-button is-open' : 'filter-dropdown-button'}
                disabled={disabled}
                onClick={() => setIsOpen((isOpen) => !isOpen)}
            >
                <span>Watched Status</span>
                <span className="dropdown-caret" aria-hidden="true" />
            </button>

            {isOpen && (
                <div className="filter-menu">
                    <label>
                        <input 
                            type="checkbox"
                            disabled={disabled}
                            checked={showWatched}
                            onChange={(event) => onShowWatchedChange(event.target.checked)}
                        />
                        Watched
                    </label>
                    <label>
                        <input 
                            type="checkbox"
                            disabled={disabled}
                            checked={showUnwatched}
                            onChange={(event) => onShowUnwatchedChange(event.target.checked)}
                        />
                        Unwatched
                    </label>
                </div>
            )}
        </div>
    )
}
