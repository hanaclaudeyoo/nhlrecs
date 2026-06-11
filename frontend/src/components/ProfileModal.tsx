import { useState } from 'react'
import type { FormEvent } from 'react'

type ProfileModalProps = {
  username: string | null
  onClose: () => void
  onLogin: (username: string) => void
  onLogout: () => void
}

export function ProfileModal({
  username,
  onClose,
  onLogin,
  onLogout,
}: ProfileModalProps) {
  const [nextUsername, setNextUsername] = useState(username ?? '')
  const trimmedUsername = nextUsername.trim()

  function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (trimmedUsername.length === 0) {
      return
    }

    onLogin(trimmedUsername)
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <div
        className="modal profile-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="profile-modal-title"
      >
        {username === null ? (
          <form onSubmit={handleLogin}>
            <h2 id="profile-modal-title">Log in</h2>
            <label className="profile-login-field">
              <span>Username</span>
              <input
                type="text"
                value={nextUsername}
                autoFocus
                onChange={(event) => setNextUsername(event.target.value)}
              />
            </label>
            <div className="modal-actions">
              <button
                type="button"
                className="modal-cancel-button"
                onClick={onClose}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="modal-confirm-button"
                disabled={trimmedUsername.length === 0}
              >
                Log in
              </button>
            </div>
          </form>
        ) : (
          <>
            <h2 id="profile-modal-title">Profile</h2>
            <p>Logged in as {username}</p>
            <div className="modal-actions">
              <button
                type="button"
                className="modal-cancel-button"
                onClick={onClose}
              >
                Cancel
              </button>
              <button
                type="button"
                className="modal-confirm-button"
                onClick={onLogout}
              >
                Log out
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
