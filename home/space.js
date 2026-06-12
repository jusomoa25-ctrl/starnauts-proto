/* ============================================================
   STARNAUTS — global space background: starfield + meteors
   ============================================================ */
(function(){
  'use strict';
  const bg = document.getElementById('space-bg');
  if(!bg) return;
  const field = document.getElementById('space-stars') || (function(){
    const d=document.createElement('div'); d.id='space-stars'; bg.appendChild(d); return d;
  })();

  /* dense twinkling starfield */
  (function(){
    const n = 200; let html='';
    for(let i=0;i<n;i++){
      const x=(Math.random()*100).toFixed(2), y=(Math.random()*100).toFixed(2);
      const s=(Math.random()*2.1+0.5).toFixed(2), o=(Math.random()*0.7+0.25).toFixed(2);
      const dur=(Math.random()*4+2.5).toFixed(1), del=(Math.random()*5).toFixed(1);
      const blue = Math.random()>0.82 ? ';background:#bcd4ff' : '';
      html+=`<span style="left:${x}%;top:${y}%;width:${s}px;height:${s}px;opacity:${o};box-shadow:0 0 ${s*2}px rgba(255,255,255,.5);animation-duration:${dur}s;animation-delay:${del}s${blue}"></span>`;
    }
    field.innerHTML = html;
  })();

  /* meteors / falling stars */
  function meteor(){
    const m = document.createElement('span');
    m.className = 'shoot';
    const fromTop = Math.random()*40;          // start in upper area
    const fromLeft = Math.random()*70 + 10;    // x start %
    const len = Math.random()*90 + 90;         // px
    const angle = 24 + Math.random()*8;        // downward-right
    const travel = 320 + Math.random()*260;
    m.style.cssText = `top:${fromTop}%;left:${fromLeft}%;width:${len}px;transform:rotate(${angle}deg)`;
    bg.appendChild(m);
    const rad = angle*Math.PI/180;
    const dx = Math.cos(rad)*travel, dy = Math.sin(rad)*travel;
    m.animate([
      {opacity:0, transform:`rotate(${angle}deg) translate(0,0)`},
      {opacity:1, offset:.12},
      {opacity:0, transform:`rotate(${angle}deg) translate(${dx}px,${dy}px)`}
    ],{duration: 900+Math.random()*500, easing:'cubic-bezier(.4,0,.5,1)'}).onfinish=()=>m.remove();
  }
  // periodic meteors, paused when tab hidden
  setInterval(()=>{ if(!document.hidden && Math.random()>0.35) meteor(); }, 2600);
  setTimeout(meteor, 1200);
})();
