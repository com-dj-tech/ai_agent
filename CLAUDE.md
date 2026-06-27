# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Purpose

- Experiment with GitHub automation agents and manage repositories via gh CLI.
- Automate GitHub operations (repo management, issues, PRs, releases) using the `gh_cli` skill.
- Build a codebase management workflow centered on the AI agent `Chunsik`.

## Tone

- Concise and clear.
- Professional and objective.
- Output results only — no filler or unnecessary modifiers.

## Format

- Commit messages: auto-generated, context-aware, accurately describing each change.
- Output: confirm only the executed commands and their result status.
- Skill reference: `~/.claude/skills/gh_cli.md`
- All translated/interpreted versions of guideline files must be saved as `.txt` (e.g., `korean/CLAUDE.txt`).

## Skills

| Skill | Path | Description |
|-------|------|-------------|
| `gh_cli` | `~/.claude/skills/gh_cli.md` | Full GitHub CLI command reference |
| `card-news-maker` | `~/.claude/skills/card-news-maker.md` | Card news generator using Python Pillow |

## Connected Repository

- `com-dj-tech/ai_agent` — main experimental repository

## 메모 자동 분류 규칙

사용자가 입력한 문장을 분석하여 아래 5개 DB 중 하나로 분류

1. 업무요청 DB
- 클라이언트, 상사, 팀원 외부 담당자가 요청한 내용
- 트리거: 수정 요청, 추가 요청, 문의, 피드백, 전달 요청
- 예) 클라이언트가 오늘까지 상세페이지 문구를 수정해달라고 함

2. 실행업무 DB
- 사용자가 직접 처리해야할 작업
- 트리거: 제작, 수정, 작성, 제출, 전달, 확인, 정리 등의 행동이 포함된 내용
- 예) 오늘 오후까지 카드뉴스 5장 수정본 전달

3. 자료조사 DB
- 참고자료, 링크, 시장조사, 경쟁사 사례, 레퍼런스, 통계, 출처 정보
- 예) 경쟁사 랜딩페이지 후기 섹션 배치 방식 참고

4. 업무지식 DB
- 반복해서 활용할 수 있는 노하우, 매뉴얼, 응대 문구, 기준, 설명 방식
- 예) 원본 파일 제공시 기본 견적에 50% 추가금 안내해야함

5. 개인일정 DB
- 사용자의 개인 업무 혹은 일정 포함된 내용
- 예) 팀원들과 주말 오후 6시 전시회 관람 약속

## 트리거 우선 규칙

입력 문장이 아래 키워드로 시작하면 해당 DB로 우선 분류

- "요청" → 업무요청 DB
- "업무" → 실행업무 DB
- "자료" → 자료조사 DB
- "노하우" → 업무지식 DB
- "개인" → 개인일정 DB

## 애매한 경우 처리

분류가 확실하지 않으면 임의로 저장하지 않고 다음 기준을 따른다.

- 외부 사람이 시킨 내용 → 업무요청 DB
- 내가 해야 할 업무 → 실행업무 DB
- 참고하거나 조사한 정보 → 자료조사 DB
- 다음에도 반복해서 쓸 수 있는 지침, 기능 → 업무지식 DB
- 친구, 동료와 같은 키워드 포함 → 개인일정 DB

트리거가 없는 경우에는 문장 내용을 분석해 가장 적합한 DB를 선택한다.
위의 분류 규칙을 모두 검토해도 분류하기 어려운 경우 "확인 필요"로 설정한다.
