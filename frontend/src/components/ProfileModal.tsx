import { useState } from 'react'
import type { FormEvent } from 'react'

type ProfileModalProps = {
  username: string | null
  error: string | null
  onClose: () => void
  onLogin: (username: string, password: string) => void
  onSignup: (username: string, password: string) => void
  onLogout: () => void
}

export function ProfileModal({
  username,
  error,
  onClose,
  onLogin,
  onSignup,
  onLogout,
}: ProfileModalProps) {
  const [mode, setMode] = useState<'login' | 'signup'>('login')
  const [nextUsername, setNextUsername] = useState(username ?? '')
  const [password, setPassword] = useState('')
  const [verifyPassword, setVerifyPassword] = useState('')
  const trimmedUsername = nextUsername.trim()
  const passwordsMatch = password === verifyPassword
  const canSubmit =
    trimmedUsername.length > 0 &&
    password.length > 0 &&
    (mode === 'login' || (verifyPassword.length > 0 && passwordsMatch))

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canSubmit) {
      return
    }

    if (mode === 'login') {
      onLogin(trimmedUsername, password)
    } else {
      onSignup(trimmedUsername, password)
    }
  }

  function switchMode(nextMode: 'login' | 'signup') {
    setMode(nextMode)
    setPassword('')
    setVerifyPassword('')
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
          <form onSubmit={handleSubmit}>
            <h2 id="profile-modal-title">
              {mode === 'login' ? 'Log in' : 'Sign up'}
            </h2>
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
            {mode === 'signup' && (
              <label className="profile-login-field">
                <span>Verify password</span>
                <input
                  type="password"
                  value={verifyPassword}
                  onChange={(event) => setVerifyPassword(event.target.value)}
                />
              </label>
            )}
            {mode === 'signup' && verifyPassword.length > 0 && !passwordsMatch && (
              <div className="profile-modal-error" role="alert">
                Passwords do not match
              </div>
            )}
            <div className="modal-actions">
              <button
                type="button"
                className="modal-cancel-button"
                onClick={onClose}
              >
                Cancel
              </button>
              <div className="profile-submit-actions">
                <button
                  type="button"
                  className="profile-mode-switch-button"
                  onClick={() =>
                    switchMode(mode === 'login' ? 'signup' : 'login')
                  }
                >
                  {mode === 'login' ? 'Sign up' : 'Log in'}
                </button>
                <button
                  type="submit"
                  className="modal-confirm-button"
                  disabled={!canSubmit}
                >
                  {mode === 'login' ? 'Log in' : 'Sign up'}
                </button>
              </div>
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
