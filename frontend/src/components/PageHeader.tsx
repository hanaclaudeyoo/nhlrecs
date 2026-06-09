type PageHeaderProps = {
  isLoading: boolean
  onRefresh: () => void
}

export function PageHeader({ isLoading, onRefresh }: PageHeaderProps) {
  return (
    <header className="page-header">
      <div>
        <h1>🏒 NHL Game Recommender</h1>
        <p>Find fun games without getting spoiled!</p>
      </div>
      <button type="button" onClick={onRefresh} disabled={isLoading}>
        Refresh
      </button>
    </header>
  )
}
