---
description: Release blog config/feature changes. Changelog, branch, commit, push, PR, merge, and tag with semver.
---

# Blog Release

Release blog infrastructure changes through a branch-based workflow.

## Steps

### 1. Create Branch

- If on main: create a branch with `git checkout -b feature/<descriptive-name>` or `fix/<name>`
- If already on a branch: skip this step

### 2. Decide Version

- Show the current latest tag with `git tag --sort=-v:refname | head -5`
- Review commits on the branch with `git log main..HEAD`
- Based on the changes, propose a semver version:
  - Patch (Z): bug fixes, minor config tweaks
  - Minor (Y): new features, new components, new templates
  - Major (X): breaking changes, major restructuring
- Ask the user to confirm or adjust the version

### 3. Update CHANGELOG

Follow [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/).

- Move the entries under `## [Unreleased]` into a new section
  `## [X.Y.Z] - YYYY-MM-DD`, add the changes from the branch commits,
  and leave an empty `## [Unreleased]` above it
- Optionally open the release with a sentence or two on its theme or
  a notable change, when the release is worth introducing
- Group entries by type, one heading per type, in this order:
  `### Added`, `### Changed`, `### Deprecated`, `### Removed`,
  `### Fixed`, `### Security`
  - Deprecated: say which version will remove the feature
  - Security: lead with the CVE ID when one exists
- Mark breaking changes with a `**Breaking:**` prefix inside their
  type section; do not create a separate breaking section
- Update the comparison links at the bottom of the file:
  - `[Unreleased]: https://github.com/yostos/blog-yostos/compare/vX.Y.Z...HEAD`
  - Add `[X.Y.Z]: https://github.com/yostos/blog-yostos/compare/v<previous>...vX.Y.Z`
- `git add .` and commit the CHANGELOG update with `/simple-commit:commit`

### 4. Push

- `git push origin <branch-name>`

### 5. Create PR

- `gh pr create` with a summary of the changes

### 6. Merge

- `gh pr merge` to merge the PR

### 7. Switch to main & Pull

- `git checkout main`
- `git pull origin main`

### 8. Tag

- `git tag vX.Y.Z` with the version decided in step 2
- `git push origin vX.Y.Z`
