# ADR-004: JSON schema constraints over natural language format instructions

**Status:** Accepted
**Date:** 2026-02-15
**Context module:** [Core Principles](../02-core-principles.md) | [Best Practices](../04-best-practices.md)

## Context

We built a code review assistant that analyses pull request diffs and produces
structured feedback. Each piece of feedback includes a severity level, the
affected file and line range, a description of the issue, and a suggested fix.
Downstream systems consume this output programmatically to post inline
comments on the pull request.

The initial prompt used natural language format instructions:

> For each issue, output the severity (critical, warning, or info), the file
> path, the line numbers, a description of the issue, and your suggested fix.
> Separate each issue with a blank line.

This approach produced three recurring problems:

1. **Parse failures.** The model's output format varied between runs: sometimes
   it used bullet points, sometimes numbered lists, sometimes markdown tables.
   Our parser broke on roughly 12 % of responses.
2. **Missing fields.** The model occasionally omitted the suggested fix or the
   line range, especially when the issue was conceptual rather than
   line-specific. Downstream systems crashed on missing fields.
3. **Extra commentary.** The model frequently added preamble ("Here are the
   issues I found:") and postscript ("Let me know if you need more details")
   that the parser had to strip out, adding fragility.

## Decision

Replace the natural language format instructions with an explicit JSON schema
constraint. The prompt now specifies:

1. The exact JSON schema the output must conform to, including required
   fields, enum values for severity, and type constraints.
2. A directive to output **only** the JSON array with no surrounding text.
3. One complete example showing the expected structure.

The schema:

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["severity", "file", "line_start", "line_end", "description", "suggestion"],
    "properties": {
      "severity": { "type": "string", "enum": ["critical", "warning", "info"] },
      "file": { "type": "string" },
      "line_start": { "type": "integer" },
      "line_end": { "type": "integer" },
      "description": { "type": "string" },
      "suggestion": { "type": "string" }
    }
  }
}
```

Where the model's API supports native JSON mode or structured output mode, we
enable it. Where it does not, the schema is included in the prompt text and
the output is validated post-hoc with a JSON Schema validator.

## Rationale

Structured output schemas address all three problems by shifting format
compliance from a soft instruction the model may interpret loosely to a hard
constraint it must satisfy:

1. **Deterministic parsing.** JSON is unambiguous to parse. The downstream
   system calls `JSON.parse()` and validates against the schema. No regex, no
   heuristic stripping [Brown2020].

2. **Field completeness.** The `required` array in the schema makes missing
   fields a validation error. When the model cannot determine a line range, it
   must still provide a value (we instruct it to use `-1` for conceptual
   issues), making the absence explicit rather than silent.

3. **No extraneous text.** JSON mode (where available) or the "output only
   JSON" directive eliminates preamble and postscript. The parser receives
   exactly what it expects.

4. **Schema as documentation.** The JSON schema serves double duty: it
   constrains the model's output *and* documents the API contract for
   downstream consumers. A single source of truth reduces drift between the
   prompt and the parser.

## Alternatives Considered

### Alternative A: Markdown with strict delimiters

Use a structured markdown format with XML-like tags:

```
<issue>
<severity>warning</severity>
<file>src/auth.py</file>
...
</issue>
```

**Pros:** More readable in logs than JSON. Models are generally good at
producing XML-like structures.
**Cons:** Still requires a custom parser. No standard validation library
equivalent to JSON Schema validators. The model occasionally self-closed tags
or nested them incorrectly. No native "XML mode" in any major model API.

Rejected because it offered worse tooling support than JSON without
meaningful advantages.

### Alternative B: YAML output

Use YAML instead of JSON for the structured output.

**Pros:** More human-readable than JSON. Supports comments.
**Cons:** YAML parsing is notoriously sensitive to indentation. Models
frequently produce invalid YAML by misaligning nested keys. No model API
offers a native "YAML mode". Indentation errors are harder to diagnose than
JSON syntax errors.

Rejected because YAML's indentation sensitivity made it unreliable as an
LLM output format.

### Alternative C: Natural language with few-shot examples

Keep the natural language format instruction but add three few-shot examples
showing the exact expected format.

**Pros:** Simpler prompt. Examples anchor the model's formatting behaviour
effectively in many cases [Brown2020].
**Cons:** Reduced but did not eliminate format variation. In testing, parse
failure rate dropped from 12 % to 4 % -- an improvement, but still
unacceptable for a production pipeline processing hundreds of PRs daily.
The few-shot examples consumed significant context window space.

Rejected because 4 % parse failure rate exceeded our reliability target of
< 0.5 %.

### Alternative D: Post-processing with a second LLM call

Let the model output in any format, then use a second prompt to extract and
structure the data into JSON.

**Pros:** Decouples content generation from formatting. The extraction prompt
can be simpler and more reliable.
**Cons:** Doubles latency and cost. Introduces a potential information-loss
step (the extractor might misinterpret the free-form output). Adds pipeline
complexity for a problem that schema constraints solve more directly.

Rejected because it was an unnecessarily complex solution to a problem with
a simpler fix.

## Consequences

### Positive

- Parse failure rate dropped from 12 % to 0.2 %. The remaining 0.2 % are
  caught by schema validation and retried automatically (one retry succeeds
  in all observed cases).
- Missing-field errors dropped to zero. The schema validator rejects
  incomplete output before it reaches downstream systems.
- Development velocity improved: new fields can be added to the schema, and
  both the prompt and the parser update from the same schema definition file.
- The approach has been adopted as a team standard for all prompts that
  produce machine-consumed output.

### Negative

- JSON output is less readable in logs and debugging sessions compared to
  natural language. Mitigated by adding a pretty-print log formatter.
- The prompt is slightly longer due to the embedded schema (~120 tokens).
  This is negligible relative to the diff content that constitutes the bulk
  of the input.
- Models occasionally produce valid JSON that passes schema validation but
  contains low-quality content (e.g., a generic suggestion like "consider
  refactoring this"). The schema enforces structure, not quality. Content
  quality is addressed through the system message and exemplars.

### Risks

- Schema evolution requires coordinated updates to the prompt template, the
  validation logic, and downstream consumers. Mitigated by generating all
  three from a single schema definition file.
- Over-constraining the schema could prevent the model from expressing
  nuanced feedback. For example, a rigid severity enum might not capture the
  difference between "this will crash in production" and "this might cause
  issues under load". Mitigated by keeping the schema pragmatically minimal
  and using the `description` field for nuance.
- Not all model providers support native JSON mode. For those that do not,
  the schema-in-prompt approach is slightly less reliable. Monitor parse
  failure rates per provider.

## Related Decisions

- [ADR-002: Split planner-executor](002-split-planner-executor.md) -- the
  planner's output uses this same schema-constraint pattern.
- [ADR-001: Few-shot over fine-tuning](001-few-shot-over-fine-tuning.md) --
  discusses when few-shot examples alone are sufficient vs. when harder
  constraints are needed.
- [Core Principles](../02-core-principles.md) -- covers output specification
  and determinism.
- [Best Practices](../04-best-practices.md) -- discusses structured output
  patterns and validation strategies.
