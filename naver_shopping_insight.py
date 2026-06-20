# -*- coding: utf-8 -*-
"""
네이버 데이터랩 쇼핑인사이트 API
주요 엔드포인트:
  분야별 트렌드:  POST https://openapi.naver.com/v1/datalab/shopping/categories
  키워드별 트렌드: POST https://openapi.naver.com/v1/datalab/shopping/category/keywords
"""
import sys
import io
import json
import urllib.request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CLIENT_ID = "3kCLAbJiO4PojOPq1hHF"
CLIENT_SECRET = "D7nkrCT3zT"
BASE = "https://openapi.naver.com/v1/datalab/shopping"


def _post(endpoint: str, body: dict) -> dict:
    url = f"{BASE}/{endpoint}"
    body_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body_bytes)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {error_body}") from e


def category_trend(start_date: str, end_date: str, time_unit: str,
                   categories: list, device: str = "",
                   gender: str = "", ages: list = None) -> dict:
    """
    쇼핑인사이트 분야별 트렌드 조회

    Args:
        categories: [{"name": str, "param": [cat_id, ...]}, ...]  최대 3개
                    cat_id 예) 패션의류=50000000, 화장품/미용=50000002
        device/gender/ages: 선택 필터
    """
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "category": categories,
    }
    if device:
        body["device"] = device
    if gender:
        body["gender"] = gender
    if ages:
        body["ages"] = ages
    return _post("categories", body)


def keyword_trend(start_date: str, end_date: str, time_unit: str,
                  category_id: str, keywords: list,
                  device: str = "", gender: str = "", ages: list = None) -> dict:
    """
    쇼핑인사이트 키워드별 트렌드 조회

    Args:
        category_id: 쇼핑 분야 코드 (cat_id 문자열)
        keywords: [{"name": str, "param": [keyword]}, ...]  최대 5개, param은 1개
    """
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "category": category_id,
        "keyword": keywords,
    }
    if device:
        body["device"] = device
    if gender:
        body["gender"] = gender
    if ages:
        body["ages"] = ages
    return _post("category/keywords", body)


def print_result(result: dict) -> None:
    print(f"\n조회 기간: {result['startDate']} ~ {result['endDate']}  단위: {result['timeUnit']}")
    for item in result.get("results", []):
        label = item.get("title", "")
        print(f"\n[{label}]")
        for d in item["data"]:
            group = f"  group={d['group']}" if "group" in d else ""
            print(f"  {d['period']}{group}  ratio: {d['ratio']}")


if __name__ == "__main__":
    print("=" * 50)
    print("1) 쇼핑인사이트 분야별 트렌드 (패션의류 vs 화장품/미용)")
    print("=" * 50)
    cats = [
        {"name": "패션의류",    "param": ["50000000"]},
        {"name": "화장품/미용", "param": ["50000002"]},
    ]
    r1 = category_trend("2024-01-01", "2024-06-30", "month", cats)
    print_result(r1)
    print("\n--- 원본 JSON ---")
    print(json.dumps(r1, ensure_ascii=False, indent=2))

    print("\n" + "=" * 50)
    print("2) 쇼핑인사이트 키워드별 트렌드 (패션의류 내 정장 vs 캐주얼)")
    print("=" * 50)
    kws = [
        {"name": "정장",   "param": ["정장"]},
        {"name": "캐주얼", "param": ["캐주얼"]},
    ]
    r2 = keyword_trend("2024-01-01", "2024-06-30", "month", "50000000", kws)
    print_result(r2)
    print("\n--- 원본 JSON ---")
    print(json.dumps(r2, ensure_ascii=False, indent=2))
