# Database runbook

Owner: Data Infrastructure
Status: current
Last reviewed: 2026-07-30

---

## RB-003 - Database is refusing connections

**Symptom:** Services cannot connect to PostgreSQL at all; connection attempts are rejected
rather than queued.

**Detection:** `postgres` logs show `connections active` at or near `max_connections`, or
`FATAL: sorry, too many clients already`.

**Remediation:** Identify the service holding the most connections and restart it to release
them. Raise `max_connections` only as a temporary measure agreed with the DBA on call.

**Escalation:** DBA on call.

---

## RB-004 - Database connection pool exhaustion in a service

**Symptom:** A single service times out waiting for a database connection while the database
itself is healthy and lightly loaded. Requests fail after the pool acquire timeout rather
than after a query runs.

**Detection:** The service logs `timeout acquiring connection from pool`,
`connection acquisition slow`, or `pool saturated` with a rising queue depth or waiter count,
while `postgres` logs show a low active connection count and no long-running transactions.

**Remediation:**
1. Check the change log for a recent configuration change to the pool. A pool maximum reduced
   by a configuration change is the most common cause, and the change record will name the
   release it shipped in.
2. If the pool size changed in the current release, roll the service back to the previous
   version per RB-010. Rollback is preferred over hot-patching configuration during an
   incident.
3. If the pool size is unchanged, look for a connection leak: waiters rising while in-use
   connections stay pinned at the maximum for minutes at a time.
4. Do not scale the service horizontally to work around pool exhaustion. Extra replicas each
   get their own undersized pool and add load without adding capacity. This supersedes the
   advice in the archived checkout runbook.

**Escalation:** Service owner, then the incident commander rota if the rollback does not
restore the error rate within 15 minutes.

---

## RB-005 - Slow queries degrading a service

**Symptom:** Requests are slow but succeed; latency tracks query duration.

**Detection:** `postgres` logs report slowest query durations in the hundreds of milliseconds
or above, rising in step with service latency.

**Remediation:** Capture the offending statement, check for a missing index, and apply the
statement timeout `statement_timeout=2s` for the affected role while a fix is prepared.

**Escalation:** DBA on call.
