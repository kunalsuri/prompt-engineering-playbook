# Beginner's Reading Guide

**New to prompt engineering — or new to AI entirely?** This page gives you a structured path through the curriculum that avoids jargon overload and builds your understanding step by step.

You do **not** need any programming experience for the first three sections below. Sections marked with a code icon (💻) are more rewarding if you can try things in an LLM like ChatGPT, Claude, or GitHub Copilot — but reading alone still works.

---

## Before You Start

Open the **[Glossary](glossary.md)** in a second tab or window. Any time you hit an unfamiliar term — *token*, *context window*, *hallucination*, *few-shot* — look it up there before moving on. The glossary is short and plain-language.

---

## Recommended Reading Order

### Phase 1 — "What is this?" (30 min)

Read **[Module 1 — Introduction](01-introduction.md)** in full.

- **Key sections:** §1.1 (What Is Prompt Engineering?) uses a search-engine analogy that translates directly to everyday experience. §1.2 shows a side-by-side comparison of a bad prompt vs. a good one — this is the single most important example in the whole curriculum.
- **Diagram to study:** The prompt-anatomy flowchart in §1.3 (Role → Context → Task → Constraints → Examples). Memorize these five components — every later module builds on them.
- **Exercise to try:** Exercise 1.1 (rewrite "Summarize this research paper" using all five components). The [reference solution](solutions/exercise-solutions.md#exercise-11-prompt-decomposition) is available if you get stuck.
- **What to skip on first pass:** The References section at the bottom — you can come back to the cited papers later.

### Phase 2 — "How do I think about this?" (30 min)

Read **[Module 2 — Core Principles](02-core-principles.md)**, focusing on §2.1 (Specificity) and §2.3 (Iteration).

- **Key idea from §2.1:** The *Substitution Test* — if you can replace a word in your prompt with a completely different word and the prompt still makes sense, that word is too vague. Example: "Improve the code" → improve *how*? Replace "improve" with "reduce the cyclomatic complexity to 5 or less" and the vagueness disappears.
- **Key idea from §2.3:** Prompting is not one-shot. You write, test, diagnose, revise, and repeat — just like editing an essay draft.
- **Diagram to study:** The iteration-loop flowchart in §2.3 (Write → Run → Diagnose → Revise → Write).
- **What to skip on first pass:** §2.2 (Decomposition) uses software engineering examples. Read it if you code; skip it if you don't — you can return after Phase 3.

### Phase 3 — "What patterns can I use?" (45 min)

Read **[Module 3 — Patterns](03-patterns.md)**, but focus on these three patterns first:

1. **§3.1 Zero-shot** — Give the model a clear instruction and nothing else. This is what you do most of the time already.
2. **§3.3 Few-shot** — Show the model 2–3 examples of what you want, then ask it to do the same for a new input. This is the single highest-impact technique for beginners.
3. **§3.5 Role-playing** — Tell the model who to be ("You are a patient biology tutor for a 10th-grader"). This changes the tone, depth, and vocabulary of the response.

- **What to skip on first pass:** §3.4 (Chain-of-Thought) and §3.7 (ReAct) involve multi-step reasoning chains. They are powerful but more abstract — save them for your second read-through.
- **Exercise to try:** Exercise 3.3 (design a few-shot prompt vs. a zero-shot prompt for the same task and compare them). 💻

### Phase 4 — "What can go wrong?" (20 min, selective reading)

In **[Module 4 — Best Practices](04-best-practices.md)**, read only:

- **§4.5 Common Anti-Patterns.** This is the most universally useful section — it names five mistakes that everyone makes (Kitchen-Sink Prompt, Implicit Assumption, Copy-Paste Drift, Untested Prompt, Stale Prompt). If you read nothing else in Module 4, read this.
- **§4.1 first two paragraphs** (Token Budget Management) — just enough to understand that LLMs have a maximum input size and that stuffing too much in degrades quality.

- **What to skip:** §4.2 (Context-Window Optimization), §4.3 (Version Control for Prompts), §4.4 (Team Workflows), and §4.6 (Prompt Versioning with Git). These are aimed at professional developers managing prompt files in code repositories.

### Phase 5 — Optional deep dives

Once you are comfortable with Phases 1–4:

- **[Worked Examples](prompt-examples/prompt-patterns-in-practice.md)** — six before/after prompt comparisons that reinforce Module 3.
- **[Few-Shot Comparison](comparisons/few-shot-comparison.md)** — the most beginner-friendly comparison doc — shows zero-shot vs. one-shot vs. few-shot with concrete examples.
- **Module 5 §5.2 (Adversarial Robustness)** — fun to read even without a technical background because it reads like a security detective story: "What happens if someone tricks the AI?"

---

## Beginner-Friendly Exercise Alternatives

The main exercises assume programming experience. Here are alternative versions of the harder exercises that work without code:

### Alternative for Exercise 1.1 (Prompt Decomposition)

The original exercise asks you to rewrite "Summarize this research paper" using all five prompt components. Here's a non-technical version:

1. Imagine you want an LLM to summarize a news article you just read.
2. Write your prompt using all five parts from the Module 1 diagram:
   - **Role:** "You are a newspaper editor writing for a general audience."  
   - **Context:** Paste the article (or describe it: "The article is about X, published in Y, and covers Z.")  
   - **Task:** "Summarize this article in 3 sentences, focusing on the main argument."  
   - **Constraints:** "Use simple language a 15-year-old would understand. Do not add opinions."  
   - **Examples:** Provide one example summary from a different article to show the style you want.
3. Try your prompt in an LLM. Does the summary match what you expected? If not, which of the five parts was too vague?

**What you learn:** Every good prompt has the same five ingredients, whether it's about code or about summarizing the news.

### Alternative for Exercise 1.2 (Ambiguity Identification)

The original exercise asks you to find ambiguities in "Write tests for the User model." Here's a non-technical version:

1. Consider this vague request to an LLM: *"Write me a good essay about climate."*
2. List everything that's unclear. Try for at least five. For example:
   - How long should the essay be? (200 words? 2000 words?)
   - What aspect of climate? (Change? Policy? Science? History?)
   - Who is the audience? (Teacher? Blog reader? Scientist?)
   - What tone? (Formal academic? Casual blog post?)
   - Should it include citations?
   - What format? (Five-paragraph essay? Argumentative? Informational?)
3. Rewrite the prompt so that all six ambiguities are eliminated.
4. Test both the vague and the specific version in an LLM. Compare the outputs.

**What you learn:** Vague prompts produce unpredictable results. Every ambiguity is a coin flip the AI makes for you — and it might flip the wrong way.

### Alternative for Exercise 2.1 (Specificity Audit)

Instead of auditing a prompt file from the `prompts/` directory, do this:

1. Write a prompt to an LLM that you've used before (e.g., "Help me write an email to my teacher asking for an extension").
2. For every word or phrase in your prompt, ask yourself: "Could I replace this with something more specific?" For example:
   - "email" → "a formal email of 4–6 sentences"
   - "my teacher" → "my high-school biology teacher, Mrs. Johnson"
   - "asking for an extension" → "requesting a 3-day extension on my lab report due Friday, because I was sick on Monday and Tuesday"
3. Rewrite the prompt with at least three substitutions.
4. Test both versions. Which one produces an email you'd actually send?

**What you learn:** The *Substitution Test* — if a word in your prompt could mean different things, replace it with the specific thing you actually meant.

### Alternative for Exercise 2.3 (Iteration Log)

Instead of iterating on a code-generation prompt, do this:

1. Pick a task you'd actually use an LLM for — for example, "Write a birthday message for my friend who loves hiking."
2. Write your first prompt. Copy the output into a note.
3. What's wrong with it? Too long? Too generic? Wrong tone? Write down your diagnosis.
4. Revise the prompt to fix what was wrong. Run it again. Copy the new output.
5. Repeat at least 3 times. Keep a simple log:

   | Version | What I Changed | What Got Better | What's Still Wrong |
   | --- | --- | --- | --- |
   | v1 | (original prompt) | — | Too formal, too long |
   | v2 | Added "casual tone, max 3 sentences" | Length is right | Still generic |
   | v3 | Added "mention the Appalachian Trail trip we took" | Personal and specific | Perfect |

**What you learn:** Nobody writes a perfect prompt on the first try. The iteration loop (write → test → diagnose → revise) is the core skill.

### Alternative for Exercise 3.2 (Pattern Selection)

Instead of selecting patterns for coding tasks, do this for everyday tasks:

For each task below, decide which pattern (from Module 3) would work best and explain your reasoning in one sentence:

1. **Ask an LLM to translate a menu from French to English.** (Hint: Is this straightforward enough for zero-shot, or do you need to show examples?)
2. **Ask an LLM to grade 10 student essays on a rubric.** (Hint: Should you show it one graded example first?)
3. **Ask an LLM to plan a 7-day road trip itinerary.** (Hint: Does this task benefit from step-by-step reasoning?)
4. **Ask an LLM to write a cover letter as if it were a hiring manager giving advice.** (Hint: What pattern assigns the AI a specific identity?)

**What you learn:** Pattern selection is about matching the technique to the task. You now have a toolkit of six strategies — the skill is knowing when to reach for each one.

### Alternative for Exercise 3.3 (Few-Shot Design)

Instead of comparing few-shot vs. zero-shot for a coding task, do this:

1. **Zero-shot version:** Ask an LLM: *"Classify the following movie review as Positive, Negative, or Neutral: 'The acting was wooden but the cinematography was stunning.'"*
2. **Few-shot version:** Give the LLM 2–3 examples first:
   ```text
   Classify movie reviews as Positive, Negative, or Neutral.

   Review: "A masterpiece of storytelling." → Positive
   Review: "Terrible plot, great soundtrack." → Neutral
   Review: "I walked out after 30 minutes." → Negative

   Review: "The acting was wooden but the cinematography was stunning." →
   ```
3. Run both versions 3 times each. Record the answers.
4. Which version was more consistent? Which gave the answer you expected?

**What you learn:** Showing examples (few-shot) often produces more consistent results than describing (zero-shot) — especially when the answer could go either way.

### Alternative for Exercise 4.1 (Token Budget Estimation)

Instead of estimating tokens for a prompt file, do this:

1. Open any LLM chat interface (ChatGPT, Claude, etc.).
2. Paste a short paragraph (3–4 sentences) and ask: *"How many tokens is this paragraph?"*
3. Now paste a long paragraph (15+ sentences) and ask the same question.
4. Compare: roughly how many characters per token? (The answer is usually around 4.)
5. If the LLM you are using has a character or word limit, calculate: how many paragraphs like your long one would fit before hitting the limit?

**What you learn:** LLMs have a hard size limit. Longer inputs leave less room for the answer. This is the core insight of §4.1.

### Alternative for Exercise 5.1 (RAG Prompt Design)

Instead of designing a RAG system for an API, do this:

1. Find a short Wikipedia article on a topic you know well (2–3 paragraphs).
2. Copy those paragraphs and paste them into an LLM chat with this instruction:

   ```text
   Answer my question using ONLY the information in the text below.
   If the text does not contain the answer, say "The provided text
   does not answer this question."

   [paste your Wikipedia paragraphs here]
   ```

3. Ask a question that IS answered in the text. Does the LLM use the text correctly?
4. Ask a question that is NOT in the text. Does the LLM admit it can't answer, or does it make something up?

**What you learn:** This is RAG in miniature — giving the model specific documents and telling it to stick to them. The challenge is making the model say "I don't know" when the answer isn't there.

### Alternative for Exercise 5.3 (Evaluation Pipeline)

Instead of designing a code-evaluation pipeline, do this:

1. Write a prompt that asks an LLM to translate a sentence from English to another language you know (or can verify with Google Translate).
2. Run the same prompt 5 times. Write down each translation.
3. Score each translation: Is it grammatically correct? Does it capture the meaning? Does it use natural phrasing?
4. Calculate your "pass rate" — how many of the 5 outputs were fully acceptable?

**What you learn:** Evaluation means running the same prompt multiple times and systematically checking the outputs. A prompt that works once might fail 2 out of 5 times — and that matters in production.

---

## Tips for Beginners

- **Start with the glossary.** Seriously. Five minutes there saves thirty minutes of confusion later.
- **Try prompts yourself.** Every concept clicks faster when you type a prompt into an LLM and see what happens. Free options: ChatGPT (free tier), Claude (free tier), Google Gemini.
- **Read the worked examples.** The [Prompt Patterns in Practice](prompt-examples/prompt-patterns-in-practice.md) document shows six real before/after comparisons — they're the fastest way to build intuition.
- **Don't read linearly.** If a section feels too technical, skip it and come back later. The Phase guide above is designed for exactly this.
- **The prompt templates in `prompts/` are for developers.** If you're not coding, you can safely ignore the entire `prompts/` directory — the `learn/` curriculum is self-contained.

---

[← Back to curriculum home](README.md) · [Start Module 1 →](01-introduction.md)
