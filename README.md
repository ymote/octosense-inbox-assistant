# Inbox Assistant

English | [简体中文](README.zh-CN.md)

A macOS **developer preview** for OctoSense: read Gmail, edit one reply shared
by Email / Reply / Chat, and review the exact saved message in the host’s
native approval sheet. Its optional app agent selectively creates Glance cards
for relevant new mail. App ID: `org.octosense.samples.inbox`, version `0.1.1` (release candidate).

## Required host

Install the [OctoSense desktop-v0.1.0-beta.2 macOS Apple Silicon preview](https://github.com/OctoSense-org/OctoSense/releases/tag/desktop-v0.1.0-beta.2).
The previous signed `0.1.0` bundle is available in the official App Hub catalog
(first admission: [sequence 7, App Hub #125](https://github.com/OctoSense-org/OctoSense-App-Hub/pull/125)). In OctoSense, open
**App Hub → Search**, search **Inbox Assistant**, then choose **Get → Install → Open**
after reviewing the requested permissions. The current `0.1.1` candidate needs
a new publisher signature and catalog admission before that installation path
serves it; use the immutable `v0.1.0` tag for the previous release.

Older shells and standalone `card-host` do not provide the OAuth/Gmail/agent
services. This repository contains the script bundle, not a desktop executable.

The host needs a registered Google desktop OAuth client, enabled Gmail API and
applicable Google consent/test-user configuration. See the
[versioned host setup guide](https://github.com/OctoSense-org/OctoSense/blob/desktop-v0.1.0-beta.2/crates/oauth-service/README.md).
There is no separate OctoSense account. Connect Google uses the host/browser;
this app receives only an account-bound handle, never your password or tokens.

## Use

1. The initial inbox is fictional and works without login. Local edits cannot
   send email; those fixtures and both listing screenshots are fictional.
2. On a compatible host, choose **Connect Google**. Manual reading/editing
   works without a model. AI sort, Chat and background triage send selected
   data to the host-configured model; read [Privacy](PRIVACY.md).
3. Allow the app agent separately to enable new-mail triage. Keep the inbox
   list open until **New-mail baseline ready** appears; local status refreshes
   every three seconds. The host normally checks new mail about every five
   minutes while execution is allowed. Existing mail is not backfilled into
   notifications. A ready baseline does not prove agent consent remains on.
4. Open a relevant Glance card, compose/edit in Reply, or ask Chat to change
   the same saved draft. Review the actual text before using **Review & Send**.
   Only the host’s physical approval control can authorize submission; the
   agent and automated clicks cannot. Gmail acceptance is not delivery.

Default triage examples include healthcare, shipping, scheduling, school/work
and family commitments. Marketing normally stays quiet. **Quiet mail is still
read by the agent/model to decide relevance.** Pin is a manual Glance action;
AI sort is a foreground helper, separate from automatic incoming events.

## What was tested

Historical [integrated evidence](https://github.com/OctoSense-org/OctoScript-App-Design-Flow/blob/5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95/examples/connected-apps/inbox/evidence/integrated/README.md)
and [Mac soak evidence](https://github.com/OctoSense-org/OctoScript-App-Design-Flow/blob/5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95/examples/connected-apps/inbox/evidence/soak/README.md)
used real DeepSeek with synthetic Gmail: 33 functional cycles over 610 seconds,
shared-draft editing, review cancellation, blocked automated approval and cold
restoration. **Two instrument frame-submission errors remain unresolved.**
Functional completion is not a clean rendering/performance pass.

Live Google OAuth, real Gmail reads/sends/delivery and physical send approval
remain unverified. Android’s Google adapter is missing; no Android, Windows
or Linux platform claim is made. Cross-app Calendar booking, attachments,
Reply All, rich-text replies, pagination beyond the first 30 rows and shared
system-memory promotion are not implemented in this app.

This version changes the notification schema, agent/skill guidance and release
metadata. The unchanged application/template UI bytes and original screenshots
do not make historical tests evidence for this new bundle digest.
[Provenance](ATTRIBUTION.md) and [0.1.0 source audit](review/SOURCE-AUDIT.json) distinguish
unchanged application bytes from the new package. No historical run is relabelled
as a test of the new signed release.

## Verify a published package

Read `public_key` from `publisher.json` into `YMOTE_PUBLIC_KEY`, then check the
unchanged release bytes:

```sh
"$HUB" check bundle --publisher-key "ymote=$YMOTE_PUBLIC_KEY"
```

Do not run `stamp` on a release just to make verification pass. An unsigned gate
is not a substitute for verifying its publisher signature.

## Develop and review

Work on an explicitly unsigned development copy (remove only
`integrity.signature` from that copy's manifest before regenerating).
Edit `src/workspace.splash`, then regenerate and check with the matching Hub:

```sh
python3 build_bundle.py
"$HUB" stamp bundle
"$HUB" check bundle --allow-unsigned
mkdir -p build
"$HUB" scan bundle --packet build/review.json
```

Only `bundle/` is submitted. Keep model profiles, accounts, captures from real
mail, signing keys and generated scan packets outside Git.
`verify_native.py --port PORT --binary /path/to/card-host` exercises fictional
UI data on an already-running owned host; its generated `evidence/` is ignored.
The full-shell launcher/soak helpers require explicitly selected private
profiles and the matching host binaries; they do not grant agent consent or
approve a send. See the versioned evidence above for those commands.

Publisher: [ymote](https://github.com/ymote). [Support](https://github.com/ymote/octosense-inbox-assistant/issues) ·
[Privacy](PRIVACY.md) · [Review answers](review/ANSWERS.md) · [Apache-2.0](LICENSE).
Do not post private messages, credentials or unredacted logs in public issues.

## 0.1.1 contract correction

The notification tool now requires the admitted `glance-workspace.splash`
template plus `initial.message`, title, summary and the notify decision. It
accepts no `script`, `source` or `data` alternative. The agent chooses relevance
and content; the signed template supplies the existing Email / Reply / Chat
workspace. Application and template UI bytes and original screenshots are
unchanged. No new live Gmail, sending or model-performance claim follows from
this declaration change. Run `python3 -m unittest discover -s tests -v` for the
release-contract checks and the matching Hub gate for structural admission.
