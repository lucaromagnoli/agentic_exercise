# Change log

Every production change: releases, configuration, feature flags, infrastructure, and
notified changes from external parties. Maintained by the release manager.
Records are added when a change ships, not when it is planned.

---

## CHG-1026 - Quarterly runbook review

- **Applied:** 2026-07-30 14:00 UTC
- **Type:** documentation
- **Author:** platform-reliability
- **Services:** none

**Change:** Reviewed and re-published the operations runbook. No entries added or removed.

**Notes:** Three entries were flagged as missing during the review and not written up.

---

## CHG-1031 - search-service 2.7.1

- **Shipped:** 2026-08-04 09:16 UTC
- **Type:** release
- **Author:** j.ferreira
- **Services:** search-service
- **Pull request:** #4703
- **Risk assessed:** low

**Change:** Upgraded the catalogue index analyser and rebuilt the index.

**Notes:** Observed no latency change over the following week. This is the most recent
search-service release.

---

## CHG-1033 - Partner settlement feed schema v3

- **Applied:** 2026-08-04 18:00 UTC
- **Type:** external, notified by partner
- **Author:** not ours, notified by Meridian Settlements
- **Services:** recon-worker (consumer)
- **Pull request:** none

**Change:** The partner moved the settlement feed to schema v3. Unsettled rows now carry
`settled_at` as the placeholder string `"0000-00-00"` instead of `null`.

**Notes:** Notified by email eight days before the change. No consumer-side work was
scheduled. Our validation still expects `null` or a valid date.

---

## CHG-1035 - recon-worker 1.9.4

- **Shipped:** 2026-08-05 06:04 UTC
- **Type:** release
- **Author:** ci-bot
- **Services:** recon-worker
- **Pull request:** #4755
- **Risk assessed:** low

**Change:** Added structured logging fields to the reconciliation consumer. No behaviour
change.

**Notes:** Shipped four hours after the nightly reconciliation window closed.

---

## CHG-1038 - payments-worker 3.4.0

- **Shipped:** 2026-08-11 14:22 UTC
- **Type:** release
- **Author:** ci-bot
- **Services:** payments-worker
- **Pull request:** #4788
- **Risk assessed:** medium

**Change:** Tuned provider retry backoff from fixed 500ms to exponential with jitter.

**Notes:** Reduced duplicate charge attempts during provider wobbles. No change to the
checkout path.

---

## CHG-1042 - Reduce idle database connections on checkout-service

- **Merged:** 2026-08-12 11:03 UTC
- **Shipped:** 2026-08-12 19:31 UTC in checkout-service v4.12.0
- **Type:** configuration
- **Author:** r.okonkwo
- **Services:** checkout-service
- **Pull request:** #4821
- **Risk assessed:** low

**Change:** `db.pool.max` reduced from `40` to `4` for checkout-service.

**Notes:** Follow-up to the July connection storm postmortem, which recommended trimming
idle connections in the **staging** environment. The value was edited in the shared default
configuration block rather than the staging override, so it applied to production on the
next release. Reviewed and approved by one reviewer. No load test was run against the new
value.

---

## CHG-1043 - Enable express checkout for 25% of traffic

- **Shipped:** 2026-08-12 19:31 UTC in checkout-service v4.12.0
- **Type:** feature flag
- **Author:** m.doyle
- **Services:** checkout-service
- **Pull request:** #4816
- **Risk assessed:** medium

**Change:** `feature.express_checkout` enabled for 25% of sessions.

**Notes:** Shipped in the same release as CHG-1042. The flag was disabled at 20:15 UTC on
2026-08-12 as a precaution during the incident and re-enabled the following morning with no
recurrence.

---

## CHG-1044 - Rollback checkout-service to 4.11.3

- **Shipped:** 2026-08-12 20:06 UTC
- **Type:** rollback
- **Author:** a.nwosu
- **Services:** checkout-service
- **Pull request:** none
- **Risk assessed:** not assessed, incident action

**Change:** Rolled checkout-service back from 4.12.0 to 4.11.3, restoring the previous
configuration including `db.pool.max` of `40`.

**Notes:** Performed during INC-2043. Release 4.12.0 is blocked pending a fix.

---

## CHG-1047 - Kernel patch rollout, node pool eu-west-1

- **Applied:** 2026-08-17 22:40 to 23:05 UTC
- **Type:** infrastructure
- **Author:** platform-reliability
- **Services:** all workloads on the affected nodes

**Change:** Rolling kernel patch across the eu-west-1 node pool. Nodes cordoned, patched
and uncordoned in sequence.

**Notes:** Pods were rescheduled as nodes returned to service. Scheduling was left to the
default scheduler, so co-location differs from before the patch.

---

## CHG-1048 - Remove CPU limits from media-transcoder

- **Applied:** 2026-08-17 21:30 UTC
- **Type:** configuration
- **Author:** k.sullivan
- **Services:** media-transcoder
- **Pull request:** #4902
- **Risk assessed:** low

**Change:** Removed the CPU limit from media-transcoder pods so transcoding jobs can burst.
CPU requests left unchanged at 500m.

**Notes:** Transcoding backlog had been growing. With no limit set, a busy transcoder can
consume whatever CPU is available on its node. No dedicated node pool was configured.

---

## CHG-1050 - api-gateway 6.1.2

- **Shipped:** 2026-08-18 10:14 UTC
- **Type:** release
- **Author:** ci-bot
- **Services:** api-gateway
- **Pull request:** #4915
- **Risk assessed:** low

**Change:** Dependency updates and a correction to upstream timeout logging.

**Notes:** Shipped after the search latency reports began that morning.
