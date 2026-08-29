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

/* 로그인 상태 표시 (localStorage 기반 — 추후 Supabase로 대체) */
(function(){
  'use strict';
  var email = null;
  try { email = localStorage.getItem('starnauts_user_email'); } catch(e){}
  var tr = document.querySelector('.top-right');
  if(!tr || !email) return;
  var ini = email.trim().charAt(0).toUpperCase();
  tr.innerHTML =
    '<a href="mypage.html" class="acct" title="'+email+'" style="display:inline-flex;align-items:center;gap:8px;text-decoration:none;color:#fff;font-weight:700;font-size:13px">'
    + '<span style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#2E6FC9,#5B47A8);display:inline-flex;align-items:center;justify-content:center;font-weight:900;font-size:13px;color:#fff">'+ini+'</span>'
    + '<span style="max-width:170px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+email+'</span></a>'
    + '<button type="button" id="snLogout" aria-label="로그아웃" style="background:none;border:1px solid rgba(255,255,255,.18);color:#9aa6bc;border-radius:9px;padding:7px 11px;font-size:12px;cursor:pointer;font-family:inherit;margin-left:8px">로그아웃</button>';
  var lo = document.getElementById('snLogout');
  if(lo) lo.addEventListener('click', function(){ try{localStorage.removeItem('starnauts_user_email');}catch(e){} location.reload(); });
})();
