# CVs session — context for Claude Code

This file is auto-loaded by Claude Code at the start of any session working in this
folder (`~/repos/Raqueshi`), so it's the "CVs session" memory doc Stefan asked for —
read this and you're caught up, no need to re-ask what happened before.

## What this project is
A personal CV for Stefan Sendyk, built as single-file HTML/CSS pages (no build tools,
no JS framework — just inline `<style>` + plain markup), hosted in this GitHub repo on
the `CV` branch. Stefan is new to coding/git and is using this project partly to learn
by doing (see "How Stefan likes to work" below).

## Two separate CV design threads

**Thread A — `index.html`** (the "main" file). Evolved directly through several full
redesigns, each one re-skinning the same content around a photo Stefan found in
Downloads for style inspiration:
1. Purple gradient, brutalist sharp-shard shapes
2. Icy blue/black duotone halftone "Snow poster" look
3. Red-frame + black panel + iridescent blue paint-flow ("shirt on red background" photo)
4. Current state: soft pastel mesh-gradient blob (blue/coral/cream/lavender), thin
   elegant type, vertical edge labels, plus scattered blue/orange blurred gradient dots

**Thread B — `CV1.html` through `CV9.html`** (numbered checkpoints). Started when
Stefan asked to save the red/black/paint-flow design as a checkpoint before trying a
new look on `index.html`. From `CV3.html` onward we established a standing rule (see
below) of creating a new numbered file per change instead of overwriting. Chain of
changes:
- **CV1/CV2** — the red-frame/black-panel/blue-paint-flow design (checkpoints of an
  earlier `index.html` state)
- **CV3** — softened the color palette (desaturated) + made interests/skills chips
  behave like real buttons (hover lift, click press, hover-reveal description text)
- **CV4** — un-desaturated colors again, flipped black→white and red→green
  (panel went from dark to white, text had to flip from light to dark to stay
  readable), stronger two-layer "3D" button shadows
- **CV5** — tried warm yellow/orange gradients on the buttons — **Stefan disliked
  this**, said it clashed with the rest of the cool-toned page
- **CV6** — switched button accent colors back to the existing cool palette
  (purple/blue/cyan/pink) with soft tinted glass-style glows instead of flat fills —
  well received
- **CV7** — replaced the whole page's core gradient identity: old
  light-blue→blue→purple→pink became black→purple→pink→warm-yellow→soft-orange,
  weighted so black dominates, purple/pink get a solid middle share, yellow/orange
  are minor accents
- **CV8** — renamed the project from "EPlantic Pitch" to "ePlantInc Pitch"; merged
  the yellow/orange into one continuous gradient flow instead of a separate bolted-on
  tail, and gave yellow/orange slightly more presence
- **CV9** — removed the Gmail contact button, kept only `spsendyk@icloud.com`

**`CV9.html` is the current "latest" state of Thread B.** `index.html` (Thread A) is a
separate, independently-evolved design — they are not the same lineage.

## CV content facts (same across all versions — do not invent new ones)
- Name: Stefan Sendyk
- Interests: Drama, Editing, Swimming, Padel/Running/Hiking (on hold — broken hip,
  back after Feb 1)
- Skills: Basic programming, Russian (fluent), English (fluent), Spanish (fluent),
  French (partial), Advanced editing, High running speed (currently unavailable),
  Navigation skills, Pitching, Presentation making
- Projects: "ePlantInc Pitch" — a pitch project by Stefan Sendyk (ePlantInc is also a
  separate business idea Stefan is developing — see "Related but separate" below)
- Contact: `spsendyk@icloud.com` only (Gmail was intentionally removed in CV9)

## Outstanding TODO
Many chips have a placeholder hover-detail of `— add a note here —` (languages show
real fluency levels, on-hold items show their real status, but most skills/interests
like "Pitching" or "Basic programming" still need a real one-line description from
Stefan). This was explicitly left for him to fill in himself as practice editing HTML.

## Standing rules Stefan has set for this project
- **Always create a new numbered file (`CV10.html`, `CV11.html`, ...) for the next
  style change, never overwrite the current one — unless Stefan explicitly says to
  change the existing file.**
- Stefan prefers to run git/terminal commands himself to learn, rather than having
  them run for him automatically — UNLESS he explicitly asks for something to be done
  directly (e.g. "push this to GitHub"), in which case just do it.
- Don't invent personal facts/descriptions that weren't actually given.

## Git / GitHub state
- Repo: `git@github.com:StefanSendyk/Raqueshi.git`, working on the `CV` branch
  (not `main`).
- As of this doc, `CV1.html`–`CV9.html`, the redesigned `index.html`, and `README.md`
  are committed and pushed to `origin/CV`.
- Known issue: `README.md` currently contains leftover HTML CV source code instead of
  a normal project description (looks like an accidental overwrite outside of a
  Claude Code session at some point). It was pushed as-is at Stefan's request but
  still needs proper content whenever he wants it fixed.
- `.DS_Store` is untracked and should stay that way (macOS system file, not project
  content) — consider adding a `.gitignore` for it if it keeps showing up in
  `git status`.

## Related but separate: the ePlant.inc business idea
In a different context (not this repo), Stefan is also planning an actual business
called ePlant.inc — an online gardening marketplace + services platform for
Andalucía, Spain, aimed at expats/second-home owners, with three revenue streams
(marketplace sales, service fees, subscription) and a planned AI shopping-helper
chatbot. Two Claude Docs exist for that: a business plan and a database schema (for
plants/nurseries/freelancers/services/orders, shared between a future website and
chatbot via one API). Not part of this repo, but it's the real-world project the
"ePlantInc Pitch" CV entry refers to, in case a future session needs that context.
