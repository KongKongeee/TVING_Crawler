# 🎬 TVING VOD 데이터 크롤러 (TVING VOD Crawler)

## 📖 프로젝트 개요

이 프로젝트는 **IPTV 추천 시스템의 핵심 데이터 파이프라인** 중 하나로, 국내 대표 OTT 서비스인 **TVING**의 VOD(다시보기) 콘텐츠 데이터를 수집, 병합, 가공하는 것을 목표로 합니다.

드라마, 영화, 예능, 애니메이션 등 다양한 카테고리와 장르별로 방대한 양의 VOD 데이터를 효율적으로 수집하고, 중복 데이터를 제거하여 정제된 통합 데이터셋을 구축합니다.

## ✨ 주요 기능

- **대규모 VOD 데이터 수집**: TVING의 주요 카테고리(드라마, 영화, 예능, 애니)와 세부 장르별 VOD 목록을 크롤링합니다.
- **병렬 처리 지원**: `ThreadPoolExecutor`를 활용하여 다수의 장르별 크롤링 작업을 동시에 수행함으로써 데이터 수집 시간을 대폭 단축합니다.
- **자동 데이터 병합 및 처리**: 크롤링 완료 후, 수집된 모든 `CSV` 파일을 자동으로 하나의 파일로 병합합니다.
- **중복 데이터 정제**: `title`, `genre`, `description`이 동일한 중복 콘텐츠를 식별하고, `subgenre` 정보를 쉼표(`,`)로 통합하여 데이터의 무결성을 보장합니다.

## 🛠️ 기술 스택

- **Language**: `Python`
- **Data Handling**: `Pandas`
- **Crawling**: `Selenium`, `BeautifulSoup4`
- **Parallel Processing**: `concurrent.futures.ThreadPoolExecutor`

## 📂 프로젝트 구조

```
tving_crawler/
├── main.py             # 크롤링 및 데이터 처리 실행 스크립트
├── crawler.py          # TVING 크롤링 핵심 로직
├── config.py           # 크롤링할 장르 및 URL 설정
├── requirements.txt    # 프로젝트 의존성 파일
├── 드라마/               # 장르별 수집 데이터(CSV) 저장 디렉토리
├── 영화/
├── 예능/
├── 애니/
├── tving_final_merged_data.csv # 최종 통합 데이터 파일
└── README.md           # 프로젝트 소개 문서
```

## 🚀 설치 및 실행 방법

1.  **리포지토리 클론**
    ```bash
    git clone https://github.com/your-username/tving-crawler.git
    cd tving-crawler
    ```

2.  **의존성 설치**
    ```bash
    pip install -r requirements.txt
    ```

3.  **크롬 드라이버 설치**
    이 프로젝트는 `Selenium`을 사용하므로, 사용자의 크롬 브라우저 버전에 맞는 [크롬 드라이버](https://chromedriver.chromium.org/downloads)를 설치하고 `crawler.py` 내의 드라이버 경로를 설정해야 합니다.

4.  **크롤러 및 데이터 처리 실행**
    `main.py`를 실행하면 크롤링과 데이터 병합/처리가 순차적으로 진행됩니다.
    ```bash
    python main.py
    ```

## 🔗 관련 프로젝트

이 프로젝트는 IPTV 추천 시스템 데이터 파이프라인의 일부입니다. 실시간 방송 편성표 데이터 수집을 위한 **[live-crawler](https://github.com/your-username/live-crawler)** 프로젝트도 함께 확인해보세요.