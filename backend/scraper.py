import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
from datetime import datetime

class KakaoChannelScraper:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.meals = []

    def setup_driver(self):
        """Selenium WebDriver 설정"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 브라우저 창 숨김
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        return webdriver.Chrome(options=chrome_options)

    def scrape_posts(self):
        """카카오톡 채널 게시물 스크래핑"""
        driver = self.setup_driver()

        try:
            print(f"접속 중: {self.channel_url}")
            driver.get(self.channel_url)

            # 페이지 로딩 대기
            time.sleep(3)

            # 스크롤하여 더 많은 게시물 로드
            for _ in range(5):  # 5번 스크롤
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # 게시물 파싱
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 여기서 실제 카카오톡 채널 구조에 맞게 선택자를 수정해야 합니다
            # 아래는 예시 구조입니다
            posts = soup.find_all('div', class_='post')  # 실제 클래스명으로 변경 필요

            print(f"발견된 게시물: {len(posts)}개")

            for post in posts:
                meal_data = self.parse_meal_post(post)
                if meal_data:
                    self.meals.append(meal_data)

        except Exception as e:
            print(f"스크래핑 오류: {e}")

        finally:
            driver.quit()

        return self.meals

    def parse_meal_post(self, post):
        """게시물에서 식단 정보 추출"""
        try:
            # 실제 카카오톡 채널 구조에 맞게 수정 필요
            # 아래는 예시 파싱 로직입니다

            text = post.get_text(strip=True)

            # 날짜 추출 (예: "2026년 3월 3일" 형식)
            # 실제 게시물 형식에 맞게 수정 필요
            date_str = self.extract_date(text)

            # 식단 메뉴 추출
            menu = self.extract_menu(text)

            if date_str and menu:
                return {
                    'date': date_str,
                    'breakfast': menu.get('breakfast', ''),
                    'lunch': menu.get('lunch', ''),
                    'dinner': menu.get('dinner', ''),
                    'raw_text': text
                }

        except Exception as e:
            print(f"게시물 파싱 오류: {e}")

        return None

    def extract_date(self, text):
        """텍스트에서 날짜 추출"""
        # 실제 게시물 형식에 맞게 정규식이나 파싱 로직 구현 필요
        # 예시: "2026-03-03" 형식으로 반환
        return datetime.now().strftime('%Y-%m-%d')

    def extract_menu(self, text):
        """텍스트에서 식단 메뉴 추출"""
        # 실제 게시물 형식에 맞게 파싱 로직 구현 필요
        return {
            'breakfast': '조식 메뉴',
            'lunch': '중식 메뉴',
            'dinner': '석식 메뉴'
        }

    def save_to_json(self, filename='meal_data.json'):
        """스크래핑한 데이터를 JSON 파일로 저장"""
        data = {
            'last_updated': datetime.now().isoformat(),
            'meals': self.meals
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"데이터 저장 완료: {filename} ({len(self.meals)}개 식단)")

if __name__ == '__main__':
    # 스크래핑 실행
    scraper = KakaoChannelScraper('https://pf.kakao.com/_xbzpvb/posts')
    meals = scraper.scrape_posts()
    scraper.save_to_json()

    print(f"\n총 {len(meals)}개의 식단을 수집했습니다.")
