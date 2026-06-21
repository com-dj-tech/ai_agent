# -*- coding: utf-8 -*-
"""
Notion API 접근 테스트 스크립트
- 사용자 정보 조회
- 페이지 검색
- 페이지 내용 읽기
- 페이지 생성 테스트
"""

import sys
import io
import os
import requests
import json
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


def print_result(title, data, success=True):
    status = "[OK]" if success else "[FAIL]"
    print(f"\n{status} [{title}]")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def test_get_current_user():
    """현재 사용자(봇) 정보 조회"""
    res = requests.get(f"{BASE_URL}/users/me", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        print_result("현재 사용자(봇) 정보", {
            "id": data.get("id"),
            "name": data.get("name"),
            "type": data.get("type"),
            "bot_owner": data.get("bot", {}).get("owner", {}).get("type"),
        })
        return data.get("id")
    else:
        print_result("현재 사용자 조회 실패", res.json(), success=False)
        return None


def test_list_users():
    """워크스페이스 멤버 목록 조회"""
    res = requests.get(f"{BASE_URL}/users", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        users = [{"id": u["id"], "name": u.get("name"), "type": u["type"]} for u in data.get("results", [])]
        print_result("워크스페이스 사용자 목록", {"count": len(users), "users": users})
    else:
        print_result("사용자 목록 조회 실패", res.json(), success=False)


def test_search_pages(query="테스트"):
    """페이지 검색"""
    payload = {
        "query": query,
        "filter": {"value": "page", "property": "object"},
        "page_size": 5,
    }
    res = requests.post(f"{BASE_URL}/search", headers=HEADERS, json=payload)
    if res.status_code == 200:
        data = res.json()
        results = []
        for r in data.get("results", []):
            title = ""
            props = r.get("properties", {})
            for v in props.values():
                if v.get("type") == "title":
                    texts = v.get("title", [])
                    title = "".join(t.get("plain_text", "") for t in texts)
                    break
            results.append({"id": r["id"], "title": title, "url": r.get("url")})
        print_result(f"페이지 검색 결과 (query='{query}')", {"count": len(results), "pages": results})
        return results
    else:
        print_result("페이지 검색 실패", res.json(), success=False)
        return []


def test_get_page(page_id):
    """특정 페이지 메타데이터 조회"""
    res = requests.get(f"{BASE_URL}/pages/{page_id}", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        props = data.get("properties", {})
        title = ""
        for v in props.values():
            if v.get("type") == "title":
                title = "".join(t.get("plain_text", "") for t in v.get("title", []))
                break
        print_result("페이지 상세 조회", {
            "id": data["id"],
            "title": title,
            "created_time": data.get("created_time"),
            "last_edited_time": data.get("last_edited_time"),
            "url": data.get("url"),
        })
    else:
        print_result("페이지 상세 조회 실패", res.json(), success=False)


def test_get_page_blocks(page_id):
    """페이지 블록(본문) 내용 조회"""
    res = requests.get(f"{BASE_URL}/blocks/{page_id}/children", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        blocks = []
        for b in data.get("results", []):
            btype = b.get("type")
            content = b.get(btype, {})
            text_parts = content.get("rich_text", [])
            text = "".join(t.get("plain_text", "") for t in text_parts)
            blocks.append({"type": btype, "text": text})
        print_result("페이지 블록 내용", {"count": len(blocks), "blocks": blocks})
    else:
        print_result("페이지 블록 조회 실패", res.json(), success=False)


def test_create_page(parent_page_id):
    """테스트 페이지 생성"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": f"API 자동 생성 테스트 — {now}"}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"Python Notion API로 {now}에 자동 생성된 페이지입니다."}}]
                },
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Notion API 연동 성공"}}]
                },
            },
        ],
    }
    res = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=payload)
    if res.status_code == 200:
        data = res.json()
        print_result("페이지 생성 성공", {"id": data["id"], "url": data.get("url")})
        return data["id"]
    else:
        print_result("페이지 생성 실패", res.json(), success=False)
        return None


def main():
    print("=" * 60)
    print("Notion API 접근 테스트")
    print("=" * 60)

    # 1. 현재 사용자(봇) 확인
    test_get_current_user()

    # 2. 워크스페이스 멤버 목록
    test_list_users()

    # 3. 페이지 검색
    pages = test_search_pages("테스트")

    # 4. 검색된 첫 번째 페이지 조회 및 블록 읽기
    if pages:
        target_id = pages[0]["id"]
        test_get_page(target_id)
        test_get_page_blocks(target_id)

        # 5. 해당 페이지 하위에 새 페이지 생성
        test_create_page(target_id)

    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
