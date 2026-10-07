# Inbox Assistant privacy

English | [简体中文](PRIVACY.zh-CN.md)

Effective: 2026-10-06. Publisher: **ymote**. This describes the `0.1.0`
developer-preview bundle `org.octosense.samples.inbox` and the matching
connected-services host, not every service running inside OctoSense.

## Data and purposes

The initial examples and supplied screenshots are fictional. When you connect
Google through the host, the app can use the authorized Gmail account to list
Inbox/Important/Sent messages and read sender, recipient, subject, plain-text
body, message/thread identifiers and relevant headers. Attachment contents are
not read by this sample; the UI indicates omitted attachments. This information
supports reading, relevance decisions and preparing a reply.

The shared host presents Google authorization and requests account identity
(`openid`, `email`, `profile`), Gmail read access (`gmail.readonly`) and send
access (`gmail.send`). The app uses the host aliases `mail.read` and `mail.send`;
it receives an opaque app/account-bound connection handle. Provider access and
refresh tokens stay in the host credential vault (macOS Keychain on the tested
platform); they are not returned to this app or stored in its bundle. The app
never asks you to type a password, verification code or model API key into its UI.
No separate OctoSense account or publisher-operated login backend is required.

## Models and background mail

Google login and app-agent consent are separate. With the app agent enabled,
an allowed background worker establishes a forward-only history baseline, then
checks new mail, normally about every five minutes while host execution is
allowed. Existing mail is not notified wholesale. New message content can be
read by the account’s app peer and sent to the host-configured model to decide
whether to publish a card or record a quiet decision. **Quiet or unimportant
mail can therefore still be sent to the model for classification.**

Chat sends your request, selected-message context and the relevant saved reply
through the same account-bound app agent. The explicit **AI sort** action sends
the selected email to the host’s one-shot model service. A model may read and
edit the shared draft using admitted host tools. The app does not choose a
bundled model endpoint or see the model provider’s credentials. If the host
uses a remote provider, these inputs leave your device for that provider; a
local provider has different processing. Provider retention and further use
depend on its configuration and terms, which this app does not control.

Disable the app agent/background access to stop its automatic model triage.
Manual reading and editing do not require a model. **AI sort** is a separate
explicit foreground action, so disabling the agent is not a promise that
pressing that button will avoid model processing. No executable tool in this
bundle promotes email contents or preference summaries into shared system
memory or another app’s account.

## Cards, replies and sending

Glance and notifications may display sender/subject and a summary of relevant
mail. These can contain personal information and be visible to someone viewing
the device, according to the host’s display/notification settings. The card
keeps an account/message binding and admitted workspace source; the instruction
requires a loading placeholder instead of embedding the full email body in
card metadata. Opening the workspace reads the full email through the host.

Reply, Chat and review share a revisioned host draft. **Review & Send** asks
the host to display the exact account, recipient, subject and body. The agent
has no sending tool; a physical human action on the host’s native approval
control is required. If approved on a supported host, the host submits that
message to Gmail and the addressed recipient through Gmail. Gmail acceptance
is recorded separately from delivery. Unknown results are not automatically
resent. Live Google login, real Gmail sending and physical send approval are
not yet validated for this preview.

## Storage, recipients and deletion

The app’s local jail holds fictional drafts and the selected opaque handle.
Host-private storage holds real reply drafts, review/submission records,
connection metadata, event cursors/decisions and Glance notification records,
scoped by app/account. The app agent also has account-scoped conversation and
workspace data; prompts and tool results may include email or draft content.
Local files/logs and device backups can retain such information. Token-vault
protection does not imply that all email files are separately encrypted by
this app.

Data goes to Google for authorization/Gmail operations and to your configured
model when you use AI features or enable triage. An approved outgoing message
goes to Gmail and its recipient. This bundle contains no publisher-operated
mail relay, advertising, analytics or direct app network client; it requests
no `net` capability. The host and providers have their own data practices.

**Sign out** invalidates this app’s local connection and stops further use of
its active handle; it does not erase historical host drafts/submission records
or delete Gmail messages. Local disconnect does not itself revoke the Google
account’s provider-side OAuth grant. Manage that grant with Google when needed.
On ordinary App Hub uninstall, the matching host removes the app jail, suspends
and purges its peers, revokes its local connections and attempts to purge its
private drafts/events and Glance outbox. Storage/vault failures can prevent
complete cleanup and are reported by the host. Uninstall cannot erase provider
records, already sent messages or external/device backups. This preview has
no separate in-app retention controls or guaranteed timed deletion for drafts
and conversation history.

## Support and changes

Use [the public issue tracker](https://github.com/ymote/octosense-inbox-assistant/issues)
for non-sensitive bug reports. The publisher receives information you choose
to post there; do not include private mail, tokens, account files, medical
details or raw logs. Source and privacy changes are versioned in this repository.
See [README](README.md) for required host versions and tested limitations.
