# ADR-001: Few-shot prompting over fine-tuning for classification

**Status:** Accepted
**Date:** 2026-02-15
**Context module:** [Core Principles](../02-core-principles.md) | [Patterns](../03-patterns.md)

## Context

Our team needed to classify incoming customer support tickets into one of 12
categories (billing, account-access, bug-report, feature-request, etc.). The
classifier feeds a routing system that assigns tickets to the correct
specialist queue.

Key constraints:

- The category taxonomy changes roughly once per quarter as the product evolves.
- We had approximately 800 labelled examples at the time of the decision, unevenly
  distributed across categories (some had fewer than 20 examples).
- The system needed to be operational within two weeks.
- The team had prompt engineering experience but limited ML-ops infrastructure
  for training and serving custom models.
- Accuracy target: at least 90 % agreement with human labellers on a held-out
  test set of 200 tickets.

## Decision

Use few-shot prompting with a foundation model (Claude) rather than
fine-tuning a custom classifier. The prompt includes:

1. A system message defining the role and the complete taxonomy with one-line
   descriptions of each category.
2. Eight carefully selected exemplar tickets (few-shot examples) covering edge
   cases and commonly confused categories.
3. An instruction to output only the category label, followed by a one-sentence
   justification to enable lightweight auditing.

## Rationale

Few-shot prompting was favoured for three main reasons:

1. **Iteration speed.** Updating the taxonomy requires editing the prompt, not
   retraining a model. Given quarterly taxonomy changes, this reduces ongoing
   maintenance from days to minutes. This aligns with the principle of
   keeping prompts easily auditable and version-controllable
   [Brown2020].

2. **Low data regime.** Several categories had fewer than 20 examples --
   insufficient for reliable fine-tuning. Few-shot prompting leverages the
   model's pre-trained knowledge to generalise from a handful of exemplars
   [Brown2020].

3. **Infrastructure simplicity.** The team could deploy the classifier as a
   single API call without building training pipelines, model registries, or
   GPU serving infrastructure.

On the held-out test set the few-shot prompt achieved 93 % accuracy, exceeding
the 90 % target. The three most confused category pairs were identified and
addressed by adding targeted exemplars for those pairs.

## Alternatives Considered

### Alternative A: Fine-tuning a smaller model

Fine-tuning a model like `distilbert-base` on the 800 labelled examples would
have produced a fast, cheap-to-serve classifier. However:

- The uneven label distribution would have required data augmentation or
  class-weighting strategies the team was not experienced with.
- Every taxonomy change would trigger a retrain-evaluate-deploy cycle.
- The two-week timeline did not leave room for ML-ops setup.

Rejected because maintenance cost and timeline risk were too high.

### Alternative B: Zero-shot classification (no exemplars)

A simpler prompt with just the taxonomy definitions and no examples. Early
testing showed 84 % accuracy -- below the 90 % target -- particularly failing
on the subtle distinction between "bug-report" and "feature-request" tickets.

Rejected because accuracy was insufficient without exemplars to anchor
the model's understanding of boundary cases.

### Alternative C: Retrieval-augmented few-shot (dynamic example selection)

Instead of static exemplars, retrieve the most similar past tickets from a
vector store and inject them at inference time. This is a strong approach but:

- Required building and maintaining an embedding index.
- Added latency (~200 ms for retrieval on top of LLM inference).
- Introduced a dependency on the vector store's availability.

Deferred as a future enhancement if accuracy degrades when the taxonomy grows
beyond 20 categories.

## Consequences

### Positive

- Achieved 93 % accuracy, exceeding the target.
- Deployed within one week, well ahead of the two-week deadline.
- First taxonomy update (adding a "security-incident" category) took 15
  minutes: add the definition, add one exemplar, run the test set.
- The one-sentence justification output enables human auditors to spot-check
  the classifier's reasoning at scale.

### Negative

- Per-ticket inference cost is higher than a fine-tuned model (~$0.002 per
  ticket vs. ~$0.0001). At current volume (5,000 tickets/day) this is
  approximately $10/day, which is acceptable but not negligible.
- Latency is ~1.2 seconds per classification vs. ~50 ms for a fine-tuned
  model. Acceptable for an async routing system but would be problematic for
  real-time, user-facing classification.

### Risks

- If ticket volume grows 10x, cost becomes significant. Mitigated by
  monitoring monthly spend and re-evaluating fine-tuning if costs exceed the
  threshold.
- Prompt injection: a malicious ticket could attempt to override the
  classification instructions. Mitigated by input sanitisation and the
  constrained output format. See [ADR-003](003-add-safety-gate.md) for the
  safety-gate pattern.
- Model updates could shift classification behaviour. Mitigated by running the
  held-out test set after each model version change.

## Related Decisions

- [ADR-003: Add safety-gate validation prompt](003-add-safety-gate.md) --
  addresses prompt injection risk for this classifier.
- [Patterns module](../03-patterns.md) -- covers few-shot prompting patterns
  in depth.
- [Core Principles](../02-core-principles.md) -- discusses when to prefer
  prompting over training.
- Comparison: [Few-shot comparison](../comparisons/few-shot-comparison.md)
