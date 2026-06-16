# -*- coding: utf-8 -*-
"""프로필 빌드 시스템: 계정 데이터(ACCOUNTS) + 공통 템플릿 → [file].html
새 계정 = ACCOUNTS에 추가 → 실행하면 엔돌핀과 동일 레이아웃 프로필 자동 생성.
대시보드는 이 데이터를 편집하는 UI."""
import os

base = os.path.dirname(__file__)

# ── 공통 셸: 현재 endolphin.html의 head/sidebar/topbar + footer 재사용 ──
_master = open(os.path.join(base, "endolphin.html"), encoding="utf-8").read()
SEC = '  <section class="section" style="padding-top:36px">'
PRE = _master[:_master.index(SEC)]
POST = _master[_master.index('  <footer class="footer"'):]


def _flags(langs):
    return "".join(f'<img class="sb-flag" src="../assets/flags/{c}.png" alt="{n}" title="{n}">' for c, n in langs)


def _hero(d):
    stats = "".join(f'\n            <span><b>{v}</b> {k}</span>' for v, k in d["stats"])
    plats = "".join(f'\n              <a href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{n}"><img src="../assets/platform/{t}.png" alt="{n}"></a>' for t, n, u in d["platforms"])
    return f'''      <!-- 배너 히어로 -->
      <div class="sb-hero">
        <img class="sb-hero-img" src="../assets/{d['banner']}" alt="{d['name']}">
        <div class="sb-hero-grad"></div>
        <div class="sb-hero-body">
          <div class="sb-badges"><span class="sb-badge">{d['badge']}</span>{_flags(d['langs'])}</div>
          <h1 class="sb-name">{d['name']}</h1>
          <p class="sb-rec">{d['rec']}</p>
          <p class="sb-intro">{d['intro']}</p>
          <div class="sb-stats">{stats}
          </div>
          <div class="sb-acts">
            <a class="sb-btn" href="mailto:{d['booking']}">행사·강의 섭외 문의</a>
            <div class="psoc">
              <span class="nat">{d['nat']}</span>{plats}
            </div>
          </div>
        </div>
      </div>'''


def _event(d):
    if not d.get("event"):
        return ""
    text, url = d["event"]
    return f'''

      <!-- 진행 중인 이벤트 -->
      <a href="{url}" style="display:flex;align-items:center;gap:14px;margin-top:14px;padding:14px 18px;border-radius:14px;border:1px solid rgba(46,111,201,.35);background:rgba(46,111,201,.1);text-decoration:none">
        <span style="font-size:11px;font-weight:800;color:var(--blue-300);background:rgba(46,111,201,.2);padding:4px 10px;border-radius:7px;white-space:nowrap">진행 중인 이벤트</span>
        <span style="flex:1;min-width:0;color:#fff;font-size:14px;font-weight:700">{text}</span>
        <span style="color:var(--blue);font-weight:800;font-size:13px;white-space:nowrap;display:inline-flex;align-items:center;gap:4px">자세히 <svg width="14" height="14"><use href="#i-chev-r"/></svg></span>
      </a>'''


def _board_card(label, slug, posts):
    items = ""
    for notice, title, date in posts:
        badge = '<span class="bi-notice">공지</span>' if notice else ''
        items += f'\n          <a class="board-item" href="{slug}">{badge}<span class="bi-title">{title}</span><span class="bi-date">{date}</span></a>'
    return f'''        <div class="info-card board-card">
          <div class="board-head"><div class="ic-label">{label}</div><a href="{slug}" class="board-more">전체 보기 ›</a></div>{items}
        </div>'''


def _info_grid(d):
    boxes = "".join(f'\n        <div class="info-card"><div class="ic-label">{k}</div><div class="ic-val">{v}</div></div>' for k, v in d["info"])
    sched = _board_card("스케줄", d["schedule_slug"], d["schedule_posts"])
    news = _board_card("뉴스", d["news_slug"], d["news_posts"])
    return f'''      <!-- 업무 안내 박스 -->
      <div class="info-grid" style="margin-top:14px">{boxes}
{sched}
{news}
      </div>'''


def _donut(g):
    circ = ['<circle cx="20" cy="20" r="15.915" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="6"/>']
    leg = []
    off = 0.0
    for k, v, pct, color in g["segs"]:
        circ.append(f'<circle class="seg" cx="20" cy="20" r="15.915" fill="none" stroke="{color}" stroke-width="6" stroke-dasharray="{pct:.2f} {100-pct:.2f}" stroke-dashoffset="{-off:.2f}"/>')
        leg.append(f'<div class="lg"><span class="dot" style="background:{color}"></span><span class="lk">{k}</span><span class="lv">{v}</span></div>')
        off += pct
    return f'''      <div class="stat-box">
        <div class="st-h">{g['title']}</div>
        <div class="donut-wrap">
          <svg class="donut" viewBox="0 0 40 40">{''.join(circ)}</svg>
          <div class="donut-leg">{''.join(leg)}</div>
        </div>
      </div>'''


def _bar(g):
    rows = "".join(f'\n        <div class="bar-row"><span class="bk">{k}</span><span class="bar"><i style="width:{p}%"></i></span><span class="bv">{v}</span></div>' for k, v, p in g["rows"])
    return f'''      <div class="stat-box">
        <div class="st-h">{g['title']}</div>
<div style="margin-top:4px">{rows}
      </div>
      </div>'''


def _num(g):
    items = "".join(f'\n          <div><div class="stat-big">{b}</div><div class="stat-cap">{c}</div></div>' for b, c in g["items"])
    return f'''      <div class="stat-box">
        <div class="st-h">{g['title']}</div>
        <div class="num-wrap">{items}
        </div>
      </div>'''


def _stat_grid(d):
    boxes = []
    for g in d["infographics"]:
        boxes.append({"donut": _donut, "bar": _bar, "num": _num}[g["type"]](g))
    return '      <!-- 성과 인포그래픽 (대시보드 연동) -->\n      <div class="stat-grid">\n' + "\n".join(boxes) + '\n      </div>'


def _class_grid(d):
    cards = ""
    for c in d["classes"]:
        href, img, lvl, hot, tag, price = c[:6]
        title = c[6] if len(c) > 6 else None  # 이미지에 제목 없으면 h3 사용(신재), 있으면 cc-thin(엔돌핀)
        hotspan = f'<span class="cc-hot">{hot}</span>' if hot else ''
        if title:
            overlay = (f'<div class="cc-overlay">\n            <h3>{title}</h3>\n'
                       f'            <div class="cc-foot"><span class="cc-tag">{tag}</span><span class="cc-price">{price}</span></div>\n          </div>')
        else:
            overlay = (f'<div class="cc-overlay cc-thin">\n'
                       f'            <div class="cc-foot"><span class="cc-tag">{tag}</span><span class="cc-price">{price}</span></div>\n          </div>')
        cards += f'''
        <a class="class-card" href="{href}" style="background:url('../assets/class/{img}') center/cover">
          <span class="cc-lvl">{lvl}</span>{hotspan}
          {overlay}
        </a>'''
    return f'''      <!-- 진행 중인 클래스 -->
      <div class="class-grid">{cards}
      </div>'''


def _goods(d):
    g = d["goods"]
    if g[0] == "image":
        _, href, label, banner = g
        return f'''      <!-- 굿즈 스토어 배너 -->
      <a href="{href}" aria-label="{label}" style="display:block;height:100px;border-radius:10px;overflow:hidden;margin-top:16px;text-decoration:none;border:1px solid rgba(232,150,199,.55);background:url('../assets/goods/{banner}') center/cover"></a>'''
    _, href, label, desc = g
    return f'''      <!-- 굿즈 스토어 배너 -->
      <a href="{href}" style="display:flex;align-items:center;gap:14px;height:100px;box-sizing:border-box;border:1px solid rgba(232,150,199,.55);background:linear-gradient(100deg,rgba(46,111,201,.18),rgba(46,111,201,.04));border-radius:10px;padding:0 22px;text-decoration:none;margin-top:16px">
        <span style="width:46px;height:46px;border-radius:13px;background:#2E6FC9;display:flex;align-items:center;justify-content:center;flex-shrink:0;color:#fff"><svg width="24" height="24"><use href="#i-cart"/></svg></span>
        <span style="flex:1"><b style="color:#fff;font-size:15.5px;display:block">{label}</b><span style="color:#9aa6bc;font-size:12.5px">{desc}</span></span>
        <span style="color:var(--blue-300);flex-shrink:0"><svg width="18" height="18"><use href="#i-chev-r"/></svg></span>
      </a>'''


def _videos(d):
    items = ""
    for i, vid in enumerate(d["videos"], 1):
        items += f'\n        <div class="yt-item"><iframe src="https://www.youtube.com/embed/{vid}" title="영상 {i}" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>'
    return f'''      <!-- 최근 영상 -->
      <div class="yt-grid" style="margin-top:16px">{items}
      </div>'''


def build(d):
    pre = PRE.replace("STARNAUTS — 엔돌핀 (소속 스트리머)", f"STARNAUTS — {d['title']}")
    body = "\n".join([
        '      <a href="agency.html" style="display:inline-flex;align-items:center;gap:4px;font-size:13px;color:#9aa6bc;margin-bottom:22px"><svg width="15" height="15"><use href="#i-chev-l"/></svg> 에이전시로 돌아가기</a>\n',
        _hero(d) + _event(d),
        "",
        _info_grid(d),
        "",
        _stat_grid(d),
        "",
        _class_grid(d),
        "",
        _goods(d),
        "",
        _videos(d),
    ])
    section = f'{SEC}\n    <div class="wrap">\n{body}\n    </div>\n  </section>\n\n  '
    return pre + section + POST


# ── 계정 데이터 (대시보드에서 편집하는 항목) ──
ACCOUNTS = {
    "endolphin.html": {
        "name": "엔돌핀", "title": "엔돌핀 (소속 스트리머)", "banner": "banner-endorphin.webp",
        "badge": "스타너츠 파트너 · 강사", "langs": [("kr", "한국어"), ("us", "English")],
        "rec": "2022 아프리카TV BJ대상 · 아프리카TV(현 SOOP) 최단기 보라 파트너 BJ",
        "intro": "보라 · 여캠 · 게임 · 여행 · 버츄얼 등 모든 분야의 콘텐츠 진행<br>엔카데미 등 다양한 스트리머 양성 콘텐츠 경험이 있는 최고의 스트리머 트레이너",
        "stats": [("2,418명", "수강생"), ("★ 4.9", "평균 평점"), ("3개", "진행 강의")],
        "nat": "KR", "booking": "booking@starnauts.com",
        "platforms": [("soop", "SOOP", "https://www.sooplive.com/station/dmsgkdn12"),
                      ("instagram", "Instagram", "https://www.instagram.com/doll0403/"),
                      ("navercafe", "네이버 카페", "https://cafe.naver.com/endolphin0403")],
        "event": ("엔돌핀의 버츄얼 팬미팅 & 토크쇼 · 7/26 (토) 서울", "endorphin/event.html"),
        "info": [("협업 분야", "행사 진행 · 온라인 1:1 코칭 · 브랜드 콜라보 · 광고 등"),
                 ("활동 분야", "보라 · 여캠 · 게임 · 여행 · 버츄얼")],
        "schedule_slug": "endolphin/schedule.html", "news_slug": "endolphin/news.html",
        "schedule_posts": [(1, "7월 정규 방송 시간 변경 안내", "06.16"), (0, "성장 로드맵 4주차 라이브 일정", "06.15"),
                           (0, "첫 송출 가이드 Q&amp;A 안내", "06.13"), (0, "7월 오프라인 팬미팅 일정 공유", "06.10")],
        "news_posts": [(1, "팬미팅 티켓 오픈 일정 안내", "06.15"), (0, "버츄얼 시상식 인기상 수상", "05.20"),
                       (0, "한·일 합동 버츄얼 콘서트 출연", "04.18"), (0, "방송 셋업 인터뷰 게재", "03.12")],
        "infographics": [
            {"type": "donut", "title": "SOOP 팬덤 · 후원", "segs": [("애청자", "57,166", 61.69, "#2E6FC9"), ("팬클럽", "35,230", 38.02, "#4FB2E8"), ("서포터", "272", 0.29, "#A9D6F5")]},
            {"type": "bar", "title": "SOOP 누적 성과", "rows": [("누적 유저", "1,807만", 100), ("누적 방문", "678만", 38), ("누적 UP", "45만", 8)]},
            {"type": "num", "title": "SOOP 방송 활동", "items": [("13,294h", "총 누적 방송 시간"), ("2014년", "방송 시작 (개설)")]},
        ],
        "classes": [("endolphin/soop-setup.html", "c1.webp", "입문", "FREE", "첫 송출까지", "무료"),
                    ("endolphin/encademy-bootcamp.html", "c2.webp", "4주 과정", "HOT", "4주 집중", "★500"),
                    ("endolphin/youtube-editing.html", "c3.webp", "입문", "", "컷편집·썸네일", "★100"),
                    ("endolphin/bora-knowhow.html", "c4.webp", "중급", "", "여캠 운영 노하우", "★100")],
        "goods": ("image", "endolphin/goods.html", "엔돌핀 굿즈 스토어", "goods-banner.webp"),
        "videos": ["jNQXAC9IVRw", "M7lc1UVf-VE", "aqz-KE-bpKQ"],
    },
    "streamer-shinjae.html": {
        "name": "신재", "title": "신재 (소속 스트리머)", "banner": "banner-shinjae.webp",
        "badge": "보컬 · 음원 · 사주 · 강사", "langs": [("kr", "한국어"), ("us", "English")],
        "rec": "현직 보컬 트레이너 · 음원 프로듀서 · 명리(사주) 연구가",
        "intro": "보컬 레슨부터 AI 음원·실음원 제작, 사주 풀이까지 — 한 사람에게 배우는 다재다능 스킬",
        "stats": [("1,640명", "수강생"), ("★ 4.8", "평균 평점"), ("3개", "진행 강의")],
        "nat": "KR", "booking": "booking@starnauts.com",
        "platforms": [("youtube", "YouTube", "https://www.youtube.com/@%EB%85%B8%EB%B8%94%EB%A0%88%EC%8A%A4%EB%A0%88%EC%9D%B4%EB%B8%94_%EC%8B%A0%EC%9E%AC"),
                      ("soop", "SOOP", "https://www.sooplive.com/station/tjdwo918"),
                      ("instagram", "Instagram", "https://www.instagram.com/god_ash94"),
                      ("threads", "Threads", "https://www.threads.com/@god_ash94?xmt=AQG0cXyC_6P9JY0HvElp7PrRgMBgRVhbGOsQG-Dn5Qy8S_I")],
        "event": None,
        "info": [("협업 분야", "행사 진행 · 오프라인 보컬 레슨 · 온라인 1:1 코칭 · 브랜드 콜라보 · 광고 등"),
                 ("활동 분야", "보컬 · 음원 제작 · 명리(사주)")],
        "schedule_slug": "shinjae/schedule.html", "news_slug": "shinjae/news.html",
        "schedule_posts": [(1, "7월 보컬 클래스 시간표 안내", "06.16"), (0, "6월 보컬 클래스 추가 모집", "06.15"),
                           (0, "AI 음원 강의 7월 일정 공개", "06.12"), (0, "작사·작곡 입문반 야간 타임 신설", "06.08")],
        "news_posts": [(1, "신곡 발매 쇼케이스 안내", "06.14"), (0, "태국 가수 신곡 프로듀싱 보도", "05.10"),
                       (0, "AI 음원 강의 화제 — 인터뷰 게재", "04.05"), (0, "사주 콘텐츠 방송 인기", "03.20")],
        "infographics": [
            {"type": "donut", "title": "SOOP 팬덤 · 후원", "segs": [("애청자", "—", 60.0, "#2E6FC9"), ("팬클럽", "—", 40.0, "#4FB2E8")]},
            {"type": "bar", "title": "강의 성과", "rows": [("누적 수강생", "1,640명", 100), ("진행 클래스", "4개", 30), ("평균 평점", "4.8", 96)]},
            {"type": "num", "title": "활동 요약", "items": [("3개", "전문 분야 (보컬·음원·사주)"), ("한·영", "방송 가능 언어")]},
        ],
        "classes": [("shinjae/vocal-training.html", "s1.png", "입문", "HOT", "8회차 · 수강생 176", "★99", "떨지 않는 라이브 보컬 트레이닝"),
                    ("shinjae/ai-music.html", "s2.png", "중급", "", "10회차 · 수강생 112", "★129", "AI 음원에서 실음원 발매까지"),
                    ("shinjae/saju-reading.html", "s3.png", "입문", "NEW", "6회차 · 신규 모집", "★100", "방송에서 바로 쓰는 사주 풀이"),
                    ("shinjae/songwriting.html", "s4.png", "입문", "", "6회차 · 수강생 84", "★89", "작사·작곡 입문 — 첫 곡 만들기")],
        "goods": ("text", "shinjae/goods.html", "신재 굿즈 스토어", "음원·음악 굿즈 등 — 스트리머 직접 판매 (스타너츠 미경유)"),
        "videos": ["jNQXAC9IVRw", "M7lc1UVf-VE", "aqz-KE-bpKQ"],
    },
}

if __name__ == "__main__":
    for fname, data in ACCOUNTS.items():
        open(os.path.join(base, fname), "w", encoding="utf-8").write(build(data))
        print("빌드:", fname)
