# LLM-Assisted Code Review and Hardening (Python CLI)

## Project Summary
This repository is a small but concrete case study in LLM-assisted software development: generate a working program with a general-purpose LLM, then iteratively review and harden it using LLM feedback plus human judgment.

The goal is not the game itself. The deliverable is the *process and artifacts*: three code versions and written analysis of what the LLM improved, what it missed, and where the workflow produced superficial changes.

## What’s in This Repo
- `roshambo_v1_baseline.py`  
  Initial working implementation produced primarily by an LLM.

- `roshambo_v2_refactor.py`  
  First revision after running structured prompts to critique code quality and security.

- `roshambo_v3_hardened.py`  
  Second revision incorporating deeper refactoring and robustness changes (dataclasses, typed state, centralized rule mapping, safer lookups).

- `llm-review-notes-part1.md` and `llm-review-notes-part2.md`  
  Short writeups reflecting on code quality, usefulness of suggestions, repetition patterns, and where human oversight mattered.

## Program Behavior (the stable requirements)
The CLI flow is consistent across versions:
- input validation loops for Y/N and R/P/S/Q/I
- randomized computer move selection
- rule-based win/lose/tie logic
- statistics tracked for overall record and per-move performance
- streak messaging for 3 wins or 3 losses
- message after 15 games played

## What Changed Across Versions (with code anchors)

### V1: Baseline implementation
The baseline version uses direct control flow and lightweight helper functions like:
- `determine_outcome(user, comp)`
- `print_info(name, overall_stats, choice_stats)`

It is functional, but relies on ad hoc dictionaries and assumes inputs stay valid once passed validation.

### V2: Refactor for maintainability and safer lookups
The V2 revision introduces stronger structure:
- centralized constants such as `VALID_MOVES` and `VALID_MENU_CHOICES`
- `get_menu_choice()` as a single validation gate
- a rules map for outcomes rather than repeated conditional branches

This reduces repeated logic and makes error handling more explicit (for example, raising on unexpected combinations).

### V3: Hardened state management and robustness
The V3 version converts stats and state into typed structures:
- `@dataclass Record` for win/loss/tie tracking with `win_percentage()`
- `@dataclass GameState` to manage streaks, games played, and per-move records
- `RULE_TEXT` as the single source of truth for win conditions

The game loop becomes easier to audit because state mutation is centralized in `play_round(state, user_move)` and INFO rendering is isolated in `print_info(state)`.

V3 also adds a top-level exception handler to avoid raw stack traces and terminate gracefully in unexpected error conditions.

## Observations on LLM Code Review Quality
Two patterns emerged during iteration:
- The LLM repeatedly suggested generic improvements even after changes were made, which created churn without clear value.
- The highest-value contribution was identifying a crash-prone pattern (fragile access and control flow) and pushing toward a safer structure that reduced runtime failures.

The written notes document where suggestions were actionable versus performative.

## How to Run
Each version is standalone:

```bash
python roshambo_v1_baseline.py
python roshambo_v2_refactor.py
python roshambo_v3_hardened.py
