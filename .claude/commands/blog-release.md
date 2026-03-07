---
description: Release blog config/feature changes. Changelog, branch, commit, push, PR, merge, and tag with semver.
---

# Blog Release

Release blog infrastructure changes through a branch-based workflow.

## Steps

### 1. Create Branch

- If on main: create a branch with `git checkout -b feature/<descriptive-name>` or `fix/<name>`
- If already on a branch: skip this step

### 2. Update CHANGELOG

- Review commits on the branch with `git log main..HEAD`
- Update CHANGELOG.md with the changes
- `git add .` and commit the CHANGELOG update with `/simple-commit:commit`

### 3. Push

- `git push origin <branch-name>`

### 4. Create PR

- `gh pr create` with a summary of the changes

### 5. Merge

- `gh pr merge` to merge the PR

### 6. Switch to main & Pull

- `git checkout main`
- `git pull origin main`

### 7. Tag

- Show the current latest tag with `git tag --sort=-v:refname | head -5`
- Based on the changes, propose a semver version:
  - Patch (Z): bug fixes, minor config tweaks
  - Minor (Y): new features, new shortcodes, new templates
  - Major (X): breaking changes, major restructuring
- Ask the user to confirm or adjust the version
- `git tag v<X.Y.Z>`
- `git push origin v<X.Y.Z>`
