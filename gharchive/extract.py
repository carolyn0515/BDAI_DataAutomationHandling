from google.cloud import bigquery
from datetime import timedelta
from pathlib import Path

QUERY_TEMPLATE="""
SELECT
    actor.id AS actor_id,
    repo.id AS repo_id,
    type,
    COUNT(*) AS cnt
FROM `githubarchive.day.{date_str}`
GROUP BY 1, 2, 3
"""
def dry_run(client, date_str):
    query = QUERY_TEMPLATE.format(date_str=date_str)
    # 실제 실행 없이 시뮬레이션만 하는 실행
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    # dry_run=True: 쿼리 실행 안 하고 얼마나 데이터 읽을지 계산만 함
    # 캐시 무시하고 실제 데이터 기준으로 계산
    # dry: 물 안 쓰는 연습 _ 연습 실행
    job = client.query(query, job_config=job_config)
    # BigQuery에 dry run 요청을 보냄 _ 실제 데이터는 안 읽고 메타 정보만 계산
    bytes_processed = job.total_bytes_processed
    # 이 쿼리가 실제로 실행되면 몇 바이트를 읽는지 가져옴
    estimated_cost_usd = (bytes_processed/(1024**4))*5
    return {
        "query": query,
        "bytes_processed": bytes_processed,
        "estimated_cost_usd": estimated_cost_usd,
    }
def extract_single_day(client, date_str):
    query=QUERY_TEMPLATE.format(date_str=date_str)
    df=client.query(query).to_dataframe(create_bqstorage_client=False)
    # bigquery.readsessions.create 권한 문제 회피용
    # BigQueryStorageAPI 쓰지 않고 기본 방식으로 df 변환
    return df
def extract_date_range(client, start_date, end_date, output_dir: Path, logger):
    saved_files=[]
    current = start_date
    while current <= end_date:
        date_str=current.strftime("%Y%m%d")
        logger.info(f"Processing {date_str}")

        df = extract_single_day(client, date_str)
        df["date"] = date_str

        output_path=output_dir/f"{date_str}.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_parquet(output_path, index=False)

        size_mb=output_path.stat().st_size/1024**2
        logger.info(f"Saved {output_path} ({size_mb:.2f} MB)")

        saved_files.append(output_path)
        
        current += timedelta(days=1)
    
    return saved_files