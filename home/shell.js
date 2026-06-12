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
