import { useEffect, useState } from 'react'

type PaginationControlsProps = {
  page: number
  pageSize: number
  total: number
  totalPages: number
  isLoading: boolean
  onPageChange: (page: number) => void
  onPageSizeChange: (pageSize: number) => void
}

const pageSizeOptions = [10, 25, 50, 100]

export function PaginationControls({
  page,
  pageSize,
  total,
  totalPages,
  isLoading,
  onPageChange,
  onPageSizeChange,
}: PaginationControlsProps) {
  const [pageInput, setPageInput] = useState(String(page))

  useEffect(() => {
    setPageInput(String(page))
  }, [page])

  function submitPageInput() {
    const nextPage = Number(pageInput)

    if (!Number.isFinite(nextPage) || pageInput.trim() === '') {
      setPageInput(String(page))
      return
    }

    const clampedPage = Math.min(Math.max(Math.floor(nextPage), 1), totalPages)
    setPageInput(String(clampedPage))
    onPageChange(clampedPage)
  }

  return (
    <section className="pagination-controls" aria-label="Pagination">
      <div className="pagination-summary">
        Page {page} of {totalPages} · {total} games
      </div>

      <div className="pagination-page-actions">
        <button
          type="button"
          disabled={isLoading || page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          <span className="pagination-arrow pagination-arrow-left" aria-hidden="true" />
          Previous
        </button>
        <label className="page-jump-control">
          <span>Go to</span>
          <input
            type="number"
            min={1}
            max={totalPages}
            value={pageInput}
            disabled={isLoading}
            onChange={(event) => setPageInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                submitPageInput()
              }
            }}
          />
        </label>
        <button
          type="button"
          disabled={isLoading || page >= totalPages}
          onClick={() => onPageChange(page + 1)}
        >
          Next
          <span className="pagination-arrow pagination-arrow-right" aria-hidden="true" />
        </button>
      </div>

      <div className="pagination-size-actions">
        <label className="page-size-control">
          <span>Rows</span>
          <select
            value={pageSize}
            disabled={isLoading}
            onChange={(event) => onPageSizeChange(Number(event.target.value))}
          >
            {pageSizeOptions.map((option) => (
              <option value={option} key={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </div>
    </section>
  )
}
