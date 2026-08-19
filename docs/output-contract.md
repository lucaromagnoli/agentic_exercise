# Output contract

The orchestrator's final result. Emit it as JSON, and render whatever human readable version
you like alongside it.

The point of the contract is the `evidence` fields. Every factual claim is traceable to a line
in `data/logs/`, a record in `data/changes/`, or an entry in `data/runbook/`. If a claim
cannot be cited, it does not belong in the output, it belongs in `open_questions`.

```json
{
  "incident_id": "INC-2043",
  "summary": "Two to four sentences a duty manager could read aloud.",
  "timeline": [
    {
      "time": "2026-08-12T19:31:12Z",
      "event": "What happened, in plain words.",
      "evidence": ["platform-events.log:10", "CHG-1042"]
    }
  ],
  "root_cause": {
    "statement": "One sentence.",
    "confidence": "high | medium | low",
    "evidence": ["checkout-service.log:5", "postgres.log:4", "CHG-1042"],
    "correlation": "The join that gets you from two partial findings to one cause: which log evidence lines up with which change, and on what (time, service, configuration key)."
  },
  "ruled_out": [
    {
      "theory": "A hypothesis from the incident report, the logs or the change log that does not hold.",
      "why": "The evidence that kills it.",
      "evidence": ["payments-worker.log:4"]
    }
  ],
  "runbook": {
    "matched": "RB-004",
    "title": "Database connection pool exhaustion in a service",
    "source": "database.md",
    "why": "Why this entry and not the near misses.",
    "remediation": ["Step one, taken from the entry.", "Step two."]
  },
  "actions": [
    {
      "action": "What to do.",
      "urgency": "now | today | follow-up",
      "source": "RB-004 | analyst | historian | orchestrator"
    }
  ],
  "stakeholder_update": "Three lines, if the comms drafter ran. Otherwise null.",
  "open_questions": ["Anything the evidence does not settle."]
}
```

## Rules

- `evidence` entries are one of:
  - `filename:line` for logs, 1 based, matching what `search_logs` returned
  - `CHG-nnnn` for a change record
  - `RB-nnn` or `LEG-nnn` for a runbook entry
- `root_cause.correlation` is the field that proves the parallel agents earned their keep. A
  root cause supported only by log evidence, or only by change evidence, is incomplete on
  INC-2043 and INC-2051. Say what lined up with what.
- `runbook.matched` is `null` when nothing current genuinely fits. In that case `why` explains
  what was searched and which entries were the near misses, and the actions follow RB-000.
- An archived `LEG-nnn` entry is never a valid `runbook.matched`. If one is the closest match,
  that is a signal the current runbooks have a gap, and it belongs in `open_questions`.
- `remediation` steps are drawn from the runbook entry, not invented. Anything you add that
  the runbook does not say belongs in `actions` with `source: "analyst"`,
  `source: "historian"` or `source: "orchestrator"`, so a reader can tell policy from
  judgement.
- `ruled_out` is not optional padding. If the incident report contains a theory, the output
  either supports it or rules it out.
- `confidence` is `low` when the evidence is consistent with more than one cause. An
  orchestrator that always reports `high` is not measuring anything. Correlated evidence from
  two independent agents is what earns `high`.
