# Data platform runbook

Owner: Data Platform
Status: current
Last reviewed: 2026-07-30

---

## RB-007 - Queue consumer stalled by a poison message

**Symptom:** A queue consumer stops making progress on one partition while lag stays flat.
Downstream jobs finish partially or miss their window.

**Detection:** Worker logs show repeated `redelivering message` for the same offset, followed
by `max redelivery attempts exhausted` and `consumer stalled`. Dead letter queue depth starts
to rise.

**Remediation:**
1. Identify the blocking offset from the redelivery log lines.
2. Drain that message to the dead letter queue so the partition can advance.
3. Resume the consumer and confirm lag starts falling.
4. Re-run the affected job in backfill mode for the records missed in the original window.
5. Raise a ticket for the validation defect that produced the unprocessable message. Check
   the change log for an upstream schema change: an unprocessable message is often the first
   sign of one.

**Escalation:** Data platform squad if the dead letter queue grows by more than 10 messages
in an hour.

---

## RB-008 - Nightly job missed its window

**Symptom:** A scheduled job reports `job window exceeded` or finishes with status `partial`.

**Detection:** Job logs show processed record counts well below expected.

**Remediation:** Establish why the job stalled before re-running it; a blind re-run repeats
the failure. Once the cause is cleared, re-run in backfill mode scoped to the missed records
rather than the full window.

**Escalation:** Data platform squad if reconciliation figures are needed for a same-day
finance close.
