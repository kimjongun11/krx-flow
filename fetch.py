import os
import re
from io import StringIO
from datetime import datetime

import pandas as pd
import requests

OUT = "data/korea_foreign.csv"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MARKETS = {"KOSPI": "01", "KOSDAQ": "02"}

frames = []
for market, sosok in MARKETS.items():
    bizdate = datetime.now().strftime("%Y%m%d")
    url = (
        "https://finance.naver.com/sise/investorDealTrendDay.naver"
        f"?bizdate={bizdate}&sosok={sosok}"
    )
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.encoding = "euc-kr"
    tables = pd.read_html(StringIO(r.text))
    raw = tables[0].iloc[:, :4].copy()
    raw.columns = ["date", "individual", "foreign", "institution"]
    raw["date"] = raw["date"].astype(str)
    raw = raw[raw["date"].str.match(r"^\d{2}\.\d{2}\.\d{2}$")]
    if raw.empty:
        print(tables[0].head(15))
        raise SystemExit(f"{market}: no rows parsed")
    raw["date"] = pd.to_datetime(raw["date"], format="%y.%m.%d").dt.strftime("%Y-%m-%d")
    for c in ["individual", "foreign", "institution"]:
        raw[c] = pd.to_numeric(raw[c].astype(str).str.replace(",", ""), errors="coerce")
    raw["market"] = market
    frames.append(raw)

new = pd.concat(frames)
os.makedirs("data", exist_ok=True)
if os.path.exists(OUT):
    new = pd.concat([pd.read_csv(OUT), new])
new = new.drop_duplicates(["date", "market"], keep="last").sort_values(["date", "market"])
new.to_csv(OUT, index=False)
print(new.tail(6))
