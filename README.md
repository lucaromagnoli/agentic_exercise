# Mini Incident Triage Squad

A two hour, hands-on exercise in building a small multi-agent system by hand.

You will build an **orchestrator** that reads an incident report and coordinates three
**specialist agents**, each with exactly one tool, to work out what happened and what to do
about it. Two of those specialists run **in parallel**, and neither can reach the answer
alone: the orchestrator has to correlate their findings.

This repository deliberately contains **no agent code**, and no answer key. It gives you the
brief, the data to work against, and the contracts your pieces have to meet. Writing the
agents is the exercise. Nobody marks the result; the only thing that matters is what you
learn from making it work.

## Why this shape

Most of the difficulty in agentic systems is not the model call. It is deciding who knows
what, who is allowed to do what, what can safely happen at the same time, and how partial
answers get merged into something a human can act on. This exercise is sized so that you hit
all of those in the first hour and spend the second hour iterating on prompts, which is where
the learning is.

## What you are building

```
              incident report (data/incidents/INC-2043.md)
                                |
                                v
                       +------------------+
                       |   ORCHESTRATOR   |  no tools of its own
                       |  plain code loop |  fans out, joins, decides
                       +------------------+
                          |            |
              fan out, concurrently    |
                          |            |
         +----------------+            +----------------+
         v                                               v
+--------------------+                         +----------------------+
|    LOG ANALYST     |                         |   CHANGE HISTORIAN   |
| tool: search_logs  |                         | tool: search_changes |
| what happened,     |                         | what changed, when,  |
| when, in what order|                         | and what it touched  |
+--------------------+                         +----------------------+
         |                                               |
         +----------------+            +-----------------+
                          v            v
                       +------------------+
                       |   JOIN + DECIDE  |  correlate on time and service
                       +------------------+
                                |
                                v  symptom description only
                       +----------------------+
                       |   RUNBOOK LOOKUP     |
                       | tool: search_runbook |
                       +----------------------+
                                |
                                v
                       +------------------+
                       |  merged triage   |
                       | summary + actions|
                       +------------------+
                                |
                                v  (optional stretch)
                       +------------------+
                       |  COMMS DRAFTER   |  tool: post_update
                       +------------------+
```

**Orchestrator.** Plain code, not a model deciding everything. It reads the incident, fans
out to the log analyst and the change historian **at the same time**, waits for both,
correlates their findings, then hands the resulting symptom to the runbook lookup. A loop with
a fan-out, a join and a couple of conditionals is the target, not a planner.

**Log analyst.** Establishes the timeline and the failure mode from the logs. It can only see
the logs through `search_logs`, and it usually needs several searches to get there. It can
see **that** a release went out. It cannot see what was in it.

**Change historian.** Establishes what changed recently and what it touched, from the change
log: releases, configuration, feature flags, infrastructure, and changes notified by external
parties. It can only see that corpus through `search_changes`. It has no idea what is
currently broken beyond the incident report.

Neither of these two is sufficient on its own, which is the point. "Connection pool
exhaustion started at 19:33" and "a config change cut the pool maximum, shipped at 19:31" are
each half an answer. The orchestrator joining them on time and service is the whole answer.

**Runbook lookup.** Runs after the join, because it needs the symptom the other two
established. Given a symptom description (not raw log lines, not raw change records), it finds
the matching remediation across several runbooks. If nothing current genuinely matches, saying
so is the correct answer.

**Comms drafter (optional, stretch).** Turns the merged findings into a three line stakeholder
update. No tool, or the trivial `post_update` stub.

## Ground rules

These exist to keep the exercise about agent design rather than about libraries.

1. **Hand-built.** No agent framework (LangChain, LangGraph, CrewAI, Autogen and friends). A
   raw model SDK plus your own loop is the point. Use whatever language you like.
2. **Three real tools plus an optional stub**, exactly as specified in
   [docs/tool-contracts.md](docs/tool-contracts.md). No extra tools, no filesystem access, no
   shelling out to grep.
3. **Specialists are sandboxed.** Each specialist sees only its own tool, and only the context
   the orchestrator hands it. The log analyst never sees the change log. The historian never
   sees a log line. The runbook lookup sees neither, only the symptom description.
4. **The two parallel specialists do not see each other's findings.** If the historian gets to
   read the analyst's output, you have built a pipeline with extra steps, not a fan-out.
5. **Specialists do not call each other.** All coordination goes through the orchestrator.
6. **The orchestrator has no tools.** It only calls agents, joins their output, and decides.
7. **Prompts live in their own files**, not inline in the middle of your loop. You will be
   editing them repeatedly in the second hour and you want the diffs to be readable.
8. **Every claim carries evidence.** A finding cites the log line, change record or runbook
   entry it came from. This is the single most effective anti-hallucination measure in the
   exercise, and the reason the data is small enough to check by hand.

## The data

```
data/
  incidents/     three incident reports, as a stressed human would write them
  logs/          seven log files across the platform, one shared corpus
  changes/       the change log: releases, config, flags, infrastructure, partner changes
  runbook/       five current runbooks owned by different squads, plus an archive
```

The logs are one corpus covering all three incidents plus unrelated day to day noise. A search
returns lines from incidents you are not working on. That is deliberate: filtering is part of
the job. The change log works the same way.

There is no master runbook and no index of symptoms. Entries are spread across files owned by
different squads, and `data/runbook/_archive/` holds a superseded runbook that is still
searchable. Some of its advice is now known to be wrong.

The incident reports contain guesses from the person who raised them. Some of those guesses
are wrong. Taking the reporter's theory at face value is the most common way to fail this
exercise.

Start with **INC-2043**. The other two are for the iteration phase.

## Contracts

- [docs/tool-contracts.md](docs/tool-contracts.md): exact input and output shape for
  `search_logs`, `search_changes`, `search_runbook` and `post_update`.
- [docs/output-contract.md](docs/output-contract.md): the shape of the final triage result
  your orchestrator produces.

## Suggested two hour plan

| Time | Activity |
|------|----------|
| 0:00 - 0:15 | Read this brief and INC-2043. Skim the data. Work out by hand, as a human, what you think happened. Write it down. You are now the benchmark. |
| 0:15 - 0:40 | Implement the three search tools against `docs/tool-contracts.md` and test them directly, with no model involved. They share most of their logic. |
| 0:40 - 1:05 | Build the log analyst: prompt, loop, tool call handling, structured result. Get it working alone. |
| 1:05 - 1:15 | Build the change historian. It is the same shape as the analyst with a different prompt and tool, so it should be quick. If it is not, your analyst is not as reusable as you thought, which is worth noticing. |
| 1:15 - 1:35 | Orchestrator: fan out to both concurrently, join, then call the runbook lookup with the joined symptom. |
| 1:35 - 1:55 | Run INC-2043 end to end. Iterate the prompts until the output matches what you wrote down at 0:15. Then try INC-2051 and INC-2062. |
| 1:55 - 2:00 | Write up what broke and what you changed. Compare with the group. |

If you are behind at 1:15, hard code the runbook agent's answer and get the fan-out and join
working. The parallel step is the part of this exercise you cannot get from a tutorial.

## Self-check

You have got there when all of these hold. Check them yourself; the data is small enough to
verify every citation by hand, and doing so is part of the exercise.

1. One command runs the whole thing for a given incident id.
2. The log analyst and the change historian genuinely run **concurrently**, and the total run
   takes about as long as the slower of the two, not the sum of both.
3. On **INC-2043** the system identifies the correct root cause, gives a start time, and cites
   evidence from **both** the logs and the change log. Neither corpus contains the whole
   answer.
4. The output says what correlated with what, rather than asserting a cause and listing
   citations underneath it.
5. It explicitly **rules out** the theory in the incident report, with evidence, rather than
   ignoring it.
6. It surfaces the matching **current** runbook entry and its concrete remediation steps, and
   is not taken in by the archived entry that keyword-matches just as well.
7. On **INC-2062** it reports that no runbook entry matches, instead of stretching the nearest
   one to fit. (This is the trap. Most first attempts fail here.)
8. The final output validates against `docs/output-contract.md`.
9. No specialist can see another specialist's tool or findings.

## Iteration prompts for the second hour

When it works, make it fail, and then make it not fail:

- Make one parallel agent fail (throw, or return nothing). Does the orchestrator hang, crash,
  or degrade to a partial answer with lower confidence? Which of those did you intend?
- Make one parallel agent slow. Add a timeout. What should the orchestrator do with a
  half-finished fan-out, and does its confidence rating reflect that?
- Ask for a confidence level on the root cause. Does it drop when you delete the change log?
  It should.
- What happens if `search_logs` returns nothing for every query the analyst tries? Does it
  admit that, or invent a timeline?
- Cap each specialist at three tool calls. What breaks, and what does that tell you about how
  they were searching?
- Give the runbook lookup a symptom description with one word changed ("timeout" to
  "latency"). Does it still find the right entry?
- Have the orchestrator send a second, narrower question back to one specialist after seeing
  the runbook entry. This is the smallest step from a pipeline towards a real agent loop.
- Run the same incident five times without changing anything. How stable is the answer?

## Stretch goals

- Add the comms drafter and the `post_update` stub.
- Add a **critic** pass: a fourth call that checks every claim in the merged result has a
  citation that actually exists in the data, and sends it back if not.
- Add a fourth parallel specialist of your own design and see what the orchestrator's join
  logic costs you. This is the question that decides whether your design scales.
- Give the orchestrator a tool call budget across all agents and make it degrade gracefully
  when it runs out.
- Add a golden test: assert the INC-2043 run names the right root cause and cites at least one
  supporting line from each corpus, then run it ten times to see how stable your prompts
  really are.
- Run all three incidents in one go and produce a single ranked action list.

## Debrief questions

- Where did your orchestrator's logic want to become a model call, and did you let it?
- What did the join actually cost? Was it prompt work, code, or both?
- Which failures were prompt problems and which were architecture problems?
- What did the evidence citation requirement cost you, and what did it buy you?
- If a fourth specialist arrived tomorrow, what would you have to change?
