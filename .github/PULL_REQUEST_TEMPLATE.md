## What

Please include a concise summary of the change (suitable for both human and AI parsing).

## Why

Please include relevant motivation and context.

Fixes # (issue)

## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## How Has This Been Tested?

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce. Please also list any relevant details for your test configuration.

- [ ] Test A
- [ ] Test B

## Prompt Review Checklist (if adding a prompt template)

- [ ] **Role assignment** — the prompt assigns a clear, appropriate role
- [ ] **Task specification** — the task is described with imperative verbs and unambiguous success criteria
- [ ] **Output format** — the expected output structure is explicitly defined
- [ ] **Constraints** — all constraints are internally consistent
- [ ] **Negative instructions** — the prompt includes relevant "do not" instructions
- [ ] **Token budget** — the prompt fits comfortably within the target model's context window
- [ ] **YAML frontmatter** — the `.prompt.md` file includes valid YAML frontmatter (`mode`, `description`, `version`)
- [ ] **Testing** — the prompt has been tested against at least three representative inputs
- [ ] **No secrets** — the prompt contains no API keys or sensitive information
- [ ] **No duplication** — the prompt does not duplicate shared content

## Curriculum Content Checklist (if adding to curriculum)

- [ ] **Learning objectives** — the module opens with clear, measurable learning objectives
- [ ] **Progressive structure** — content builds logically
- [ ] **Worked examples** — at least one concrete, worked example demonstrates each key concept
- [ ] **Cross-references** — connections to other documents are explicitly noted
- [ ] **Exercises** — at least two exercises are included
- [ ] **Citations** — all empirical/factual claims are cited using `references.md`

## General Checklist:

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] Any dependent changes have been merged and published in downstream modules
