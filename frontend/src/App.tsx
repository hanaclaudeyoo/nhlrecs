import { useCallback, useEffect, useState } from 'react'
import './styles/app.css'
import {
  fetchCurrentProfile,
  fetchGameRecommendations,
  fetchMetricWeights,
  loginProfile,
  logoutProfile,
  saveMetricWeights,
  signupProfile,
  toggleGameWatched,
} from './api/games'
import { GameFilters } from './components/GameFilters'
import { GameTable } from './components/GameTable'
import { PageHeader } from './components/PageHeader'
import { PaginationControls } from './components/PaginationControls'
import { StatusBar } from './components/StatusBar'
import { ProfileModal } from './components/ProfileModal'
import {
  defaultMetricWeights,
  MetricWeightsModal,
} from './components/MetricWeightsModal'
import type { DateWindow, GameRecommendation, MetricWeightKey } from './types/games'

function App() {
  const seasonPhase = '02'
  const defaultProfileId = 0
  const defaultUsername = 'Guest'
  const [season, setSeason] = useState('20252026')
  const [team, setTeam] = useState<string | null>(null)
  const [dateWindow, setDateWindow] = useState<DateWindow>('all')
  const [games, setGames] = useState<GameRecommendation[]>([])
  const [showWatched, setShowWatched] = useState(true)
  const [showUnwatched, setShowUnwatched] = useState(true)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(25)
  const [totalPages, setTotalPages] = useState(1)
  const [totalGames, setTotalGames] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [profileId, setProfileId] = useState(defaultProfileId)
  const [username, setUsername] = useState<string | null>(null)
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false)
  const [isMetricWeightsModalOpen, setIsMetricWeightsModalOpen] =
    useState(false)
  const [metricWeights, setMetricWeights] = useState(defaultMetricWeights)
  const [profileModalError, setProfileModalError] = useState<string | null>(
    null,
  )
  const [metricWeightsModalError, setMetricWeightsModalError] = useState<
    string | null
  >(null)
  const displayUsername = username ?? defaultUsername

  const loadGames = useCallback(async (pageOverride?: number) => {
    setIsLoading(true)
    setError(null)
    const nextPage = pageOverride ?? page

    try {
      const nextGames = await fetchGameRecommendations(
        season,
        seasonPhase,
        showWatched,
        showUnwatched,
        team,
        dateWindow,
        nextPage,
        pageSize,
      )
      setGames(nextGames.games)
      setPage(nextGames.page)
      setPageSize(nextGames.page_size)
      setTotalPages(nextGames.total_pages)
      setTotalGames(nextGames.total)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load games')
    } finally {
      setIsLoading(false)
    }
  }, [season, seasonPhase, showWatched, showUnwatched, team, dateWindow, page, pageSize])

  function handleSeasonChange(value: string) {
    setSeason(value)
    setPage(1)
  }

  function handleTeamChange(value: string | null) {
    setTeam(value)
    setPage(1)
  }

  function handleDateWindowChange(value: DateWindow) {
    setDateWindow(value)
    setPage(1)
  }

  function handleShowWatchedChange(value: boolean) {
    setShowWatched(value)
    setPage(1)
  }

  function handleShowUnwatchedChange(value: boolean) {
    setShowUnwatched(value)
    setPage(1)
  }

  function handlePageSizeChange(value: number) {
    setPageSize(value)
    setPage(1)
  }

  function handleMetricWeightChange(metricKey: MetricWeightKey, value: number) {
    setMetricWeightsModalError(null)
    setMetricWeights((weights) => ({
      ...weights,
      [metricKey]: value,
    }))
  }

  const loadMetricWeights = useCallback(async () => {
    try {
      const nextMetricWeights = await fetchMetricWeights()
      setMetricWeights(nextMetricWeights)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to load metric weights',
      )
    }
  }, [])

  async function handleOpenMetricWeightsModal() {
    setMetricWeightsModalError(null)
    setIsMetricWeightsModalOpen(true)
    await loadMetricWeights()
  }

  async function handleCancelMetricWeightsModal() {
    setMetricWeightsModalError(null)
    setIsMetricWeightsModalOpen(false)
    await loadMetricWeights()
  }

  async function handleSaveMetricWeights() {
    if (profileId === defaultProfileId) {
      setMetricWeightsModalError('Log in to customize metric weights')
      return
    }

    setIsLoading(true)
    setError(null)
    setMetricWeightsModalError(null)

    try {
      const savedMetricWeights = await saveMetricWeights(metricWeights)
      setMetricWeights(savedMetricWeights)
      setIsMetricWeightsModalOpen(false)
      setPage(1)
      await loadGames(1)
    } catch (err) {
      setMetricWeightsModalError(
        err instanceof Error && err.message.includes('Log in to save metric weights')
          ? 'Log in to customize metric weights'
          : 'Failed to save metric weights',
      )
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    async function restoreCurrentProfileAndLoadGames() {
      try {
        const profile = await fetchCurrentProfile()
        if (profile !== null) {
          setProfileId(profile.id)
          setUsername(profile.username)
        }
      } catch {
        setProfileId(defaultProfileId)
        setUsername(null)
      }

      await loadGames()
    }

    void restoreCurrentProfileAndLoadGames()
  }, [loadGames])

  async function handleToggleWatched(gameId: string) {
    if (profileId === defaultProfileId) {
      setProfileModalError('Log in to track watched games')
      setIsProfileModalOpen(true)
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      await toggleGameWatched(season, seasonPhase, gameId)
      await loadGames(1)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to toggle watched state',
      )
    } finally {
      setIsLoading(false)
    }
  }

  async function handleLogin(nextUsername: string, password: string) {
    setIsLoading(true)
    setError(null)

    try {
      const profile = await loginProfile(nextUsername, password)
      setProfileId(profile.id)
      setUsername(profile.username)
      setProfileModalError(null)
      setPage(1)
      setIsProfileModalOpen(false)
      await loadGames()
    } catch (err) {
      setProfileModalError(
        err instanceof Error &&
          err.message.includes('Invalid username or password')
          ? 'Invalid username or password'
          : 'Failed to log in',
      )
    } finally {
      setIsLoading(false)
    }
  }

  async function handleSignup(nextUsername: string, password: string) {
    setIsLoading(true)
    setError(null)

    try {
      const profile = await signupProfile(nextUsername, password)
      setProfileId(profile.id)
      setUsername(profile.username)
      setProfileModalError(null)
      setPage(1)
      setIsProfileModalOpen(false)
      await loadGames(1)
    } catch (err) {
      setProfileModalError(
        err instanceof Error && err.message.includes('Username already exists')
          ? 'Username already exists'
          : 'Failed to sign up',
      )
    } finally {
      setIsLoading(false)
    }
  }

  async function handleLogout() {
    setIsLoading(true)
    setError(null)

    try {
      await logoutProfile()
      setProfileId(defaultProfileId)
      setUsername(null)
      setProfileModalError(null)
      setPage(1)
      setIsProfileModalOpen(false)
      await loadGames()
    } catch (err) {
      setProfileModalError(
        err instanceof Error ? err.message : 'Failed to log out',
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <PageHeader
        displayUsername={displayUsername}
        isLoggedIn={username !== null}
        onSettingsClick={() => void handleOpenMetricWeightsModal()}
        onProfileClick={() => {
          setProfileModalError(null)
          setIsProfileModalOpen(true)
        }}
      />
      <GameFilters
        showWatched={showWatched}
        showUnwatched={showUnwatched}
        selectedSeason={season}
        selectedTeam={team}
        selectedDateWindow={dateWindow}
        isLoading={isLoading}
        onSeasonChange={handleSeasonChange}
        onTeamChange={handleTeamChange}
        onDateWindowChange={handleDateWindowChange}
        onShowWatchedChange={handleShowWatchedChange}
        onShowUnwatchedChange={handleShowUnwatchedChange}
      />
      <StatusBar isLoading={isLoading} error={error} />
      <GameTable
        games={games}
        isLoading={isLoading}
        onToggleWatched={(gameId) => void handleToggleWatched(gameId)}
      />
      <PaginationControls
        page={page}
        pageSize={pageSize}
        total={totalGames}
        totalPages={totalPages}
        isLoading={isLoading}
        onPageChange={setPage}
        onPageSizeChange={handlePageSizeChange}
      />
      {isProfileModalOpen && (
        <ProfileModal
          username={username}
          error={profileModalError}
          onClose={() => {
            setProfileModalError(null)
            setIsProfileModalOpen(false)
          }}
          onLogin={handleLogin}
          onSignup={handleSignup}
          onLogout={handleLogout}
        />
      )}
      {isMetricWeightsModalOpen && (
        <MetricWeightsModal
          weights={metricWeights}
          error={metricWeightsModalError}
          onCancel={() => void handleCancelMetricWeightsModal()}
          onDone={() => void handleSaveMetricWeights()}
          onWeightChange={handleMetricWeightChange}
        />
      )}
    </main>
  )
}

export default App
