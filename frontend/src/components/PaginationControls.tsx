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
  return (
    <section className="pagination-controls" aria-label="Pagination">
      <div className="pagination-summary">
        Page {page} of {totalPages} · {total} games
      </div>

      <div className="pagination-actions">
        <button
          type="button"
          disabled={isLoading || page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          Previous
        </button>
        <button
          type="button"
          disabled={isLoading || page >= totalPages}
          onClick={() => onPageChange(page + 1)}
        >
          Next
        </button>
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
