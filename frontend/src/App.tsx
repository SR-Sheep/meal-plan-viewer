import { useState, useEffect } from 'react'
import './App.css'

interface Meal {
  date: string
  breakfast: string
  lunch: string
  dinner: string
  raw_text?: string
}

interface Week {
  week: string
  year: number
  week_number: number
  meals: Meal[]
}

function App() {
  const [todayMeal, setTodayMeal] = useState<Meal | null>(null)
  const [weeks, setWeeks] = useState<Week[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [view, setView] = useState<'today' | 'weekly'>('today')

  const API_BASE = 'http://localhost:5000/api'

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      // 오늘의 식단 조회
      const todayRes = await fetch(`${API_BASE}/today`)
      if (todayRes.ok) {
        const todayData = await todayRes.json()
        setTodayMeal(todayData)
      }

      // 주차별 식단 조회
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

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    const weekdays = ['일', '월', '화', '수', '목', '금', '토']
    return `${date.getMonth() + 1}월 ${date.getDate()}일 (${weekdays[date.getDay()]})`
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
        <h1>🍽️ 식단표</h1>
        <div className="view-toggle">
          <button
            className={view === 'today' ? 'active' : ''}
            onClick={() => setView('today')}
          >
            오늘의 식단
          </button>
          <button
            className={view === 'weekly' ? 'active' : ''}
            onClick={() => setView('weekly')}
          >
            주차별 보기
          </button>
        </div>
      </header>

      {view === 'today' ? (
        <div className="today-view">
          {todayMeal ? (
            <div className="meal-card today">
              <h2>오늘의 식단 ({formatDate(todayMeal.date)})</h2>
              <div className="meal-content">
                {todayMeal.breakfast && (
                  <div className="meal-time">
                    <h3>🌅 아침</h3>
                    <p>{todayMeal.breakfast}</p>
                  </div>
                )}
                {todayMeal.lunch && (
                  <div className="meal-time">
                    <h3>☀️ 점심</h3>
                    <p>{todayMeal.lunch}</p>
                  </div>
                )}
                {todayMeal.dinner && (
                  <div className="meal-time">
                    <h3>🌙 저녁</h3>
                    <p>{todayMeal.dinner}</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="no-data">오늘의 식단이 없습니다.</div>
          )}
        </div>
      ) : (
        <div className="weekly-view">
          {weeks.length > 0 ? (
            weeks.map((week) => (
              <div key={week.week} className="week-card">
                <h2>{week.year}년 {week.week_number}주차</h2>
                <div className="meals-grid">
                  {week.meals.map((meal) => (
                    <div key={meal.date} className="meal-card">
                      <h3>{formatDate(meal.date)}</h3>
                      <div className="meal-content">
                        {meal.breakfast && (
                          <div className="meal-time">
                            <strong>아침:</strong> {meal.breakfast}
                          </div>
                        )}
                        {meal.lunch && (
                          <div className="meal-time">
                            <strong>점심:</strong> {meal.lunch}
                          </div>
                        )}
                        {meal.dinner && (
                          <div className="meal-time">
                            <strong>저녁:</strong> {meal.dinner}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="no-data">식단 데이터가 없습니다.</div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
