/** 11주차 저장소 · Cloudflare Worker (KV)
 *  학생 화면: POST /submit  (stage=model|draft|vote|sim, 별명만. 키 불필요)
 *  관리자:   GET  /rows?stage=model|draft|all   헤더 X-Admin-Pin 필수(시크릿 ADMIN_PIN과 비교)
 *            POST /control           헤더 X-Admin-Pin 필수 (교수님 판정·지목) → verdict:<기기> 키 하나
 *            POST /reset             헤더 X-Admin-Pin 필수. 제출·초안·판정을 지운다(기기 등록 tok:은 남김)
 *  학생:     GET  /control?dev=...   자기 기기 앞으로 온 판정만(목록 조회 없이 키 두 개를 읽는다)
 *            GET  /peers             다른 학생의 별명·자료·정의·칸
 *            POST /ai                연구질문 한 줄 코멘트(선택). ANTHROPIC_API_KEY는 시크릿, 모델 고정, 선행연구 목록 밖 언급 금지 프롬프트
 *  수업 뒤:  wrangler kv namespace delete 로 전부 삭제(가드레일 5)
 *
 *  무료 요금제 한도(하루, 00:00 UTC 초기화): 읽기 100,000 · 쓰기 1,000 · 목록 1,000 · 삭제 1,000.
 *  그래서 학생 쪽 반복 요청에는 목록 조회를 쓰지 않고(판정은 키 읽기), 목록이 필요한 /peers·/rows는 이 isolate 안에서 잠깐 캐시한다.
 *  shortcut: 캐시는 isolate 메모리라 isolate가 여럿이면 그만큼 목록 조회가 늘어난다. 수업 17명 규모에서는 한도의 절반 아래. 더 커지면 Durable Object로.
 *  shortcut: KV list는 1,000건 단위 페이징 없이 한 번에 읽는다(수업 17명이면 키 수십 개). 더 커지면 cursor 페이징.
 */
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, X-Admin-Pin", "Access-Control-Allow-Methods": "GET, POST, OPTIONS" };
const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json", ...CORS } });
const clean = (s, n) => String(s ?? "").slice(0, n);
const TTL = 60 * 60 * 24 * 14;
const ROW_PREFIX = /^(model|draft|vote|sim):/;

const memo = new Map();  // 키 → {at, val}. isolate가 살아 있는 동안만
async function cached(key, ms, fn) {
  const hit = memo.get(key); if (hit && Date.now() - hit.at < ms) return hit.val;
  const val = await fn(); memo.set(key, { at: Date.now(), val }); return val;
}
const forget = () => memo.clear();  // 쓰기 뒤에는 이 isolate의 캐시를 비운다

async function rowsOf(env, prefix) {
  const list = await env.W11.list(prefix ? { prefix } : {});
  const keys = list.keys.map(k => k.name).filter(n => ROW_PREFIX.test(n));
  return (await Promise.all(keys.map(k => env.W11.get(k, "json")))).filter(Boolean);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), path = url.pathname;
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    const admin = req.headers.get("X-Admin-Pin") && req.headers.get("X-Admin-Pin") === env.ADMIN_PIN;

    if (req.method === "POST" && path === "/submit") {
      const b = await req.json().catch(() => null);
      if (!b || !/^(model|draft|vote|sim)$/.test(b.stage)) return json({ ok: false, error: "stage" }, 400);
      const dev = clean(b.dev, 24), tok = clean(b.tok, 64); if (!dev || !tok) return json({ ok: false, error: "dev/tok" }, 400);
      const had = await env.W11.get("tok:" + dev); if (had && had !== tok) return json({ ok: false, error: "dev taken" }, 403);  // 기기 ID 도용 방지: 첫 토큰만 유효
      if (!had) await env.W11.put("tok:" + dev, tok, { expirationTtl: TTL });
      const row = { ts: new Date().toISOString(), dev, nick: clean(b.nick, 12) || "익명", stage: b.stage, key: clean(b.key, 32), value: b.value ?? null };
      const body = JSON.stringify(row); if (body.length > 60000) return json({ ok: false, error: "too large" }, 413);
      const id = b.stage === "draft" ? `draft:${row.dev}` : `${b.stage}:${row.ts}:${row.dev}`;  // 초안은 기기당 최신 하나만
      await env.W11.put(id, body, { expirationTtl: TTL });
      forget();
      return json({ ok: true });
    }
    if (req.method === "GET" && path === "/rows") {
      if (!admin) return json({ ok: false, error: "admin" }, 401);
      const stage = url.searchParams.get("stage") || "model";
      if (!/^(model|draft|vote|sim|all)$/.test(stage)) return json({ ok: false, error: "stage" }, 400);
      return json(await cached("rows:" + stage, 8000, () => rowsOf(env, stage === "all" ? "" : stage + ":")));
    }
    if (req.method === "GET" && path === "/peers") {  // 학생용: 별명·자료·정의·칸만. 기기 ID는 내보내지 않는다(자기 것만 제외)
      const me = url.searchParams.get("dev") || "";
      const latest = await cached("peers", 30000, async () => {
        const rows = (await rowsOf(env, "model:")).sort((a, b) => (a.ts < b.ts ? -1 : 1));
        const by = {}; rows.forEach(r => { by[r.dev] = r; }); return Object.values(by);
      });
      return json(latest.filter(r => r.dev !== me).map(r => ({ ts: r.ts, dev: "", nick: r.nick, stage: "model", value: { survey: r.value?.survey, definition: r.value?.definition, lineage: r.value?.lineage } })));
    }
    if (req.method === "POST" && path === "/control") {
      if (!admin) return json({ ok: false, error: "admin" }, 401);
      const b = await req.json().catch(() => null); if (!b || !b.value) return json({ ok: false }, 400);
      const target = clean(b.value.dev, 24) || "all";
      const row = { ts: new Date().toISOString(), dev: "admin", nick: "admin", stage: "control", key: clean(b.key, 32), value: b.value };
      await env.W11.put(`verdict:${target}`, JSON.stringify(row), { expirationTtl: 60 * 60 * 24 * 7 });  // 기기당 최신 판정 하나
      return json({ ok: true });
    }
    if (req.method === "GET" && path === "/control") {
      const dev = clean(url.searchParams.get("dev"), 24), tok = url.searchParams.get("tok") || "";
      const had = dev && await env.W11.get("tok:" + dev); if (!had || had !== tok) return json([], 200);  // 남의 판정은 못 본다
      const rows = await Promise.all([env.W11.get("verdict:" + dev, { type: "json", cacheTtl: 30 }), env.W11.get("verdict:all", { type: "json", cacheTtl: 30 })]);
      return json(rows.filter(Boolean));
    }
    if (req.method === "POST" && path === "/reset") {  // 당일 아침 시험 제출 정리용. 기기 등록(tok:)은 남긴다
      if (!admin) return json({ ok: false, error: "admin" }, 401);
      const list = await env.W11.list();
      const del = list.keys.map(k => k.name).filter(n => !n.startsWith("tok:"));
      await Promise.all(del.map(k => env.W11.delete(k)));
      forget();
      return json({ ok: true, deleted: del.length });
    }
    if (req.method === "POST" && path === "/ai") {
      if (!env.ANTHROPIC_API_KEY) return json({ ok: false, error: "no key" }, 503);
      const b = await req.json().catch(() => null); if (!b || !b.q) return json({ ok: false }, 400);
      const dev = clean(b.dev, 24), tok = clean(b.tok, 64), had = dev && await env.W11.get("tok:" + dev); if (!had || had !== tok) return json({ ok: false, error: "dev/tok" }, 403);  // 등록된 기기만. 키 지출을 남이 못 쓰게
      const studies = (Array.isArray(b.matches) ? b.matches : []).slice(0, 5).map(m => `- ${clean(m?.au, 60)} (${clean(m?.y, 8)}) ${clean(m?.t, 200)}`).join("\n") || "- (없음)";
      const system = "당신은 행정학 수업의 조교다. 학생의 연구질문 한 줄에 대해 두 문장으로만 답한다: (1) 이 질문이 상관인지 인과인지, (2) 아래 목록의 선행연구 중 무엇과 가장 닮았는지. 목록에 없는 논문·저자·수치는 절대 언급하지 않는다. 한국어, 합쇼체.";
      const user = `연구질문: ${clean(b.q, 300)}\n정의: ${clean(b.definition, 300)}\n선행연구 목록:\n${studies}`;
      const r = await fetch("https://api.anthropic.com/v1/messages", { method: "POST", headers: { "Content-Type": "application/json", "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
        body: JSON.stringify({ model: "claude-haiku-5-5", max_tokens: 200, system, messages: [{ role: "user", content: user }] }) });
      const j = await r.json().catch(() => ({}));
      return json({ ok: r.ok, text: (j.content || []).map(c => c.text || "").join("") });
    }
    return json({ ok: false, error: "not found" }, 404);
  }
};
