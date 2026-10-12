# Host and Post

From one short idea to a **live demo**, a **video**, and **two post drafts** — on GitHub. You approve before anything is posted.

## Three steps

1. **Make your copy.** Click **Use this template → Create a new repository**, name it, then open **Settings → Pages → Source: GitHub Actions**.

2. **Open a New demo.** On a **laptop where you’re signed into GitHub**, either click **[New demo](../../issues/new?template=new-demo.yml)** and fill the form, or use the free ChatGPT prompt below to get a prefilled link.

3. **Watch the issue.** You’ll see `Building…`, then a **Live** link, a **video** link, and LinkedIn / X drafts. **Nothing has been posted.**

### Free ChatGPT → page + prefilled New demo link

Do this on a **laptop where you’re signed into GitHub**. Paste the whole block into ChatGPT (free is fine):

```text
I want to open a GitHub "New demo" issue for my Host and Post repo.

Ask me once for my GitHub username and repository name, then help me shape one small demo idea (one screen, one main action).

Then write the full page in ONE fenced code block. Rules:
- Complete file from <!doctype html> through </html> — never abbreviate, never say "rest unchanged"
- Under 300 lines; plain HTML/CSS/JS only
- No frameworks, CDN, <script src>, fetch/XHR/WebSocket, backend, accounts, API keys, or personal data
- Works at phone width; sample/placeholder data only; include <title> and <meta name="description">
- If it would need a server, fake it with sample data

Then output:
1) A short plain-text idea and a 3–5 line spec.
2) The ONE code block with the full HTML.
3) ONE URL (URL-encoded) with only title, idea, and spec (the page is too long for a URL), params in this order:
https://github.com/<username>/<repo>/issues/new?template=new-demo.yml&title=<urlencode("New demo: " + idea)>&idea=<urlencode(idea)>&spec=<urlencode(spec)>

Tell me to: tap the link, paste the code block into the form field "Paste your page", then click Submit.
If the link breaks: Issues → New demo, paste idea/spec/page myself.
```

Example link (page is pasted into the form, not the URL):

https://github.com/Almost-lucid/hp-dryrun/issues/new?template=new-demo.yml&title=New%20demo%3A%20tip%20splitter&idea=tip%20splitter&spec=Enter%20a%20bill%20in%20pounds%2C%20pick%20a%20tip%20percent%2C%20set%20how%20many%20people%2C%20and%20show%20what%20each%20person%20pays.

### What we won’t host
No accounts, no real personal data, no secret API keys, no backends. Demos are small public static pages with sample data. If the idea needs a server, the build should fake it with placeholders.

## File paste fallback

If you prefer not to use the issue form, you can still commit a file by hand:

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

Needs admin. Without a ruleset, nothing technically stops a write-access account pushing to `main`.
**Note:** the one-click issue build commits to `main` as `github-actions[bot]`. If your ruleset requires a pull request, add a bypass for GitHub Actions — or skip Lock it down and use the paste route. Create labels `build`, `replace`, and `protocol`, then a branch ruleset on `main` requiring checks `smoke-and-record` and `slug-guard` (and `build` if you want).

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
- Prefer pasting a complete page into **Paste your page** on the New demo form (ChatGPT prompt above). If that field is empty, the workflow tries GitHub Models; when Models isn’t available it says so in a comment.
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
