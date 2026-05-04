---
name: commit-message
description: Generate a commit message using conventional commit format based on staged changes. Use when the user asks to "generate a commit message", "write a commit message", or "suggest a commit message".
---
Generate a commit message using conventional commit format based on the current staged changes.

Steps:
1. Run `git diff --staged` to see what changes are staged for commit.
2. Run `git status` to understand the context of the changes.
3. Run `git log -5 --oneline` to see recent commit message style in this repository.
4. Analyze the changes and determine the appropriate conventional commit type:
   - `feat`: New feature or functionality
   - `fix`: Bug fix
   - `refactor`: Code restructuring without changing behavior
   - `docs`: Documentation changes
   - `test`: Adding or updating tests
   - `chore`: Maintenance tasks (deps, configs, build)
   - `perf`: Performance improvements
   - `style`: Code formatting, whitespace, etc.
5. Write a commit message in the format `type(scope): subject`:
   - Use imperative mood for the subject ("add" not "added")
   - Choose an appropriate scope if applicable
   - Keep the subject clear and concise
6. If the changes are complex, include a body explaining the reasoning.
7. Present the generated commit message and optionally provide alternative versions.
