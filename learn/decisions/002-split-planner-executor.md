# ADR-002: Split monolithic prompt into planner + executor pipeline

**Status:** Accepted
**Date:** 2026-02-15
**Context module:** [Advanced Patterns](../05-advanced-patterns.md) | [Agentic Patterns](../06-agentic-patterns.md)

## Context

We had a single large prompt that accepted a codebase diff and a refactoring
goal (e.g., "migrate all class components to functional components with hooks")
and attempted to produce the complete refactored code in one pass.

The prompt worked acceptably on small diffs (< 200 lines) but exhibited three
failure modes at scale:

1. **Dropped changes.** On diffs exceeding ~500 lines the model would silently
   skip files or hunks, producing incomplete refactors.
2. **Inconsistent strategy.** The model would apply different migration
   patterns to similar components within the same diff, because it chose its
   approach locally for each component rather than planning globally.
3. **Difficult debugging.** When the output was wrong it was hard to tell
   whether the model misunderstood the goal, chose a bad strategy, or simply
   ran out of context window capacity.

The system needed to handle diffs of up to 2,000 lines reliably.

## Decision

Decompose the single prompt into a two-stage pipeline:

**Stage 1 -- Planner.** Receives the full diff and the refactoring goal.
Outputs a structured plan in JSON:

- A list of files to modify, in dependency order.
- For each file, the specific transformation to apply, referencing named
  patterns (e.g., "classToFunction", "lifecycleToEffect").
- Any cross-file constraints (e.g., shared type changes, import updates).

**Stage 2 -- Executor.** Receives one file at a time along with the relevant
slice of the plan. Outputs the refactored code for that single file. The
executor runs in a loop, once per file, so each invocation operates within a
manageable context window.

A lightweight validation step between stages checks that the plan references
only files present in the diff and that every file in the diff is accounted
for.

## Rationale

This decomposition follows the well-established planning-then-execution
pattern described in the chain-of-thought and task-decomposition literature
[Wei2022] [Yao2023]. The key insight is that planning and execution place
different demands on the model:

- **Planning** requires broad context (the full diff) but produces a small
  output (a structured plan). The model can devote its capacity to reasoning
  about relationships between files.
- **Execution** requires deep, focused context (one file plus its plan entry)
  and produces a large output (the refactored code). By narrowing the input,
  we reduce the chance of dropped content.

Separating the stages also creates a natural **observability boundary**. If the
output is wrong, we inspect the plan first. If the plan is correct, the bug is
in execution; if the plan is wrong, we improve the planner prompt. This aligns
with the debugging principles in the [prompt debugging guide](../prompt-debugging.md).

## Alternatives Considered

### Alternative A: Chunked single-prompt (sliding window)

Split the diff into overlapping chunks and run the original monolithic prompt
on each chunk independently.

**Pros:** Minimal prompt rewrite; parallelisable.
**Cons:** No global strategy -- each chunk is refactored in isolation, leading
to the same inconsistency problem. Overlapping regions can produce conflicting
edits. Merging outputs requires a non-trivial reconciliation step.

Rejected because it traded one problem (context overflow) for another
(inconsistency), without solving the core issue.

### Alternative B: Fine-tuned code-refactoring model

Train a specialised model on refactoring examples to handle large diffs
natively.

**Pros:** Potentially faster inference; could learn project-specific patterns.
**Cons:** Requires a large, high-quality training dataset of before/after
refactors that we did not have. Training and serving infrastructure was out of
scope. The approach is brittle to new refactoring types not seen in training.

Rejected due to data requirements and infrastructure cost.

### Alternative C: Three-stage pipeline (planner + executor + reviewer)

Add a third stage where a reviewer prompt checks the executor's output against
the plan and the original code, requesting corrections if needed.

**Pros:** Higher reliability through self-verification.
**Cons:** Doubles latency and cost for marginal accuracy gains in initial
testing (plan accuracy was already 97 %). The reviewer often "hallucinated"
issues that did not exist, creating false-positive correction loops.

Deferred. May revisit if executor accuracy drops below 90 % on larger diffs.

## Consequences

### Positive

- Diffs of up to 2,000 lines are handled reliably. The planner correctly
  identifies all files in 97 % of test cases. The executor produces correct
  refactors for 94 % of files (up from 71 % with the monolithic prompt).
- Debugging time dropped roughly 60 %. Inspecting the structured plan
  immediately reveals whether the model understood the goal.
- The executor can run in parallel across files when there are no
  cross-file dependencies, reducing wall-clock time by ~40 % for large diffs.
- The planner's JSON output is version-controllable and reviewable in pull
  requests before execution begins.

### Negative

- Total token usage increased by approximately 30 % due to repeated context
  in executor calls and the planning overhead.
- The pipeline is more complex to maintain: two prompt templates, a validation
  step, and orchestration logic instead of a single prompt.
- Latency increased for small diffs (< 100 lines) where the monolithic prompt
  was already reliable. We added a size-based router to skip the planner for
  trivially small diffs.

### Risks

- Plan drift: if the planner's output schema evolves, the executor prompt must
  be updated in lockstep. Mitigated by defining the plan schema in a shared
  JSON Schema file used by both prompts.
- Over-decomposition: splitting into too many stages can introduce error
  propagation. We deliberately stopped at two stages after testing showed
  diminishing returns from a third. Monitor executor accuracy quarterly.

## Related Decisions

- [ADR-004: Structured output schema](004-structured-output-schema.md) --
  the planner's JSON output uses the schema-constraint pattern documented
  there.
- [Advanced Patterns](../05-advanced-patterns.md) -- covers task decomposition
  and chain-of-thought prompting.
- [Agentic Patterns](../06-agentic-patterns.md) -- discusses planner-executor
  and multi-agent orchestration patterns.
- Comparison: [Chain-of-thought comparison](../comparisons/chain-of-thought-comparison.md)
