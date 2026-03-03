import { useState, useEffect } from 'react'
import './App.css'

interface MealWeek {
  id: string
  title: string
  year: number
  month: number
  week: number
  image_url: string
  posted_date: string
  scraped_at: string
}

function App() {
  const [currentWeek, setCurrentWeek] = useState<MealWeek | null>(null)
  const [weeks, setWeeks] = useState<MealWeek[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [view, setView] = useState<'today' | 'weekly'>('today')
  const [imageErrors, setImageErrors] = useState<Set<string>>(new Set())

  const API_BASE = '/api'

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      // 현재 주차 식단 조회
      const thisWeekRes = await fetch(`${API_BASE}/this-week`)
      if (thisWeekRes.ok) {
        const thisWeekData = await thisWeekRes.json()
        setCurrentWeek(thisWeekData)
      }

      // 모든 주차 식단 조회
      const weeksRes = await fetch(`${API_BASE}/weeks`)
      const weeksData = await weeksRes.json()
      setWeeks(weeksData)

    } catch (err) {
      setError('데이터를 불러오는데 실패했습니다.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleImageError = (weekId: string) => {
    setImageErrors(prev => new Set(prev).add(weekId))
  }

  if (loading) {
    return <div className="container"><div className="loading">로딩 중...</div></div>
  }

  if (error) {
    return <div className="container"><div className="error">{error}</div></div>
  }

  return (
    <div className="container">
      <header>
        <h1>🍽️ 주간 식단표</h1>
        <div className="view-toggle">
          <button
            className={view === 'today' ? 'active' : ''}
            onClick={() => setView('today')}
          >
            이번주 식단
          </button>
          <button
            className={view === 'weekly' ? 'active' : ''}
            onClick={() => setView('weekly')}
          >
            전체 보기
          </button>
        </div>
      </header>

      {view === 'today' ? (
        <div className="today-view">
          {currentWeek ? (
            <div className="week-card featured">
              <h2>{currentWeek.title}</h2>
              <div className="week-image-container">
                {imageErrors.has(currentWeek.id) ? (
                  <div className="image-error">
                    <p>이미지를 불러올 수 없습니다</p>
                    <small>{currentWeek.image_url}</small>
                  </div>
                ) : (
                  <img
                    src={currentWeek.image_url}
                    alt={currentWeek.title}
                    loading="lazy"
                    onError={() => handleImageError(currentWeek.id)}
                  />
                )}
              </div>
              <div className="week-meta">
                <span>{currentWeek.year}년 {currentWeek.month}월 {currentWeek.week}주차</span>
              </div>
            </div>
          ) : (
            <div className="no-data">이번주 식단표가 없습니다.</div>
          )}
        </div>
      ) : (
        <div className="weekly-view">
          {weeks.length > 0 ? (
            <div className="weeks-grid">
              {weeks.map((week) => (
                <div key={week.id} className="week-card">
                  <h3>{week.title}</h3>
                  <div className="week-image-container">
                    {imageErrors.has(week.id) ? (
                      <div className="image-error">
                        <p>이미지를 불러올 수 없습니다</p>
                      </div>
                    ) : (
                      <img
                        src={week.image_url}
                        alt={week.title}
                        loading="lazy"
                        onError={() => handleImageError(week.id)}
                      />
                    )}
                  </div>
                  <div className="week-meta">
                    <span>{week.year}년 {week.month}월 {week.week}주차</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">식단 데이터가 없습니다.</div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
