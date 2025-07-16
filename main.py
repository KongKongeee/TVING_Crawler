# -*- coding: utf-8 -*-
"""
Tving 병렬 크롤링 실행 스크립트
"""
from concurrent.futures import ThreadPoolExecutor
from config import genre_links
from crawler import crawl_tving_category

if __name__ == "__main__":
    # ✅ 병렬 처리 (max_workers는 동시에 실행할 스레드 수)
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 각 장르에 대해 크롤링 작업을 제출
        futures = [executor.submit(crawl_tving_category, genre, subgenre, url) for genre, subgenre, url in genre_links]
        
        # 모든 작업이 완료될 때까지 대기
        for future in futures:
            future.result()  # 작업 중 발생한 예외가 있다면 여기서 발생

    print("🎉 전체 병렬 크롤링 완료!")
