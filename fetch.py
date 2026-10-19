import os
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock

OUT = "data/korea_foreign.csv"
end = datetime.now()
start = end - timedelta(days=7)
f, t = start.strftime("%Y%m%d"), end.strftime("%Y%m%d")

frames = []
for market in ["KOSPI", "KOSDAQ"]:
    df = stock.get_market_trading_value_by_date(f, t, market)
    df = df[["외국인합계"]].copy()
    df["foreign_net_100m_krw"] = (df["외국인합계"] / 1e8).round(1)
    df = df[["foreign_net_100m_krw"]]
    df["market"] = market
    df.index.name = "date"
    frames.append(df.reset_index())

new = pd.concat(frames)
new["date"] = pd.to_datetime(new["date"]).dt.strftime("%Y-%m-%d")

os.makedirs("data", exist_ok=True)
if os.path.exists(OUT):
    old = pd.read_csv(OUT)
    new = pd.concat([old, new])

new = new.drop_duplicates(["date", "market"], keep="last")
new = new.sort_values(["date", "market"])
new.to_csv(OUT, index=False)
