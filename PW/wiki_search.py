# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Wikipedia 검색 자동화 스크립트 - Playwright 활용
사용법: python wiki_search.py <검색어>
예시:  python wiki_search.py 인공지능
       python wiki_search.py 블랙홀
"""

import sys
import io
import asyncio

# Windows 콘솔 UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from playwright.async_api import async_playwright


async def search_wikipedia(query: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 1. 위키피디아 포털 접속
        print(f"  [1/4] 위키피디아 접속 중...")
        await page.goto("https://www.wikipedia.org")
        await page.wait_for_load_state("networkidle")

        # 2. 언어를 한국어로 설정 후 검색어 입력
        print(f"  [2/4] 검색어 입력: '{query}'")
        await page.select_option("select", label="한국어")
        await page.fill("input[name='search']", query)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")

        current_url = page.url

        # 3. 검색 결과 목록 페이지인 경우 첫 번째 결과 클릭
        if "Special:Search" in current_url or "특수:검색" in current_url:
            print(f"  [3/4] 검색 결과 목록에서 첫 번째 항목 선택 중...")
            first_result = await page.query_selector(".mw-search-result-heading a")
            if first_result:
                await first_result.click()
                await page.wait_for_load_state("networkidle")
                current_url = page.url
            else:
                await browser.close()
                return {"error": "검색 결과가 없습니다."}
        else:
            print(f"  [3/4] 문서 페이지로 직접 이동됨")

        # 4. 본문 내용 추출
        print(f"  [4/4] 본문 내용 추출 중...")

        title = await page.inner_text("h1#firstHeading, h1.firstHeading")

        paragraphs = await page.evaluate("""() => {
            const content = document.querySelector('#mw-content-text');
            if (!content) return [];
            const paras = content.querySelectorAll('p');
            let results = [];
            for (let p of paras) {
                const text = p.innerText.trim();
                if (text.length > 60) {
                    results.push(text);
                }
                if (results.length >= 3) break;
            }
            return results;
        }""")

        sections = await page.evaluate("""() => {
            const hs = document.querySelectorAll('#mw-content-text h2');
            const skip = ['각주', '외부 링크', '같이 보기', '참고 문헌', '참고문헌'];
            return Array.from(hs)
                .map(h => h.innerText.replace('[편집]', '').trim())
                .filter(t => t && !skip.includes(t))
                .slice(0, 8);
        }""")

        last_edited = await page.evaluate("""() => {
            const el = document.querySelector('#footer-info-lastmod');
            return el ? el.innerText.trim() : '';
        }""")

        await browser.close()

        return {
            "query": query,
            "title": title.strip(),
            "url": current_url,
            "paragraphs": paragraphs,
            "sections": sections,
            "last_edited": last_edited,
        }


def print_result(result: dict):
    if "error" in result:
        print(f"\n오류: {result['error']}")
        return

    div = "=" * 65
    print(f"\n{div}")
    print(f" 검색어    : {result['query']}")
    print(f" 문서 제목 : {result['title']}")
    print(f" URL       : {result['url']}")
    if result["last_edited"]:
        print(f" 최종 편집 : {result['last_edited']}")
    print(div)

    print("\n▶ 요약 (주요 단락)")
    for i, para in enumerate(result["paragraphs"], 1):
        short = para[:450] + ("..." if len(para) > 450 else "")
        print(f"\n  [{i}] {short}")

    if result["sections"]:
        print("\n▶ 주요 섹션 목차")
        for section in result["sections"]:
            print(f"      · {section}")

    print(f"\n{div}\n")


async def main():
    if len(sys.argv) < 2:
        query = input("검색어를 입력하세요: ").strip()
    else:
        query = " ".join(sys.argv[1:]).strip()

    if not query:
        print("검색어를 입력해 주세요.")
        return

    print(f"\n'{query}' 위키피디아 검색 시작...\n")
    result = await search_wikipedia(query)
    print_result(result)


if __name__ == "__main__":
    asyncio.run(main())
