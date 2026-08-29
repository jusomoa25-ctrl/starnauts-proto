/* ============================================================================
   STARNAUTS — 사이트 실적 수치 단일 데이터 소스
   ----------------------------------------------------------------------------
   사이트 전역의 실적 수치는 전부 이 파일 한 곳에서만 정의한다.
   HTML은 값을 직접 쓰지 않고 data-stat 속성으로 자리만 표시한다.

   [값 규칙]
     null  = 아직 실측 데이터가 없음 → 해당 자리를 화면에서 자동으로 숨긴다.
             ("0명", "-", "N/A" 같은 표시는 절대 남기지 않는다)
     숫자/문자열 = 실측 근거가 있는 값. 근거를 반드시 주석으로 병기한다.
     추정값·예시값·자리 채우기 값은 넣지 않는다.

   [HTML 마크업 규약]
     <b data-stat="키" data-stat-suffix="명"></b>
       → 값이 있으면 "1,234명", 없으면 요소가 숨겨진다.
     data-stat-prefix / data-stat-suffix : 값 앞뒤에 붙일 고정 문구
     data-stat-item : 수치를 감싸는 상자에 붙인다.
       상자 안의 수치가 전부 비어 있으면 상자째 숨겨 라벨만 떠 있는 상태를 막는다.
     HTML에는 style="display:none"을 미리 넣어 둔다.
       (JS가 없거나 실패해도 근거 없는 수치가 노출되지 않게 하는 안전 기본값)

   [범위 밖]
     콘텐츠 카드별 조회수, 스트리머별 실시간 시청자 수처럼 항목마다 값이 다른
     지표는 이 파일이 아니라 콘텐츠/스트리머 피드가 항목과 함께 내려주는 값이다.
     여기에 키를 만들지 않는다.
   ========================================================================== */
(function () {
  'use strict';

  var SITE_STATS = {
    /* ── 실측 근거 있는 값 ───────────────────────────────────────────────── */
    curriculum_courses: 4,             // 근거: 커리큘럼 초안 C1~C4
    curriculum_lessons: 27,            // 근거: 커리큘럼 초안 회차 합계 (7+8+6+6)
    curriculum_hours: '14시간 30분',    // 근거: 커리큘럼 초안 과목별 분량 합계
    suno_reference_db: 1062,           // 근거: music-library SUNO 레퍼런스 곡 DB 보유 건수
    suno_manuals: 12,                  // 근거: music-library/SUNO 매뉴얼 문서 편수
    distributor_compare: 9,            // 근거: 유통사 실비용 비교 대상 사수

    /* ── 실측 데이터 없음 (서버 연결 전까지 null 유지) ──────────────────────
       주석의 "이전 표기"는 근거 없이 사이트에 적혀 있던 값이다. 복원 금지. */
    students_total: null,      // 이전 표기 1,121명 · 출처 예정: 수강 등록 DB
    instructors_total: null,   // 이전 표기 38명    · 출처 예정: 강사 계정 DB
    satisfaction_avg: null,    // 이전 표기 4.9점   · 출처 예정: 수강 후기 평점 집계
    completions_total: null,   // 이전 표기 3,521회 · 출처 예정: 수강 완료 로그
    repeat_rate: null,         // 이전 표기 97%     · 출처 예정: 재수강 전환 집계
    mentor_available: null,    // 이전 표기 21명    · 출처 예정: 1:1 예약 가능 강사 수
    mentor_slots_left: null,   // 이전 표기 34      · 출처 예정: 주간 예약 슬롯 잔여
    tutor_students: null,      // 이전 표기 2,418명 · 출처 예정: 강사 대시보드 수강생 집계
    tutor_rating: null         // 이전 표기 ★4.9    · 출처 예정: 강사별 후기 평점 집계
  };

  /* --------------------------------------------------------------------------
     데이터 로딩 지점 — 서버가 붙으면 이 함수 하나만 교체하면 된다.

       function loadStats() {
         return fetch('/api/site-stats')
           .then(function (r) { return r.json(); })
           .catch(function () { return {}; });   // 실패 시 전부 숨김(빈 객체)
       }

     반환 형식은 위 SITE_STATS와 같은 평면 객체 { 키: 값|null } 이다.
     -------------------------------------------------------------------------- */
  function loadStats() {
    return Promise.resolve(SITE_STATS);
  }

  function each(sel, fn) {
    var list = document.querySelectorAll(sel);
    for (var i = 0; i < list.length; i++) fn(list[i]);
  }

  function format(value, el) {
    var body = (typeof value === 'number') ? value.toLocaleString('ko-KR') : String(value);
    return (el.getAttribute('data-stat-prefix') || '') + body
         + (el.getAttribute('data-stat-suffix') || '');
  }

  function apply(stats) {
    // 1) 수치 자리를 채우거나, 값이 없으면 그 자리를 숨긴다.
    each('[data-stat]', function (el) {
      var value = stats[el.getAttribute('data-stat')];
      var has = value !== null && value !== undefined && value !== '';
      el.textContent = has ? format(value, el) : '';
      el.style.display = has ? '' : 'none';
    });

    // 2) 상자 안 수치가 전부 비었으면 상자째 숨긴다 (라벨만 남는 것 방지).
    each('[data-stat-item]', function (box) {
      var slots = box.querySelectorAll('[data-stat]');
      var visible = false;
      for (var i = 0; i < slots.length; i++) {
        if (slots[i].style.display !== 'none') visible = true;
      }
      box.style.display = visible ? '' : 'none';
    });
  }

  function run() {
    loadStats().then(apply);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
