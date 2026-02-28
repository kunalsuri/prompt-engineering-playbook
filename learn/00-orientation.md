# Module 0 — Orientation: A Story About Better Prompts

> **Who this is for:** Anyone. No programming experience needed. No prior AI knowledge required. This module is a 15-minute story that shows you what prompt engineering looks like *before* you learn any vocabulary or theory.

---

## The Story

Maya is writing a college application essay. She opens a browser, types into an AI assistant, and hits Enter.

---

### Attempt 1

**Maya types:**
> "Help me with my college essay."

**The AI replies:**
> "Of course! College essays are important. What topic are you writing about? Make sure your essay is personal, authentic, and shows growth. Consider starting with a hook. Proofread carefully for grammar."

Maya stares at the screen. *That's... generic advice I could find anywhere.* She wanted a draft, not a lecture.

**What went wrong?** The AI had no idea what to write. "Help me" could mean a thousand things: write a draft, give feedback, brainstorm topics, fix grammar, or just listen. The AI guessed wrong.

---

### Attempt 2

Maya tries again, adding more detail.

**Maya types:**
> "Write a college essay about how I learned resilience."

**The AI replies:**
> "Title: Learning Resilience
>
> Resilience is a quality that many people value. I have faced challenges in my life that taught me to be resilient. For example, when I was in high school, I faced a setback. This made me stronger. In conclusion, resilience is important and I have it."

Maya cringes. *It's technically an essay about resilience. But it sounds like a robot wrote it — because it did.*

**What went wrong?** The topic is there, but the AI doesn't know *her* story, her voice, or what kind of essay she wants. It filled the gap with generic filler.

---

### Attempt 3

A teacher had told Maya to "be specific." She decides to try it.

**Maya types:**
> "Write a personal college essay for me. Here is some background:
>
> - I started a small plant business during COVID when my family lost income. I was 16.
> - I failed the first two months — killed 40 plants, lost $200. I almost quit.
> - A retired florist neighbor named Gloria taught me to read soil and light conditions.
> - By month 6, I had 12 steady customers and was earning $300/month.
>
> Tone: reflective and personal, not boastful. Length: 300–400 words. Audience: college admissions officer.
> Start with a specific scene, not a generic statement."

**The AI reply now starts:**
> "The third time the spider plant drooped, I cried — not because I'd lost another $12, but because I'd promised myself this time would be different.
>
> I was sixteen, our family's income had just collapsed, and I'd decided — with the unearned confidence that only teenagers possess — that I could grow and sell houseplants out of our garage..."

Maya reads it twice. *That's my story. That sounds like me.*

**What changed?** Maya gave the AI:
- **Her actual content** (the plant story, the neighbor, the numbers)
- **A specific tone** (reflective, not boastful)
- **A format constraint** (300–400 words, scene-first opening)
- **An audience** (admissions officer, not a general reader)

---

## What Just Happened

Maya ran the same experiment three times with the same AI, on the same topic. The AI didn't change. *Her prompt did.*

This is prompt engineering in its simplest form:

| Attempt | What Maya gave | What she got |
|---------|---------------|--------------|
| 1 | A vague request | Generic advice |
| 2 | A topic | A hollow draft |
| 3 | Her story + constraints + format | A personal, usable essay |

The difference was not the AI's intelligence. The difference was **how clearly Maya communicated her intent**.

---

## The Five Things Maya Learned to Include

Looking back at Attempt 3, you can see five ingredients:

1. **Who should "speak"** — an authentic personal voice, not a generic one
2. **Background** — the specific facts (plant business, Gloria, the numbers)
3. **The task** — "write a personal college essay"
4. **Constraints** — tone, length, audience
5. **Format** — start with a scene, not a statement

These five ingredients have names in the rest of this curriculum:

| Ingredient | Curriculum Name | Where to Learn More |
|-----------|----------------|---------------------|
| "Who should speak" | **Role** | Module 1 §1.3 |
| Background | **Context** | Module 1 §1.3 |
| The task | **Task** | Module 1 §1.3 |
| Constraints | **Constraints** | Module 1 §1.3 |
| Format / Example | **Examples** | Module 1 §1.3 |

---

## Try It Before You Continue

Pick one task you actually want to do with an AI today — anything. It could be:

- Explaining a concept you're trying to learn
- Drafting a message you need to send
- Getting recipe ideas for what's in your fridge

Write your first draft of a prompt. Then ask: *What would Maya add to make this more like Attempt 3?*

You don't need to get it perfect. You just need to notice the difference between vague and specific.

---

## Where to Go Next

You've just seen the core idea. The rest of the curriculum gives it names, teaches the patterns behind it, and shows you how to use it systematically — whether you're writing essays, writing code, or building AI-powered products.

- **If you're new to AI and not a programmer:** Continue with [Module 1](01-introduction.md), then follow the [Beginner's Guide](beginners-guide.md).
- **If you're a developer:** Skim [Module 1](01-introduction.md) and jump to [Module 3 — Patterns](03-patterns.md).
- **If you already know prompt basics:** Start at [Module 4 — Best Practices](04-best-practices.md) or [Module 5 — Advanced Patterns](05-advanced-patterns.md).

---

[Module 1 →](01-introduction.md) · [Back to curriculum](README.md)
