# Case 02 — Solution

## Analysis

**Primary failure mode:** Hallucination Bait — the prompt requests information the model cannot reliably have (recent version changelogs, specific 2025 features) and provides no grounding context.

**Why this fails:**
- LLMs have a training data cutoff; they do not have access to real-time information
- When asked for specific version numbers and "exact changelog entries," the model has two options: refuse, or hallucinate. Most models hallucinate — they produce plausible-sounding but fabricated version histories
- The instruction "list every new hook added in 2025" is not verifiable by the model; it will produce a confident list of invented hooks
- The words "exact" and "latest" create false certainty without providing any grounding source

## Fixed Version — Three Approaches

### Approach A: Supply the Grounding (RAG)

Copy the actual changelog from the React docs and inject it:

```
You are a React documentation assistant. Answer the user's question using ONLY
the information in the <context> section below. If the context does not contain
the answer, say "I don't have that information in the provided documentation."

<context>
[Paste content from https://react.dev/blog/2025/... React 19 release notes]
</context>

User question: What new hooks were added in React 19? List their names, signatures,
and intended use cases.
```

### Approach B: Clarify Knowledge Boundary (No external context)

```
You are a React expert with knowledge up to your training cutoff. I am asking about
React 19 features.

Important instruction: If you are uncertain whether a feature exists in React 19
specifically, or if you cannot verify a specific version number, say so explicitly.
Do NOT fabricate changelog entries or version numbers. Distinguish between:
- Features you are confident about
- Features you believe may exist but cannot confirm
- Information you do not have

With that in mind: what React 19 features do you know about with confidence?
```

### Approach C: Redirect to a Reliable Source

```
You cannot provide real-time changelog data. Instead:
1. Tell me what React 19 features you know about as of your training data.
2. List the official sources I should check for the most current information
   (e.g., react.dev/blog, GitHub releases).
3. Flag any claims that might be out of date.
```

## Key Lesson

For any query involving "latest," "current," "2024/2025," specific version numbers, or exact reference data: either provide the grounding context yourself (RAG pattern, Module 5 §5.1), or instruct the model to acknowledge uncertainty boundaries rather than hallucinate.
