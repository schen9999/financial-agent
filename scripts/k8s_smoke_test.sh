#!/usr/bin/env bash
# End-to-end smoke test for the kind cluster deployment.
#
# Asserts, in order:
#   1. API /health responds
#   2. Sync brief end-to-end (POST /research) — real data fetch + RAG + LLM
#   3. Cache WRITE: Redis holds exact key research:<TICKER> afterwards
#   4. Cache HIT: repeat request returns the byte-identical brief, fast
#   5. Cache MISS isolation: a different ticker's exact key is absent
#   6. Async brief via Celery (POST /research/async → poll → complete)
#      — the FIRST environment where the designed async path runs end-to-end
#   7. MCP server answers an initialize handshake over streamable-HTTP
#   8. Streamlit health endpoint responds
#
# Requires: kubectl context kind-financial-agent, curl, jq. Run via `make smoke-test`.
set -euo pipefail

NS=financial-agent
API=http://localhost:30080
MCP=http://localhost:30800/mcp
UI=http://localhost:30501
SYNC_TICKER=${SYNC_TICKER:-AAPL}
ASYNC_TICKER=${ASYNC_TICKER:-NVDA}
MISS_TICKER=${MISS_TICKER:-MSFT}

pass=0; fail=0
ok()   { echo "  PASS  $1"; pass=$((pass+1)); }
bad()  { echo "  FAIL  $1"; fail=$((fail+1)); }
say()  { echo; echo "== $1"; }

redis_cli() { kubectl -n "$NS" exec deploy/redis -- redis-cli "$@"; }

say "0. Reset smoke-test cache keys (deterministic re-runs)"
redis_cli DEL "research:${SYNC_TICKER}" "research:${ASYNC_TICKER}" "research:${MISS_TICKER}" >/dev/null
ok "cleared research:{${SYNC_TICKER},${ASYNC_TICKER},${MISS_TICKER}}"

say "1. API health"
health=$(curl -fsS --max-time 10 "$API/health" | jq -r .status)
[ "$health" = "ok" ] && ok "GET /health -> ok" || { bad "GET /health -> $health"; exit 1; }

say "2. Sync brief end-to-end (POST /research ${SYNC_TICKER}) — cold, ~60-120s on CPU"
t0=$(date +%s)
brief1=$(curl -fsS --max-time 420 -X POST "$API/research" \
  -H 'Content-Type: application/json' -d "{\"ticker\":\"${SYNC_TICKER}\"}" | jq -r .brief)
t1=$(date +%s); cold_s=$((t1-t0))
if [ "${#brief1}" -gt 400 ] && grep -q "Executive Summary" <<<"$brief1"; then
  ok "brief generated (${#brief1} chars, ${cold_s}s, contains Executive Summary)"
else
  bad "brief too short or malformed (${#brief1} chars)"; exit 1
fi

say "3. Cache WRITE: exact key research:${SYNC_TICKER} exists in Redis"
exists=$(redis_cli EXISTS "research:${SYNC_TICKER}")
[ "$exists" = "1" ] && ok "EXISTS research:${SYNC_TICKER} = 1" || bad "EXISTS research:${SYNC_TICKER} = $exists"
cached_ticker=$(redis_cli --no-raw GET "research:${SYNC_TICKER}" >/dev/null 2>&1; redis_cli GET "research:${SYNC_TICKER}" | jq -r .ticker)
[ "$cached_ticker" = "${SYNC_TICKER}" ] && ok "cached payload .ticker = ${SYNC_TICKER}" || bad "cached payload .ticker = $cached_ticker"

say "4. Cache HIT: repeat request returns identical brief, fast"
t0=$(date +%s)
brief2=$(curl -fsS --max-time 60 -X POST "$API/research" \
  -H 'Content-Type: application/json' -d "{\"ticker\":\"${SYNC_TICKER}\"}" | jq -r .brief)
t1=$(date +%s); warm_s=$((t1-t0))
h1=$(sha256sum <<<"$brief1" | cut -d' ' -f1); h2=$(sha256sum <<<"$brief2" | cut -d' ' -f1)
[ "$h1" = "$h2" ] && ok "repeat brief byte-identical (exact-key hit)" || bad "repeat brief differs — cache did not serve"
[ "$warm_s" -le 15 ] && ok "warm response ${warm_s}s (cold was ${cold_s}s)" || bad "warm response took ${warm_s}s — suspicious for a cache hit"

say "5. Cache MISS isolation: different ticker has no key"
exists=$(redis_cli EXISTS "research:${MISS_TICKER}")
[ "$exists" = "0" ] && ok "EXISTS research:${MISS_TICKER} = 0 (no cross-ticker contamination)" || bad "EXISTS research:${MISS_TICKER} = $exists"

say "6. Async brief via Celery (POST /research/async ${ASYNC_TICKER})"
job=$(curl -fsS --max-time 15 -X POST "$API/research/async" \
  -H 'Content-Type: application/json' -d "{\"ticker\":\"${ASYNC_TICKER}\"}")
job_id=$(jq -r .job_id <<<"$job")
[ -n "$job_id" ] && [ "$job_id" != "null" ] && ok "job queued: $job_id" || { bad "no job_id in: $job"; exit 1; }
status=queued; async_brief=""
for i in $(seq 1 60); do
  sleep 7
  # Tolerate transient poll failures — only the FINAL state decides the assert.
  resp=$(curl -sS --max-time 15 "$API/research/status/$job_id" || true)
  status=$(jq -r .status <<<"$resp" 2>/dev/null || echo poll-failed)
  if [ "$status" = "complete" ]; then async_brief=$(jq -r .result.brief <<<"$resp"); break; fi
  if [ "$status" = "error" ]; then bad "async job errored: $(jq -r .error <<<"$resp")"; break; fi
done
if [ "$status" = "complete" ] && [ "${#async_brief}" -gt 400 ]; then
  echo  "  ============================================================"
  echo  "  >>> CELERY TASK COMPLETED END-TO-END (${#async_brief} chars) <<<"
  echo  "  >>> First environment where the designed FastAPI+Celery+   <<<"
  echo  "  >>> Redis+Postgres topology runs complete (see Phase 0).   <<<"
  echo  "  ============================================================"
  ok "async brief complete via Celery worker"
else
  bad "async job final status=$status (brief ${#async_brief} chars)"
fi
exists=$(redis_cli EXISTS "research:${ASYNC_TICKER}")
[ "$exists" = "1" ] && ok "worker wrote exact key research:${ASYNC_TICKER}" || bad "worker did not write research:${ASYNC_TICKER}"

say "7. MCP initialize handshake (streamable-HTTP)"
mcp_resp=$(curl -fsSL --max-time 20 -X POST "$MCP" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"smoke","version":"0.0.0"}}}' || true)
if grep -q "financial-research-agent" <<<"$mcp_resp"; then
  ok "MCP initialize returned serverInfo financial-research-agent"
else
  bad "MCP initialize unexpected response: $(head -c 200 <<<"$mcp_resp")"
fi

say "8. Streamlit health"
ui=$(curl -fsS --max-time 10 "$UI/_stcore/health" || true)
[ "$ui" = "ok" ] && ok "Streamlit /_stcore/health -> ok" || bad "Streamlit health -> $ui"

echo
echo "==================== SMOKE TEST: $pass passed, $fail failed ===================="
[ "$fail" -eq 0 ]
