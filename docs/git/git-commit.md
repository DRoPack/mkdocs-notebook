# Git Commit Standard

Use the following prefixes to categorize commits. The goal is to quickly understand **what** changed before reading the full commit message.

| Prefix | When to Use | Example |
|---------|-------------|---------|
| **Feat:** | New functionality or feature | `Feat: Add recurring inspection scheduling` |
| **Fix:** | Bug fixes or behavior corrections | `Fix: Prevent timer from running on startup` |
| **Docs:** | Documentation only (README, wiki, comments, guides) | `Docs: Update Azure deployment instructions` |
| **Refactor:** | Code restructuring without changing behavior | `Refactor: Simplify schedule calculation logic` |
| **Perf:** | Performance improvements | `Perf: Reduce SharePoint REST requests` |
| **Test:** | Add or modify unit/integration tests | `Test: Add schedule calculation tests` |
| **Chore:** | Maintenance, tooling, configuration, dependencies, version bumps | `Chore: Update package dependencies` |
| **Build:** | Build system or packaging changes | `Build: Add Node.js engine requirement` |
| **CI:** | Continuous Integration changes | `CI: Deploy documentation on push` |
| **Style:** | Formatting or whitespace changes only (no logic changes) | `Style: Format timer.ts` |
| **Revert:** | Revert a previous commit | `Revert: Remove experimental scheduling logic` |

## Guidelines

### Feat

Use when adding user-visible functionality.

**Examples**

- `Feat: Add monthly inspection scheduling`
- `Feat: Support static recurring dates`

---

### Fix

Use when correcting incorrect behavior.

**Examples**

- `Fix: Prevent duplicate timer execution`
- `Fix: Handle null inspection dates`

---

### Docs

Use when only documentation changes.

**Examples**

- `Docs: Update README deployment guide`
- `Docs: Clarify Azure Function configuration`

---

### Refactor

Use when improving the implementation without changing functionality.

**Examples**

- `Refactor: Extract schedule calculation helpers`
- `Refactor: Simplify timer initialization`

---

### Chore

Use for project maintenance that isn't a feature or fix.

**Examples**

- `Chore: Bump package version`
- `Chore: Update npm dependencies`
- `Chore: Clean up project configuration`

---

### Build

Use for build or runtime configuration.

**Examples**

- `Build: Add Node.js engine requirement`
- `Build: Update TypeScript compiler settings`
- `Build: Update Azure Function host configuration`

---

### CI

Use for GitHub Actions, Azure Pipelines, or other automation.

**Examples**

- `CI: Deploy MkDocs on release`
- `CI: Add npm cache to workflow`

---

### Perf

Use when improving performance without changing functionality.

**Examples**

- `Perf: Cache SharePoint list lookups`
- `Perf: Reduce Azure Function startup time`

---

### Test

Use when adding or modifying tests.

**Examples**

- `Test: Add schedule validation tests`
- `Test: Improve timer unit test coverage`

---

### Style

Use for formatting changes only. No functional code changes.

**Examples**

- `Style: Format timer.ts`
- `Style: Apply ESLint formatting`

---

## Multiple Changes

When a commit contains several related changes, choose the prefix that best represents the primary purpose.

| Changes | Preferred Prefix |
|---------|------------------|
| Feature + version bump | `Feat:` |
| Bug fix + logging | `Fix:` |
| Runtime config + package.json | `Build:` |
| Dependency updates | `Chore:` |
| README updates | `Docs:` |

## General Recommendations

- Keep the summary under 72 characters when practical.
- Use the imperative mood ("Add", "Update", "Remove", "Fix").
- Don't end the summary with a period.
- Make each commit represent one logical change whenever possible.