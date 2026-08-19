# Search and caching runbook

Owner: Discovery
Status: current
Last reviewed: 2026-07-30

---

## RB-006 - Cache node restart causing a cold cache

**Symptom:** Latency rises sharply immediately after a cache node restart and recovers as the
cache refills.

**Detection:** Cache hit rate drops well below its normal baseline and eviction counts spike.

**Remediation:** Wait for the cache to refill; if the recovery window is unacceptable, run the
warm-cache job `ops/warm-cache --index <name>`.

**Escalation:** None required if the hit rate recovers within 30 minutes.
