---
name: gh_cli
description: GitHub CLI(gh) 전체 기능을 활용하는 스킬. 리포지토리·이슈·PR·릴리즈·Actions·검색·시크릿·SSH키·GPG키·Gist 등 모든 gh 명령어를 다룹니다. 사용자가 GitHub 관련 작업(리포 생성/삭제, PR 열기/머지, 이슈 관리, 워크플로우 실행, 릴리즈 배포 등)을 요청하면 반드시 이 스킬을 참조하세요.
---

# gh CLI 완전 가이드

GitHub CLI(gh) v2.93.0 기준. 모든 명령어는 PowerShell에서 실행 가능하며, 인증된 계정(`com-dj-tech`)을 기준으로 동작합니다.

---

## 인증 (auth)

```powershell
gh auth login                        # GitHub 로그인
gh auth logout                       # 로그아웃
gh auth status                       # 인증 상태 확인
gh auth switch                       # 활성 계정 전환
gh auth token                        # 현재 토큰 출력
gh auth refresh                      # 토큰 갱신
gh auth setup-git                    # git credential helper 설정
```

---

## 리포지토리 (repo)

```powershell
# 생성 / 클론
gh repo create <name>                # 리포 생성 (대화형)
gh repo create <name> --public       # 공개 리포 생성
gh repo create <name> --private      # 비공개 리포 생성
gh repo create <name> --clone        # 생성 후 바로 클론
gh repo clone <owner>/<repo>         # 리포 클론
gh repo fork <owner>/<repo>          # 리포 포크
gh repo fork <owner>/<repo> --clone  # 포크 후 클론

# 조회 / 수정
gh repo list                         # 내 리포 목록
gh repo list <org>                   # 조직 리포 목록
gh repo view                         # 현재 리포 정보
gh repo view <owner>/<repo>          # 특정 리포 정보
gh repo view --web                   # 브라우저로 열기
gh repo edit --description "설명"    # 리포 설명 수정
gh repo edit --visibility public     # 공개/비공개 전환
gh repo rename <new-name>            # 리포 이름 변경
gh repo sync                         # 포크 동기화

# 삭제 / 아카이브
gh repo delete <owner>/<repo>        # 리포 삭제
gh repo archive                      # 리포 아카이브
gh repo unarchive                    # 아카이브 해제

# 기타
gh repo set-default <owner>/<repo>   # 기본 리포 설정
gh repo gitignore list               # gitignore 템플릿 목록
gh repo license list                 # 라이선스 목록
```

---

## 이슈 (issue)

```powershell
# 생성 / 조회
gh issue create                      # 이슈 생성 (대화형)
gh issue create --title "제목" --body "내용"
gh issue create --label bug --assignee @me
gh issue list                        # 이슈 목록
gh issue list --state closed         # 닫힌 이슈 목록
gh issue list --label "bug"          # 라벨 필터
gh issue view <number>               # 이슈 상세
gh issue view <number> --web         # 브라우저로 열기
gh issue status                      # 내 관련 이슈 현황

# 수정 / 관리
gh issue edit <number> --title "새 제목"
gh issue edit <number> --add-label "enhancement"
gh issue edit <number> --remove-label "bug"
gh issue close <number>              # 이슈 닫기
gh issue reopen <number>             # 이슈 다시 열기
gh issue delete <number>             # 이슈 삭제
gh issue comment <number> --body "댓글 내용"
gh issue transfer <number> <owner>/<repo>  # 이슈 이전
gh issue lock <number>               # 이슈 잠금
gh issue unlock <number>             # 잠금 해제
gh issue pin <number>                # 이슈 고정
gh issue unpin <number>              # 고정 해제
gh issue develop <number>            # 연결 브랜치 관리
```

---

## Pull Request (pr)

```powershell
# 생성 / 조회
gh pr create                         # PR 생성 (대화형)
gh pr create --title "제목" --body "내용" --base main
gh pr create --draft                 # 드래프트 PR
gh pr create --reviewer user1,user2  # 리뷰어 지정
gh pr list                           # PR 목록
gh pr list --state closed            # 닫힌 PR
gh pr list --draft                   # 드래프트 PR
gh pr view <number>                  # PR 상세
gh pr view <number> --web            # 브라우저로 열기
gh pr status                         # 내 PR 현황
gh pr diff <number>                  # PR diff 보기

# 리뷰 / 체크
gh pr review <number> --approve      # PR 승인
gh pr review <number> --request-changes --body "수정 필요"
gh pr review <number> --comment --body "댓글"
gh pr checks <number>                # CI 상태 확인

# 머지 / 관리
gh pr merge <number>                 # PR 머지 (대화형)
gh pr merge <number> --merge         # 일반 머지
gh pr merge <number> --squash        # 스쿼시 머지
gh pr merge <number> --rebase        # 리베이스 머지
gh pr merge <number> --delete-branch # 머지 후 브랜치 삭제
gh pr checkout <number>              # PR 브랜치 체크아웃
gh pr edit <number> --title "새 제목"
gh pr edit <number> --add-reviewer user1
gh pr ready <number>                 # 드래프트 → 리뷰 준비
gh pr close <number>                 # PR 닫기
gh pr reopen <number>                # PR 다시 열기
gh pr revert <number>                # PR 되돌리기
gh pr lock <number>                  # PR 잠금
gh pr unlock <number>                # 잠금 해제
gh pr update-branch <number>         # 브랜치 업데이트
gh pr comment <number> --body "댓글"
```

---

## 릴리즈 (release)

```powershell
# 생성 / 조회
gh release create <tag>              # 릴리즈 생성
gh release create <tag> --title "v1.0" --notes "변경 사항"
gh release create <tag> --draft      # 드래프트 릴리즈
gh release create <tag> --prerelease # 프리릴리즈
gh release create <tag> ./dist/*     # 파일 첨부
gh release list                      # 릴리즈 목록
gh release view <tag>                # 릴리즈 상세

# 수정 / 관리
gh release edit <tag> --title "새 제목"
gh release upload <tag> ./file.zip   # 에셋 업로드
gh release download <tag>            # 에셋 다운로드
gh release download <tag> --pattern "*.zip"
gh release delete <tag>              # 릴리즈 삭제
gh release delete-asset <tag> <asset>

# 검증
gh release verify <tag>              # 어테스테이션 검증
gh release verify-asset <tag> <file>
```

---

## GitHub Actions (workflow / run / cache)

```powershell
# 워크플로우
gh workflow list                     # 워크플로우 목록
gh workflow view <name>              # 워크플로우 상세
gh workflow run <name>               # 워크플로우 실행
gh workflow run <name> --ref main    # 특정 브랜치에서 실행
gh workflow enable <name>            # 워크플로우 활성화
gh workflow disable <name>           # 워크플로우 비활성화

# 실행 결과 (run)
gh run list                          # 최근 실행 목록
gh run view <id>                     # 실행 상세
gh run view <id> --log               # 로그 보기
gh run watch <id>                    # 실행 모니터링
gh run download <id>                 # 아티팩트 다운로드
gh run rerun <id>                    # 재실행
gh run rerun <id> --failed           # 실패한 잡만 재실행
gh run cancel <id>                   # 실행 취소
gh run delete <id>                   # 실행 기록 삭제

# 캐시 (cache)
gh cache list                        # 캐시 목록
gh cache delete <key>                # 캐시 삭제
```

---

## 검색 (search)

```powershell
gh search repos "query"              # 리포 검색
gh search repos "query" --language python
gh search repos "query" --stars ">100"
gh search issues "query"             # 이슈 검색
gh search issues "query" --label bug --state open
gh search prs "query"                # PR 검색
gh search prs "query" --author @me
gh search commits "query"            # 커밋 검색
gh search code "query"               # 코드 검색
```

---

## 시크릿 / 변수 (secret / variable)

```powershell
# 시크릿
gh secret list                       # 시크릿 목록
gh secret set MY_SECRET              # 시크릿 설정 (입력 프롬프트)
gh secret set MY_SECRET --body "value"
gh secret set MY_SECRET < secret.txt # 파일에서 읽기
gh secret delete MY_SECRET           # 시크릿 삭제

# Actions 변수
gh variable list                     # 변수 목록
gh variable set MY_VAR --body "value"
gh variable delete MY_VAR            # 변수 삭제
```

---

## Gist

```powershell
gh gist create file.txt              # Gist 생성
gh gist create file.txt --public     # 공개 Gist
gh gist create file.txt --desc "설명"
gh gist list                         # Gist 목록
gh gist view <id>                    # Gist 보기
gh gist edit <id>                    # Gist 수정
gh gist clone <id>                   # Gist 클론
gh gist delete <id>                  # Gist 삭제
```

---

## SSH키 / GPG키

```powershell
# SSH 키
gh ssh-key list                      # SSH 키 목록
gh ssh-key add ~/.ssh/id_ed25519.pub # SSH 키 추가
gh ssh-key add key.pub --title "My Key"
gh ssh-key delete <id>               # SSH 키 삭제

# GPG 키
gh gpg-key list                      # GPG 키 목록
gh gpg-key add public.gpg            # GPG 키 추가
gh gpg-key delete <id>               # GPG 키 삭제
```

---

## 조직 / 라벨 / 프로젝트

```powershell
# 조직
gh org list                          # 조직 목록

# 라벨
gh label list                        # 라벨 목록
gh label create "bug" --color "#d73a4a" --description "버그"
gh label edit "bug" --name "버그"
gh label delete "bug"                # 라벨 삭제
gh label clone <owner>/<repo>        # 라벨 복사

# 프로젝트
gh project list                      # 프로젝트 목록
gh project view <number>             # 프로젝트 상세
gh project create --title "프로젝트명"
gh project delete <number>           # 프로젝트 삭제
gh project item-list <number>        # 항목 목록
gh project item-add <number> --url <issue-url>
gh project item-edit                 # 항목 수정
gh project item-delete               # 항목 삭제
gh project field-list <number>       # 필드 목록
```

---

## 기타 유용한 명령어

```powershell
# 브라우저 열기
gh browse                            # 현재 리포 열기
gh browse --repo <owner>/<repo>      # 특정 리포 열기
gh browse <number>                   # 이슈/PR 번호로 열기
gh browse --settings                 # 리포 설정 페이지

# 상태 확인
gh status                            # 내 이슈·PR·알림 현황

# API 직접 호출
gh api /user                         # 사용자 정보
gh api /repos/{owner}/{repo}/issues  # API 직접 요청
gh api graphql -f query='...'        # GraphQL 쿼리

# 설정 / 단축키
gh config list                       # 설정 목록
gh config get editor                 # 설정값 조회
gh config set editor nvim            # 설정 변경
gh alias list                        # 단축키 목록
gh alias set pv 'pr view'            # 단축키 설정
gh alias delete pv                   # 단축키 삭제

# 확장
gh extension list                    # 확장 목록
gh extension install <owner>/<repo>  # 확장 설치
gh extension remove <name>           # 확장 제거
gh extension upgrade --all           # 전체 업그레이드
```

---

## 공통 유용 플래그

| 플래그 | 설명 |
|--------|------|
| `--repo <owner>/<repo>` | 대상 리포 지정 |
| `--json <fields>` | JSON 형식 출력 |
| `--jq <expr>` | jq 표현식으로 필터 |
| `--template <tmpl>` | Go 템플릿 출력 |
| `--web` | 브라우저로 열기 |
| `--help` | 명령어 도움말 |
| `--limit <N>` | 결과 수 제한 |

### JSON 출력 예시

```powershell
# PR 목록을 JSON으로 받아 특정 필드만 추출
gh pr list --json number,title,state
gh pr list --json number,title --jq '.[].title'

# 이슈 번호와 제목만 출력
gh issue list --json number,title,labels --jq '.[] | "\(.number): \(.title)"'
```

---

## 자주 쓰는 워크플로우 예시

```powershell
# 1. 새 기능 브랜치 → PR 생성 → 머지
git checkout -b feature/my-feature
git add . && git commit -m "feat: add new feature"
git push origin feature/my-feature
gh pr create --title "feat: add new feature" --base main
gh pr merge --squash --delete-branch

# 2. 이슈 생성 → 브랜치 연결
gh issue create --title "버그 수정" --label bug
gh issue develop <number> --checkout  # 이슈용 브랜치 생성 & 체크아웃

# 3. 릴리즈 배포
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0" --generate-notes ./dist/*

# 4. CI 실패 시 재실행
gh run list --status failure
gh run rerun <id> --failed
```
