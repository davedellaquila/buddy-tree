# Buddy Tree — Project Buddy Dashboard

The web dashboard for Dave's Buddy family. One page per buddy, hierarchical
views (Tree, Org chart, Outline), and a shared-notes + photos layer that syncs
back to each buddy's repo.

- **Live:** https://davedellaquila.github.io/buddy-tree/
- **Repo:** https://github.com/davedellaquila/buddy-tree
- **Build:** `build.py` generates `index.html` from `buddies.json` + `plans.json`.
- **Features:** see [FEATURES.md](FEATURES.md) (living registry — update it when a feature ships or changes).
- **Changelog:** see [CHANGELOG.md](CHANGELOG.md).

## GitHub token (read this once)

Some features write **directly to your buddy repos from your browser** via the
GitHub API:

- **Shared notes** — each buddy page's shared-notes section syncs to that
  buddy's repo as `docs/notes.md`, so anyone with repo access sees them.
- **Photo uploads** — photos dropped on a buddy page publish to
  `photos/<buddy-id>/` in that buddy's repo.

GitHub's API requires a personal access token to accept those writes. Key
facts:

- **One token, entered once, globally** — it is *not* per buddy. Enter it a
  single time and every buddy page uses it.
- **Where to get it:** https://github.com/settings/tokens/new — create a
  **classic** token with the **`repo`** scope ticked. Nothing else is needed.
- **Where to enter it:** the token field in the Photos section of any buddy
  page. After saving, the field is replaced with a green checkmark.
- **Storage:** the token lives only in your browser on that device
  (localStorage). It is never sent anywhere except GitHub's API.
- **Without it:** the shared-notes field is disabled with an amber warning
  explaining what's missing. The device-local scratch pad still works —
  it never needed a token.

Heads-up: `buddy-tree` itself is a **public** repo, so anything rendered on
the dashboard site is public. The individual buddy repos are private.
