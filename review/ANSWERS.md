# App Hub scan answers — 0.2.1

Publisher self-review for `io.github.ymote.inboxassistant`; not an administrator verdict.
The eight questions below were emitted by the recorded Hub scan.

## 1. Does the app do what its name, subtitle and description claim? Cite the text in its source.

The current src/workspace.splash controller implements message selection, shared reply editing, details, save, Chat, local fictional-send refusal and explicit unavailable-service states. Native verification drove those states and exact multiline Unicode draft restoration. Auth/Gmail/model and background notification code remain present but were not connected to a provider in this release test.

## 2. Do the listing's platforms and category fit an app of this kind?

Productivity and macOS developer preview match the bounded evidence. Original captures are from an owned hidden Mac card-host at412x892 logical points. Google Android authorization remains unsupported; no Android, Windows or Linux platform claim is added. This is not an end-to-end provider or performance soak.

## 3. Do the granted capabilities match what the app visibly does? For a script app, name every host it requests and why. Name any grant nothing on screen needs.

storage retains local fictional drafts and selected opaque handle; auth connects/selects/disconnects through the host; gmail serves messages/revisioned drafts/review; model powers explicit AI sort; glance publishes/retires local cards; octos.session.open and octos.turn.start power consented Chat. The host-generated inboxassistant.new_message event uses the fresh namespace. No net capability or direct hosts are requested; Google/model network calls stay in host services.

## 4. Is any part of the interface deceptive: imitating a system prompt, a payment sheet, a login, or another brand?

Connect Google requests the actual host/provider flow and never imitates a password form. Review requests the host-owned exact-content control; the app does not grant approval to itself. Names describe Google compatibility, not endorsement. Screenshots use fictional content and clearly show local or unavailable-service states. There is no payment interface.

## 5. Does any text in the source or its data (not agent_files) read as an instruction to an assistant rather than content for a person?

Yes. classify and ask construct explicit prompts for this app’s configured model/account-bound peer. The source names only inboxassistant.message/draft_get/draft_edit and treats email context as data. These developer-authored prompts do not authorize sending. The agent skill explicitly treats external email instructions as untrusted.

## 6. Is any wording abusive, or aimed at a private individual?

No abusive or targeted private-person content was found. Current screenshots contain reserved/example fictional senders or synthetic event text. No personal account, OAuth registration, token, mail/calendar export or raw private log is distributed.

## 7. The agent files (agent_files) instruct this app's own assistant. Do they stay within this app's data and tools, without addressing other apps' assistants or the system agent, or asking for tools, hosts or approvals the manifest does not grant? Does each tool's risk match what it does: anything that sends, posts, shares, deletes or spends must be destructive; is anything marked shareable that returns the person's private data? For a tool with confirm "app", does the app visibly show its own confirmation, with the exact action, before it runs?

All nine inboxassistant.* tools retain private_data:true, shareable:false and their reviewed host_method/risk flags. Message/draft/event reads are read; local draft edits, durable decisions and local card display are act. No tool calls gmail.send, gmail.draft.review or gmail.sheet.close. The notification alias accepts only the admitted template+initial message schema, not script/source. The renamed skill and host event stay inside the fresh app/account. Physical host approval remains required for actual sending; this test did not attempt it.

## 8. Route: pass, human-review, or reject. Give reasons a publisher can act on.

human-review. Unsigned source gate and bounded native local UI checks passed; original pixels were inspected separately. Verify the successful GitHub workflow, exact tag/commit/pack/proof, privacy URL and compatible host before admission. No developer signing key is requested. The fresh ID must not adopt the legacy catalog history. Genuine 0.2.0 proof verification and isolated Mac install/local editing passed; genuine 0.2.1 update, exact local draft retention and Library reopening passed on the recorded Mac host. Official catalog publication still requires maintainer admission; live Google/provider/model/physical-write evidence is not supplied here.
