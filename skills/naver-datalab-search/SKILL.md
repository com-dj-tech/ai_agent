---
name: naver-datalab-search
description: >
  네이버 데이터랩 통합 검색어 트렌드 API 스킬.
  사용자가 "네이버 검색 트렌드", "검색어 추이", "네이버 데이터랩", "키워드 검색량 비교",
  "특정 단어가 네이버에서 얼마나 많이 검색됐는지", "검색 트렌드 분석" 등을 요청하면 반드시 이 스킬을 사용하세요.
  기간, 키워드 그룹(최대 5개, 그룹당 최대 20개 검색어), 기기·성별·연령 필터를 지원합니다.
  일간/주간/월간 단위로 상대적 검색량 비율(0~100)을 반환합니다.
---

# naver-datalab-search — 네이버 검색어 트렌드 조회 스킬

네이버 데이터랩 통합 검색어 트렌드 API를 호출해 키워드별 검색 추이 데이터를 가져옵니다.

---

## 스크립트 위치

```
C:/Users/SBS/.claude/skills/naver-datalab-search/naver_datalab_search.py
```

---

## 사용법

### 기본 실행 (데모)

```powershell
$env:PYTHONIOENCODING="utf-8"; python "C:/Users/SBS/.claude/skills/naver-datalab-search/naver_datalab_search.py"
```

### CLI 호출 (JSON 인자)

```powershell
$env:PYTHONIOENCODING="utf-8"; python "C:/Users/SBS/.claude/skills/naver-datalab-search/naver_datalab_search.py" '<JSON_BODY>'
```

JSON_BODY 구조:

```json
{
  "startDate": "yyyy-mm-dd",
  "endDate":   "yyyy-mm-dd",
  "timeUnit":  "date 또는 week 또는 month",
  "keywordGroups": [
    { "groupName": "그룹이름1", "keywords": ["검색어A", "검색어B"] },
    { "groupName": "그룹이름2", "keywords": ["검색어C"] }
  ],
  "device": "",
  "gender": "",
  "ages": []
}
```

---

## 파라미터 설명

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| startDate | Y | 조회 시작일 (2016-01-01 이후) |
| endDate | Y | 조회 종료일 |
| timeUnit | Y | `date`(일간) / `week`(주간) / `month`(월간) |
| keywordGroups | Y | 키워드 그룹 배열, 최대 5그룹 / 그룹당 최대 20개 검색어 |
| device | N | `""` 전체 / `"pc"` / `"mo"` 모바일 |
| gender | N | `""` 전체 / `"m"` 남성 / `"f"` 여성 |
| ages | N | `[]` 전체 / `["1"~"11"]` (1=0~12세 … 11=60세 이상) |

---

## 실행 절차 (Claude 사용 시)

1. 사용자 요청에서 키워드·기간·단위를 파악한다.
2. JSON_BODY를 구성한다.
3. PowerShell에서 **임시 파일 경유**로 실행한다 (한글 인코딩 보장):

```powershell
$env:PYTHONIOENCODING="utf-8"
$json = '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month","keywordGroups":[{"groupName":"키워드명","keywords":["검색어1","검색어2"]}]}'
$tmp = "$env:TEMP\naver_search_body.json"
[System.IO.File]::WriteAllText($tmp, $json, (New-Object System.Text.UTF8Encoding($false)))
python "C:/Users/SBS/.claude/skills/naver-datalab-search/naver_datalab_search.py" $tmp
```

4. 결과의 `ratio` 값(0~100)은 조회 기간 중 가장 높은 검색량을 100으로 설정한 상대값이다.
5. 결과를 표나 그래프 설명으로 사용자에게 제공한다.

---

## 응답 구조

```json
{
  "startDate": "...",
  "endDate": "...",
  "timeUnit": "month",
  "results": [
    {
      "title": "그룹명",
      "keywords": ["검색어1", "검색어2"],
      "data": [
        { "period": "2024-01-01", "ratio": 49.41 },
        { "period": "2024-02-01", "ratio": 44.18 }
      ]
    }
  ]
}
```

---

## 인증 정보

- Client ID / Secret이 스크립트 내부에 하드코딩되어 있습니다.
- 하루 API 호출 한도: **1,000회**

---

## 사용 예시

```powershell
# 인공지능 vs 머신러닝 검색 트렌드 (2024년 상반기, 월간)
$body = '{"startDate":"2024-01-01","endDate":"2024-06-30","timeUnit":"month","keywordGroups":[{"groupName":"인공지능","keywords":["인공지능","AI","ChatGPT"]},{"groupName":"머신러닝","keywords":["머신러닝","딥러닝"]}]}'
python "C:/Users/SBS/.claude/skills/naver-datalab-search/naver_datalab_search.py" $body
```
