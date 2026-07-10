---
name: execution-task-manager-integration-auth
description: gws CLI(Sheets/Gmail)와 Google Drive MCP 인증 상태 — 실행 전 반드시 먼저 확인할 것
metadata:
  type: project
---

2026-07-10 기준 관찰: `gws-sheets`/`gws-gmail` 스킬이 의존하는 `gws` CLI와 `mcp__claude_ai_Google_Drive__*` 도구 모두
"invalid_grant: Token has been expired or revoked" / "requires re-authorization"으로 실패했다.
반면 `mcp__claude_ai_Gmail__*` (별도 커넥터)는 읽기/검색/초안 작성(create_draft)까지는 정상 동작했지만
**실제 메일 발송 도구가 없다** (send 전용 툴 미제공, draft만 가능).

**Why:** Google Workspace 관련 3개 경로(gws CLI, Drive MCP, Gmail MCP)의 인증 상태가 서로 독립적이고 각각 별도로 끊길 수 있다.
Sheets 동기화와 실제 메일 발송은 현재 gws CLI 경로에만 의존하므로, gws 인증이 끊기면 두 기능 모두 불가능해진다.

**How to apply:** 실행업무 에이전트 워크플로우를 시작하기 전에, 먼저 가벼운 확인 커맨드로 인증 상태를 점검해라
(예: `gws gmail users getProfile --params '{"userId":"me"}'`). 실패 시 Step3(Sheets)/Step4(Gmail 발송)를 스킵하고
사용자에게 재인증을 요청한 뒤, Notion 조회·분류 결과만이라도 보고하는 것이 낫다. Step5(Notion 동기화 메모)는
"Sheets 쓰기 성공 확인 후에만 진행" 원칙에 따라 Sheets 실패 시 절대 건너뛰어야 한다 — 이 원칙은 지시문에 명시되어 있으므로 임의로 우회하지 말 것.
이 메모는 시점 스냅샷이므로, 다음 실행 시 반드시 재확인하고 최신 상태로 판단할 것 (인증이 이미 복구되었을 수 있음).

관련: [[notion-execution-db]]
