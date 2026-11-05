/** 2부 연구모형 저장소 (Google Apps Script 웹앱)
 * 배포: 새 Google 시트 → 확장 프로그램 → Apps Script → 이 파일 붙여넣기 → 배포 → 새 배포 → 유형 '웹 앱', 실행 주체 '나', 액세스 '모든 사용자'
 *       → 나온 URL을 model/canvas_v4.html.tpl의 SAVE_URL, model/dashboard.html.tpl의 READ_URL에 넣고 build_canvas.py 재실행.
 * 시트 열: ts | nick | stage | key | value(JSON 문자열). 수업 뒤 시트는 지운다(가드레일 5). API 키는 여기 없다(2부 데모는 AI 호출 없음).
 * shortcut: 인증 없음(누구나 POST 가능), 수업 1회·시트 삭제 전제. 공개 운영이면 토큰 검사 추가.
 */
const SHEET = 'models';

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET);
  if (!sh) { sh = ss.insertSheet(SHEET); sh.appendRow(['ts', 'nick', 'stage', 'key', 'value']); }
  return sh;
}

function doPost(e) {
  try {
    const row = JSON.parse(e.postData.contents);
    if (!row.stage || !row.key) return out_({ ok: false, error: 'stage/key 없음' });
    const nick = String(row.nick || '익명').slice(0, 12);
    sheet_().appendRow([row.ts || new Date().toISOString(), nick, String(row.stage), String(row.key), JSON.stringify(row.value || null).slice(0, 45000)]);
    return out_({ ok: true });
  } catch (err) { return out_({ ok: false, error: String(err) }); }
}

function doGet(e) {
  const stage = (e.parameter && e.parameter.stage) || '';
  const vals = sheet_().getDataRange().getValues().slice(1);
  const rows = vals.filter(r => !stage || r[2] === stage).map(r => ({ ts: r[0], nick: r[1], stage: r[2], key: r[3], value: safe_(r[4]) }));
  return out_(rows);
}

function safe_(s) { try { return JSON.parse(s); } catch (_) { return s; } }
function out_(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }

function clearAll() { const sh = sheet_(); sh.clearContents(); sh.appendRow(['ts', 'nick', 'stage', 'key', 'value']); }  // 수업 뒤 실행
