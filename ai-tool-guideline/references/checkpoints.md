# The nine stage skeleton

A spine, not a template. Cut stages that do not apply to the tool, merge stages the
tool merges, and stop at whatever the client answered for how far they want to get.

For each stage below: what the stage is, the traps that recur across almost every AI
tool at this stage, and what a good pass check looks like. The recurring traps are
prompts for research, not content to paste. Verify each one against this specific
tool before it goes in the manual.

---

## Stage 1, choose the version and the plan

Which build of this tool, on which plan. Many AI tools ship a different product per
region under the same brand, with different models, different domains and different
pricing.

Recurring traps to check for:

- Two regional builds, and the beginner downloads the one their account cannot use
- The free tier limit is stated per day, per month or per feature, and the reader
  assumes the wrong one
- Sign up region is chosen at registration and cannot be changed afterwards
- The plan that unlocks the feature they actually came for is not the cheapest paid plan

Pass check: they can state which build they are on and what the free tier gives them.

---

## Stage 2, download and install

Getting the software onto the machine.

Recurring traps to check for:

- Install path containing non ASCII characters or spaces, which breaks the tool later
  rather than at install time
- Operating system version below the stated minimum, with a failure message that does
  not say so
- Antivirus or the operating system blocking an unsigned or unrecognised installer
- macOS refusing to open an application from an unidentified developer
- Missing runtime dependencies that the installer does not bundle and does not check for
- Disk space or directory permission failures reported as a generic error code

Pass check: the application opens and shows its main window.

---

## Stage 3, first launch and sign in

Account creation, verification, and the first run wizard.

Recurring traps to check for:

- Verification code never arrives, and the alternative sign in method is not obvious
- Account region locked at sign up, affecting which models appear later
- The first run wizard offers a config import that is easy to skip and expensive to
  redo later
- The tool appears to work while signed out, but the part they came for needs sign in

Pass check: their account name is visible inside the tool.

---

## Stage 4, choose the model or connect the key

Picking a model, or supplying an API key from another provider.

Recurring traps to check for:

- The model list is short or empty, and the reason is an account setting rather than a fault
- An automatic model selector hides the model list until it is turned off
- Custom provider setup needs a model identifier that the provider names differently
  from the tool
- The key is pasted with trailing whitespace, or into the wrong field
- Free quota exhausted, reported as a generic failure rather than as a quota message
- Some models do not support attachments or images, and the failure looks like a bug

Pass check: the tool answers a one line question with the model they intended to use.

---

## Stage 5, get one real thing working

The first end to end result. The moment the tool stops being an install and starts
being useful.

Recurring traps to check for:

- No project or folder open, so the tool has nothing to act on
- The runtime the generated code needs is not installed
- Output written somewhere other than where the reader is looking
- Long sessions losing earlier instructions, and the reader assuming the tool is broken
- The reader asks for too many things in one request, and cannot tell which one failed

Pass check: a named artefact exists and does the thing it was supposed to do.

---

## Stage 6, install extensions

Plugins, MCP connectors, skills, agents.

Recurring traps to check for:

- The extension mechanism needs a runtime the tool does not ship with
- Extensions install into several scopes, project, user and global, and the reader
  installs into one and looks in another
- Command names differing per operating system
- Credentials expiring silently, so something that worked last week returns an
  authorisation error
- Too many extensions installed at once, producing contradictory behaviour that is
  hard to attribute
- The tool must be restarted before an extension appears

This stage links to `install-safety-check` for anything from an untrusted source.

Pass check: the tool visibly uses the extension when asked to.

---

## Stage 7, build something real

Sustained use on an actual project.

Recurring traps to check for:

- No version control, so a bad change cannot be undone
- Changing many things at once, so a break cannot be localised
- No project level instruction file, so the tool contradicts earlier decisions in
  later sessions
- Accepting output without ever reading it, until the project becomes unmaintainable
- Security decisions delegated to the model and never reviewed

Pass check: they can undo yesterday's work and get back to a state that runs.

---

## Stage 8, put it in front of other people

Deployment, publishing, sharing.

Recurring traps to check for:

- Works locally, fails in the deployed environment, because configuration differs
- Secrets committed into a public repository
- Registration, filing or verification requirements that apply in the reader's
  jurisdiction before a service may be offered publicly
- Domain and hosting bought in the wrong order, or in incompatible places
- No cost ceiling set, so a traffic spike becomes a bill

Pass check: someone who is not them can open it and use it.

---

## Stage 9, keeping it running

The part every beginner guide omits.

Recurring traps to check for:

- Quota or credit exhausted mid task
- An update changing a menu location or removing a feature the manual described
- Bills growing quietly
- No backup of configuration, so a reinstall means starting over

Pass check: they know where to look at usage and where to look at spend.
