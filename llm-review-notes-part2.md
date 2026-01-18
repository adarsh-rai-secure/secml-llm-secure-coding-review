# LLM-Assisted Code Review – Part 2

## Context
In the second phase, the same LLM was prompted to critique and improve the initial implementation. The goal was to observe whether iterative prompting would lead to materially better code, or simply cosmetic changes.

This phase focuses on how the quality of suggestions evolved and where human oversight remained essential.

## Improvements Introduced
The revised version incorporated several meaningful changes:

- **Centralized validation logic**  
  Input validation was consolidated into dedicated helper functions, reducing repeated checks and making control flow easier to audit.

- **Explicit constants and mappings**  
  Valid moves, menu options, and outcome rules were represented as constants and dictionaries rather than embedded conditionals. This reduced duplication and improved readability.

- **Clearer functional boundaries**  
  Some separation emerged between input handling, game logic, and output formatting, making the execution path easier to follow.

These changes improved maintainability and reduced the likelihood of simple runtime errors.

## Limitations of LLM Feedback
Despite visible improvements, several issues remained:

- **Repetitive suggestions**  
  The LLM frequently re-proposed changes that had already been implemented, suggesting limited state awareness across iterations.

- **Surface-level refactoring**  
  Many recommendations focused on stylistic cleanup rather than deeper structural risks, such as how state was mutated or how invariants were enforced.

- **No explicit threat modeling**  
  The LLM did not reason about failure modes beyond correctness. It did not proactively address crash safety, unexpected control paths, or defensive boundaries.

## Human-Guided Corrections
At this stage, human judgment was required to:
- decide which suggestions meaningfully reduced risk,
- reject refactors that increased complexity without benefit,
- and identify areas where structural redesign was needed rather than incremental cleanup.

This directly informed the third iteration, where state was formalized using dataclasses and control flow was centralized.

## Takeaway
Iterative prompting improved code quality, but only up to a point. The LLM was effective at local improvements but struggled with holistic design and robustness reasoning.

The most reliable workflow combined LLM speed with human-led architectural decisions. Without that oversight, the process risked converging on verbose but still fragile code.
