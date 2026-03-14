import json
import time
from pathlib import Path

import requests

URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

CONFIG = [
    {"fiat": "OMR", "tradeType": "BUY"},
    {"fiat": "OMR", "tradeType": "SELL"},
    {"fiat": "EGP", "tradeType": "BUY"},
    {"fiat": "EGP", "tradeType": "SELL"},
    {"fiat": "AED", "tradeType": "BUY"},
    {"fiat": "AED", "tradeType": "SELL"},
    {"fiat": "SAR", "tradeType": "BUY"},
    {"fiat": "SAR", "tradeType": "SELL"},
    {"fiat": "USD", "tradeType": "BUY"},
    {"fiat": "USD", "tradeType": "SELL"},
    {"fiat": "EUR", "tradeType": "BUY"},
    {"fiat": "EUR", "tradeType": "SELL"},
]

HEADERS = {
    "content-type": "application/json",
    "accept": "application/json",
    "user-agent": "Mozilla/5.0",
    "origin": "https://p2p.binance.com",
    "referer": "https://p2p.binance.com/",
}

def fetch_one(fiat: str, trade_type: str):
    payload = {
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "asset": "USDT",
        "tradeType": trade_type,
        "fiat": fiat,
        "publisherType": None,
        "merchantCheck": False,
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "filterType": "all",
        "periods": [],
        "additionalKycVerifyFilter": 0,
        "classifies": ["mass", "profession", "fiat_trade"],
    }

    r = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()

    ads = data.get("data", [])
    index_to_pick = 1 if len(ads) > 1 else 0

    if not ads:
        return {
            "price": None,
            "pickedIndex": None,
            "availableRows": 0,
            "advNo": None,
            "nickName": None,
            "minSingleTransAmount": None,
            "maxSingleTransAmount": None,
            "tradeMethods": [],
        }

    chosen = ads[index_to_pick]
    adv = chosen.get("adv", {})
    advertiser = chosen.get("advertiser", {})

    trade_methods = []
    for method in adv.get("tradeMethods", []):
        if isinstance(method, dict):
            name = method.get("tradeMethodName")
            if name:
                trade_methods.append(name)

    return {
        "price": float(adv.get("price")) if adv.get("price") else None,
        "pickedIndex": index_to_pick,
        "availableRows": len(ads),
        "advNo": adv.get("advNo"),
        "nickName": advertiser.get("nickName"),
        "minSingleTransAmount": adv.get("minSingleTransAmount"),
        "maxSingleTransAmount": adv.get("maxSingleTransAmount"),
        "tradeMethods": trade_methods,
    }

def main():
    output = {
        "updatedAt": int(time.time() * 1000),
        "source": "Binance P2P web endpoint",
        "asset": "USDT",
        "prices": {}
    }

    grouped = {}

    for item in CONFIG:
        fiat = item["fiat"]
        trade_type = item["tradeType"]

        result = fetch_one(fiat=fiat, trade_type=trade_type)
        grouped.setdefault(fiat, {})
        grouped[fiat][trade_type] = result

    output["prices"] = grouped

    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "p2p_prices.json"
    out_file.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Saved: {out_file}")

if __name__ == "__main__":
    main()
