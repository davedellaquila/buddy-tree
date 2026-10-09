# Changelog

All notable changes to the Buddies dashboard and buddy system. Newest first.
`FEATURES.md` describes the current state; this file describes how it got there.

## 2026-10-09

### Added
- **Zoom slider floats over the chart** — moved from the margin into the
  chart area itself, map-control style. (`94948af`)
- **Chart viewport polish** — visible border around the chart viewport so its
  edges are clear; the viewport now fills the available page height instead
  of clipping. (`f6aa25c`)
- **Responsive layouts** — three breakpoints: small (<640px) stacks tiles as
  full-width cards with a drawer sidebar (hamburger) and detail as a bottom
  sheet; medium (640–1100px) has a collapsible sidebar, horizontal segmented
  view control, and detail as a right-docked side sheet; large (>1100px) is
  tri-pane with a persistent detail panel. **⛶ Fit button** next to the zoom
  slider zooms to fit content. Tile child counts. Keyboard navigation
  (arrows move between buddies, Esc closes detail). (`d606e04`)
- **Standalone buddy mode** — hash deep-links (`#/buddy:<id>`, `#/view:tree`,
  `#/plan:<id>`) with working back/forward; chromeless standalone view
  (`#/buddy:<id>/standalone`) hiding the sidebar; **💾 Save to desktop**
  button on every buddy page downloading a `.webloc` (Mac) / `.url`
  (Windows) launcher that opens the buddy by itself. (`d406f51`)
- **Gripper handles (⠿)** on every tree tile — drag a buddy onto another to
  reparent it; loop protection included. (`8bdbdea`)
- **Orphaned buddies section** — parentless buddies render in their own tree
  section with grippers instead of being invisible. (`8bdbdea`)
- **Ingest box** on every buddy page — brain-dump raw thoughts; each dump
  appends a timestamped entry to the buddy's repo `docs/ingest.md`
  (device-local fallback). (`79e4ae2`)
- **Sharing Buddy** — new buddy (brief, repo, thread, registry entry)
  exploring per-buddy share links, access levels, and privacy. (`4f19bc2`)
- **FEATURES.md** — living feature registry in the repo root. (`d1f4ea2`)
- **README + docs/brief.md sweep** — 25 buddy repos stamped with a README
  (name, mission, brief links) and `docs/brief.md` (full brief text); the
  new-project drill now does this automatically for every new repo, along
  with an empty `docs/ingest.md`.
- **Dream Buddy repo link** — wired `davedellaquila/dream-buddy` into the
  dashboard registry. (`86c3c5e`)

### Fixed
- **Grab-to-pan** — the chart pan was half-built (scrolled a non-scrollable
  element and the whole page). Rewrote it: the tree is now a real scroll
  viewport with grab/grabbing cursors, a 5px click threshold, and
  click-suppression after drags. (`6776cd1`)
- **Shared notes without a token** — the field is now disabled with an amber
  warning instead of silently failing. (`7839093`)

### Changed
- **Tree chart is a scroll viewport** (part of the pan fix) — bounded height,
  pans in any direction once content overflows.

## Earlier 2026-10-09

- Buddy pages: resizable sidebar (220–560 px, remembered), Prev/Next/Back
  navigation, change journal with one-shot revert, photo dropzone with
  in-browser HEIC→JPEG conversion and repo push, shared repo notes.
  (`cf67d52`)
- Vertical zoom slider, timestamp build numbers on buddy and plan pages,
  back-to-buddies link. (`f2a33d7`)
- Tree nodes and Projects rows as drag-drop reparenting targets. (`7898c0d`)
- Click-to-rename app name, Shift+scroll zoom. (`d8aa179`)
- MGA + ML500 buddy records, zoom slider scaffolding, photo galleries.
  (`b1a7606`)
- App rename to Buddies, per-buddy icons, sidebar drag-to-reparent,
  Business Plans view. (`04d8bda`)
