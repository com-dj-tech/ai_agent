# -*- coding: utf-8 -*-
"""
네이버 데이터랩 쇼핑인사이트 API

CLI 사용법:
  python naver_shopping_insight.py <mode> '<JSON_BODY>'

mode:
  categories  분야별 트렌드 조회
  keywords    카테고리 내 키워드별 트렌드 조회

categories 예시:
  python naver_shopping_insight.py categories \
    '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month",
      "category":[{"name":"패션의류","param":["50000000"]},{"name":"화장품/미용","param":["50000002"]}]}'

keywords 예시:
  python naver_shopping_insight.py keywords \
    '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month",
      "category":"50000000",
      "keyword":[{"name":"정장","param":["정장"]},{"name":"캐주얼","param":["캐주얼"]}]}'

주요 카테고리 코드 (cat_id):
  50000000 패션의류
  50000001 패션잡화
  50000002 화장품/미용
  50000003 디지털/가전
  50000004 가구/인테리어
  50000005 출산/육아
  50000006 식품
  50000007 스포츠/레저
  50000008 생활/건강
  50000009 여행/문화
  50000010 면세점
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


def print_result(result: dict) -> None:
    print(f"\n조회 기간: {result['startDate']} ~ {result['endDate']}  단위: {result['timeUnit']}")
    for item in result.get("results", []):
        label = item.get("title", "")
        print(f"\n[{label}]")
        for d in item["data"]:
            group = f"  group={d['group']}" if "group" in d else ""
            print(f"  {d['period']}{group}  ratio: {d['ratio']}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        mode = sys.argv[1]
        arg = sys.argv[2]
        if arg.startswith("@"):
            body = json.loads(open(arg[1:], encoding="utf-8").read())
        elif os.path.isfile(arg):
            body = json.loads(open(arg, encoding="utf-8").read())
        else:
            body = json.loads(arg)

        if mode == "categories":
            result = _post("categories", body)
        elif mode == "keywords":
            result = _post("category/keywords", body)
        else:
            print(f"오류: 알 수 없는 mode '{mode}'. 'categories' 또는 'keywords' 를 사용하세요.")
            sys.exit(1)

        print_result(result)
        print("\n--- JSON ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif len(sys.argv) == 2 and not sys.argv[1].startswith("{"):
        mode = sys.argv[1]
        body = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))

        if mode == "categories":
            result = _post("categories", body)
        elif mode == "keywords":
            result = _post("category/keywords", body)
        else:
            print(f"오류: 알 수 없는 mode '{mode}'. 'categories' 또는 'keywords' 를 사용하세요.")
            sys.exit(1)

        print_result(result)
        print("\n--- JSON ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        # 기본 데모 (mode 미지정)
        print("=" * 50)
        print("분야별 트렌드 (패션의류 vs 화장품/미용)")
        print("=" * 50)
        body1 = {
            "startDate": "2024-01-01",
            "endDate": "2024-06-30",
            "timeUnit": "month",
            "category": [
                {"name": "패션의류",    "param": ["50000000"]},
                {"name": "화장품/미용", "param": ["50000002"]},
            ],
        }
        r1 = _post("categories", body1)
        print_result(r1)

        print("\n" + "=" * 50)
        print("키워드별 트렌드 (정장 vs 캐주얼)")
        print("=" * 50)
        body2 = {
            "startDate": "2024-01-01",
            "endDate": "2024-06-30",
            "timeUnit": "month",
            "category": "50000000",
            "keyword": [
                {"name": "정장",   "param": ["정장"]},
                {"name": "캐주얼", "param": ["캐주얼"]},
            ],
        }
        r2 = _post("category/keywords", body2)
        print_result(r2)
