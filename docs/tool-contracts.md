# Tool contracts

Implement these as described. They are deliberately dumb: keyword matching over local files,
no ranking, no embeddings. Making the tools clever is not the exercise, and a naive tool is
what forces the agent to search well.

Everything is local. No network calls, no filesystem access outside `data/`.

Three real tools, one optional stub. Each specialist gets exactly one of them.

| Tool | Used by | Corpus |
|------|---------|--------|
| `search_logs` | log analyst | `data/logs/` |
| `search_changes` | change historian | `data/changes/` |
| `search_runbook` | runbook lookup | `data/runbook/` including `_archive/` |
| `post_update` | comms drafter (optional) | writes to `out/` |

---

## `search_logs(query, max_results = 20)`

Searches every `.log` file in `data/logs/`.

**Matching.** Split `query` on whitespace into terms. A log line matches if **every** term
appears in it, case insensitively, as a plain substring. No stemming, no synonyms, no regex.

**Ordering.** Results are sorted by the timestamp at the start of each line, ascending, so the
agent gets a timeline rather than a pile.

**Result shape:**

```json
{
  "query": "pool timeout",
  "total_matches": 7,
  "returned": 7,
  "truncated": false,
  "results": [
    {
      "file": "checkout-service.log",
      "line": 9,
      "text": "2026-08-12T19:33:41Z  checkout-service  ERROR  timeout acquiring connection from pool=primary after 5000ms queue_depth=41 order_id=ord_88213"
    }
  ]
}
```

- `line` is 1 based, so a human can open the file and check the citation.
- If `total_matches` exceeds `max_results`, return the first `max_results` after sorting and
  set `truncated` to `true`. Do not silently drop the rest without saying so.
- An empty or whitespace only query returns
  `{"error": "query must contain at least one term"}` rather than every line in the corpus.
- Zero matches is a normal result, not an error: `total_matches` is `0` and `results` is `[]`.

---

## `search_changes(query, max_results = 5)`

Searches `data/changes/change-log.md`: releases, configuration changes, feature flags,
infrastructure work and changes notified by external parties.

**Unit of retrieval is the change record**, not the line. Split the document on `## `
headings. Each record has an id (`CHG-1042`), a title, and a body.

**Matching.** A record matches if every term in `query` appears somewhere in that record,
case insensitively.

**Ordering.** Most recent first, by the date in the record. A historian asking "what changed
recently" wants the newest, and this is the one place where ordering is worth getting right.

**Result shape:**

```json
{
  "query": "checkout-service configuration",
  "total_matches": 3,
  "returned": 3,
  "truncated": false,
  "results": [
    {
      "id": "CHG-1042",
      "title": "Reduce idle database connections on checkout-service",
      "text": "- **Merged:** ... full record body ..."
    }
  ]
}
```

- Return the **full** record. The dates and the notes are where the answer usually is, and
  summarising inside the tool moves judgement out of the agent, where you can see it, and
  into your code, where you cannot.

---

## `search_runbook(query, max_results = 3)`

Searches **every** `.md` file under `data/runbook/`, recursively, including `_archive/`.

There is no single runbook. Entries are spread across five current files owned by different
squads, plus one archived file whose advice has been superseded. The tool does not filter the
archive out, and it does not tell the agent which entries are current. Noticing that is the
agent's job.

**Unit of retrieval is the entry.** Split each file on `## ` headings. Each entry has an id
(`RB-004`, `LEG-014`), a title, and a body. Files with no `## ` headings, such as the index
`README.md`, contribute nothing.

**Matching.** As above: an entry matches if every term in `query` appears somewhere in that
entry, case insensitively.

**Ordering.** Most terms matched first; ties broken by entry id ascending. If you keep it
simpler than that, say so in your write up.

**Result shape:**

```json
{
  "query": "connection pool",
  "total_matches": 3,
  "returned": 3,
  "results": [
    {
      "id": "RB-004",
      "title": "Database connection pool exhaustion in a service",
      "source": "database.md",
      "text": "**Symptom:** ... full entry body ..."
    }
  ]
}
```

- `source` is the path relative to `data/runbook/`, so `_archive/checkout-runbook-2024.md`
  looks different from `database.md` in the results. Do not add a `status` field: let the
  agent work out what an archived entry means.
- Return the **full** entry text. The agent needs the remediation steps verbatim.
- Zero matches is a normal and meaningful result. RB-000 exists for that case, and finding it
  is the agent's job, not the tool's: do not special case it.

---

## `post_update(text)` (optional, for the comms drafter)

A stub. It does not talk to Slack.

**Behaviour:** append `text` to `out/comms.log` with a timestamp, and return:

```json
{ "status": "posted", "channel": "#incident-updates", "characters": 214 }
```

**Reject** text longer than 600 characters with
`{"error": "update exceeds 600 characters"}`, so the drafter has a real constraint to satisfy
and something to react to when it fails.

---

## Testing your tools before you wire up a model

Do this. It takes five minutes and saves half an hour later.

| Call | Expect |
|------|--------|
| `search_logs("pool")` | 19 lines, nearly all from `checkout-service.log` |
| `search_logs("checkout deploy")` | the deploy lines in `platform-events.log` |
| `search_logs("zzz")` | `total_matches: 0`, no error |
| `search_logs("")` | the error object |
| `search_changes("db.pool.max")` | two records, the change and the rollback |
| `search_changes("checkout")` | four records, newest first |
| `search_runbook("connection pool")` | entries from two different files, one of them archived |
| `search_runbook("timeout")` | more than one entry, including a decoy |
| `search_runbook("noisy neighbour")` | zero matches |
