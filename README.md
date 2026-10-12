# Host and Post

From one short idea to a **live demo**, a **video**, and **two post drafts** — on GitHub. You approve before anything is posted.

## Three steps

1. **Make your copy.** Click **Use this template → Create a new repository**, name it, then open **Settings → Pages → Source: GitHub Actions**.

2. **Open a New demo.** Click **[New demo](../../issues/new?template=new-demo.yml)** (on your copy: `Issues → New issue → New demo`). Fill in **Your idea** and **What should it do?**, then Submit.

3. **Watch the issue.** You’ll see `Building…`, then a **Live** link, a **video** link, and LinkedIn / X drafts. **Nothing has been posted.**

Optional: ask free ChatGPT to help write the idea and “what should it do?”, then paste that into the form.

### What we won’t host
No accounts, no real personal data, no secret API keys, no backends. Demos are small public static pages with sample data. If the idea needs a server, the build should fake it with placeholders.

## Paste fallback (works with free ChatGPT)

If the one-click build isn’t available, paste a page in by hand:

1. Ask ChatGPT (or any AI) something like:

   > Write one complete `index.html` for a small tip-splitter demo.
   > Rules: one screen; one main action; plain HTML/CSS/JS only; no frameworks; no CDN; no `<script src>`; no fetch/XHR; no backend/accounts/keys/personal data; under 300 lines; works at phone width; include `<title>` and `<meta name="description">`.
   > End with the exact filename `demos/tip-splitter/index.html` and the words: paste this, then click Commit.

2. In your repo click **Add file → Create new file**.
3. Set the path to `demos/<slug>/index.html` (use the filename the AI gave you).
4. Paste the HTML. Commit directly to `main` (or open a PR if you prefer).

GitHub Actions will smoke-test, record a video, publish to Pages, and leave drafts on the commit. **Nothing has been posted.**

## Optional upgrades

- **Claude:** connect the GitHub connector in Claude, then install the [Claude GitHub app](https://github.com/apps/claude/installations/select_target) on **only this repo**. If Claude can’t push (403), you skipped the app install.
- **OpenAI Codex:** Plus+; untested here.
- **Any other AI with a token:** [fine-grained PAT](https://github.com/settings/personal-access-tokens/new) — this repo only; Contents R/W, Pull requests R/W, Metadata R; no Workflows / Administration / Secrets; 90-day expiry.
- **Copilot coding agent:** no token; assign an idea issue to Copilot; on its PRs click **Approve and run workflows** only after you read the diff.

In plain terms: a scoped AI can only change this one repo, and your review (or the automated checks plus what you publish) still stands between a draft and the public internet.

## Optional: Lock it down

Needs admin. Without a ruleset, nothing technically stops a write-access account pushing to `main`. Create labels `build`, `replace`, and `protocol`, then a branch ruleset on `main` requiring checks `smoke-and-record` and `slug-guard` (and `build` if you want).

```sh
gh label create build -R <you>/<repo> -d "Build a demo from a New demo issue"
gh label create replace -R <you>/<repo> -d "Allow changing an existing demo"
gh label create protocol -R <you>/<repo> -d "Change the template itself"
gh api -X POST repos/<you>/<repo>/pages -f build_type=workflow
gh api -X POST repos/<you>/<repo>/rulesets --input - <<'JSON'
{"name": "gate 1", "target": "branch", "enforcement": "active",
 "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
 "rules": [{"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": false,
   "required_status_checks": [{"context": "smoke-and-record"}, {"context": "slug-guard"}]}}]}
JSON
```

**Teams:** optionally require 1 approving review (`required_approving_review_count: 1`, with `dismiss_stale_reviews_on_push` and `require_last_push_approval` true).

## Gallery

A browsable gallery of demos is coming soon. For now the Pages root lists whatever is in `demos/`.

### `site.json`
```json
{ "base_url": "" }
```
Leave empty unless you use a custom domain.

## Good to know
- Everything published on Pages is public. Placeholder data only.
- The one-click issue build uses GitHub Models with your `GITHUB_TOKEN` (no secrets to add). If Models isn’t available on the account, use the paste fallback.
- Template edits need the `protocol` label to pass `slug-guard`.
- Run locally: `npm install && npx playwright install --with-deps chromium`, then `node tools/smoke_record.mjs <slug>` (needs `ffmpeg`).

## Layout
```
AGENTS.md                     rules for coding agents / paste AIs
demos/<slug>/index.html       one static demo per folder
demos/<slug>/demo.json        optional title, pitch, video steps
tools/smoke_record.mjs        Playwright smoke test + recorder
tools/build_index.mjs         demos index at deploy time
.github/workflows/            build, smoke-and-record, slug-guard, deploy, drafts
.github/ISSUE_TEMPLATE/       New demo form
```
