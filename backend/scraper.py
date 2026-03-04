import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
import re
from datetime import datetime

class KakaoChannelScraper:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.weeks = []

        # CSS 선택자 설정 (카카오 채널 실제 HTML 구조 기반)
        self.selectors = {
            'post_item': 'div.area_card',
            'post_title': 'strong.tit_card',
            'post_image': 'div.wrap_fit_thumb',
            'post_date': 'span.txt_date'
        }

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

            # 디버그: 페이지 소스 저장
            with open('page_source_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("디버그: page_source_debug.html 파일 저장 완료")

            # 게시물 파싱
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # area_card 클래스를 가진 모든 div 찾기
            posts = soup.find_all('div', class_='area_card')

            print(f"발견된 게시물: {len(posts)}개")

            for post in posts:
                week_data = self.parse_week_post(post)
                if week_data:
                    self.weeks.append(week_data)

        except Exception as e:
            print(f"스크래핑 오류: {e}")
            import traceback
            traceback.print_exc()

        finally:
            driver.quit()

        return self.weeks

    def parse_week_post(self, post):
        """게시물에서 주간 식단표 정보 추출"""
        try:
            # 제목 추출
            title_elem = post.find('strong', class_='tit_card')

            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            # "[주간식단표]"로 시작하는 게시물만 필터링
            if not title.startswith('[주간식단표]'):
                return None

            print(f"주간식단표 발견: {title}")

            # 제목에서 월, 주차 추출 (예: "[주간식단표] 3월 1주차")
            pattern = r'\[주간식단표\]\s*(\d+)월\s*(\d+)주차'
            match = re.search(pattern, title)

            if not match:
                print(f"제목 파싱 실패: {title}")
                return None

            month = int(match.group(1))
            week = int(match.group(2))

            # 년도 판별: 현재 월보다 미래 월이면 작년 데이터로 간주
            now = datetime.now()
            year = now.year
            # 예: 현재 3월인데 12월 데이터면 작년(2025년)
            if month > now.month + 3:  # 3개월 이상 차이나면 작년으로 판단
                year -= 1

            # 이미지 URL 추출 (div.wrap_fit_thumb의 background-image에서)
            image_div = post.find('div', class_='wrap_fit_thumb')
            image_url = None

            if image_div and image_div.get('style'):
                style = image_div.get('style')
                # background-image: url("https://..."); 형식에서 URL 추출
                import re as regex
                url_match = regex.search(r'url\(["\']?([^"\']+)["\']?\)', style)
                if url_match:
                    image_url = url_match.group(1)

            if not image_url:
                print(f"이미지를 찾을 수 없음: {title}")
                return None

            # ID 생성 (중복 방지)
            week_id = f"{year}-{month:02d}-w{week}"

            # 중복 확인
            if any(w['id'] == week_id for w in self.weeks):
                print(f"중복 데이터: {week_id}")
                return None

            return {
                'id': week_id,
                'title': title,
                'year': year,
                'month': month,
                'week': week,
                'image_url': image_url,
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"게시물 파싱 오류: {e}")
            import traceback
            traceback.print_exc()

        return None

    def save_to_json(self, filename='meal_data.json'):
        """스크래핑한 데이터를 JSON 파일로 저장"""
        # 년-월-주차 기준 내림차순 정렬 (최신순)
        sorted_weeks = sorted(self.weeks, key=lambda x: (x['year'], x['month'], x['week']), reverse=True)

        data = {
            'last_updated': datetime.now().isoformat(),
            'weeks': sorted_weeks
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"데이터 저장 완료: {filename} ({len(self.weeks)}개 주간식단표)")

if __name__ == '__main__':
    # 스크래핑 실행
    scraper = KakaoChannelScraper('https://pf.kakao.com/_xbzpvb/posts')
    weeks = scraper.scrape_posts()
    scraper.save_to_json()

    print(f"\n총 {len(weeks)}개의 주간식단표를 수집했습니다.")
    for week in weeks:
        print(f"  - {week['title']} (이미지: {week['image_url'][:50]}...)")
