---
name: publish-to-superturbo-github
description: >
  Publish or update a skill in Turbo's GitHub skill library. Use whenever Turbo
  says "update this skill to superturbo github", "push this skill to superturbo",
  "publish to superturbo github", "add this skill to my github", "update the
  superturbo skills repo", or otherwise asks to send a skill built or edited in
  the session to his GitHub. Always targets the repo github.com/TurboGuo/superturbo-skills
  (owner TurboGuo, repo superturbo-skills), follows its one folder per skill
  layout, and ALWAYS updates the repo README skill index in the same pass.
---

# Publish to superturbo GitHub

Ship a skill that was built or edited in the current session into Turbo's public
skill library, and keep the README index in sync. This is a fixed destination
and a fixed convention; do not ask Turbo where to push unless he says a different
repo.

## Target (fixed)

- Repo: https://github.com/TurboGuo/superturbo-skills
- owner: `TurboGuo`
- repo: `superturbo-skills`
- Default branch: `main`. Commit directly to `main` (that is how the existing
  skills sit). Only open a branch or PR if Turbo explicitly asks for one.

## Layout convention (match the existing repo)

- Each skill lives in its OWN folder at the repo root, named exactly after the
  skill's `name` frontmatter (kebab case), e.g. `macro-impact/SKILL.md`.
- There is NO wrapper `skills/` folder. Do not create one.
- A skill folder contains `SKILL.md` plus any templates or assets it needs.
- The root `README.md` holds a `## 📚 Skills` index with one entry per skill.

## Tools

Use the GitHub connection tools (they act on GitHub through Turbo's authenticated
device bridge): `mcp__remote-devices__github__*`. Load their schemas first with
ToolSearch, e.g.
`select:mcp__remote-devices__github__get_file_contents,mcp__remote-devices__github__create_or_update_file,mcp__remote-devices__github__push_files`.

If the GitHub connection is unavailable (no device / not authenticated), do not
retry blindly: tell Turbo, and fall back to delivering the skill as a `.skill`
file with SendUserFile so he can add it manually.

## Steps (run every time)

1. Identify the skill to publish.
   - It is the skill just built or edited this session, or the one Turbo names.
   - Read its `SKILL.md` frontmatter to get `name`, `description`, and the
     trigger phrases. The folder name in the repo MUST equal `name`.

2. Push the skill files.
   - Check whether the folder / file already exists with
     `get_file_contents` (path `"<name>/SKILL.md"`, owner `TurboGuo`, repo
     `superturbo-skills`).
   - New file -> `create_or_update_file` with no `sha`.
   - Existing file -> get its blob `sha` first, then `create_or_update_file`
     WITH that `sha` (updates require the sha, or the call fails).
   - Multiple files (SKILL.md plus assets) -> use `push_files` to commit them in
     one commit.
   - Commit message: short and clear, e.g. "Add <name> skill" or
     "Update <name> skill: <what changed>".

3. ALWAYS update the README index (this is a hard requirement, never skip it).
   - `get_file_contents` on `README.md` to get its current text AND blob `sha`.
   - Add a new section for the skill under `## 📚 Skills`, or replace the
     existing section if the skill is already listed.
   - Match the existing entry format EXACTLY:
     ```
     ### <emoji> <skill-name>
     <one or two sentence plain description of what it does>
     - 🗣️ **Triggers:** "<trigger 1>", "<trigger 2>", "<trigger 3>"
     - <optional extra note line, e.g. a 🔑 requirement or 🌏 language note>
     ```
   - Pick a fitting emoji for the H3 heading, keep the description concise, and
     pull the triggers from the skill's own frontmatter.
   - Keep every other skill entry untouched. Place the new entry in a sensible
     spot (group with thematically similar skills).
   - `create_or_update_file` on `README.md` WITH the sha you fetched.

4. Confirm to Turbo with the commit link(s) and the skill folder URL. State
   plainly that it went to `main` and that the README was updated.

## Rules

- The README update in step 3 is mandatory on every publish, whether the skill
  is new or an update. A skill push without a README entry is incomplete.
- Never invent a different repo or a `skills/` wrapper folder.
- Do not delete or reorder unrelated skills or README sections.
- Preserve exact file content; do not reformat the skill being published.
- If the same skill already exists, this is an update: reuse the folder name and
  supply the existing file sha rather than duplicating.
