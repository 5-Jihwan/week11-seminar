/** 11주차 저장소 · Cloudflare Worker (KV)
 *  학생 화면: POST /submit  (stage=model|draft|vote|sim, 별명만. 키 불필요)
 *  관리자:   GET  /rows?stage=model   헤더 X-Admin-Pin 필수(시크릿 ADMIN_PIN과 비교) → 서버에서 분리
 *            POST /control           헤더 X-Admin-Pin 필수 (교수님 판정·지목)
 *  학생:     GET  /control?dev=...   자기 기기 앞으로 온 판정만
 *            POST /ai                연구질문 한 줄 코멘트(선택). ANTHROPIC_API_KEY는 시크릿, 모델 고정, 선행연구 목록 밖 언급 금지 프롬프트
 *  수업 뒤:  wrangler kv namespace delete 로 전부 삭제(가드레일 5)
 *  shortcut: KV list는 1,000건 단위 페이징 없이 한 번에 읽는다(수업 17명×초안 수백 행이면 충분). 더 커지면 cursor 페이징.
 */
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, X-Admin-Pin", "Access-Control-Allow-Methods": "GET, POST, OPTIONS" };
const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json", ...CORS } });
const clean = (s, n) => String(s ?? "").slice(0, n);

export default {
  async fetch(req, env) {
    const url = new URL(req.url), path = url.pathname;
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    const admin = req.headers.get("X-Admin-Pin") && req.headers.get("X-Admin-Pin") === env.ADMIN_PIN;

    if (req.method === "POST" && path === "/submit") {
      const b = await req.json().catch(() => null);
      if (!b || !/^(model|draft|vote|sim)$/.test(b.stage)) return json({ ok: false, error: "stage" }, 400);
      const row = { ts: new Date().toISOString(), dev: clean(b.dev, 24), nick: clean(b.nick, 12) || "익명", stage: b.stage, key: clean(b.key, 32), value: b.value ?? null };
      const body = JSON.stringify(row); if (body.length > 60000) return json({ ok: false, error: "too large" }, 413);
      const id = b.stage === "draft" ? `draft:${row.dev}` : `${b.stage}:${row.ts}:${row.dev}`;  // 초안은 기기당 최신 하나만
      await env.W11.put(id, body, { expirationTtl: 60 * 60 * 24 * 14 });
      return json({ ok: true });
    }
    if (req.method === "GET" && path === "/rows") {
      if (!admin) return json({ ok: false, error: "admin" }, 401);
      const stage = url.searchParams.get("stage") || "model";
      const list = await env.W11.list({ prefix: stage + ":" });
      const rows = await Promise.all(list.keys.map(k => env.W11.get(k.name, "json")));
      return json(rows.filter(Boolean));
    }
    if (req.method === "POST" && path === "/control") {
      if (!admin) return json({ ok: false, error: "admin" }, 401);
      const b = await req.json().catch(() => null); if (!b || !b.value) return json({ ok: false }, 400);
      const row = { ts: new Date().toISOString(), dev: "admin", nick: "admin", stage: "control", key: clean(b.key, 32), value: b.value };
      await env.W11.put(`control:${row.ts}`, JSON.stringify(row), { expirationTtl: 60 * 60 * 24 * 7 });
      return json({ ok: true });
    }
    if (req.method === "GET" && path === "/control") {
      const dev = url.searchParams.get("dev") || "";
      const list = await env.W11.list({ prefix: "control:" });
      const rows = (await Promise.all(list.keys.map(k => env.W11.get(k.name, "json")))).filter(r => r && r.value && (r.value.dev === dev || r.value.dev === "all"));
      return json(rows);
    }
    if (req.method === "POST" && path === "/ai") {
      if (!env.ANTHROPIC_API_KEY) return json({ ok: false, error: "no key" }, 503);
      const b = await req.json().catch(() => null); if (!b || !b.q) return json({ ok: false }, 400);
      const studies = (b.matches || []).slice(0, 5).map(m => `- ${m.au} (${m.y}) ${m.t}`).join("\n") || "- (없음)";
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
