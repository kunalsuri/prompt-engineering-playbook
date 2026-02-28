# Prompt Cookbook: Ready-to-Use Prompts for Everyday Tasks

## About This Cookbook

This collection provides **20 copy-paste prompts for non-programming tasks** — writing, analysis, research, communication, and decision-making. Each recipe identifies which pattern(s) from Module 3 it uses, so you can connect the theory to practice.

> **How to use:** Replace the `{placeholders}` with your content, paste into any LLM (ChatGPT, Claude, Gemini, Copilot, etc.), and refine the output to your needs.

---

## Quick Index

| # | Recipe | Category | Pattern(s) Used |
|---|--------|----------|-----------------|
| 1 | [Meeting Summary](#1-meeting-summary) | Communication | Zero-Shot, Constrained Output |
| 2 | [Email Drafting](#2-email-drafting) | Communication | Role-Playing, Zero-Shot |
| 3 | [Pros/Cons Analysis](#3-proscons-analysis) | Decision-Making | Chain-of-Thought, Constrained Output |
| 4 | [Resume Bullet Points](#4-resume-bullet-points) | Writing | Few-Shot, Constrained Output |
| 5 | [Research Summary](#5-research-summary) | Research | Zero-Shot, Constrained Output |
| 6 | [Slide Outline](#6-slide-outline) | Communication | Zero-Shot, Constrained Output |
| 7 | [Study Guide](#7-study-guide) | Learning | Chain-of-Thought |
| 8 | [Feedback Drafting](#8-feedback-drafting) | Communication | Role-Playing |
| 9 | [Creative Brainstorm](#9-creative-brainstorm) | Creativity | Zero-Shot |
| 10 | [Data Interpretation](#10-data-interpretation) | Analysis | Chain-of-Thought |
| 11 | [Travel Itinerary](#11-travel-itinerary) | Planning | Constrained Output |
| 12 | [Interview Prep](#12-interview-prep) | Career | Role-Playing, Few-Shot |
| 13 | [Document Comparison](#13-document-comparison) | Analysis | Chain-of-Thought, Constrained Output |
| 14 | [Social Media Post](#14-social-media-post) | Writing | Few-Shot, Constrained Output |
| 15 | [Lesson Plan](#15-lesson-plan) | Education | Zero-Shot, Constrained Output |
| 16 | [Negotiation Prep](#16-negotiation-prep) | Decision-Making | Role-Playing, Chain-of-Thought |
| 17 | [Bug Report](#17-bug-report) | Technical Writing | Constrained Output |
| 18 | [Book/Article Summary](#18-bookarticle-summary) | Research | Zero-Shot, Constrained Output |
| 19 | [Weekly Report](#19-weekly-report) | Communication | Constrained Output |
| 20 | [Explanation for Different Audiences](#20-explanation-for-different-audiences) | Communication | Role-Playing |

---

## Recipes

### 1. Meeting Summary

**Patterns:** Zero-Shot Instruction (§3.2), Constrained Output (§3.6)

```
Summarize the following meeting notes into a structured format:

## Decisions Made
- [list each decision]

## Action Items
- [ ] [owner]: [task] — due [date]

## Key Discussion Points
- [2-3 sentence summary of each major topic]

## Open Questions
- [any unresolved items]

Meeting notes:
---
{paste your meeting notes here}
---
```

---

### 2. Email Drafting

**Patterns:** Role-Playing (§3.5), Zero-Shot Instruction (§3.2)

```
You are a professional communicator who writes clear, concise emails.

Write an email with these parameters:
- To: {recipient and their role}
- Purpose: {what you need from them}
- Tone: {formal / friendly-professional / casual}
- Length: 3-5 sentences in the body
- Context: {any background they need}

Include a clear subject line. End with a specific call-to-action
(what you want them to do and by when).
```

---

### 3. Pros/Cons Analysis

**Patterns:** Chain-of-Thought (§3.4), Constrained Output (§3.6)

```
I need to decide between: {option A} vs. {option B}.

Context: {relevant background, constraints, priorities}

Analyze this decision step by step:

1. List 4-5 pros and 4-5 cons for each option.
2. For each pro/con, rate its importance (High / Medium / Low).
3. Identify the top 2 risks for each option.
4. Provide a recommendation with a one-paragraph justification.

Format as a comparison table where possible.
```

---

### 4. Resume Bullet Points

**Patterns:** Few-Shot Learning (§3.3), Constrained Output (§3.6)

```
Transform job responsibilities into achievement-oriented resume bullets.
Each bullet should follow the formula: [Action verb] + [What you did] +
[Quantified result or impact].

Examples:
- Input: "Managed social media accounts"
  Output: "Grew Instagram following by 45% (12K → 17.4K) in 6 months through data-driven content strategy and A/B-tested posting schedules"

- Input: "Helped with customer complaints"
  Output: "Resolved 200+ customer escalations monthly with 94% satisfaction rating, reducing average resolution time from 48 to 12 hours"

Now transform these responsibilities:
1. {responsibility 1}
2. {responsibility 2}
3. {responsibility 3}
```

---

### 5. Research Summary

**Patterns:** Zero-Shot Instruction (§3.2), Constrained Output (§3.6)

```
Summarize the following research paper/article for a {audience: e.g.,
"non-technical executive" / "graduate student" / "general audience"}.

Structure your summary as:
1. **Main Finding** (1 sentence)
2. **Why It Matters** (2-3 sentences connecting to real-world impact)
3. **Method** (1-2 sentences on how the research was conducted)
4. **Key Limitations** (1-2 sentences)
5. **So What?** (1 sentence on what the reader should do with this info)

Total length: 150-200 words.

Paper/article:
---
{paste the text or abstract here}
---
```

---

### 6. Slide Outline

**Patterns:** Zero-Shot Instruction (§3.2), Constrained Output (§3.6)

```
Create a presentation outline for a {duration: e.g., "15-minute"} talk.

Topic: {topic}
Audience: {who will be listening}
Goal: {what you want the audience to think/feel/do afterward}

For each slide, provide:
- Slide title
- 3-4 bullet points (key messages, not full sentences)
- Speaker notes (2-3 sentences of what to say)
- Suggested visual (chart type, image description, or "text only")

Include an opening hook slide and a closing call-to-action slide.
Aim for {number} slides total.
```

---

### 7. Study Guide

**Patterns:** Chain-of-Thought (§3.4)

```
I'm studying {topic} for a {context: exam / certification / personal learning}.

Create a study guide that:
1. Lists the 5-7 most important concepts I must understand.
2. For each concept:
   a. Provide a clear definition (1-2 sentences).
   b. Give a concrete example or analogy.
   c. List one common misconception to avoid.
   d. Suggest one practice question to test understanding.
3. Recommend a study sequence (what to learn first, second, etc.)
   with brief reasoning for the order.

My current knowledge level: {beginner / intermediate / advanced}
```

---

### 8. Feedback Drafting

**Patterns:** Role-Playing (§3.5)

```
You are an experienced manager who gives constructive, specific feedback.

Write feedback for: {person's name/role}
Context: {project, performance period, or specific situation}
What went well: {positive observations}
What needs improvement: {areas of concern}

Structure the feedback using the SBI model:
- Situation: When and where the behavior occurred
- Behavior: What specifically was observed (facts, not judgments)
- Impact: How the behavior affected the team/project/outcome

Tone: supportive but direct. End with 1-2 specific, actionable
suggestions for improvement.
```

---

### 9. Creative Brainstorm

**Patterns:** Zero-Shot Instruction (§3.2)

```
Generate 10 creative ideas for: {problem or opportunity}

Constraints:
- Budget: {budget range or "no budget constraint"}
- Timeline: {timeframe}
- Audience: {who benefits}

For each idea, provide:
- A catchy name (3-5 words)
- A one-sentence description
- Feasibility rating: Easy / Medium / Hard
- Originality rating: Common / Fresh / Wild

Include at least 2 "wild card" ideas that are unconventional or high-risk,
high-reward. Sort from most feasible to most creative.
```

---

### 10. Data Interpretation

**Patterns:** Chain-of-Thought (§3.4)

```
Interpret the following data and provide business insights.

Data:
---
{paste your data, table, or key metrics here}
---

Think through this step by step:
1. What are the 3 most notable trends or patterns in this data?
2. What might be causing each trend? (propose 1-2 hypotheses per trend)
3. Are there any anomalies or outliers? If so, what might explain them?
4. What are 2-3 actionable recommendations based on these insights?

Audience for this analysis: {who will read it}
Present findings from most important to least important.
```

---

### 11. Travel Itinerary

**Patterns:** Constrained Output (§3.6)

```
Create a day-by-day travel itinerary:

Destination: {city/region}
Dates: {start} to {end}
Travelers: {number and type, e.g., "2 adults, 1 child (age 8)"}
Interests: {food, history, nature, nightlife, shopping, etc.}
Budget level: {budget / mid-range / luxury}
Pace: {relaxed / moderate / packed}

For each day, provide:
- Morning, afternoon, and evening activities
- Restaurant recommendations for lunch and dinner (with cuisine type)
- Estimated costs for major activities
- Transportation between locations
- One insider tip per day

Include a packing reminder section at the end.
```

---

### 12. Interview Prep

**Patterns:** Role-Playing (§3.5), Few-Shot Learning (§3.3)

```
You are an experienced hiring manager for {company type / industry}.

I'm preparing for an interview for: {job title}
Company/industry: {details}
My background: {brief summary}

Provide:
1. The 5 most likely interview questions for this role.
2. For each question:
   a. Why they ask it (what they're really evaluating).
   b. A strong answer framework (not a script — key points to hit).
   c. One common mistake candidates make.
3. 3 smart questions I should ask the interviewer.
4. One "curveball" question to prepare for.

Example of a strong answer framework:
Q: "Tell me about a time you handled conflict."
Framework: Use STAR method → Situation (set the scene in 1 sentence) →
Task (your responsibility) → Action (specific steps YOU took) →
Result (quantified outcome + lesson learned).
```

---

### 13. Document Comparison

**Patterns:** Chain-of-Thought (§3.4), Constrained Output (§3.6)

```
Compare the following two documents and produce a structured analysis.

Document A:
---
{paste document A}
---

Document B:
---
{paste document B}
---

Analyze:
1. **Key Similarities** — list 3-5 points where the documents agree.
2. **Key Differences** — present as a comparison table:
   | Topic | Document A | Document B |
3. **Contradictions** — highlight any conflicting claims.
4. **Gaps** — what does each document cover that the other doesn't?
5. **Recommendation** — which document is more {complete / accurate /
   suitable for {purpose}}?
```

---

### 14. Social Media Post

**Patterns:** Few-Shot Learning (§3.3), Constrained Output (§3.6)

```
Write a {platform: LinkedIn / Twitter / Instagram} post about: {topic}

Tone: {professional / conversational / inspirational / humorous}
Goal: {engagement / thought leadership / promotion / announcement}
Include: {hashtags: yes/no} {emoji: yes/no} {call-to-action: yes/no}

Examples of the style I want:
- "{example post 1}"
- "{example post 2}"

Constraints:
- LinkedIn: 150-300 words, professional, paragraph format
- Twitter/X: under 280 characters, punchy
- Instagram: 50-150 words, visual-first, end with hashtags

Provide 3 variants to choose from.
```

---

### 15. Lesson Plan

**Patterns:** Zero-Shot Instruction (§3.2), Constrained Output (§3.6)

```
Design a lesson plan for teaching: {topic}
Grade level / audience: {who}
Duration: {time}
Learning objectives (students will be able to): {1-3 objectives}

Structure:
1. **Hook** (5 min) — engaging opening activity or question
2. **Direct instruction** (10-15 min) — key concepts, explained simply
3. **Guided practice** (10-15 min) — activity where students apply
   concepts with support
4. **Independent practice** (10 min) — students work on their own
5. **Closure** (5 min) — summary + exit ticket question

For each section, provide:
- What the teacher does
- What students do
- Materials needed
- Differentiation for advanced and struggling learners
```

---

### 16. Negotiation Prep

**Patterns:** Role-Playing (§3.5), Chain-of-Thought (§3.4)

```
You are a negotiation strategist. Help me prepare for a negotiation.

Situation: {what you're negotiating}
My position: {what I want}
Their likely position: {what they probably want}
My BATNA (best alternative): {what I'll do if negotiation fails}
Relationship importance: {one-time / ongoing / critical}

Provide:
1. Opening strategy — how to frame the conversation.
2. 3 key arguments in my favor, with supporting reasoning.
3. 3 likely objections they'll raise, with responses for each.
4. Concession strategy — what I can offer (ordered from least to most
   costly to me) and what I should ask for in return.
5. Walk-away point — clear criteria for when to end the negotiation.
6. One psychological principle to keep in mind (anchoring, framing, etc.).
```

---

### 17. Bug Report

**Patterns:** Constrained Output (§3.6)

```
Help me write a clear bug report from these rough notes.

My notes: {paste your rough description of the problem}

Format the bug report as:

**Title:** [concise, specific summary]

**Environment:** [OS, browser/app version, device]

**Steps to Reproduce:**
1. [step 1]
2. [step 2]
3. ...

**Expected Behavior:** [what should happen]

**Actual Behavior:** [what actually happens]

**Severity:** Critical / Major / Minor / Cosmetic

**Screenshots/Logs:** [describe what to attach]

**Additional Context:** [any patterns — e.g., "only happens on mobile",
"started after update X"]
```

---

### 18. Book/Article Summary

**Patterns:** Zero-Shot Instruction (§3.2), Constrained Output (§3.6)

```
Summarize {title} by {author} for someone who hasn't read it.

Provide:
1. **One-Line Summary:** The core argument in one sentence.
2. **Key Ideas** (3-5 bullet points): The most important concepts,
   each explained in 2-3 sentences.
3. **Notable Quotes:** 2-3 memorable quotes with brief context.
4. **Who Should Read This:** Describe the ideal reader in one sentence.
5. **Key Takeaway:** The single most actionable insight.

Length: 300-400 words total.
Tone: informative but engaging — imagine you're recommending it
to a smart friend over coffee.
```

---

### 19. Weekly Report

**Patterns:** Constrained Output (§3.6)

```
Transform these rough notes into a polished weekly status report.

My notes:
---
{paste your scattered notes, bullet points, or stream of consciousness}
---

Format as:

## Week of {date range}

### Completed
- [task] — [one-sentence result or impact]

### In Progress
- [task] — [current status] — [expected completion]

### Blocked
- [task] — [what's blocking] — [what I need to unblock]

### Next Week
- [planned priorities, ordered by importance]

### Metrics (if applicable)
- [key numbers from the week]

Tone: professional, concise, results-oriented. Each bullet should
be one line. Total length: under 200 words.
```

---

### 20. Explanation for Different Audiences

**Patterns:** Role-Playing (§3.5)

```
Explain {concept} at three levels:

1. **For a 10-year-old:** Use a simple analogy, no jargon, 2-3 sentences.
2. **For a college student:** Use accurate terminology, 1 short paragraph,
   include one real-world example.
3. **For an expert in {related field}:** Use domain-specific language,
   compare to concepts they already know, 1 short paragraph.

For each level, end with a one-sentence "check for understanding" question
that tests whether the listener got the key idea.
```

---

## Pattern Usage Summary

| Pattern | Recipes That Use It | Key Technique |
| --- | --- | --- |
| Zero-Shot (§3.2) | 1, 2, 5, 6, 9, 15, 17, 18, 19 | Detailed instruction replaces examples |
| Few-Shot (§3.3) | 4, 12, 14 | 1–2 examples anchor format and quality |
| Chain-of-Thought (§3.4) | 3, 7, 10, 13, 16 | "Step by step" reasoning produces deeper analysis |
| Role-Playing (§3.5) | 2, 8, 12, 16, 20 | Expert persona improves domain quality |
| Constrained Output (§3.6) | 1, 3, 4, 5, 6, 11, 13, 14, 15, 17, 18, 19 | Explicit format prevents rambling |

---

[← Back to curriculum](README.md)
