---
name: gws-cli-auth-expired
description: gws CLI(calendar 등) 인증 토큰이 invalid_grant로 만료됨 - MCP Google Calendar 도구(computer.daejeons@gmail.com)로 대체 가능
metadata:
  type: project
---

2026-07-10 기준, `gws calendar events list` 등 gws CLI 명령 실행 시 다음 오류 발생:

```
error[auth]: Authentication failed: Failed to get token: Server error: invalid_grant: Token has been expired or revoked.
```

`gws auth login`은 브라우저 OAuth2 동의를 여는 대화형 명령이라 에이전트가 임의로 실행하면 안 됨(사용자 명시 동의 없이 OAuth 권한 부여 불가 원칙 위반). 재인증은 사용자가 직접 `gws auth login`을 실행해야 함.

**대체 경로**: 이 환경에는 `mcp__claude_ai_Google_Calendar__*` 도구(list_calendars/list_events/create_event/update_event/get_event/delete_event 등)가 이미 연결되어 있고, `list_calendars` 결과 계정이 `computer.daejeons@gmail.com` (사용자 본인 계정)으로 확인됨. gws CLI가 인증 실패 상태일 때는 이 MCP 도구로 캘린더 등록/조회 작업을 대신 수행할 수 있다.

**Why:** gws-calendar 스킬이 명시적으로 지정되어도, 인증이 깨져 있으면 스킬 자체가 동작하지 않는다. 매번 재시도하며 시간 낭비하지 말고 즉시 대체 경로로 전환하는 것이 효율적.

**How to apply:**
- gws CLI 호출이 401/invalid_grant로 실패하면, 재시도하지 말고 곧바로 `mcp__claude_ai_Google_Calendar__list_calendars`로 연결된 계정을 확인한 뒤 동일 작업을 MCP 도구로 수행한다.
- 최종 보고 시 "gws CLI 인증 만료로 MCP Google Calendar 도구로 대체 수행했다"는 점을 사용자에게 명시적으로 알린다(스킬 미준수가 아니라 우회임을 투명하게 밝히기 위함).
- 사용자가 원하면 `gws auth login`으로 재인증하도록 안내(에이전트가 직접 실행하지 않음).

관련: [[notion-mcp-not-available-use-notion-api-skill]]
