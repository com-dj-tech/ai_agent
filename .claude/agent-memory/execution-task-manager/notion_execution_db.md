---
name: notion-execution-db
description: 실행업무 DB의 실제 Notion 스키마와 조회 방법 — MCP Notion 도구가 없을 때 notion-api 스킬로 어떻게 전체 프로퍼티를 가져오는지
metadata:
  type: reference
---

실행업무 DB의 database_id: `736fbc07-f533-4d91-b49d-75fc816b3c8b`

## 실제 프로퍼티 스키마 (2026-07-10 기준 확인)
DB 페이지의 실제 프로퍼티 이름은 지시문 상의 이름과 다르다:
- `제목` (title) — 업무명
- `마감일` (date)
- `상태` (select) — 값 예: "진행 중", "시작 전" (긴급/지연 같은 값은 select 옵션에 없음 — D-day 기반으로 매번 새로 계산해야 함)
- `우선순위` (select) — 값 예: "높음", "중간"
- `담당자` (people) — 실제로는 비어있는 경우가 많음; 담당자 이름은 `메모` 필드의 자유 텍스트에 들어있음
- `메모` (rich_text) — 배경 설명, 담당자명, 관련 회의 등이 서술형으로 들어있음
- `진행률` (number) — 비어있는 경우 많음

**"행동유형" 프로퍼티 자체가 없다.** 업무명 텍스트에서 키워드(작성/검토·승인/수립/정리 등)를 보고 추론해야 한다.
**동기화 확인용 프로퍼티도 없다** (예: "시트 동기화 완료" 같은 필드 없음). Step5의 "시트 동기화 완료: {날짜}" 메모를 남기려면 페이지에 코멘트를 추가하거나 `메모` 필드에 append하는 방식을 검토해야 하는데, `메모`는 업무 설명용으로 이미 쓰이고 있어 섞으면 안 됨 — 별도 프로퍼티 추가를 사용자에게 제안하는 것이 나을 수 있음.

## MCP Notion 도구가 로드되어 있지 않을 때
이 환경엔 `mcp__notion__*` 계열 도구가 없었다 (ToolSearch로 찾아도 안 나옴). 대신 `notion-api` 스킬의
`C:/Users/SBS/.claude/skills/notion-api/notion_api.py`를 사용했다.

- `query-db` 커맨드는 **id/title/url만** 반환한다 (전체 프로퍼티 반환 안 함). 페이지의 전체 속성값이 필요하면
  `notion_api.py`에 하드코딩된 토큰(환경변수 `NOTION_TOKEN`으로 덮어쓰기 가능, 값은 스크립트 파일 참조 — 여기 기록하지 않음)으로
  `GET https://api.notion.com/v1/pages/{page_id}` 를 직접 호출하는 별도 파이썬 스크립트를 스크래치패드에 작성해 실행하는 것이 가장 빠르다.
- Bash 도구에서 Windows 경로 따옴표 이슈로 heredoc이 깨질 수 있으니, 임시 스크립트는 Write 도구로 파일을 만들고
  `python "절대경로"`로 실행하는 방식이 안정적이다.

관련: [[execution-task-manager-integration-auth]]
