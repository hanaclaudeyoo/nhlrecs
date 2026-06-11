import { UserRound } from 'lucide-react'

type PageHeaderProps = {
  displayUsername: string
  isLoggedIn: boolean
  profileError: string | null
  onProfileClick: () => void
}

export function PageHeader({
  displayUsername,
  isLoggedIn,
  profileError,
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
      <div className="profile-header-control">
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
        {profileError && (
          <div className="profile-header-error" role="status">
            {profileError}
          </div>
        )}
      </div>
    </header>
  )
}
