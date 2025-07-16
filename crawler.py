# -*- coding: utf-8 -*-
"""
Tving 크롤링 모듈
"""
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def setup_driver():
    """웹 드라이버를 설정하고 반환합니다."""
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def get_content_links(driver, url):
    """주어진 URL에서 콘텐츠 링크를 수집합니다."""
    driver.get(url)
    time.sleep(5)
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    cards = driver.find_elements(By.CSS_SELECTOR, "a[href^='/contents/']")
    return list(set(card.get_attribute("href") for card in cards if card.get_attribute("href")))

def get_content_details(driver, link):
    """개별 콘텐츠 페이지에서 상세 정보를 추출합니다."""
    driver.get(link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    title_tag = soup.select_one("img[alt]")
    title = title_tag["alt"] if title_tag and title_tag.has_attr("alt") else "제목 없음"

    desc_tag = soup.select_one("#__next > main > section > article > article > div.css-1iz9gs3.ee4wkaf4 > div.css-1gc7po1.ee4wkaf5 > p")
    description = desc_tag.get_text(strip=True) if desc_tag else ""

    img_tags = soup.select('img.loaded')
    thumbnail = ""
    for img in img_tags:
        src = img.get("src", "")
        if ".jpg" in src and "/resize/480" in src:
            thumbnail = src
            break

    age_rating = "정보 없음"
    age_div = soup.select_one(".tag-age")
    if age_div:
        for cls in age_div.get("class", []):
            if "tag-age-" in cls:
                code = cls.split("-")[-1]
                age_rating = {
                    "all": "전체 이용가",
                    "seven": "7세 이상",
                    "twelve": "12세 이상",
                    "fifteen": "15세 이상",
                    "nineteen": "19세 이상"
                }.get(code, f"등급 미상 ({code})")
                break

    cast = "정보 없음"
    for dt in soup.find_all("dt"):
        if dt.get_text(strip=True) == "출연":
            dd = dt.find_next_sibling("dd")
            if dd:
                cast = dd.get_text(strip=True)
            break
            
    return {
        "title": title,
        "description": description,
        "thumbnail": thumbnail,
        "age_rating": age_rating,
        "cast": cast,
    }

def save_to_csv(data, genre, subgenre):
    """크롤링된 데이터를 CSV 파일로 저장합니다."""
    save_dir = f"./{genre}"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"tving_{genre}_{subgenre}.csv"
    filepath = os.path.join(save_dir, filename)

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"✅ 저장 완료: {filepath}")

def crawl_tving_category(genre, subgenre, url):
    """지정된 카테고리의 모든 콘텐츠를 크롤링합니다."""
    print(f"🚀 시작: {genre}-{subgenre}")
    driver = setup_driver()
    links = get_content_links(driver, url)
    print(f"🔗 [{genre}-{subgenre}] 총 {len(links)}개 링크 수집")

    data = []
    for idx, link in enumerate(links):
        try:
            details = get_content_details(driver, link)
            details.update({"genre": genre, "subgenre": subgenre})
            data.append(details)
            print(f"[{idx+1}/{len(links)}] {details['title']} 완료")
        except Exception as e:
            print(f"[{idx+1}] ❌ 에러: {e}")
            continue
    
    driver.quit()
    save_to_csv(data, genre, subgenre)
