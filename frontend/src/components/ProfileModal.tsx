import { useState } from 'react'
import type { FormEvent } from 'react'

type ProfileModalProps = {
  username: string | null
  error: string | null
  onClose: () => void
  onLogin: (username: string, password: string) => void
  onLogout: () => void
}

export function ProfileModal({
  username,
  error,
  onClose,
  onLogin,
  onLogout,
}: ProfileModalProps) {
  const [nextUsername, setNextUsername] = useState(username ?? '')
  const [password, setPassword] = useState('')
  const trimmedUsername = nextUsername.trim()
  const canSubmit = trimmedUsername.length > 0 && password.length > 0

  function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canSubmit) {
      return
    }

    onLogin(trimmedUsername, password)
  }

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="modal profile-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="profile-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        {username === null ? (
          <form onSubmit={handleLogin}>
            <h2 id="profile-modal-title">Log in</h2>
            {error && (
              <div className="profile-modal-error" role="alert">
                {error}
              </div>
            )}
            <label className="profile-login-field">
              <span>Username</span>
              <input
                type="text"
                value={nextUsername}
                autoFocus
                onChange={(event) => setNextUsername(event.target.value)}
              />
            </label>
            <label className="profile-login-field">
              <span>Password</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
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
                disabled={!canSubmit}
              >
                Log in
              </button>
            </div>
          </form>
        ) : (
          <>
            <h2 id="profile-modal-title">Profile</h2>
            {error && (
              <div className="profile-modal-error" role="alert">
                {error}
              </div>
            )}
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
