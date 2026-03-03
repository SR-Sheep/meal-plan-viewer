from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'meal_data.json'

def load_meal_data():
    """JSON 파일에서 식단 데이터 로드"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"meals": []}

def save_meal_data(data):
    """식단 데이터를 JSON 파일에 저장"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_week_number(date):
    """날짜로부터 주차 계산 (월요일 시작)"""
    return date.isocalendar()[1]

def get_today_meal():
    """오늘의 식단 찾기"""
    data = load_meal_data()
    today = datetime.now().strftime('%Y-%m-%d')

    for meal in data['meals']:
        if meal['date'] == today:
            return meal
    return None

def get_meals_by_week():
    """주차별로 식단 그룹화"""
    data = load_meal_data()
    weeks = {}

    for meal in data['meals']:
        meal_date = datetime.strptime(meal['date'], '%Y-%m-%d')
        week_num = get_week_number(meal_date)
        year = meal_date.year
        week_key = f"{year}-W{week_num:02d}"

        if week_key not in weeks:
            weeks[week_key] = {
                'week': week_key,
                'year': year,
                'week_number': week_num,
                'meals': []
            }
        weeks[week_key]['meals'].append(meal)

    # 날짜순 정렬
    for week in weeks.values():
        week['meals'].sort(key=lambda x: x['date'])

    return sorted(weeks.values(), key=lambda x: x['week'], reverse=True)

@app.route('/api/today', methods=['GET'])
def today_meal():
    """오늘의 식단 조회 API"""
    meal = get_today_meal()
    if meal:
        return jsonify(meal)
    return jsonify({'error': '오늘의 식단이 없습니다'}), 404

@app.route('/api/weeks', methods=['GET'])
def weeks_meals():
    """주차별 식단 조회 API"""
    weeks = get_meals_by_week()
    return jsonify(weeks)

@app.route('/api/meals', methods=['GET'])
def all_meals():
    """모든 식단 조회 API"""
    data = load_meal_data()
    return jsonify(data['meals'])

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크 API"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
