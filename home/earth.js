/* ============================================================
   STARNAUTS — live rotating globe (smooth, no frame-stepping)
   Renders the equirectangular map onto a shaded sphere each frame.
   ============================================================ */
(function(){
  'use strict';
  const globe = document.querySelector('.earth-globe');
  if(!globe) return;
  const FS = 340;                       // internal render resolution
  const cv = document.createElement('canvas');
  cv.width = FS; cv.height = FS; cv.className = 'earth-canvas';
  const ctx = cv.getContext('2d');
  const out = ctx.createImageData(FS, FS), O = out.data;

  const img = new Image();
  img.onload = function(){
    const EW = img.naturalWidth, EH = img.naturalHeight;
    const oc = document.createElement('canvas'); oc.width = EW; oc.height = EH;
    const octx = oc.getContext('2d'); octx.drawImage(img, 0, 0);
    let T;
    try { T = octx.getImageData(0, 0, EW, EH).data; }
    catch(e){ return; }                 // keep fallback img if blocked

    // replace fallback img with the live canvas
    globe.innerHTML = ''; globe.appendChild(cv);

    const npx = FS*FS;
    const rowBase = new Int32Array(npx), baseU = new Float32Array(npx),
          mul = new Float32Array(npx), rimT = new Float32Array(npx),
          alpha = new Uint8ClampedArray(npx), inside = new Uint8Array(npx);
    let lx=-0.5, ly=0.5, lz=0.72; const ll=Math.hypot(lx,ly,lz); lx/=ll; ly/=ll; lz/=ll;
    const TWO=Math.PI*2;
    for(let py=0; py<FS; py++){
      const ny=(py+0.5)/FS*2-1;
      for(let px=0; px<FS; px++){
        const nx=(px+0.5)/FS*2-1, p=py*FS+px, r2=nx*nx+ny*ny;
        if(r2>1){ inside[p]=0; continue; }
        inside[p]=1;
        const z=Math.sqrt(1-r2), X=nx, Y=-ny, Z=z;
        const lat=Math.asin(Y), lon0=Math.atan2(X,Z);
        let v=((Math.PI/2-lat)/Math.PI*EH)|0; if(v<0)v=0; if(v>=EH)v=EH-1;
        rowBase[p]=v*EW;
        baseU[p]=lon0/TWO;
        let dif=X*lx+Y*ly+Z*lz; if(dif<0)dif=0;
        let b=0.32+0.84*dif; if(b>1.35)b=1.35; mul[p]=b;
        rimT[p]= r2>0.80 ? (r2-0.80)/0.20 : 0;
        alpha[p]= r2>0.992 ? Math.max(0,255*(1-(r2-0.992)/0.008)) : 255;
      }
    }
    const period=36000;                 // ms per full rotation
    function frame(ts){
      const rotFrac=(ts % period)/period;
      for(let p=0; p<npx; p++){
        const o=p*4;
        if(!inside[p]){ O[o+3]=0; continue; }
        let uf=baseU[p]+rotFrac; uf-=Math.floor(uf);
        let u=(uf*EW)|0; if(u>=EW)u=EW-1;
        const e=(rowBase[p]+u)*4, m=mul[p];
        let r=T[e]*m, g=T[e+1]*m, b=T[e+2]*m;
        const t=rimT[p];
        if(t>0){ r+=(120-r)*0.30*t; g+=(160-g)*0.30*t; b+=(225-b)*0.32*t; }
        O[o]=r>255?255:r; O[o+1]=g>255?255:g; O[o+2]=b>255?255:b; O[o+3]=alpha[p];
      }
      ctx.putImageData(out,0,0);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  };
  img.src='assets/earth-equirect.png?v=5';
})();
