# Platform operations runbook

Owner: Platform Reliability
Status: current
Last reviewed: 2026-07-30

---

## RB-000 - No matching runbook entry

**Symptom:** An incident whose symptom does not match any current entry in any runbook.

**Detection:** You have searched the runbooks and the closest entries describe a different
failure mode.

**Remediation:** Do not improvise a remediation from a partially matching entry, and do not
follow an archived entry that has been superseded. Record the symptom, the evidence gathered
so far, and the fact that no entry matches.

**Escalation:** Page the service owner listed in the service catalogue. Raise a follow-up
ticket to add a runbook entry once the incident is resolved.

---

## RB-001 - Elevated 5xx rate at the API gateway

**Symptom:** The gateway reports an upstream error rate above the 5% threshold, or returns
502 with `upstream_circuit_open`.

**Detection:** `api-gateway` logs show `upstream error rate breached threshold` or
`circuit breaker opened`.

**Remediation:** The gateway is reporting, not causing, the failure. Identify the named
upstream and triage that service. Do not raise the circuit breaker threshold to suppress the
alert.

**Escalation:** If the named upstream has no owner on call, escalate to the incident
commander rota.

---

## RB-009 - Disk pressure on a node

**Symptom:** Pods are evicted or fail to schedule; writes fail with no space left on device.

**Detection:** Platform logs report node resource pressure with a high disk figure, or
eviction events.

**Remediation:** Clear rotated logs and unused images on the node, then cordon it if pressure
persists.

**Escalation:** Platform squad.

---

## RB-010 - Deploy rollback procedure

**Symptom:** A release is confirmed or strongly suspected as the cause of an active incident.

**Detection:** The incident start correlates with a `deploy succeeded` event for the affected
service, or with a change record that shipped in that release.

**Remediation:** Roll back to the previous version with
`ops/deploy rollback --service <name> --to <version>`. Confirm the service restarts on the
previous configuration, then verify the error rate returns to baseline before closing. Keep
the faulty release blocked until the defect is fixed, and record the rollback in the change
log.

**Escalation:** Release manager if the rollback itself fails.

---

## RB-012 - TLS certificate expiry

**Symptom:** Clients report certificate errors; internal calls fail handshake.

**Detection:** Handshake failures naming an expired certificate, starting at a round hour.

**Remediation:** Renew through `ops/cert renew --domain <name>` and confirm propagation to
the edge before declaring recovery.

**Escalation:** Platform squad.
