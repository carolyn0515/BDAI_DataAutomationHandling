import pandas as pd
def optimize_types(df:pd.DataFrame)->pd.DataFrame:
    df=df.copy()
    int_cols=["actor_id", "repo_id", "cnt"]
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # 숫자로 변환 _ 이상값 있으면 NaN으로 change by errors="coerce"
            if df[col].isna().any():
                df[col]=df[col].astype("Int64")
            else:
                df[col]=pd.to_numeric(df[col], downcast="integer")
            if "type" in df.columns:
                df["type"]=df["type"].astype("category")
            if "date" in df.columns:
                df["date"]=pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
            return df
        # 이후 read_parquet()으로 읽어오면 타입이 꼭 최적 상태라는 보장이 없어서
        # optimize_types()로 한 번 정리
