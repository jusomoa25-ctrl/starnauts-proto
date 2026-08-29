/* tool-store.js — 도구 공통 기록 저장소 (로컬 우선, 나중에 Supabase 교체 가능)
 *
 * 접근 모델:
 *   - channel-research 기록  = shared:true  → 모든 계정이 봄 (전체 공유)
 *   - music-lab / 기타 기록   = shared:false → 해당 owner(계정)만 봄
 *
 * 백엔드 어댑터: 현재 backend=local(localStorage + 선택적 로컬폴더 백업).
 *   Supabase 연결 시 backend 객체만 교체하면 됨 (save/all/remove 시그니처 동일).
 *   tool_records(id, owner, tool, kind, shared bool, payload jsonb, created_at) + RLS(shared OR owner=auth.uid())로 매핑.
 */
(function (global) {
  'use strict';
  var HKEY = 'starnauts_tool_history';
  var AKEY = 'starnauts_account';
  var ALKEY = 'starnauts_accounts';

  function rd(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function wr(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  /* ── 로컬 계정 (지금은 단순 프로필; 나중에 Supabase Auth uid로 대체) ── */
  function account() { return localStorage.getItem(AKEY) || 'default'; }
  function accounts() { var a = rd(ALKEY, ['default']); if (a.indexOf(account()) < 0) a.push(account()); return a; }
  function setAccount(name) {
    name = (name || '').trim() || 'default';
    localStorage.setItem(AKEY, name);
    var a = rd(ALKEY, ['default']); if (a.indexOf(name) < 0) { a.push(name); wr(ALKEY, a); }
    return name;
  }

  /* ── 레코드 ── */
  function all() { return rd(HKEY, []); }
  function isShared(r) { return r.shared === true || r.tool === 'channel-research'; }
  function ownerOf(r) { return r.owner || 'default'; }
  function visible() { var acc = account(); return all().filter(function (r) { return isShared(r) || ownerOf(r) === acc; }); }

  function save(rec) {
    var a = all();
    rec.id = rec.id || ('h' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5));
    rec.ts = rec.ts || new Date().toISOString();
    if (rec.owner == null) rec.owner = account();
    if (rec.shared == null) rec.shared = (rec.tool === 'channel-research');
    a.unshift(rec);
    if (a.length > 800) a.length = 800;
    wr(HKEY, a);
    fileBackup(rec);
    return rec.id;
  }
  function update(id, patch) {
    var a = all();
    for (var i = 0; i < a.length; i++) { if (a[i].id === id) { for (var k in patch) a[i][k] = patch[k]; wr(HKEY, a); fileBackup(a[i]); return; } }
  }
  function remove(id) { wr(HKEY, all().filter(function (r) { return r.id !== id; })); }

  function exportJSON() { return JSON.stringify(all(), null, 2); }
  function importJSON(txt) {
    try {
      var inc = JSON.parse(txt); if (!Array.isArray(inc)) return 0;
      var a = all(), seen = {}; a.forEach(function (r) { seen[r.id] = 1; });
      var n = 0; inc.forEach(function (r) { if (r && r.id && !seen[r.id]) { a.push(r); n++; } });
      a.sort(function (x, y) { return (y.ts || '').localeCompare(x.ts || ''); });
      wr(HKEY, a); return n;
    } catch (e) { return 0; }
  }

  /* ── 로컬 폴더 자동 백업 (File System Access API) — 브라우저 데이터 삭제돼도 안 날아감 ──
   * 한 번 폴더를 지정하면 이후 생성물이 그 폴더에 .json/.md로 자동 저장됨.
   * 폴더 핸들은 IndexedDB에 보관 → 세션 넘어가도 유지(권한 재확인 1회).        */
  var dirHandle = null, fsReady = false;
  function idb(cb) {
    var op = indexedDB.open('starnauts_fs', 1);
    op.onupgradeneeded = function () { op.result.createObjectStore('h'); };
    op.onsuccess = function () { cb(op.result); };
    op.onerror = function () { cb(null); };
  }
  function idbGet(key, cb) { idb(function (db) { if (!db) return cb(null); var t = db.transaction('h', 'readonly').objectStore('h').get(key); t.onsuccess = function () { cb(t.result || null); }; t.onerror = function () { cb(null); }; }); }
  function idbSet(key, val) { idb(function (db) { if (!db) return; db.transaction('h', 'readwrite').objectStore('h').put(val, key); }); }

  function supportsFS() { return typeof global.showDirectoryPicker === 'function'; }
  function folderName() { return dirHandle ? dirHandle.name : null; }

  function restoreFolder(cb) {
    if (!supportsFS()) return cb && cb(false);
    idbGet('dir', function (h) {
      if (!h) return cb && cb(false);
      h.queryPermission({ mode: 'readwrite' }).then(function (p) {
        if (p === 'granted') { dirHandle = h; fsReady = true; cb && cb(true); }
        else { dirHandle = h; fsReady = false; cb && cb('prompt'); } // 권한 재요청 필요
      }).catch(function () { cb && cb(false); });
    });
  }
  function enableFolder() {
    if (!supportsFS()) return Promise.reject(new Error('이 브라우저는 폴더 저장을 지원하지 않습니다(Chrome/Edge 권장).'));
    return global.showDirectoryPicker({ mode: 'readwrite' }).then(function (h) {
      dirHandle = h; fsReady = true; idbSet('dir', h);
      return dumpAll().then(function () { return h.name; });
    });
  }
  function reauth() {
    if (!dirHandle) return Promise.resolve(false);
    return dirHandle.requestPermission({ mode: 'readwrite' }).then(function (p) { fsReady = (p === 'granted'); return fsReady; });
  }
  function slug(s) { return (s || 'rec').replace(/[^\w가-힣\- ]+/g, '').replace(/\s+/g, '_').slice(0, 60); }
  function recBody(r) {
    if (r.result) return r.result;                       // 가사·스타일 본문
    if (r.data) return JSON.stringify(r.data, null, 2);  // 리서치 결과
    return JSON.stringify(r, null, 2);
  }
  function fileBackup(rec) {
    if (!fsReady || !dirHandle) return;
    try {
      var folder = isShared(rec) ? 'shared' : ('accounts/' + slug(ownerOf(rec)));
      var sub = rec.tool || 'misc';
      var fname = (rec.ts || '').slice(0, 19).replace(/[:T]/g, '-') + '_' + slug(rec.summary || rec.toolName || rec.tool) + '.md';
      ensureDir(folder + '/' + sub).then(function (d) {
        return d.getFileHandle(fname, { create: true }).then(function (fh) {
          return fh.createWritable().then(function (w) {
            var head = '# ' + (rec.summary || rec.toolName || rec.tool || 'record') + '\n\n- tool: ' + (rec.tool || '') + '\n- account: ' + ownerOf(rec) + '\n- shared: ' + isShared(rec) + '\n- ts: ' + (rec.ts || '') + '\n\n';
            return w.write(head + recBody(rec)).then(function () { return w.close(); });
          });
        });
      }).catch(function () {});
    } catch (e) {}
  }
  function ensureDir(path) {
    var parts = path.split('/').filter(Boolean);
    var p = Promise.resolve(dirHandle);
    parts.forEach(function (name) { p = p.then(function (d) { return d.getDirectoryHandle(name, { create: true }); }); });
    return p;
  }
  function dumpAll() { // 폴더 첫 지정 시 기존 기록 전부 내려쓰기
    var list = all(); var p = Promise.resolve();
    list.forEach(function (r) { p = p.then(function () { fileBackup(r); }); });
    return p.then(function () { return true; });
  }

  global.ToolStore = {
    account: account, accounts: accounts, setAccount: setAccount,
    all: all, visible: visible, isShared: isShared, ownerOf: ownerOf,
    save: save, update: update, remove: remove,
    exportJSON: exportJSON, importJSON: importJSON,
    supportsFS: supportsFS, folderName: folderName, folderReady: function () { return fsReady; },
    restoreFolder: restoreFolder, enableFolder: enableFolder, reauth: reauth, dumpAll: dumpAll
  };
})(window);
