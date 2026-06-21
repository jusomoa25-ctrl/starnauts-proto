/* ============================================================
   STARNAUTS — homepage interactions
   ============================================================ */
(function(){
  'use strict';
  const $  = (s,c)=> (c||document).querySelector(s);
  const $$ = (s,c)=> Array.from((c||document).querySelectorAll(s));
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Starfield ---------- */
  (function stars(){
    const host = $('#stars'); if(!host) return;
    const n = 120; let html='';
    for(let i=0;i<n;i++){
      const x=Math.random()*100, y=Math.random()*100;
      const s=Math.random()*2+0.6, o=Math.random()*0.7+0.25;
      const tw=(Math.random()*3+2).toFixed(1), d=(Math.random()*4).toFixed(1);
      html+=`<span style="position:absolute;left:${x}%;top:${y}%;width:${s}px;height:${s}px;border-radius:50%;background:#fff;opacity:${o};box-shadow:0 0 ${s*2}px rgba(255,255,255,.6);animation:tw ${tw}s ease-in-out ${d}s infinite"></span>`;
    }
    host.innerHTML = html;
    if(!document.getElementById('tw-kf')){
      const st=document.createElement('style'); st.id='tw-kf';
      st.textContent='@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}';
      document.head.appendChild(st);
    }
  })();

  /* ---------- Mobile menu ---------- */
  (function menu(){
    const b=$('#burger'), m=$('#mobileMenu'); if(!b||!m) return;
    const items=[['에이전트','#agent'],['강의','#courses'],['도구','#tool'],['콘텐츠','#streamers']];
    m.innerHTML=`<div class="mm-panel">
      <div class="mm-links">${items.map(i=>`<a href="${i[1]}">${i[0]}</a>`).join('')}</div>
      <div class="mm-cta"><a class="btn btn--ghost btn--block" href="#">로그인</a><a class="btn btn--primary btn--block" href="#">무료로 시작</a></div>
    </div>`;
    const css=document.createElement('style');
    css.textContent=`
      .mobile-menu{position:fixed;inset:0;z-index:100;background:rgba(14,17,22,.5);backdrop-filter:blur(4px);opacity:0;pointer-events:none;transition:opacity .25s}
      .mobile-menu.open{opacity:1;pointer-events:auto}
      .mm-panel{position:absolute;top:0;right:0;bottom:0;width:min(82vw,340px);background:#fff;padding:84px 22px 28px;display:flex;flex-direction:column;gap:24px;transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1)}
      .mobile-menu.open .mm-panel{transform:none}
      .mm-links{display:flex;flex-direction:column}
      .mm-links a{padding:15px 6px;font-size:18px;font-weight:700;border-bottom:1px solid var(--line)}
      .mm-cta{display:flex;flex-direction:column;gap:10px;margin-top:auto}`;
    document.head.appendChild(css);
    const open=()=>m.classList.add('open');
    const close=()=>m.classList.remove('open');
    b.addEventListener('click',open);
    m.addEventListener('click',e=>{ if(e.target===m||e.target.tagName==='A') close(); });
  })();

  /* ---------- Course tabs ---------- */
  (function tabs(){
    const wrap=$('#courseTabs'), grid=$('#courseGrid'); if(!wrap||!grid) return;
    const cards=$$('.course',grid);
    const tabsList=$$('.tab',wrap);
    function activate(t){
      tabsList.forEach(x=>{ x.classList.remove('is-active'); x.setAttribute('aria-selected','false'); });
      t.classList.add('is-active'); t.setAttribute('aria-selected','true');
      const cat=t.dataset.cat;
      cards.forEach(c=>{
        const show = cat==='all' || c.dataset.cat===cat;
        c.style.display = show ? '' : 'none';
        if(show){ c.style.animation='none'; void c.offsetWidth; c.style.animation='fadeUp .4s ease'; }
      });
    }
    wrap.addEventListener('click',e=>{
      const t=e.target.closest('.tab'); if(!t) return;
      activate(t);
    });
    // arrow-key navigation between tabs (WAI-ARIA tablist pattern)
    wrap.addEventListener('keydown',e=>{
      if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft') return;
      const i=tabsList.indexOf(document.activeElement); if(i<0) return;
      e.preventDefault();
      const next=e.key==='ArrowRight' ? (i+1)%tabsList.length : (i-1+tabsList.length)%tabsList.length;
      tabsList[next].focus(); activate(tabsList[next]);
    });
    if(!document.getElementById('fu-kf')){
      const st=document.createElement('style'); st.id='fu-kf';
      st.textContent='@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}';
      document.head.appendChild(st);
    }
  })();

  /* ---------- Suno prompt generator ---------- */
  (function suno(){
    const out=$('#promptOut'); if(!out) return;
    const moodMap={dreamy:'dreamy, ethereal',energetic:'energetic, upbeat',calm:'calm, mellow',epic:'epic, cinematic'};
    const state={genre:'Lo-fi',mood:'dreamy',bpm:'90',kw:''};
    function render(){
      const extra = state.kw.trim() ? `, ${state.kw.trim()}` : '';
      out.innerHTML =
        `<span class="hl">${state.genre}</span> background music, ${moodMap[state.mood]}, `+
        `<span class="hl">${state.bpm} BPM</span>, smooth instrumental for live streaming`+
        `${extra}, no vocals, loopable, copyright-safe`;
    }
    $$('.chiprow').forEach(row=>{
      const group=row.dataset.group;
      row.addEventListener('click',e=>{
        const c=e.target.closest('.chip'); if(!c) return;
        $$('.chip',row).forEach(x=>x.classList.remove('on'));
        c.classList.add('on');
        state[group]=c.dataset.val;
        render();
      });
    });
    const bpm=$('#bpm'), bpmVal=$('#bpmVal');
    if(bpm) bpm.addEventListener('input',()=>{ state.bpm=bpm.value; bpmVal.textContent=bpm.value; render(); });
    const kw=$('#kw'); if(kw) kw.addEventListener('input',()=>{ state.kw=kw.value; render(); });
    const copy=$('#copyBtn');
    if(copy) copy.addEventListener('click',()=>{
      const txt=out.textContent;
      const done=()=>{ const o=copy.textContent; copy.textContent='복사됨 ✓'; setTimeout(()=>copy.textContent=o,1400); };
      if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(txt).then(done).catch(done); }
      else done();
    });
    render();
  })();

  /* ---------- Generic carousel (streamers) ---------- */
  (function carousel(){
    const track=$('#sTrack'); if(!track) return;
    const vp=track.parentElement;
    const cards=$$('.scard',track);
    const prev=$('#sPrev'), next=$('#sNext'), dotsHost=$('#sDots');
    let index=0;
    function perView(){ const w=window.innerWidth; return w<=680?1:w<=980?2:w<=1180?3:4; }
    function maxIndex(){ return Math.max(0, cards.length-perView()); }
    function step(){
      const gap=parseFloat(getComputedStyle(track).gap)||20;
      return cards[0].getBoundingClientRect().width+gap;
    }
    function buildDots(){
      if(!dotsHost) return; dotsHost.innerHTML='';
      for(let i=0;i<=maxIndex();i++){
        const b=document.createElement('button');
        if(i===index) b.classList.add('on');
        b.addEventListener('click',()=>{ index=i; update(); });
        dotsHost.appendChild(b);
      }
    }
    function update(){
      index=Math.min(index,maxIndex());
      track.style.transform=`translateX(${-index*step()}px)`;
      if(prev) prev.disabled=index<=0;
      if(next) next.disabled=index>=maxIndex();
      if(dotsHost) $$('button',dotsHost).forEach((d,i)=>d.classList.toggle('on',i===index));
    }
    if(prev) prev.addEventListener('click',()=>{ index=Math.max(0,index-1); update(); });
    if(next) next.addEventListener('click',()=>{ index=Math.min(maxIndex(),index+1); update(); });
    let rt; window.addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(()=>{ buildDots(); update(); },150); });
    buildDots(); update();
  })();

  /* ---------- Testimonials slider ---------- */
  (function testi(){
    const track=$('#tTrack'); if(!track) return;
    const slides=$$('.tslide',track);
    const prev=$('#tPrev'), next=$('#tNext'), dotsHost=$('#tDots');
    let index=0, timer;
    function buildDots(){
      dotsHost.innerHTML='';
      slides.forEach((_,i)=>{
        const b=document.createElement('button');
        if(i===0) b.classList.add('on');
        b.addEventListener('click',()=>{ index=i; update(); reset(); });
        dotsHost.appendChild(b);
      });
    }
    function update(){
      track.style.transform=`translateX(${-index*100}%)`;
      $$('button',dotsHost).forEach((d,i)=>d.classList.toggle('on',i===index));
    }
    function go(d){ index=(index+d+slides.length)%slides.length; update(); }
    function reset(){ clearInterval(timer); if(!reduceMotion) timer=setInterval(()=>go(1),6000); }
    if(prev) prev.addEventListener('click',()=>{ go(-1); reset(); });
    if(next) next.addEventListener('click',()=>{ go(1); reset(); });
    // L4) pause auto-advance on hover/focus, resume on leave/blur
    const region=track.closest('.review-panel')||track;
    region.addEventListener('mouseenter',()=>clearInterval(timer));
    region.addEventListener('mouseleave',reset);
    region.addEventListener('focusin',()=>clearInterval(timer));
    region.addEventListener('focusout',reset);
    buildDots(); update(); reset();
  })();

  /* ---------- Shooting stars in hero ---------- */
  (function shooters(){
    const host=$('#stars'); if(!host || reduceMotion) return;
    function shoot(){
      const s=document.createElement('span');
      s.className='shooter';
      const top=Math.random()*45, left=Math.random()*60;
      s.style.cssText=`top:${top}%;left:${left}%;transform:rotate(18deg)`;
      host.appendChild(s);
      s.animate([
        {opacity:0,transform:'rotate(18deg) translateX(0)'},
        {opacity:1,offset:.15},
        {opacity:0,transform:'rotate(18deg) translateX(240px)'}
      ],{duration:1100,easing:'ease-out'}).onfinish=()=>s.remove();
    }
    setInterval(()=>{ if(Math.random()>0.4) shoot(); }, 3200);
  })();

})();
