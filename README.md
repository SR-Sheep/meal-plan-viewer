# 식단표 뷰어 (Meal Plan Viewer)

카카오톡 채널의 식단표를 크롤링하여 주차별로 정리하고 오늘의 식단을 보여주는 웹 애플리케이션입니다.

## 기능

- **오늘의 식단**: 오늘 날짜의 식단 정보를 한눈에 확인
- **주차별 식단 보기**: 주차별로 그룹화된 식단표 조회
- **자동 크롤링**: 카카오톡 채널에서 식단 정보 자동 수집

## 기술 스택

### Frontend
- React 18
- TypeScript
- Vite
- CSS3 (그라디언트 디자인)

### Backend
- Python 3.x
- Flask
- Flask-CORS
- BeautifulSoup4
- Selenium

### 데이터 저장
- JSON 파일

## 프로젝트 구조

```
meal-plan-viewer/
├── backend/
│   ├── app.py              # Flask API 서버
│   ├── scraper.py          # 카카오톡 채널 크롤러
│   ├── requirements.txt    # Python 의존성
│   ├── meal_data.json      # 식단 데이터 (자동 생성)
│   └── .env                # 환경 변수
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # 메인 React 컴포넌트
│   │   └── App.css         # 스타일시트
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 설치 및 실행

### 1. 백엔드 설정

```bash
cd backend

# Python 가상환경 생성 (선택사항)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
copy .env.example .env
```

### 2. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install
```

### 3. 식단 데이터 크롤링

크롤링 스크립트를 실행하기 전에 `scraper.py`의 파싱 로직을 실제 카카오톡 채널의 HTML 구조에 맞게 수정해야 합니다.

```bash
cd backend

# 크롤링 실행
python scraper.py
```

**중요**:
- Chrome 브라우저가 설치되어 있어야 합니다.
- ChromeDriver는 Selenium이 자동으로 관리합니다.
- 실제 카카오톡 채널의 HTML 구조에 맞게 `scraper.py`의 선택자를 수정해야 합니다.

### 4. 서버 실행

**백엔드 서버:**
```bash
cd backend
python app.py
```
서버는 http://localhost:5000 에서 실행됩니다.

**프론트엔드 개발 서버:**
```bash
cd frontend
npm run dev
```
앱은 http://localhost:3000 에서 실행됩니다.

## API 엔드포인트

### GET `/api/health`
서버 상태 확인

### GET `/api/today`
오늘의 식단 조회

**응답 예시:**
```json
{
  "date": "2026-03-03",
  "breakfast": "토스트, 우유, 과일",
  "lunch": "비빔밥, 된장찌개, 김치",
  "dinner": "김치찌개, 밥, 계란말이"
}
```

### GET `/api/weeks`
주차별 식단 조회

**응답 예시:**
```json
[
  {
    "week": "2026-W10",
    "year": 2026,
    "week_number": 10,
    "meals": [
      {
        "date": "2026-03-03",
        "breakfast": "...",
        "lunch": "...",
        "dinner": "..."
      }
    ]
  }
]
```

### GET `/api/meals`
모든 식단 조회

## 데이터 형식

`meal_data.json` 파일 구조:

```json
{
  "last_updated": "2026-03-03T12:00:00",
  "meals": [
    {
      "date": "2026-03-03",
      "breakfast": "조식 메뉴",
      "lunch": "중식 메뉴",
      "dinner": "석식 메뉴",
      "raw_text": "원본 텍스트 (선택사항)"
    }
  ]
}
```

## 크롤링 커스터마이징

`scraper.py`의 다음 메서드들을 실제 카카오톡 채널 구조에 맞게 수정하세요:

1. **`scrape_posts()`**: 게시물 선택자 수정
2. **`parse_meal_post()`**: 식단 정보 파싱 로직
3. **`extract_date()`**: 날짜 추출 로직
4. **`extract_menu()`**: 메뉴 추출 로직

## 개발 팁

### 테스트용 샘플 데이터 생성

크롤링 없이 앱을 테스트하려면 `backend/meal_data.json`을 수동으로 생성하세요:

```bash
cd backend
# 아래 샘플 데이터 참조
```

### 프론트엔드 빌드

```bash
cd frontend
npm run build
```

빌드된 파일은 `frontend/dist` 디렉토리에 생성됩니다.

## 문제 해결

### CORS 오류
- 백엔드 서버가 실행 중인지 확인
- `flask-cors`가 설치되어 있는지 확인

### 크롤링 오류
- Chrome 브라우저가 설치되어 있는지 확인
- 카카오톡 채널 URL이 올바른지 확인
- 웹페이지 구조가 변경되었을 수 있으므로 선택자 확인

### 데이터 없음
- `meal_data.json` 파일이 존재하는지 확인
- 크롤링을 먼저 실행했는지 확인

## 라이선스

MIT

## 참고사항

- 이 프로젝트는 교육 목적으로 제작되었습니다.
- 웹 크롤링 시 대상 웹사이트의 이용약관과 robots.txt를 준수하세요.
- 과도한 요청으로 서버에 부하를 주지 않도록 주의하세요.
