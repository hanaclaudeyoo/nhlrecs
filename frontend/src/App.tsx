import { useCallback, useEffect, useState } from 'react'
import './styles/app.css'
import {
  fetchGameRecommendations,
  toggleGameWatched,
  updateSeason,
} from './api/games'
import { GameFilters } from './components/GameFilters'
import { GameTable } from './components/GameTable'
import { PageHeader } from './components/PageHeader'
import { PaginationControls } from './components/PaginationControls'
import { StatusBar } from './components/StatusBar'
import type { DateWindow, GameRecommendation } from './types/games'

function App() {
  const seasonType = '02'
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

  const loadGames = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const nextGames = await fetchGameRecommendations(
        season,
        seasonType,
        showWatched,
        showUnwatched,
        team,
        dateWindow,
        page,
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
  }, [season, seasonType, showWatched, showUnwatched, team, dateWindow, page, pageSize])

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

  useEffect(() => {
    void loadGames()
  }, [loadGames])

  async function handleToggleWatched(gameId: string) {
    setIsLoading(true)
    setError(null)

    try {
      await toggleGameWatched(season, seasonType, gameId)
      await loadGames()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to toggle watched state',
      )
    } finally {
      setIsLoading(false)
    }
  }

  async function handleUpdateSeason() {
    setIsLoading(true)
    setError(null)

    try {
      await updateSeason(season)
      await loadGames()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update season')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <PageHeader />
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
        onUpdateSeason={handleUpdateSeason}
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
    </main>
  )
}

export default App
