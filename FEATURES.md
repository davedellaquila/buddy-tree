# Buddies Dashboard — Feature Registry

Living list of every feature in the dashboard. Update this file when a feature
ships or changes — it's the source of truth for future documentation.

Repo: https://github.com/davedellaquila/buddy-tree
Live: https://davedellaquila.github.io/buddy-tree/
Build: `build.py` generates `index.html` from `buddies.json` + `plans.json`.

---

## Tree chart

- **Classic tree layout** — the canonical design. (A card-based redesign was
  tried and reverted; preserved on branch `card-tree-redesign` for reference.)
- **Zoom slider** — vertical slider beside the chart, 50–160%.
- **Shift+scroll zoom** — hold Shift and scroll over the tree to zoom.
- **Grab-to-pan** — click-drag the chart to slide it around; grab/grabbing
  cursors; small movements still count as clicks; the stray click after a
  drag is swallowed so you don't navigate by accident.
- **Gripper handles (⠿)** — every tree tile has a drag handle (top-left,
  appears on hover). Drag a tile onto another buddy to reparent it.
  Loop protection: can't drop a parent onto its own descendant.
- **Orphaned buddies section** — buddies with no parent render in their own
  tree section with grippers, instead of being invisible.
- **Drop targets** — tree nodes and Projects rows accept drops from the
  sidebar and from tile grippers to assign/change parents.

## Appearance

- **Light / Dark / System theme** — segmented picker under the sidebar
  brand; per-device localStorage (default System, follows the OS live).

## Sidebar

- **Main views** — Tree, Projects, Plans, Manifest, Project, Changelog;
  order is user-rearrangeable in settings (gear icon). Number keys 1–6
  select views in that order; Up/Down arrow through views then buddies.
- **Project view** — shows the current project's homepage in the center;
  clicking a sidebar buddy selects it as the current project. A buddy with
  a `homepage` field loads that page in a full-center frame (with an "Open
  on Muse ↗" link to its canonical URL); buddies without one show the
  built-in detail page.
- **Horizontally resizable** — drag the edge, 220–560 px, width remembered
  per device.
- **Drag-to-reparent** — drag any sidebar buddy onto a tree node or
  Projects row to change its parent.
- **App name** — the top-left "Buddies" label is inline-editable,
  device-persisted, and updates the browser title.

## Buddy detail pages

- **Navigation** — Back, Prev, Next, and All buddies.
- **Build numbers** — every buddy and business-plan page shows a timestamp
  build number.
- **Click-to-rename** — buddy names are inline editable.
- **Scratch notes** — device-local freeform notes (localStorage).
- **Shared notes** — sync to the buddy's repo at `docs/notes.md` via the
  GitHub Contents API (needs a token; falls back to device-local).
- **Ingest box** — brain-dump raw thoughts about the buddy; each dump is
  appended as a timestamped entry to the buddy's repo `docs/ingest.md`.
  Raw material for later dossier work. Dumps live in a collapsible
  "Dumps (n)" section (collapsed by default, state remembered per buddy);
  each dump tile has edit (✏️) and delete (🗑️) buttons in its upper-right
  corner.
- **Token gating** — photos, shared notes, and ingest are locked until a
  GitHub token is saved; an amber banner at the top of every buddy page
  prompts for it.
- **Photo strip** — photos from `photos/<buddy-id>/` in the dashboard repo;
  drag/drop upload area; HEIC files are converted to JPEG in-browser
  (`heic2any`); uploads push to the repo via the GitHub API.
- **💾 Save to desktop** — downloads a launcher file (`.webloc` on Mac,
  `.url` on Windows) that opens the buddy in standalone mode.

## Standalone mode

- **Hash deep-links** — `#/buddy:<id>`, `#/view:tree`, `#/plan:<id>`;
  back/forward buttons work.
- **Chromeless standalone view** — `#/buddy:<id>/standalone` hides the
  sidebar and shows just the buddy page, with a small "open full
  dashboard" bar. Feels like its own little app.

## Change journal

- Tracks buddy renames, note edits, hierarchy moves, and app-name changes.
- Shows `Revert (N)`, "What changed?", and a labeled Dismiss button;
  persists across reloads via localStorage; reverts all logged changes
  at once.
- "What changed?" lists each entry with old → new values; expanding it
  marks entries reviewed so the sticky bar only returns for new changes.
- The **Changelog** main view keeps the full history permanently.

## GitHub integration

- Token stored in localStorage (`S.ghToken`); used for photo uploads,
  shared notes, and ingest sync.
- Photo uploads target the public `buddy-tree` repo; shared notes and
  ingest target each buddy's own (usually private) repo.

## Repo automation (project-buddy drill)

- Every new buddy repo is stamped with `README.md` (name, mission,
  brief links) and `docs/brief.md` (full brief text), plus an empty
  `docs/ingest.md` log — committed and pushed automatically.

---

## Responsive design

- **Fit button (⛶)** next to the zoom slider — zooms to fit the chart content.
- **Small (<640px)**: tiles stack as full-width cards; sidebar becomes a
  drawer (hamburger button); detail opens as a bottom sheet.
- **Medium (640–1100px)**: collapsible sidebar; view nav becomes a horizontal
  segmented control; detail opens as a right-docked side sheet (380px).
- **Large (>1100px)**: tri-pane with persistent detail panel (400px).
- **Keyboard**: arrows move between buddies, Esc closes the detail panel.

## Known limitations / follow-ups

- Photo "all image types" claim is aspirational: HEIC is converted and
  JPEG/PNG/GIF/WebP work, but other formats are merely renamed to `.jpg`.
- Shared-note edits, photo uploads, and ingest dumps are not in the
  change journal.
- Back-history is session memory, not persisted across reloads.
- The localStorage GitHub token is convenient but risky; a fine-grained
  token (or backend) is the safer long-term design.
- The dashboard is public and currently contains family dossiers.
