type StatusBarProps = {
  isLoading: boolean
  error: string | null
}

export function StatusBar({ isLoading, error }: StatusBarProps) {
  return (
    <section className="status-bar" aria-live="polite">
      {isLoading && <span>Loading...</span>}
      {error && <strong>{error}</strong>}
    </section>
  )
}
