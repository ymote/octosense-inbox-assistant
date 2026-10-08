# Inbox Assistant for OctoSense

English | [简体中文](README.zh-CN.md)

A **macOS developer preview** to read Gmail, edit a shared reply through Email / Reply / Chat, and review the exact saved reply in the host before sending.
Publisher: [ymote](https://github.com/ymote). Fresh app ID: `io.github.ymote.inboxassistant`;
editable version: **0.2.0**. This is an independent sample, not a Google product.

The new app uses GitHub release attestations; no developer signing key or
repository signing secret is required. It is a separate install from
`org.octosense.samples.inbox`: existing app data and account grants are not migrated.
Old `v0.1.0` / `v0.1.1` tags, signatures and receipts remain unchanged.
`publisher.json` describes only that historical signing identity.

## Install and connect

This release requires **app contract 1.8.0 / `publisher-github-v1`** and the
compatible OctoSense connected-services host. The old desktop beta.2 cannot
install this GitHub-attested release. A repository tag alone is not App Hub
admission; use the submission's verified catalog/release status before expecting
it in search. In a compatible admitted catalog, open **App Hub → Search →
Inbox Assistant → Get → Install → Open** and review the requested permissions.

Google login uses the host's browser/provider flow, never a password field in
the app. The host operator supplies the registered OAuth client and enabled
provider APIs; normal users do not register developer clients. There is no
separate OctoSense account. See the [host OAuth guide](https://github.com/OctoSense-org/OctoSense/blob/main/crates/oauth-service/README.md).
The app receives an account-bound opaque handle, never credentials.

**Live Google login, provider reads/writes and physical approval are not
validated by this release's publishing tests.** Android Google authorization
remains unavailable; Android, Linux and Windows are not advertised platforms.
Standalone `card-host` checks local UI and explicit missing-service states only.

## Use

1. Start with the clearly fictional offline inbox. Select a message and use
   **Compose reply**. Local fictional drafts cannot send email.
2. In **Reply**, edit the body; **Details** reveals recipient and subject.
   Email, Reply and Chat share one saved draft. **Save** retains local edits.
3. On a configured host, **Connect Google** enables manual reading/editing.
   Review [Privacy](PRIVACY.md) before AI sort, Chat or background triage.
4. App-agent consent is separate from Google login. Allowing it enables a
   forward-only new-mail baseline and normally five-minute checks while host
   execution is allowed. Existing mail is not notified wholesale. The account
   peer decides which new mail deserves a Glance card; marketing normally stays
   quiet. **Quiet mail may still be sent to the configured model for triage.**
5. Use **Review & Send** to inspect the exact saved account, recipient, subject
   and body. Only a physical action on the native host approval control can
   authorize sending; automated input and the agent cannot. Gmail accepting a
   submission does not establish delivery.

The agent has private account-scoped read/draft/notification tools, with no send
alias. Cross-app Calendar booking, attachments, Reply All, rich-text replies,
pagination beyond the first 30 rows and system-memory promotion are not
implemented. AI sort is a separate foreground model action; disabling the
background agent does not disable that explicit button.

## Publishing and local checks

The editable `bundle/` contains no release proof. The generated
[GitHub workflow](.github/workflows/publish-app.yml) pins the reviewed Hub tools.
After testing and reviewing the final source, push a new `v<manifest.version>`
tag. GitHub prepares, attests, verifies and uploads `app.bundle.pack.json`;
never commit the sealed output over editable source or move an existing tag.

```sh
python3 -m unittest discover -s tests -v
python3 build_bundle.py
"$HUB" stamp bundle
"$HUB" check bundle --allow-unsigned
mkdir -p build
"$HUB" scan bundle --packet build/review.json
```

Open an [App Hub submission issue](https://github.com/OctoSense-org/OctoSense-App-Hub/issues)
with the app ID, source, permissions, screenshots and review answers. It can
precede the tag; add the successful workflow, exact commit and pack hash when
ready. Administrator review and catalog publication are separate from release
creation. Downloaded sealed packs are verified with `hub publisher-unpack` and
`hub publisher-verify`, not by restamping or removing their proof.

## Evidence boundaries

This version republishes the current functional source with a fresh identity
and workflow. Historical records under `review/`, `evidence/` where present,
and the immutable old tags keep their original source/binary identities. They
are not new acceptance evidence for version 0.2.0. Original screenshots are
replaced only by freshly inspected native captures before release.

The current Email/Reply/Chat layout comes from the previously unpublished
`0.1.2-ux.1` candidate, preserved without controller redesign. Historical Mac
runs used synthetic Gmail plus DeepSeek; two frame-submission errors remain
recorded. A separate private Android candidate completed 30 cycles, but that
is not Android Google support or a test of this package. See [layout history](review/UX-CANDIDATE.md)
and the [immutable prior README](https://github.com/ymote/octosense-inbox-assistant/blob/5025af76a4928b526111ea35b1b1300588ca6bd8/README.md).

Read [Privacy](PRIVACY.md) before connecting an account or enabling AI.
[Support](https://github.com/ymote/octosense-inbox-assistant/issues) is public: do not post private
messages, events, credentials or raw logs. [Apache-2.0](LICENSE).

Current source check: [native offline receipt](review/releases/0.2.0/NATIVE.json), [gate](review/releases/0.2.0/GATE.txt), [eight review answers](review/ANSWERS.md).
