# 주간 식단표 뷰어

한국동서발전 풀무원푸드앤컬처 카카오톡 채널에서 주간 식단표를 자동으로 수집하여 보여주는 웹 애플리케이션입니다.

## 주요 기능

- 📅 **이번주 식단**: 오늘 날짜를 기준으로 현재 주차의 식단표를 자동으로 표시
- 📋 **전체 보기**: 수집된 모든 주간 식단표를 한눈에 확인
- 📌 **고정 헤더**: 스크롤 시 상단에 고정되는 네비게이션
- 🔄 **자동 크롤링**: Selenium을 이용한 카카오톡 채널 자동 스크래핑
- 🎨 **깔끔한 UI**: 다크 테마의 현대적이고 간결한 인터페이스
- 🔍 **이미지 확대**: 클릭하여 식단표 이미지를 크게 볼 수 있음

## 기술 스택

### Backend
- Python 3.x
- Flask (REST API 서버)
- Selenium (웹 스크래핑)
- BeautifulSoup4 (HTML 파싱)

### Frontend
- React 18
- TypeScript
- Vite
- CSS3

## 프로젝트 구조

```
meal-plan-viewer/
├── backend/
│   ├── app.py              # Flask API 서버
│   ├── scraper.py          # 카카오톡 채널 스크래퍼
│   ├── meal_data.json      # 식단 데이터 저장소
│   └── requirements.txt    # Python 의존성
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # 메인 React 컴포넌트
│   │   └── App.css         # 스타일시트
│   ├── vite.config.ts      # Vite 설정
│   └── package.json        # npm 의존성
├── run.bat                 # 서버 실행 스크립트 (Windows)
└── README.md
```

## 설치 및 실행

### 빠른 시작 (Windows)

```bash
git clone https://github.com/SR-Sheep/meal-plan-viewer.git
cd meal-plan-viewer

# 의존성 설치
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
cd ..

# 서버 실행 (백엔드 + 프론트엔드 동시 실행)
run
```

`run.bat` 파일이 자동으로:
- 기존 실행 중인 서버를 종료하고
- 백엔드(Flask)와 프론트엔드(Vite)를 동시에 실행합니다

### 수동 설치 및 실행

#### 1. 저장소 클론

```bash
git clone https://github.com/SR-Sheep/meal-plan-viewer.git
cd meal-plan-viewer
```

#### 2. Backend 설정

```bash
cd backend

# 의존성 설치
pip install -r requirements.txt

# Flask 서버 실행 (포트 5000)
python app.py
```

#### 3. Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행 (포트 11120)
npm run dev
```

#### 4. 스크래핑 실행

```bash
cd backend
python scraper.py
```

## API 엔드포인트

### GET `/api/this-week`
현재 주차의 식단표를 반환합니다.

**응답 예시:**
```json
{
  "id": "2026-03-w1",
  "title": "[주간식단표] 3월 1주차",
  "year": 2026,
  "month": 3,
  "week": 1,
  "image_url": "https://k.kakaocdn.net/...",
  "posted_date": "2026-03-03",
  "scraped_at": "2026-03-03T17:57:32.245492"
}
```

### GET `/api/weeks`
모든 주간 식단표 목록을 반환합니다.

**응답 예시:**
```json
[
  {
    "id": "2026-03-w1",
    "title": "[주간식단표] 3월 1주차",
    ...
  },
  ...
]
```

### GET `/api/health`
서버 상태를 확인합니다.

## 주차 계산 방식

월 기준 주차 계산을 사용합니다:
- 1일 ~ 7일: 1주차
- 8일 ~ 14일: 2주차
- 15일 ~ 21일: 3주차
- 22일 ~ 28일: 4주차
- 29일 ~ 말일: 5주차

## 데이터 구조

식단 데이터는 `meal_data.json` 파일에 다음 형식으로 저장됩니다:

```json
{
  "last_updated": "2026-03-03T17:57:39.095749",
  "weeks": [
    {
      "id": "2026-03-w1",
      "title": "[주간식단표] 3월 1주차",
      "year": 2026,
      "month": 3,
      "week": 1,
      "image_url": "https://k.kakaocdn.net/...",
      "posted_date": "2026-03-03",
      "scraped_at": "2026-03-03T17:57:32.245492"
    }
  ]
}
```

## 스크래핑 소스

카카오톡 채널: [한국동서발전 풀무원푸드앤컬처](https://pf.kakao.com/_xbzpvb/posts)

제목이 "[주간식단표]"로 시작하는 게시물만 필터링하여 수집합니다.

## 포트 설정

- **Backend (Flask)**: 5000
- **Frontend (Vite)**: 11120
- Frontend의 `/api` 요청은 Vite 프록시를 통해 Backend로 전달됩니다.

## 브라우저 지원

- Chrome (최신 버전)
- Firefox (최신 버전)
- Safari (최신 버전)
- Edge (최신 버전)

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트는 언제나 환영합니다!
