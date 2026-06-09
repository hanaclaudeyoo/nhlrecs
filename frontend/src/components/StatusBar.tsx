type StatusBarProps = {
  isLoading: boolean
  status: string
  error: string | null
}

export function StatusBar({ isLoading, status, error }: StatusBarProps) {
  return (
    <section className="status-bar" aria-live="polite">
      <span>{isLoading ? 'Loading...' : status}</span>
      {error && <strong>{error}</strong>}
    </section>
  )
}
