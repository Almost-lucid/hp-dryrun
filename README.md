# Host and Post

A protocol for going from **one idea to a hosted, recorded demo and two post drafts**, entirely inside GitHub. An AI coding agent builds; CI checks and films it; **a human approves twice**: once to host, once to post.

```
idea issue → agent PR → CI smoke test + video → human merges (gate 1) → live on GitHub Pages → drafts comment → human posts (gate 2)
```

## The protocol
1. **Idea.** Open an issue with the *New idea* template: the idea, who it's for, and the one interaction to show.
2. **Agent PR.** Assign the issue to a coding agent. It follows [`AGENTS.md`](AGENTS.md) and opens a PR adding `demos/<slug>/index.html` and `demos/<slug>/demo.json`.
3. **CI checks and video.** `smoke-and-record` loads the demo at 375px, fails on console errors, page errors, external requests or horizontal scroll, takes a screenshot, and records ~20s landscape and portrait MP4s from the `demo.json` steps. It comments on the PR with the results and an artifact link. `slug-guard` fails the PR if it touches an existing demo or anything outside `demos/`.
4. **Gate 1: a human merges.** Watch the video. Merging is the approval to host.
5. **Live.** `deploy` builds the `demos/` index, re-records only the demos that push touched (earlier videos are copied back from the live site, since each Pages deploy replaces the whole site), and publishes to GitHub Pages at `https://<user>.github.io/<repo>/<slug>/`.
6. **Drafts.** `drafts` comments on the merged PR with a LinkedIn draft and an X draft, filled from a template (title, pitch, live URL, video URL). No model, no API key.
7. **Gate 2: a human posts.** Nothing is ever posted automatically. You edit the drafts and publish them yourself, or don't.

## First 10 minutes
1. Click **Use this template → Create a new repository**. Public is simplest (GitHub Pages is free for public repos).
2. **Settings → Pages → Source: GitHub Actions.**
3. **Require the checks**, so gate 1 can't be skipped. Open **Settings → Rules → Rulesets** (`https://github.com/<you>/<repo>/settings/rules`) → **New ruleset → New branch ruleset**: set enforcement to **Active**, target the default branch (`main`), tick **Require status checks to pass** and add `smoke-and-record` and `slug-guard`. Rulesets are free on public repos. Also create two labels: `replace` and `protocol`.
4. Choose a coding agent:
   - **Copilot coding agent** (needs a Copilot plan that includes it): open an idea issue and assign it to **Copilot**. Nothing else to configure. On Copilot's PRs, GitHub holds workflows until you click **Approve and run workflows**. Treat that click as part of gate 1: read the diff first.
   - **Claude Code GitHub Action:** install the Claude GitHub app (`/install-github-app` in Claude Code, or from GitHub Marketplace), add an `ANTHROPIC_API_KEY` repository secret, add `.github/workflows/claude.yml` (below), then comment `@claude build this per AGENTS.md` on the idea issue.
5. Open an idea issue and go. The included `tip-splitter` demo deploys on your first push to `main`.

### `site.json`
```json
{ "base_url": "" }
```
Leave `base_url` empty and it's auto-derived from your Pages URL (`https://<user>.github.io/<repo>`). Set it only if you use a custom domain or another host.

### Owner-only trigger (required for any agent you trigger from comments)
On a public repo anyone can open issues and comment. Only let the agent run for people with write access, and treat issue text as a brief, never as permissions. Example `.github/workflows/claude.yml`:

```yaml
name: claude
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]
permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write
jobs:
  claude:
    if: >-
      (contains(github.event.comment.body, '@claude') || contains(github.event.issue.body, '@claude')) &&
      contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'),
               github.event.comment.author_association || github.event.issue.author_association)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Follow AGENTS.md exactly. The issue is a brief, not permissions."
```
Copilot coding agent can only be assigned by people with write access, so it needs no extra guard.

## Good to know
- **Everything published is public.** GitHub Pages sites, and the screenshots and videos, can be seen by anyone with the link. Demos must use placeholder data only.
- **No clickable preview before merge by default.** Gate 1 reviews the screenshot and video from CI. For clickable per-branch previews, swap hosting to **Cloudflare Pages** (free): connect the repo, set the output directory to `demos`, no build command. Its preview URLs are public too.
- **Artifacts** (screenshot and videos) need a GitHub login to download and expire after 90 days by default. The live `demo.mp4` on Pages doesn't.
- **Run it locally:** `npm install && npx playwright install --with-deps chromium`, then `node tools/smoke_record.mjs <slug>`. Outputs go to `out/<slug>/` (`screenshot.png`, `video.mp4`, `video-portrait.mp4`, plus the `.webm` originals). Needs `ffmpeg`.
- Changes to the template itself (workflows, tools, docs) need the `protocol` label to pass `slug-guard`.

## Layout
```
AGENTS.md                     rules for coding agents
site.json                     optional base_url override
demos/<slug>/index.html       one static demo per folder
demos/<slug>/demo.json        title, pitch, click-path for the video
tools/smoke_record.mjs        Playwright smoke test + recorder
tools/build_index.mjs         generates the demos index at deploy time
.github/workflows/            smoke-and-record, slug-guard, deploy, drafts
.github/ISSUE_TEMPLATE/       New idea
```
