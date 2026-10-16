// 최소 DOM 스텁으로 sim/index.html의 단계 흐름을 끝까지 걸어본다.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const js = html.match(/<script>([\s\S]*)<\/script>/)[1];
let store = {};
const localStorage = { getItem: k => store[k] ?? null, setItem: (k, v) => store[k] = v, removeItem: k => delete store[k] };
const location = { search: '', reload(){} };
const window = { scrollTo(){} };
let app = { innerHTML: '' }, who = { textContent: '' };
function buttons(){
  const out = []; const re = /<button([^>]*)>([\s\S]*?)<\/button>/g; let m;
  while ((m = re.exec(app.innerHTML))) {
    const attrs = m[1];
    const b = { dataset: {}, classList: { toggle(){} }, disabled: /disabled/.test(attrs), onclick: null,
      cls: (attrs.match(/class="([^"]*)"/) || [])[1] || '', id: (attrs.match(/id="([^"]*)"/) || [])[1] || '', text: m[2] };
    const k = attrs.match(/data-k="([^"]*)"/); if (k) b.dataset.k = k[1];
    out.push(b);
  }
  // 같은 innerHTML에 대해 같은 객체를 돌려줘야 onclick 배선이 유지된다
  if (app._html === app.innerHTML && app._btns) return app._btns;
  app._html = app.innerHTML; return app._btns = out;
}
app._nk = { value: '', oninput: null };
const document = {
  getElementById: id => id === 'app' ? app : id === 'who' ? who : id === 'nk' ? app._nk : (buttons().find(b => b.id === id) || null),
  querySelectorAll: sel => sel === '.opt' ? buttons().filter(b => b.cls.includes('opt')) : sel === '#sc button' ? buttons().filter(b => !b.cls && !b.id) : [],
};
const pending = []; const setTimeout = fn => pending.push(fn);
const fetch = () => Promise.resolve();
function flush(){ while (pending.length) pending.shift()(); }
const ref = {};
new Function('localStorage', 'location', 'window', 'document', 'setTimeout', 'fetch', 'ref', js + ';ref.S=S;')(localStorage, location, window, document, setTimeout, fetch, ref);
const S = ref.S;
function click(pred){ flush(); const b = buttons().find(pred); if (!b || !b.onclick) throw new Error('button not found at step ' + S.step); b.onclick(); flush(); }
const seen = [S.step];
const step = pred => { click(pred); seen.push(S.step); };
app._nk.value = '파란우산'; flush(); app._nk.oninput(); step(b => b.id === 'nx');
step(b => b.dataset.k === 'B');   // q1 공동 경작
step(b => b.text === '3');        // q2 신뢰 3
step(b => b.dataset.k === 'A');   // q3 있었다
step(b => b.id === 'nx');         // start → c5_1
step(b => b.id === 'nx');         // c5_1 → c5_2
step(b => b.dataset.k === 'B');   // fair2018 의심
step(b => b.id === 'nx');         // c5_3 → c5_4
step(b => b.id === 'nx');         // c5_4 → c5_5
step(b => b.id === 'nx');         // c5_5 → c5_6
step(b => b.dataset.k === 'B');   // policy 보편
step(b => b.dataset.k === 'B');   // design 전환 전후 → end
console.log('steps:', seen.join(' > '));
console.log('bars:', S.trust, S.part, S.tie, 'init', JSON.stringify(S.init));
console.log('log:', S.log.map(r => r.chapter + ':' + r.step + '=' + r.choice).join(', '));
let ok = true; const check = (c, m) => { if (!c) { ok = false; console.log('FAIL', m); } };
check(S.step === 'end', 'did not reach end');
check(S.trust === 24 && S.tie === 60 && S.part === 60, 'bar math off');
check(S.log.length === 6 && S.log.slice(2).every(r => r.init_trust === 3), 'log/init_trust wrong');
check(/파란우산의 사회자본/.test(app.innerHTML) && /출발 신뢰 3점/.test(app.innerHTML), 'ending card text');
console.log(ok ? 'PASS' : 'FAILED');
process.exit(ok ? 0 : 1);
