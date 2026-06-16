import { Settings, UserRound } from 'lucide-react'

type PageHeaderProps = {
  displayUsername: string
  isLoggedIn: boolean
  onSettingsClick: () => void
  onProfileClick: () => void
}

export function PageHeader({
  displayUsername,
  isLoggedIn,
  onSettingsClick,
  onProfileClick,
}: PageHeaderProps) {
  const profileLabel = isLoggedIn
    ? `Open profile for ${displayUsername}`
    : 'Open profile login'

  return (
    <header className="page-header">
      <div className="page-header-main">
        <div>
          <h1>🏒 NHL Game Recommender</h1>
          <p>Find fun games without getting spoiled!</p>
        </div>
      </div>
      <div className="page-header-actions">
        <button
          type="button"
          className="profile-menu-button"
          aria-label={profileLabel}
          title={displayUsername}
          onClick={onProfileClick}
        >
          <UserRound size={22} aria-hidden="true" />
          <span>{displayUsername}</span>
        </button>
        <button
          type="button"
          className="header-icon-button"
          aria-label="Open metric weight settings"
          title="Metric weights"
          onClick={onSettingsClick}
        >
          <Settings size={22} aria-hidden="true" />
        </button>
      </div>
    </header>
  )
}
