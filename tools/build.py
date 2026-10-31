"""Build index.html (Korean) and en/index.html (English) from tools/page.template.html.

The template carries both languages as lang="ko" / lang="en" twins.
Each output keeps only its own language so search engines index clean pages.
Run: python3 tools/build.py
"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://gmlakd1526-haon.github.io/ashen-crown-site/"
TEMPLATE = (ROOT / "tools/page.template.html").read_text(encoding="utf-8")

META = {
    "ko": {
        "url": BASE,
        "title": "Ashen Crown 에션 크라운 | 수집형 RPG · 외부 시험 참가 모집",
        "description": "Ashen Crown(에션 크라운)은 날아오는 마법까지 막아 내는 실시간 전투, 급습·정예·네임드 몬스터, 레이드와 유물 던전 파밍, 에픽·신화 장비를 갖춘 PC 수집형 RPG입니다. Steam 출시 준비 중, 외부 시험 참가자를 모집합니다.",
        "keywords": "Ashen Crown, 에션 크라운, 애션 크라운, 에센 크라운, 수집형 RPG, 스팀 RPG, 인디 게임, 외부 시험, 베타 테스트",
        "og_title": "Ashen Crown 에션 크라운 | 수집형 RPG",
        "og_description": "날아오는 마법까지 막아 내는 전투, 매번 다른 몬스터, 레이드와 유물 던전, 에픽·신화 장비. 외부 시험 참가자 모집 중.",
        "locale": "ko_KR", "alt_locale": "en_US",
        "ld_description": "날아오는 마법까지 막아 내는 실시간 전투, 다양한 몬스터, 레이드·유물 던전 파밍, 에픽·신화 장비를 갖춘 수집형 RPG.",
        "nav": "메뉴", "dialog": "스크린샷",
    },
    "en": {
        "url": BASE + "en/",
        "title": "Ashen Crown | Free-to-Play Collectible RPG · Playtest Sign-ups Open",
        "description": "Ashen Crown is a free-to-play collectible RPG for PC: real-time battles where you can stop spells mid-air, ambushes, elites and named monsters, raids and relic dungeons, and Epic and Mythic gear. Coming to Steam. Playtest sign-ups are open.",
        "keywords": "Ashen Crown, collectible RPG, gacha RPG, Steam RPG, indie game, free to play, playtest, beta test",
        "og_title": "Ashen Crown | Collectible RPG",
        "og_description": "Block spells mid-air, face ever-changing monsters, farm raids and relic dungeons, and chase Epic and Mythic gear. Playtest sign-ups open.",
        "locale": "en_US", "alt_locale": "ko_KR",
        "ld_description": "A collectible RPG with real-time battles where you can stop spells mid-air, varied monsters, raid and relic-dungeon farming, and Epic and Mythic gear.",
        "nav": "Menu", "dialog": "Screenshot",
    },
}

ALT_EN = {
    "3장 전투 시작 화면": "Chapter 3 battle intro screen",
    "급습 경고가 뜬 전투": "Battle with an ambush warning",
    "네임드 몬스터 전투": "Battle against a named monster",
    "대장간 화면: 대장장이 볼드린, 강화할 동료, 에픽 무기가 끼워진 장비 칸": "Forge screen: Boldrin the smith, companions to upgrade, and an equipped Epic weapon",
    "로비 화면: 안내인 미라와 다음 여정, 요일 던전, 주간 보스, 결전 레이드, 유물 던전, 투기장 메뉴": "Lobby: guide Mira, the next journey, weekday dungeons, weekly boss, raid, relic dungeon and arena",
    "보른 앞에 세운 방벽이 날아온 공격을 받아 내고, 오른쪽 위에 날아오는 기술 목록과 요격·방벽 버튼이 뜬 장면": "A barrier in front of Born absorbs an attack while the top-right panel lists incoming attacks with intercept and barrier buttons",
    "사막 모래 벌레 전투": "Battle against a desert sandworm",
    "소환 화면: 왼쪽에 큰 동료 원화, 오른쪽에 이번 픽업 목록": "Summon screen: featured companion art on the left, rate-up list on the right",
    "수호자 보른이 방패로 공격을 받아 내며 「완벽 방어!」 문구가 뜬 장면": "Guardian Born blocks an attack with his shield and a Perfect Guard! pops up",
    "장비 옵션 예시: 화염 피해 +30% 최대치, 공격력 +10%, 흡혈 +4%p 최대치": "Example affixes: Fire damage +30% (max roll), Attack +10%, Lifesteal +4%p (max roll)",
    "정예 몬스터가 섞인 전투": "Battle with elite monsters",
    "4-1 실제 전투: 방벽이 파티를 지키고, 날아오는 기술을 격추하고, 완벽 방어로 막아 내는 장면": "Stage 4-1 gameplay: a barrier protects the party, incoming attacks are shot down, and a Perfect Guard blocks the last one",
    "장비 등급": "Gear rarities",
}

ASSET = re.compile(r"^(img|video)/")


def build(lang):
    m = META[lang]
    other = "en" if lang == "ko" else "ko"
    soup = BeautifulSoup(TEMPLATE, "html.parser")
    html = soup.html
    html["lang"] = lang
    html["data-lang"] = lang

    for el in soup.find_all(attrs={"lang": other}):
        if el is not html:
            el.decompose()

    head = soup.head
    head.title.string = m["title"]
    def meta(attr, key, value):
        tag = head.find("meta", attrs={attr: key})
        if tag is not None:
            tag["content"] = value
    meta("name", "description", m["description"])
    meta("name", "keywords", m["keywords"])
    meta("name", "robots", "index,follow")
    meta("property", "og:title", m["og_title"])
    meta("property", "og:description", m["og_description"])
    meta("property", "og:url", m["url"])
    meta("property", "og:locale", m["locale"])
    meta("property", "og:locale:alternate", m["alt_locale"])
    head.find("link", rel="canonical")["href"] = m["url"]
    for old in head.find_all("link", rel="alternate"):
        old.decompose()
    canon = head.find("link", rel="canonical")
    for hl, href in (("x-default", BASE), ("en", BASE + "en/"), ("ko", BASE)):
        canon.insert_after(soup.new_tag("link", rel="alternate", hreflang=hl, href=href))

    ld = head.find("script", type="application/ld+json")
    data = json.loads(ld.string)
    data["description"] = m["ld_description"]
    data["url"] = m["url"]
    ld.string = json.dumps(data, ensure_ascii=False)

    soup.find("nav")["aria-label"] = m["nav"]
    soup.find("dialog")["aria-label"] = m["dialog"]

    # language switch: real links between the two pages
    group = soup.find(class_="lang")
    group.clear()
    for code, label, href in (("ko", "한국어", "../" if lang == "en" else "./"), ("en", "EN", "./" if lang == "en" else "en/")):
        a = soup.new_tag("a", href=href, hreflang=code)
        a.string = label
        if code == lang:
            a["aria-current"] = "page"
        group.append(a)

    if lang == "en":
        for el in soup.find_all(alt=True):
            el["alt"] = ALT_EN.get(el["alt"], el["alt"])
        for el in soup.find_all(attrs={"aria-label": True}):
            el["aria-label"] = ALT_EN.get(el["aria-label"], el["aria-label"])
        for attr in ("src", "href", "poster"):
            for el in soup.find_all(attrs={attr: ASSET}):
                el[attr] = "../" + el[attr]

    out = ROOT / ("index.html" if lang == "ko" else "en/index.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text("<!doctype html>\n" + str(soup.html) + "\n", encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


for code in ("ko", "en"):
    build(code)
