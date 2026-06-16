# -*- coding: utf-8 -*-
"""대시보드 v2: 프로필 1:1 미리보기 + 섹션별 수정 버튼(모달) + 탭(프로필/마이클래스/굿즈).
미리보기는 build_profiles.profile_sections 재사용(실제 프로필과 동일 레이아웃)."""
import os
import build_profiles as bp

base = os.path.dirname(__file__)
d = bp.ACCOUNTS["endolphin.html"]
sec = bp.profile_sections(d)

PRE = bp.PRE.replace("STARNAUTS — 엔돌핀 (소속 스트리머)", "STARNAUTS — 강사 대시보드")

DASH_CSS = """.db-field{margin-bottom:13px}
.db-field label{display:block;font-size:12px;color:#9aa6bc;margin-bottom:6px;font-weight:700}
.db-field input,.db-field select,.db-field textarea{width:100%;padding:10px 12px;border-radius:8px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#fff;font-size:13.5px;font-family:inherit;box-sizing:border-box}
.db-tabs{display:flex;gap:6px;margin:6px 0 20px;border-bottom:1px solid rgba(255,255,255,.1)}
.db-tab{padding:11px 20px;background:none;border:none;color:#9aa6bc;font-weight:800;font-size:14px;cursor:pointer;border-bottom:2px solid transparent;font-family:inherit}
.db-tab.on{color:#fff;border-bottom-color:var(--blue)}
.db-pane{display:none}
.db-pane.on{display:block}
.edit-sec{position:relative}
.edit-sec+.edit-sec{margin-top:2px}
.edit-sec:hover{outline:1px dashed rgba(46,111,201,.55);outline-offset:7px;border-radius:6px}
.edit-btn{position:absolute;top:8px;right:8px;z-index:6;background:var(--blue);color:#fff;border:none;border-radius:7px;padding:6px 12px;font-size:11.5px;font-weight:800;cursor:pointer;opacity:0;transition:.15s;font-family:inherit}
.edit-sec:hover .edit-btn{opacity:1}
.db-modal{position:fixed;inset:0;background:rgba(4,6,10,.7);display:none;align-items:flex-start;justify-content:center;z-index:100;overflow-y:auto;padding:48px 16px}
.db-modal.on{display:flex}
.db-modal-box{background:#0E1116;border:1px solid rgba(255,255,255,.14);border-radius:12px;max-width:580px;width:100%;padding:24px 26px}
.db-modal-box h3{color:#fff;font-size:18px;font-weight:900;margin-bottom:4px}
.db-modal-box .msub{color:#9aa6bc;font-size:12.5px;margin-bottom:18px}
.db-modal-box .mfoot{display:flex;gap:8px;margin-top:18px}
.pl-item{display:flex;align-items:center;gap:9px;padding:8px 10px;border:1px solid rgba(255,255,255,.1);border-radius:8px;margin-bottom:7px;font-size:12.5px;color:#C6CEDC}
.pl-item .pl-dot img{width:20px;height:20px;border-radius:5px;object-fit:cover;display:block}
.pl-item .pl-nm{font-weight:700;color:#fff}.pl-item .pl-url{flex:1;min-width:0;color:#9aa6bc;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pl-item button{margin-left:auto;background:none;border:none;color:#7c8699;cursor:pointer;font-size:15px}
.lang-checks{display:flex;flex-wrap:wrap;gap:8px}
.lang-checks label{display:flex;align-items:center;gap:5px;font-size:12.5px;color:#C6CEDC;cursor:pointer}
.lang-checks img{width:18px;height:18px;border-radius:50%;object-fit:cover}
</style>"""
HEAD = PRE.replace("</style>", DASH_CSS, 1)


def field(label, value="", sub="", typ="text"):
    s = f' <span style="color:#7c8699;font-weight:400">— {sub}</span>' if sub else ""
    return f'<div class="db-field"><label>{label}{s}</label><input type="{typ}" value="{value}"></div>'


def esec(key, label, html, modal=True):
    fn = f"openM('{key}')" if modal else f"goTab('{key}')"
    return f'<div class="edit-sec"><button class="edit-btn" onclick="{fn}">✎ {label}</button>\n{html}</div>'


# ── 프로필 탭: 미리보기 + 섹션 수정 버튼 ──
preview = "\n".join([
    esec("hero", "프로필 수정", sec["hero"]),
    esec("info", "소식·분야 수정", sec["info"]),
    esec("stat", "성과 지표 수정", sec["stat"]),
    esec("class", "마이 클래스에서 편집", sec["classes"], modal=False),
    esec("goods", "굿즈 스토어에서 편집", sec["goods"], modal=False),
    esec("videos", "영상 수정", sec["videos"]),
])

# ── 모달: 데이터로 채운 편집 폼 ──
plats = "".join(f'<div class="pl-item"><span class="pl-dot"><img src="../assets/platform/{t}.png" alt=""></span><span class="pl-nm">{n}</span><span class="pl-url">{u}</span><button onclick="this.parentNode.remove()">×</button></div>' for t, n, u in d["platforms"])
ALL_LANGS = [("kr", "한국어"), ("us", "English"), ("jp", "日本語"), ("cn", "中文"), ("th", "ไทย"), ("vn", "Tiếng Việt"), ("de", "Deutsch"), ("it", "Italiano"), ("es", "Español"), ("pt", "Português"), ("ru", "Русский")]
sel_langs = {c for c, _ in d["langs"]}
langchecks = "".join(f'<label><input type="checkbox"{" checked" if c in sel_langs else ""}><img src="../assets/flags/{c}.png" alt=""> {n}</label>' for c, n in ALL_LANGS)
stats_in = "".join(f'<input type="text" value="{v} {k}" style="flex:1 1 90px;min-width:0">' for v, k in d["stats"])
ev = d["event"][0] if d.get("event") else ""
vids = "".join(f'<input type="text" value="https://youtu.be/{v}" style="margin-bottom:6px">' for v in d["videos"])
name_intro = d.get("intro", "").split("<br>")[0]


def posts_list(posts):
    out = ""
    for notice, title, date in posts:
        b = '<span style="font-size:9.5px;font-weight:800;color:#fff;background:#D64545;padding:2px 6px;border-radius:3px;flex-shrink:0">공지</span>' if notice else ''
        out += f'<div class="pl-item">{b}<span class="pl-url" style="flex:1;color:#fff">{title}</span><span style="color:#7c8699;font-size:12px">{date}</span><button onclick="this.parentNode.remove()">×</button></div>'
    return out


MODALS = f'''
<div class="db-modal" id="m-hero"><div class="db-modal-box">
  <h3>프로필 (히어로) 수정</h3><p class="msub">배너 위에 노출되는 기본 정보입니다.</p>
  <div class="db-field"><label>프로필 사진 · 배너 이미지</label><div style="display:flex;gap:10px;align-items:center">
    <span style="width:44px;height:44px;border-radius:50%;background:#B85C9E;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;flex-shrink:0">엔</span>
    <span style="width:90px;height:34px;border-radius:6px;background:#0E1116 url('../assets/{d['banner']}') center/cover;flex-shrink:0;border:1px solid rgba(255,255,255,.15)"></span>
    <input type="file" accept="image/*" style="flex:1"></div></div>
  {field("배지 · 직함", d["badge"])}
  {field("이름", d["name"])}
  {field("한 줄 소개", name_intro)}
  {field("한 줄 이력", d["rec"])}
  <div class="db-field"><label>대표 통계 3</label><div style="display:flex;gap:8px;flex-wrap:wrap">{stats_in}</div></div>
  {field("국적", d["nat"])}
  <div class="db-field"><label>플랫폼 링크</label>{plats}</div>
  <div class="db-field"><label>구사 언어</label><div class="lang-checks">{langchecks}</div></div>
  {field("섭외 문의 이메일", d["booking"], typ="email")}
  {field("진행 중인 이벤트", ev, sub="비우면 미노출")}
  <div class="mfoot"><a class="btn btn--ghost" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">취소</a><a class="btn btn--primary" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">저장</a></div>
</div></div>

<div class="db-modal" id="m-info"><div class="db-modal-box">
  <h3>소식 · 분야 수정</h3><p class="msub">협업·활동 분야를 설정합니다.</p>
  {field("협업 분야", d["info"][0][1])}
  {field("활동 분야", d["info"][1][1])}
  <div style="border:1px solid rgba(46,111,201,.35);background:rgba(46,111,201,.08);border-radius:8px;padding:13px 15px;font-size:12.5px;color:#C6CEDC;line-height:1.6">스케줄·뉴스 글은 작성하면 <b style="color:#fff">최신순으로 자동 노출</b>됩니다. 특정 글을 위에 고정하려면 <b style="color:#fff">게시판에서 글 작성 시 ‘공지’를 체크</b>하세요.
    <div style="display:flex;gap:8px;margin-top:11px"><a class="btn btn--ghost" href="schedule-board.html" style="flex:1;justify-content:center;display:flex">스케줄 게시판</a><a class="btn btn--ghost" href="news-board.html" style="flex:1;justify-content:center;display:flex">뉴스 게시판</a></div>
  </div>
  <div class="mfoot"><a class="btn btn--ghost" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">취소</a><a class="btn btn--primary" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">저장</a></div>
</div></div>

<div class="db-modal" id="m-stat"><div class="db-modal-box">
  <h3>성과 지표 수정</h3><p class="msub">박스 위치별 표시 형식(도넛/막대/숫자)과 값.</p>
  {"".join(f'<div class="db-field"><label>{g["title"]} <span style=\"color:#7c8699;font-weight:400\">— {g["type"]}</span></label><input type="text" value="{g["title"]}"></div>' for g in d["infographics"])}
  <div class="mfoot"><a class="btn btn--ghost" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">취소</a><a class="btn btn--primary" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">저장</a></div>
</div></div>

<div class="db-modal" id="m-videos"><div class="db-modal-box">
  <h3>최근 영상 수정</h3><p class="msub">프로필 하단에 노출되는 유튜브 3개.</p>
  <div class="db-field"><label>유튜브 링크 (3개)</label>{vids}</div>
  <div class="mfoot"><a class="btn btn--ghost" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">취소</a><a class="btn btn--primary" href="#" onclick="closeM();return false" style="flex:1;justify-content:center;display:flex">저장</a></div>
</div></div>'''

# ── 마이 클래스 탭 ──
class_rows = "".join(f'<div class="pl-item"><span class="pl-url" style="flex:1;color:#fff">{(c[6] if len(c)>6 else c[4])}</span><span style="color:var(--blue-300);font-weight:700">{c[5]}</span><button onclick="this.parentNode.remove()">×</button></div>' for c in d["classes"])
CLASS_PANE = f'''      <div class="db-pane" data-pane="class">
        <p style="color:#9aa6bc;font-size:13.5px;margin-bottom:14px">진행 중인 강의를 관리하고 새 강의를 등록합니다. 등록 = 심사 후 게시.</p>
        <div class="db-field"><label>내 강의</label>{class_rows}</div>
        <div style="border-top:1px dashed rgba(255,255,255,.15);margin:16px 0 14px"></div>
        <p style="font-size:13px;font-weight:800;color:#fff;margin-bottom:10px">새 강의 등록</p>
        {field("유튜브 비공개(unlisted) 링크", "", "https://youtu.be/...")}
        <div class="db-field"><label>판매 유형 · 가격(스타)</label><div style="display:flex;gap:8px"><select style="flex:1"><option>강의 구매 (영구)</option><option>콘텐츠 구독</option></select><input type="number" placeholder="99" style="width:90px"></div></div>
        <div class="db-field"><label>카테고리</label><select><option>스트리밍</option><option>편집</option><option>보컬·댄스</option><option>음원 제작</option><option>콘텐츠 스킬</option><option>지식·재능</option></select></div>
        <div class="db-field"><label>수익 분배 <span style="color:#7c8699;font-weight:400">— 국내 / 해외(스타너츠 더빙 제작 시)</span></label>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <div style="flex:1 1 130px"><span style="font-size:11px;color:#7c8699">국내 (강사/스타너츠)</span><input type="text" value="{d['revenue']['domestic']}" readonly style="width:100%;opacity:.75;margin-top:4px"></div>
            <div style="flex:1 1 150px"><span style="font-size:11px;color:#7c8699">해외 (강사/스타너츠)</span><select style="width:100%;margin-top:4px;padding:9px 10px;border-radius:8px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#fff;font-size:12.5px"><option>{d['revenue']['overseas_dub']} — 스타너츠 더빙 제작</option><option>70 / 30 — 직접 자막</option></select></div>
          </div>
          <p style="font-size:11.5px;color:#7c8699;margin-top:6px">스타너츠가 외국어 더빙·자막을 제작한 강의는 해외 시청 수익을 5:5로 분배합니다.</p>
        </div>
        <a class="btn btn--primary" href="#" style="width:100%;justify-content:center;display:flex">등록 신청 (심사 후 게시)</a>
      </div>'''

# ── 굿즈 스토어 탭 ──
_GSEC = "font-size:13px;font-weight:800;color:#fff;margin:18px 0 11px"
_INP = "padding:10px 12px;border-radius:8px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#fff;font-family:inherit;font-size:13.5px"
_ORD = "border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:12px 14px;margin-bottom:8px;font-size:13px"
_GUIDE = "border:1px solid rgba(255,255,255,.1);border-radius:8px;margin-bottom:13px"
GOODS_PANE = f'''      <div class="db-pane" data-pane="goods">
        <p style="color:#9aa6bc;font-size:13.5px;margin-bottom:8px">굿즈는 <b style="color:#F4C969">스타너츠 미경유 100% 직접 결제</b>입니다. 스타너츠는 진열·주문(주소) 정리·결제 자동확인만 제공하고 수수료는 받지 않습니다 — <b style="color:#fff">개인 쇼핑몰처럼</b> 운영하세요.</p>

        <p style="{_GSEC}">내 굿즈</p>
        <div id="goodsList">
          <div class="pl-item"><span class="pl-dot"><img src="../assets/goods/tshirt.webp" alt=""></span><span class="pl-nm">티셔츠</span><span class="pl-url">엔돌핀 굿즈 티셔츠 (S/M/L/XL)</span><span style="color:#fff;font-weight:700">65,000원</span><button onclick="this.parentNode.remove()">×</button></div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px">
          <input type="text" placeholder="굿즈 이름" style="flex:1 1 140px;min-width:0;{_INP}">
          <input type="number" placeholder="가격(원)" style="flex:0 1 110px;{_INP}">
          <input type="file" accept="image/*" style="flex:1 1 120px;min-width:0;font-size:12px;color:#9aa6bc">
          <a class="btn btn--ghost" href="#" style="white-space:nowrap">＋ 추가</a>
        </div>

        <div style="border-top:1px dashed rgba(255,255,255,.15);margin:20px 0 0"></div>
        <p style="{_GSEC}">결제 연동 — 주문 시 자동 확인</p>
        <div class="db-field"><label>판매 국가</label><select><option>한국</option><option>일본</option><option>태국</option><option>미국·해외</option></select></div>
        <div class="db-field"><label>네이버페이 API 키 <span style="color:#7c8699;font-weight:400">— 한국 · 등록 시 결제·주문 자동 확인</span></label><input type="password" placeholder="네이버페이 가맹점 API 키 붙여넣기"></div>
        <details style="{_GUIDE}"><summary style="padding:11px 14px;cursor:pointer;font-size:12.5px;color:var(--blue-300);font-weight:700;list-style:none">＋ 네이버페이 API 발급 방법</summary><ol style="padding:0 16px 14px 34px;margin:0;font-size:12.5px;color:#9aa6bc;line-height:1.7"><li>네이버페이 가맹점 센터(admin.pay.naver.com) 가입</li><li>가맹점 등록 후 심사 완료</li><li>‘개발 관리 &gt; 결제·API 관리’에서 API 키(Client ID·Secret) 발급</li><li>발급된 키를 위 칸에 붙여넣기 → 주문·결제가 자동으로 확인됩니다</li></ol></details>
        <div class="db-field"><label>해외 결제 API <span style="color:#7c8699;font-weight:400">— 해외 판매 시 (PayPal / Stripe 등 국가별)</span></label><input type="password" placeholder="PayPal Client ID 또는 Stripe Secret Key"></div>
        <details style="{_GUIDE}"><summary style="padding:11px 14px;cursor:pointer;font-size:12.5px;color:var(--blue-300);font-weight:700;list-style:none">＋ 해외 결제 API 발급 방법</summary><ol style="padding:0 16px 14px 34px;margin:0;font-size:12.5px;color:#9aa6bc;line-height:1.7"><li>PayPal: developer.paypal.com → 앱 생성 → Client ID·Secret 발급</li><li>Stripe: dashboard.stripe.com → 개발자 → API 키</li><li>판매 국가에 맞는 키를 등록하면 해당 결제가 자동 확인됩니다</li></ol></details>
        <div class="db-field"><label>입금 계좌 <span style="color:#7c8699;font-weight:400">— 계좌이체 · 입금은 아래에서 수동 확인</span></label><input type="text" value="카카오뱅크 0000-00-0000000 (예금주 엔돌핀)"></div>

        <div style="border-top:1px dashed rgba(255,255,255,.15);margin:20px 0 0"></div>
        <p style="{_GSEC}">주문 관리</p>
        <div style="{_ORD}">
          <div>＊<b>06.17</b> · 엔돌핀 굿즈 티셔츠 (M) ×1</div>
          <div style="color:#9aa6bc;font-size:12px;margin-top:5px">홍길동 · 010-1234-5678 · 서울시 강남구 ○○로 12, 101동 502호 (06234)</div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px"><span style="color:#fff;font-weight:700">68,000원</span><span style="font-size:11.5px;font-weight:700;padding:3px 9px;border-radius:5px;background:rgba(46,158,91,.18);color:#5BC98A">네이버페이 결제완료 ✓ 자동</span></div>
        </div>
        <div style="{_ORD}">
          <div>＊<b>06.16</b> · 엔돌핀 굿즈 티셔츠 (L) ×1</div>
          <div style="color:#9aa6bc;font-size:12px;margin-top:5px">김민지 · 010-9876-5432 · 부산시 해운대구 ○○대로 88, 303호 (48095)</div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px"><span style="color:#fff;font-weight:700">68,000원</span><label style="display:flex;align-items:center;gap:5px;font-size:12px;color:#C6CEDC;cursor:pointer"><input type="checkbox"> 계좌이체 입금확인 (수동)</label></div>
        </div>
        <a class="btn btn--ghost" href="#" style="display:inline-flex;margin-top:6px">⤓ 주소·주문 내역 엑셀(.xlsx) 다운로드</a>

        <div style="border-top:1px dashed rgba(255,255,255,.15);margin:20px 0 14px"></div>
        <a class="btn btn--ghost" href="endolphin/goods.html" target="_blank" style="display:inline-flex">굿즈 페이지 미리보기 ›</a>
      </div>'''

BODY = f'''  <section class="section" style="padding-top:36px">
    <div class="wrap">
      <h1 style="font-size:26px;font-weight:900">강사 대시보드</h1>
      <p style="color:#9aa6bc;font-size:13.5px;margin-top:6px">실제 공개 화면을 그대로 보면서, 각 영역의 <b style="color:#fff">수정</b> 버튼으로 편집하세요. 저장 = 즉시 공개 반영.</p>
      <div class="db-tabs">
        <button class="db-tab on" onclick="goTab('profile')">프로필</button>
        <button class="db-tab" onclick="goTab('class')">마이 클래스</button>
        <button class="db-tab" onclick="goTab('goods')">굿즈 스토어</button>
      </div>
      <div class="db-pane on" data-pane="profile">
{preview}
      </div>
{CLASS_PANE}
{GOODS_PANE}
    </div>
  </section>

  '''

JS = '''
<script>
function goTab(t){
  document.querySelectorAll('.db-pane').forEach(p=>p.classList.toggle('on',p.dataset.pane===t));
  document.querySelectorAll('.db-tab').forEach((b,i)=>b.classList.toggle('on',['profile','class','goods'][i]===t));
  window.scrollTo(0,0);
}
function openM(k){document.getElementById('m-'+k).classList.add('on');document.body.style.overflow='hidden';}
function closeM(){document.querySelectorAll('.db-modal').forEach(m=>m.classList.remove('on'));document.body.style.overflow='';}
document.querySelectorAll('.db-modal').forEach(m=>m.addEventListener('click',e=>{if(e.target===m)closeM();}));
</script>
'''

html = HEAD + BODY + bp.POST.replace("</body>", MODALS + JS + "\n</body>")
open(os.path.join(base, "dashboard.html"), "w", encoding="utf-8").write(html)
print("대시보드 v2: 탭 + 프로필 미리보기 + 섹션 수정 버튼(모달) + 마이클래스/굿즈 탭")
