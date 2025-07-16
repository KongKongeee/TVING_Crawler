# TVING 콘텐츠 크롤러

이 프로젝트는 TVING 웹사이트의 영화, 드라마, 예능 카테고리별 콘텐츠 정보를 크롤링하는 Python 스크립트입니다.

## ✨ 주요 기능

- **장르별 콘텐츠 크롤링**: 영화, 드라마, 예능 등 다양한 카테고리와 장르별로 콘텐츠 정보를 수집합니다.
- **상세 정보 수집**: 각 콘텐츠의 제목, 설명, 썸네일 이미지, 연령 등급, 출연진 정보를 추출합니다.
- **병렬 처리**: `ThreadPoolExecutor`를 사용하여 여러 카테고리를 동시에 크롤링하여 작업 시간을 단축합니다.
- **CSV 파일 저장**: 수집된 데이터는 각 장르별 폴더에 CSV 파일로 깔끔하게 정리하여 저장됩니다.

## ⚙️ 설치 및 실행

1.  **필요 라이브러리 설치:**

    ```bash
    pip install pandas selenium beautifulsoup4
    ```

2.  **ChromeDriver 설치:**

    사용 중인 Chrome 브라우저 버전에 맞는 [ChromeDriver](https://chromedriver.chromium.org/downloads)를 다운로드하여 프로젝트 경로 또는 시스템 경로에 추가해야 합니다.

3.  **크롤링 실행:**

    `main.py` 파일을 실행하여 크롤링을 시작합니다.

    ```bash
    python main.py
    ```

## 🛠️ 프로젝트 구조

-   `main.py`: 크롤링 프로세스를 시작하고 병렬 작업을 관리하는 메인 스크립트입니다.
-   `crawler.py`: 실제 웹 크롤링 로직(Selenium, BeautifulSoup)을 담고 있는 모듈입니다.
-   `config.py`: 크롤링할 대상 카테고리와 URL 목록을 관리하는 설정 파일입니다.
-   `.gitignore`: 버전 관리에서 제외할 파일(예: CSV 데이터, IDE 설정)을 정의합니다.
