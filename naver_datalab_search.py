# -*- coding: utf-8 -*-
"""
네이버 데이터랩 통합 검색어 트렌드 API
endpoint: POST https://openapi.naver.com/v1/datalab/search
"""
import sys
import io
import json
import urllib.request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CLIENT_ID = "3kCLAbJiO4PojOPq1hHF"
CLIENT_SECRET = "D7nkrCT3zT"
URL = "https://openapi.naver.com/v1/datalab/search"


def search_trend(start_date: str, end_date: str, time_unit: str,
                 keyword_groups: list, device: str = "",
                 gender: str = "", ages: list = None) -> dict:
    """
    네이버 통합 검색어 트렌드 조회

    Args:
        start_date: 조회 시작일 (yyyy-mm-dd), 2016-01-01 이후
        end_date:   조회 종료일 (yyyy-mm-dd)
        time_unit:  구간 단위 ("date" | "week" | "month")
        keyword_groups: [{"groupName": str, "keywords": [str, ...]}, ...]
                         최대 5그룹, 그룹당 최대 20개 검색어
        device:     기기 조건 ("" | "pc" | "mo")
        gender:     성별 조건 ("" | "m" | "f")
        ages:       연령 조건 ([] | ["1"~"11"])
    """
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "keywordGroups": keyword_groups,
    }
    if device:
        body["device"] = device
    if gender:
        body["gender"] = gender
    if ages:
        body["ages"] = ages

    body_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(URL, data=body_bytes)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {error_body}") from e


def print_result(result: dict) -> None:
    print(f"\n조회 기간: {result['startDate']} ~ {result['endDate']}  단위: {result['timeUnit']}")
    for item in result.get("results", []):
        print(f"\n[{item['title']}] 검색어: {item['keywords']}")
        for d in item["data"]:
            print(f"  {d['period']}  ratio: {d['ratio']}")


if __name__ == "__main__":
    groups = [
        {"groupName": "인공지능", "keywords": ["인공지능", "AI", "ChatGPT"]},
        {"groupName": "머신러닝",  "keywords": ["머신러닝", "딥러닝"]},
    ]
    result = search_trend(
        start_date="2024-01-01",
        end_date="2024-06-30",
        time_unit="month",
        keyword_groups=groups,
    )
    print_result(result)
    print("\n--- 원본 JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
