#!/bin/sh
# lead.php 자체 점검. 배포본에는 들어가지 않는다 (workflow 가 _* 를 제외한다).
#
# 로컬 php 내장 서버에 실제 요청을 던지고, 리드가 정말 파일에 남는지까지 본다.
# 메일 발송은 로컬에 sendmail 이 없어 실패하지만 그것으로 접수를 실패 처리하지
# 않는 것이 lead.php 의 설계다 — 그 점도 여기서 확인한다.
#
#   sh _test-lead.sh
set -e
cd "$(dirname "$0")"

php -S 127.0.0.1:8099 >/dev/null 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null' EXIT
for i in 1 2 3 4 5 6 7 8 9 10; do
  curl -s -o /dev/null "http://127.0.0.1:8099/lead.php" && break
  sleep 1
done

code() { curl -s -o /dev/null -w '%{http_code}' "$@"; }
fails=0
check() {
  if [ "$2" = "$3" ]; then echo "ok   $1 ($3)"; else echo "FAIL $1 — expected $2, got $3"; fails=1; fi
}

check "GET 은 거절"              405 "$(code http://127.0.0.1:8099/lead.php)"
check "빈 이메일 거절"            400 "$(code -X POST -d 'email=' http://127.0.0.1:8099/lead.php)"
check "형식 틀린 이메일 거절"      400 "$(code -X POST -d 'email=notanemail' http://127.0.0.1:8099/lead.php)"
check "헤더 인젝션 거절"          400 "$(code -X POST --data-urlencode 'email=a@b.com
Bcc: x@y.com' http://127.0.0.1:8099/lead.php)"
check "봇 덫은 조용히 200"        200 "$(code -X POST -d 'email=a@b.com&website=spam' http://127.0.0.1:8099/lead.php)"
check "메일이 안 나가도 접수는 성공" 200 "$(code -X POST -d 'email=test@example.com' http://127.0.0.1:8099/lead.php)"

if grep -q '"email":"test@example.com"' leads/leads.ndjson 2>/dev/null; then
  echo "ok   리드가 파일에 남는다"
else
  echo "FAIL 리드가 파일에 남지 않았다"; fails=1
fi
if grep -q '"email":"a@b.com"' leads/leads.ndjson 2>/dev/null; then
  echo "FAIL 봇 덫에 걸린 값이 파일에 들어갔다"; fails=1
else
  echo "ok   봇 덫 값은 저장되지 않는다"
fi
rm -rf leads

[ "$fails" = 0 ] && echo "--- 통과" || { echo "--- 실패"; exit 1; }
