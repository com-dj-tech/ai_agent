# -*- coding: utf-8 -*-
"""
네이버 데이터랩 통합 검색어 트렌드 API
endpoint: POST https://openapi.naver.com/v1/datalab/search

CLI 사용법:
  python naver_datalab_search.py '<JSON_BODY>'

JSON_BODY 형식:
  {
    "startDate": "yyyy-mm-dd",       (필수, 2016-01-01 이후)
    "endDate":   "yyyy-mm-dd",       (필수)
    "timeUnit":  "date|week|month",  (필수)
    "keywordGroups": [               (필수, 최대 5그룹)
      {"groupName": "그룹명", "keywords": ["검색어1", "검색어2"]}
    ],
    "device": ""|"pc"|"mo",          (선택)
    "gender": ""|"m"|"f",            (선택)
    "ages":   ["1"~"11"]             (선택)
  }

예시:
  python naver_datalab_search.py '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month","keywordGroups":[{"groupName":"AI","keywords":["인공지능","ChatGPT"]}]}'
"""
import sys
import io
import os
import json
import urllib.request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CLIENT_ID = "3kCLAbJiO4PojOPq1hHF"
CLIENT_SECRET = "D7nkrCT3zT"
URL = "https://openapi.naver.com/v1/datalab/search"


def search_trend(body: dict) -> dict:
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
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
        if arg.startswith("@"):
            body = json.loads(open(arg[1:], encoding="utf-8").read())
        elif os.path.isfile(arg):
            body = json.loads(open(arg, encoding="utf-8").read())
        else:
            body = json.loads(arg)
    elif not sys.stdin.isatty():
        body = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
    else:
        # 기본 데모
        body = {
            "startDate": "2024-01-01",
            "endDate": "2024-06-30",
            "timeUnit": "month",
            "keywordGroups": [
                {"groupName": "인공지능", "keywords": ["인공지능", "AI", "ChatGPT"]},
                {"groupName": "머신러닝",  "keywords": ["머신러닝", "딥러닝"]},
            ],
        }

    result = search_trend(body)
    print_result(result)
    print("\n--- JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
