/* ============================================================
   STARNAUTS — sidebar shell: mobile drawer + scrollspy
   ============================================================ */
(function(){
  'use strict';
  const sidebar = document.getElementById('sidebar');
  const toggle  = document.getElementById('sideToggle');
  const scrim   = document.getElementById('sbScrim');

  function open(){ sidebar && sidebar.classList.add('open'); scrim && scrim.classList.add('show'); }
  function close(){ sidebar && sidebar.classList.remove('open'); scrim && scrim.classList.remove('show'); }
  if(toggle) toggle.addEventListener('click', ()=> sidebar.classList.contains('open') ? close() : open());
  if(scrim) scrim.addEventListener('click', close);

  // close drawer after picking a sidebar link (mobile)
  document.querySelectorAll('#sideNav a, .side-logo').forEach(a=>{
    a.addEventListener('click', ()=>{ if(window.innerWidth<=980) close(); });
  });

  // scrollspy — highlight current section in sidebar
  const links = Array.from(document.querySelectorAll('#sideNav a'));
  const map = {};
  links.forEach(a=>{ const id=a.getAttribute('data-sec'); const el=document.getElementById(id); if(el) map[id]=el; });
  const ids = Object.keys(map);
  function spy(){
    const y = window.scrollY + (window.innerHeight*0.32);
    let cur = ids[0];
    for(const id of ids){ if(map[id].offsetTop <= y) cur = id; }
    links.forEach(a=> a.classList.toggle('active', a.getAttribute('data-sec')===cur));
  }
  let tick=false;
  window.addEventListener('scroll', ()=>{ if(!tick){ requestAnimationFrame(()=>{ spy(); tick=false; }); tick=true; } }, {passive:true});
  window.addEventListener('load', spy); spy();
})();

/* 가짜 로그인 상태 표시는 제거했다 (2026-09-01).
   비밀번호를 검증하지 않는 localStorage 로그인을 걷어냈으므로, 그것이 만들던
   계정 칩도 함께 내린다. 실인증이 생기면 그때 서버 세션 기준으로 다시 넣는다.
   남아 있던 옛 값은 한 번 지운다. */
(function(){
  'use strict';
  try { localStorage.removeItem('starnauts_user_email'); } catch(e){}
})();
