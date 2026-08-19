# Payments runbook

Owner: Payments
Status: current
Last reviewed: 2026-07-30

---

## RB-002 - Payment provider timeouts

**Symptom:** Charges fail or stall with timeouts from the external payment provider.

**Detection:** `payments-worker` logs show `provider gateway responded 504`,
`provider timeout`, or a falling provider success rate over a 5 minute window.

**Remediation:** Confirm the provider status page. Retries are automatic with backoff; if the
provider is degraded for more than 15 minutes, enable the queued-capture fallback flag
`payments.queue_on_provider_error` so charges are captured asynchronously.

**Escalation:** Notify the payments squad and open a ticket with the provider.

---

## RB-013 - Partner API rate limit exhausted

**Symptom:** Calls to a partner API fail with 429 once a daily or hourly quota is spent.

**Detection:** Repeated 429 responses from a single partner host, clustered at the same time
each day.

**Remediation:** Back off to the documented quota, and request a temporary increase through
the partner portal if the volume is legitimate.

**Escalation:** Partnerships, then the payments squad if settlement is affected.
