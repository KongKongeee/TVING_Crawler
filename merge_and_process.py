

import pandas as pd
import glob
import os

try:
    base_dir = r'C:\work_python\project\crawler\tving_crawler'
    sub_dirs = ['드라마', '애니', '영화', '예능']
    all_files = []
    for sub_dir in sub_dirs:
        path = os.path.join(base_dir, sub_dir, '*.csv')
        found_files = glob.glob(path)
        all_files.extend(found_files)

    if not all_files:
        print("병합할 CSV 파일을 찾을 수 없습니다.")
    else:
        print(f"총 {len(all_files)}개의 파일을 병합하고 처리합니다.")
        
        all_dfs = []
        for f in all_files:
            try:
                df = pd.read_csv(f)
                all_dfs.append(df)
            except Exception as e:
                print(f"파일을 읽는 중 오류 발생: {f}, 오류: {e}")

        if all_dfs:
            merged_df = pd.concat(all_dfs, ignore_index=True)

            key_cols = ['title', 'genre', 'description']
            for col in key_cols:
                if col in merged_df.columns:
                    merged_df[col] = merged_df[col].fillna('')

            if 'subgenre' in merged_df.columns:
                merged_df['subgenre'] = merged_df['subgenre'].astype(str).replace('nan', '')

            agg_funcs = {col: 'first' for col in merged_df.columns if col not in ['title', 'genre', 'description', 'subgenre']}
            agg_funcs['subgenre'] = lambda x: ', '.join(sorted(set(i for i in x if i)))

            processed_df = merged_df.groupby(key_cols, as_index=False).agg(agg_funcs)
            
            processed_df = processed_df[merged_df.columns.tolist()]

            output_file = os.path.join(base_dir, 'tving_all_merged.csv')
            processed_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"성공적으로 파일을 처리하여 {output_file} 에 저장했습니다.")
            print(f"원본 데이터 수: {len(merged_df)}, 중복 처리 후 데이터 수: {len(processed_df)}")
        else:
            print("병합할 데이터프레임이 없습니다.")

except Exception as e:
    print(f"스크립트 실행 중 오류 발생: {e}")

