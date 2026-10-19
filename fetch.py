import requests

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CODE = "005930"
URLS = [
    f"https://m.stock.naver.com/api/stock/{CODE}/trend?pageSize=10",
    f"https://m.stock.naver.com/api/stock/{CODE}/trend",
    f"https://m.stock.naver.com/api/item/getTrendList.nhn?code={CODE}&size=10",
    f"https://m.stock.naver.com/api/stock/{CODE}/integration",
    "https://m.stock.naver.com/api/index/KOSPI/integration",
]

for u in URLS:
    print("=" * 60)
    print(u)
    try:
        r = requests.get(u, headers=H, timeout=30)
        print("status:", r.status_code, "| bytes:", len(r.content))
        print(r.text[:700])
    except Exception as e:
        print("ERROR:", repr(e))
