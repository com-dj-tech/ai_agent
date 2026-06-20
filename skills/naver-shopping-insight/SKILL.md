---
name: naver-shopping-insight
description: >
  네이버 데이터랩 쇼핑인사이트 API 스킬.
  사용자가 "네이버 쇼핑 트렌드", "쇼핑인사이트", "카테고리별 쇼핑 클릭량",
  "쇼핑 검색 키워드 비교", "네이버 쇼핑에서 어떤 상품이 많이 클릭됐는지",
  "패션/화장품/가전 등 쇼핑 분야 트렌드 분석" 등을 요청하면 반드시 이 스킬을 사용하세요.
  분야별 트렌드와 카테고리 내 키워드별 트렌드 두 가지 모드를 지원합니다.
  기간, 기기·성별·연령 필터를 지원하며 상대적 클릭량 비율(0~100)을 반환합니다.
---

# naver-shopping-insight — 네이버 쇼핑인사이트 트렌드 조회 스킬

네이버 데이터랩 쇼핑인사이트 API를 호출해 분야별 또는 키워드별 쇼핑 클릭 트렌드를 가져옵니다.

---

## 스크립트 위치

```
C:/Users/SBS/.claude/skills/naver-shopping-insight/naver_shopping_insight.py
```

---

## 두 가지 조회 모드

### 1) categories — 분야별 트렌드

여러 쇼핑 카테고리(분야)를 비교합니다.

```powershell
$env:PYTHONIOENCODING="utf-8"
$body = '{"startDate":"yyyy-mm-dd","endDate":"yyyy-mm-dd","timeUnit":"month","category":[{"name":"분야명","param":["카테고리코드"]}]}'
python "C:/Users/SBS/.claude/skills/naver-shopping-insight/naver_shopping_insight.py" categories $body
```

### 2) keywords — 키워드별 트렌드

특정 카테고리 내에서 키워드별 클릭량을 비교합니다.

```powershell
$env:PYTHONIOENCODING="utf-8"
$body = '{"startDate":"yyyy-mm-dd","endDate":"yyyy-mm-dd","timeUnit":"month","category":"카테고리코드","keyword":[{"name":"키워드그룹명","param":["검색어"]}]}'
python "C:/Users/SBS/.claude/skills/naver-shopping-insight/naver_shopping_insight.py" keywords $body
```

---

## 주요 카테고리 코드 (cat_id)

| 코드 | 분야명 |
|------|--------|
| 50000000 | 패션의류 |
| 50000001 | 패션잡화 |
| 50000002 | 화장품/미용 |
| 50000003 | 디지털/가전 |
| 50000004 | 가구/인테리어 |
| 50000005 | 출산/육아 |
| 50000006 | 식품 |
| 50000007 | 스포츠/레저 |
| 50000008 | 생활/건강 |

네이버쇼핑에서 카테고리 선택 후 URL의 `cat_id` 파라미터로 코드를 확인할 수 있습니다.

---

## 파라미터 설명

### categories 모드

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| startDate | Y | 조회 시작일 (2017-08-01 이후) |
| endDate | Y | 조회 종료일 |
| timeUnit | Y | `date` / `week` / `month` |
| category | Y | 분야 배열 (최대 3개): `[{"name": str, "param": [cat_id]}]` |
| device | N | `""` / `"pc"` / `"mo"` |
| gender | N | `""` / `"m"` / `"f"` |
| ages | N | `[]` 또는 `["10","20","30","40","50","60"]` |

### keywords 모드

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| startDate | Y | 조회 시작일 |
| endDate | Y | 조회 종료일 |
| timeUnit | Y | `date` / `week` / `month` |
| category | Y | 단일 카테고리 코드 문자열 |
| keyword | Y | 키워드 배열 (최대 5개): `[{"name": str, "param": ["검색어"]}]` (param은 1개) |
| device | N | 선택 필터 |
| gender | N | 선택 필터 |
| ages | N | 선택 필터 |

---

## 실행 절차 (Claude 사용 시)

1. 사용자 요청에서 분야/키워드·기간·단위를 파악한다.
2. 분야 비교이면 `categories` 모드, 특정 카테고리 내 키워드 비교이면 `keywords` 모드를 선택한다.
3. JSON_BODY를 구성하고 PowerShell에서 **임시 파일 경유**로 실행한다 (한글 인코딩 보장):

```powershell
$env:PYTHONIOENCODING="utf-8"
$json = '{"startDate":"...","endDate":"...","timeUnit":"month","category":"50000000","keyword":[...]}'
$tmp = "$env:TEMP\naver_shopping_body.json"
[System.IO.File]::WriteAllText($tmp, $json, (New-Object System.Text.UTF8Encoding($false)))
python "C:/Users/SBS/.claude/skills/naver-shopping-insight/naver_shopping_insight.py" keywords $tmp
```

4. `ratio` 값(0~100)은 조회 기간 중 가장 높은 클릭량을 100으로 설정한 상대값이다.
5. 결과를 표나 텍스트로 사용자에게 제공한다.

---

## 사용 예시

```powershell
# 패션의류 vs 화장품/미용 분야 비교 (2024년 상반기, 월간)
$body = '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month","category":[{"name":"패션의류","param":["50000000"]},{"name":"화장품/미용","param":["50000002"]}]}'
python "C:/Users/SBS/.claude/skills/naver-shopping-insight/naver_shopping_insight.py" categories $body

# 패션의류 카테고리 내 정장 vs 캐주얼 키워드 비교 (2024년 상반기, 월간)
$body = '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month","category":"50000000","keyword":[{"name":"정장","param":["정장"]},{"name":"캐주얼","param":["캐주얼"]}]}'
python "C:/Users/SBS/.claude/skills/naver-shopping-insight/naver_shopping_insight.py" keywords $body
```

---

## 인증 정보

- Client ID / Secret이 스크립트 내부에 하드코딩되어 있습니다.
- 하루 API 호출 한도: **1,000회**
