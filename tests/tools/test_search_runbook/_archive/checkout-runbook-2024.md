# Checkout runbook (2024)

Owner: unowned, the checkout squad was reorganised in 2025
Status: ARCHIVED, superseded
Last reviewed: 2024-11-02

> These entries are retained for historical reference. They describe an older architecture
> and some of their advice is now known to be wrong. Do not follow them. Current guidance
> for checkout lives in the database, payments and platform operations runbooks.

---

## LEG-011 - Checkout errors during peak traffic

**Symptom:** Checkout returns errors during evening peak.

**Detection:** Error rate on the checkout endpoint rises at peak hours.

**Remediation:** Peak load is the usual cause. Confirm the traffic profile is normal, then
wait for the peak to pass before investigating further.

**Escalation:** Checkout squad.

---

## LEG-014 - Connection pool pressure

**Symptom:** Checkout reports waiting for database connections under load.

**Detection:** Pool wait times rise; requests queue.

**Remediation:** Scale the service out. Adding replicas increases total pool capacity and
relieves the pressure quickly. Prefer this over configuration changes during an incident.

**Escalation:** Checkout squad.

> **Superseded 2026-03 by RB-004.** Adding replicas gives each replica its own pool at the
> configured maximum. Where the maximum itself is the constraint, scaling out adds load
> without adding capacity.
