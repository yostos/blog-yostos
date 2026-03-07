---
description: Guide for safely refactoring blog config and templates. Analyze, branch, apply changes, verify, review, and commit.
---

# Blog Config Refactoring

Safely refactor blog configuration, templates, or infrastructure step by step.

## Steps

### 1. Analyze Current State

- Read target files and understand current state
- Identify scope and impact of the refactoring

### 2. Create Branch

- If on main: create a branch with `git checkout -b refactor/<descriptive-name>`
- If already on a branch: skip this step

### 3. Apply Changes

- Apply changes one at a time
- Confirm each change with the user before proceeding

### 4. Build Verification

- Run `zola check`
- Run `zola build`

### 5. Run /blog-review

Execute the blog code review on the changes.

### 6. Commit

- `git add .`
- Use `/simple-commit:commit` skill

After commit, the branch is ready for `/blog-release`.
