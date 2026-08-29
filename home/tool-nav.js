/* STARNAUTS 공통 도구 네비 — 도구 목록은 여기 한 곳에서만 관리.
   · 기존 페이지(.side-sub-nav 보유): 사이드바 도구 목록을 통째 교체(현재 페이지 자동 cur)
   · 신규 self-contained 도구 페이지: 상단 공통 도구 바를 주입 */
(function(){
  // 개별 도구 페이지만 단색 배경(#0d1117) — tool.html(도구 허브)은 우주 배경 유지
  if(location.pathname.split('/').pop()!=='tool.html'){
    var bgStyle=document.createElement('style');
    bgStyle.textContent='body{background:#0d1117!important}#space-bg{display:none!important}';
    document.head.appendChild(bgStyle);
  }
  var TOOLS=[
    {h:'pli-studio.html',      t:'플리채널 스튜디오'},
    {h:'plichannel-planning.html', t:'노바 디렉터'},
    {h:'music-lab.html',       t:'음원 프롬프트 생성'},
    {h:'channel-research.html', t:'채널 딥 리서치'},
    {h:'auto-video.html',      t:'자동영상'},
    {h:'auto-upload.html',     t:'자동 업로드'},
    {h:'translate.html',       t:'번역+SRT'},
    {h:'timestamp.html',       t:'타임스탬프'},
    {h:'metadata.html',        t:'메타데이터'},
    {h:'video-artwork.html',   t:'영상 만들기'},
    {h:'loop-master.html',     t:'루프 마스터'},
    {h:'playlist-maker.html',  t:'플레이리스트 업데이트 메이커'},
    {h:'capcut.html',          t:'캡컷 보내기'},
    {h:'history.html',         t:'내 기록'}
  ];
  var cur=location.pathname.split('/').pop();
  function links(){return TOOLS.map(function(o){return '<a href="'+o.h+'"'+(o.h===cur?' class="cur"':'')+'>'+o.t+'</a>';}).join('');}
  // 공통 breadcrumb 주입(개별 도구만, tool.html 제외) — 콘텐츠 맨 위, 넉넉한 간격으로 통일
  if(cur!=='tool.html'){
    // 상단 헤더 바(topbar) 없는 도구(신규 self-contained)에 동일 헤더 바 주입
    var mainEl=document.querySelector('.main');
    if(mainEl&&!mainEl.querySelector('.topbar')){
      var tb=document.createElement('header');tb.className='topbar';
      tb.innerHTML='<button class="side-toggle" id="sideToggle" aria-label="메뉴"><span></span></button>'
        +'<nav class="topnav" aria-label="상단 메뉴">'
        +'<a href="/">STARNAUTS<span class="tko">스타너츠</span></a>'
        +'<a href="class">CLASS<span class="tko">강의</span></a>'
        +'<a href="tool" class="active">TOOL<span class="tko">도구</span></a>'
        +'<a href="content">CONTENT<span class="tko">콘텐츠</span></a>'
        +'<a href="agency">AGENCY<span class="tko">에이전시</span></a>'
        +'</nav>'
        +'<div class="top-right"><a class="top-cta" href="signup">무료로 시작</a></div>';
      mainEl.insertBefore(tb,mainEl.firstChild);
    }
    var tname=(TOOLS.filter(function(o){return o.h===cur;})[0]||{}).t||'도구';
    var box=document.querySelector('.main main, .wrap')||document.querySelector('.main');
    if(box&&!document.querySelector('.st-crumb')){
      var cb=document.createElement('nav');cb.className='st-crumb';cb.setAttribute('aria-label','위치');
      cb.innerHTML='<a href="/">홈</a><span>/</span><a href="tool">도구</a><span>/</span><b>'+tname+'</b>';
      box.style.paddingTop='30px';box.style.maxWidth='1180px';box.insertBefore(cb,box.firstChild);
      Array.prototype.forEach.call(document.querySelectorAll('.cr-crumb, .crumb, nav[aria-label="위치"]'),function(o){if(o!==cb)o.style.display='none';});
      var cs=document.createElement('style');
      cs.textContent='.st-crumb{display:flex;align-items:center;gap:10px;font-size:12.5px;color:#9aa6bc;padding:0 0 14px;margin:0;flex-wrap:wrap}.st-crumb a{color:#9aa6bc;text-decoration:none}.st-crumb a:hover{color:#e6edf3}.st-crumb b{color:#C6CEDC;font-weight:700}.st-crumb span{color:#566677}';
      document.head.appendChild(cs);
    }
  }
  var subs=document.querySelectorAll('.side-sub-nav');
  if(subs.length){ // 기존 사이드바 페이지 — 목록 통일
    Array.prototype.forEach.call(subs,function(n){n.innerHTML=links();});
    return;
  }
  // 신규 self-contained 도구 — 상단 공통 도구 바 주입
  var st=document.createElement('style');
  st.textContent='#st-bar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:14px;padding:9px 16px;background:rgba(13,17,23,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,255,255,.08);overflow-x:auto;white-space:nowrap;font-family:Pretendard,system-ui,-apple-system,sans-serif}'
    +'#st-bar::-webkit-scrollbar{height:0}'
    +'#st-bar .st-home{color:#4d7cff;font-weight:800;font-size:13px;text-decoration:none;flex-shrink:0}'
    +'#st-bar .st-links{display:flex;gap:4px}'
    +'#st-bar .st-links a{color:#9aa6bc;font-size:13px;text-decoration:none;padding:5px 11px;border-radius:7px;flex-shrink:0}'
    +'#st-bar .st-links a:hover{color:#e6edf3;background:rgba(255,255,255,.05)}'
    +'#st-bar .st-links a.cur{color:#fff;background:rgba(77,124,255,.18)}';
  document.head.appendChild(st);
  var bar=document.createElement('nav');
  bar.id='st-bar';bar.setAttribute('aria-label','도구 바로가기');
  bar.innerHTML='<a class="st-home" href="tool">★ STARNAUTS 도구</a><div class="st-links">'+links()+'</div>';
  // 스킵 링크가 있으면 그 뒤에 넣는다 — 앞에 넣으면 스킵 링크가 첫 탭 스톱을 잃어 무력화된다
  var skip=document.body.querySelector(':scope > a.skip-link');
  document.body.insertBefore(bar,skip?skip.nextSibling:document.body.firstChild);
})();
