# -*- coding: utf-8 -*-
"""
Tving 병렬 크롤링 및 데이터 병합/처리 실행 스크립트
"""
import sys
import pandas as pd
import glob
import os
from concurrent.futures import ThreadPoolExecutor
from config import genre_links
from crawler import crawl_tving_category

# Windows 터미널의 인코딩 오류 방지를 위해 표준 출력 인코딩을 UTF-8로 설정
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def merge_and_process_data():
    """
    크롤링된 CSV 파일들을 병합하고 중복 데이터를 처리하는 함수
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sub_dirs = ['드라마', '애니', '영화', '예능']
        all_files = []
        for sub_dir in sub_dirs:
            path = os.path.join(base_dir, sub_dir, '*.csv')
            found_files = glob.glob(path)
            all_files.extend(found_files)

        if not all_files:
            print("병합할 CSV 파일을 찾을 수 없습니다.")
            return

        print(f"총 {len(all_files)}개의 파일을 병합하고 처리합니다.")
        
        all_dfs = []
        for f in all_files:
            try:
                df = pd.read_csv(f)
                all_dfs.append(df)
            except Exception as e:
                print(f"파일을 읽는 중 오류 발생: {f}, 오류: {e}")

        if not all_dfs:
            print("병합할 데이터프레임이 없습니다.")
            return

        merged_df = pd.concat(all_dfs, ignore_index=True)

        key_cols = ['title', 'genre', 'description']
        for col in key_cols:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].fillna('')

        if 'subgenre' in merged_df.columns:
            merged_df['subgenre'] = merged_df['subgenre'].astype(str).replace('nan', '')

        agg_funcs = {col: 'first' for col in merged_df.columns if col not in ['title', 'genre', 'description', 'subgenre']}
        agg_funcs['subgenre'] = lambda x: ','.join(sorted(set(i for i in x if i)))

        processed_df = merged_df.groupby(key_cols, as_index=False).agg(agg_funcs)
        
        processed_df = processed_df[merged_df.columns.tolist()]

        output_file = os.path.join(base_dir, 'tving_final_merged_data.csv')
        processed_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"✅ 성공적으로 파일을 처리하여 {output_file} 에 저장했습니다.")
        print(f"   - 원본 데이터 수: {len(merged_df)}")
        print(f"   - 중복 처리 후 데이터 수: {len(processed_df)}")

    except Exception as e:
        print(f"데이터 병합 및 처리 중 오류 발생: {e}")


if __name__ == "__main__":
    # 1. 병렬 크롤링 실행
    print("🚀 Tving 병렬 크롤링을 시작합니다...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(crawl_tving_category, genre, subgenre, url) for genre, subgenre, url in genre_links]
        
        for future in futures:
            future.result()

    print("🎉 전체 병렬 크롤링 완료!")
    
    # 2. 데이터 병합 및 처리 실행
    print("\n🔄 크롤링된 데이터의 병합 및 처리를 시작합니다...")
    merge_and_process_data()
    print("\n✨ 모든 작업이 완료되었습니다.")
