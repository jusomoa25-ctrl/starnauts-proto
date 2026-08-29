#!/usr/bin/env python3
# Starnauts 로컬 서버 — 정적 서빙 + 채널 리서치 결과 캐시 API (의존성 0, 표준 라이브러리만)
# 실행:  python server.py [port]      (기본 8000)
# 노출:  cloudflared tunnel --url http://localhost:8000
#
# 목적(사용자 제안): 채널 분석 결과를 서버(data/research/)에 자동 저장 →
#   1) 같은 채널 재조회 시 캐시 반환 = YouTube/Gemini 토큰·쿼터 절약
#   2) ?channel=<핸들> 공유 링크로 누구나 조회
#   3) data/research/ 누적 = 우리만의 채널 데이터 자산(_index.json = 목록)
import http.server, socketserver, json, os, sys, urllib.parse, datetime, re

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(ROOT, 'data', 'research')
INDEX = os.path.join(CACHE_DIR, '_index.json')
os.makedirs(CACHE_DIR, exist_ok=True)


def slug(ch):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', (ch or '').strip().lstrip('@'))[:80]


def load_index():
    try:
        with open(INDEX, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_index(idx):
    with open(INDEX, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass  # 조용히

    def end_headers(self):
        # 모든 응답 no-cache → 사용자·협업자 모두 항상 최신 페이지 수신(하드리프레시 불필요)
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self._json(204, {})

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == '/api/research':
            q = urllib.parse.parse_qs(u.query)
            ch = (q.get('channel') or [''])[0]
            if not ch:                       # 목록(우리 자산 인덱스)
                return self._json(200, {'items': load_index()})
            fp = os.path.join(CACHE_DIR, slug(ch) + '.json')
            if not os.path.exists(fp):
                return self._json(404, {'cached': False})
            with open(fp, encoding='utf-8') as f:
                rec = json.load(f)
            age = None
            try:
                ts = rec.get('ts', '').replace('Z', '')
                age = (datetime.datetime.utcnow() - datetime.datetime.fromisoformat(ts)).days
            except Exception:
                pass
            return self._json(200, {'cached': True, 'age_days': age, 'record': rec})
        return super().do_GET()

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == '/api/research':
            ln = int(self.headers.get('Content-Length') or 0)
            try:
                body = json.loads(self.rfile.read(ln) or b'{}')
            except Exception:
                return self._json(400, {'ok': False, 'error': 'bad json'})
            ch = body.get('channel') or ''
            if not ch:
                return self._json(400, {'ok': False, 'error': 'channel required'})
            s = slug(ch)
            rec = {
                'id': 'r' + datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
                'ts': datetime.datetime.utcnow().isoformat() + 'Z',
                'channel': ch,
                'input': body.get('input'),
                'score': body.get('score'),
                'data': body.get('data'),
            }
            with open(os.path.join(CACHE_DIR, s + '.json'), 'w', encoding='utf-8') as f:
                json.dump(rec, f, ensure_ascii=False, indent=1)
            idx = [x for x in load_index() if x.get('slug') != s]   # 채널당 1엔트리(최신 교체)
            idx.insert(0, {'slug': s, 'channel': ch, 'score': body.get('score'), 'ts': rec['ts']})
            save_index(idx)
            return self._json(200, {'ok': True, 'slug': s, 'ts': rec['ts']})
        return self._json(404, {'ok': False})


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(('0.0.0.0', port), H)
    httpd.daemon_threads = True
    print('Starnauts server on :%d  (threaded · static + /api/research)' % port)
    httpd.serve_forever()
