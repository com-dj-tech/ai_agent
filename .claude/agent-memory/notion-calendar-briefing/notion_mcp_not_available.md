---
name: notion-mcp-not-available-use-notion-api-skill
description: 이 환경에는 mcp__notion 도구가 로드되지 않음 - Notion 조회/수정은 notion-api 스킬(Python 스크립트)로 대체 수행
metadata:
  type: reference
---

이 세션 환경에는 `mcp__notion__*` MCP 도구가 존재하지 않는다 (ToolSearch로 "notion" 검색해도 매칭 없음). 워크플로 스펙 문서(Step 1/Step 6)는 mcp__notion 사용을 전제하지만 실제로는 사용 불가.

**대체 경로**: `notion-api` 스킬 (`C:/Users/SBS/.claude/skills/notion-api/notion_api.py`)
- DB 조회: `query-db --db-id <ID>` (필터 없이 호출하면 title+url만 반환하는 요약 리스트)
- 페이지 전체 프로퍼티 조회: 전용 CLI 커맨드 없음 → `python -c "import notion_api as n; n.api('get', '/pages/<PAGE_ID>')"` 로 직접 호출
- 페이지 프로퍼티 업데이트(상태 변경, 텍스트 append 등): 전용 CLI 커맨드 없음 → 동일하게 `n.api('patch', f'/pages/{page_id}', body)` 를 인라인 python으로 호출
- DB 스키마(select 옵션 등) 확인: `n.api('get', f'/databases/{db_id}')`

**Why:** notion_api.py는 archive/restore/delete-block/update-block/query-db/get-property 등 "MCP가 못 하는 고급 작업"만 CLI 서브커맨드로 노출하고, 범용 페이지 조회·프로퍼티 업데이트는 별도 커맨드가 없다. 다만 내부에 범용 `api(method, path, body)` 헬퍼가 있어 python -c로 직접 호출하면 페이지 GET/PATCH 등 임의 Notion API 호출이 가능하다.

**How to apply:** 이 세션에서 Notion 페이지 상세 조회나 프로퍼티 업데이트가 필요하면, 먼저 mcp__notion 도구가 실제로 로드 가능한지 ToolSearch로 확인하고, 없으면 곧바로 notion-api 스킬의 인라인 python `api()` 호출 방식을 사용할 것 (매번 새 CLI 서브커맨드를 찾으려 하지 말 것).

관련: [[notion-personal-schedule-db-schema]]
