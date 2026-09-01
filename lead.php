<?php
/* STARNAUTS — 출시 알림 이메일 수집.
 *
 * 정적 사이트지만 Hostinger 공유 호스팅에 PHP 8.3 이 이미 켜져 있다. 외부 폼
 * 백엔드에 새로 가입하지 않고, 이미 값을 치르고 있는 것으로 처리한다.
 *
 * 기록이 먼저, 알림은 덤이다. 이 워크스페이스 어디에도 실제로 도는 메일 발송
 * 수단이 없어서(2026-09-01 확인) mail() 이 정말 배달되는지 보장할 수 없다.
 * 그래서 리드는 파일에 먼저 남기고, 메일은 실패해도 접수를 성공으로 친다.
 * 파일은 남았는데 성공을 안 돌려주면 같은 사람이 계속 다시 넣는다.
 *
 * 저장 위치는 웹루트 한 칸 위다. 정적 배포가 웹루트를 통째로 덮어쓰기 때문에
 * 안에 두면 배포할 때마다 모아둔 리드가 날아간다. 겸사겸사 웹으로도 안 열린다.
 */
declare(strict_types=1);

const LEAD_DIR  = __DIR__ . '/../leads';
const LEAD_FILE = LEAD_DIR . '/leads.ndjson';
const LEAD_TO   = 'starnauts2025@gmail.com';
const LEAD_FROM = 'no-reply@starnauts.com';

header('Content-Type: application/json; charset=utf-8');

function fail(int $code, string $msg): never {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}

function done(): never {
    echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fail(405, '지원하지 않는 요청입니다.');
}

// 봇 덫. 사람은 숨겨진 칸을 채우지 않는다. 티 내지 않고 접수한 척한다.
if (trim((string)($_POST['website'] ?? '')) !== '') {
    done();
}

$email = trim((string)($_POST['email'] ?? ''));
if ($email === '' || strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fail(400, '이메일 주소를 다시 확인해주세요.');
}
// 메일 헤더 인젝션 차단 — 개행이 섞인 주소는 받지 않는다.
if (preg_match('/[\r\n]/', $email) === 1) {
    fail(400, '이메일 주소를 다시 확인해주세요.');
}

if (!is_dir(LEAD_DIR) && !@mkdir(LEAD_DIR, 0700, true) && !is_dir(LEAD_DIR)) {
    fail(500, '지금은 접수가 되지 않습니다. ' . LEAD_TO . ' 으로 메일 주시면 등록해 드리겠습니다.');
}

$row = json_encode([
    'email' => $email,
    'at'    => gmdate('c'),
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n";

if (@file_put_contents(LEAD_FILE, $row, FILE_APPEND | LOCK_EX) === false) {
    fail(500, '지금은 접수가 되지 않습니다. ' . LEAD_TO . ' 으로 메일 주시면 등록해 드리겠습니다.');
}
@chmod(LEAD_FILE, 0600);

// 알림. 배달 여부는 보장할 수 없으므로 실패해도 접수는 성공이다.
@mail(
    LEAD_TO,
    '[STARNAUTS] 출시 알림 신청',
    "STARNAUTS 출시 알림 신청\n\n이메일: {$email}\n신청 시각(UTC): " . gmdate('Y-m-d H:i:s') . "\n",
    "From: STARNAUTS <" . LEAD_FROM . ">\r\nContent-Type: text/plain; charset=UTF-8\r\n"
);

done();
