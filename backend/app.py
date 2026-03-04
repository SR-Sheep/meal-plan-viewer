from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import json
import os
import logging

app = Flask(__name__)
CORS(app)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = 'meal_data.json'

def load_meal_data():
    """JSON 파일에서 식단 데이터 로드"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"weeks": []}

def save_meal_data(data):
    """식단 데이터를 JSON 파일에 저장"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_current_week():
    """현재 주차 식단 찾기"""
    data = load_meal_data()

    # 실제 날짜 사용
    now = datetime.now()

    current_year = now.year
    current_month = now.month

    # 월 기준 주차 계산: 1일부터 7일까지를 1주차, 8일부터 14일까지를 2주차로 계산
    current_week = ((now.day - 1) // 7) + 1

    print(f"현재 날짜: {now.year}년 {now.month}월 {now.day}일 → {now.month}월 {current_week}주차")

    for week in data['weeks']:
        if week['year'] == current_year and week['month'] == current_month and week['week'] == current_week:
            print(f"매칭된 식단표 발견: {week['title']}")
            return week

    print(f"해당 주차({current_year}년 {current_month}월 {current_week}주차) 식단표를 찾을 수 없습니다.")
    return None

def get_all_weeks():
    """모든 주간 식단표 반환"""
    data = load_meal_data()
    return data['weeks']

def run_scraper():
    """스크래퍼 실행 함수"""
    try:
        logger.info("스크래핑 시작...")
        from scraper import KakaoChannelScraper

        scraper = KakaoChannelScraper('https://pf.kakao.com/_xbzpvb/posts')
        weeks = scraper.scrape_posts()
        scraper.save_to_json()

        logger.info(f"스크래핑 완료: {len(weeks)}개의 주간식단표 수집")
    except Exception as e:
        logger.error(f"스크래핑 오류: {e}")
        import traceback
        traceback.print_exc()

@app.route('/api/this-week', methods=['GET'])
def this_week():
    """현재 주차 식단표 조회 API"""
    week = get_current_week()
    if week:
        return jsonify(week)
    return jsonify({'error': '현재 주차 식단표가 없습니다'}), 404

@app.route('/api/weeks', methods=['GET'])
def weeks_list():
    """모든 주간 식단표 조회 API"""
    weeks = get_all_weeks()
    return jsonify(weeks)

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크 API"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    # 스케줄러 설정
    scheduler = BackgroundScheduler()

    # 서버 시작 시 즉시 스크래핑 실행
    logger.info("서버 시작 시 스크래핑 실행...")
    run_scraper()

    # 매주 월요일 오전 8시에 스크래핑 실행
    scheduler.add_job(
        func=run_scraper,
        trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
        id='weekly_scraper',
        name='매주 월요일 8시 스크래핑',
        replace_existing=True
    )

    scheduler.start()
    logger.info("스케줄러 시작: 매주 월요일 오전 8시에 스크래핑 실행")

    try:
        app.run(debug=True, host='0.0.0.0', port=15000, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("스케줄러 종료")
