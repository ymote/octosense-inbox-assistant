# Source attribution and packaging changes

Inbox Assistant derives from the Apache-2.0
[OctoScript-App-Design-Flow sample](https://github.com/OctoSense-org/OctoScript-App-Design-Flow/tree/5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95/examples/connected-apps/inbox)
at commit `5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95`. Copyright 2026 The OctoSense
Authors; see [LICENSE](LICENSE) and [NOTICE](NOTICE). The package preserves
`org.octosense.samples.inbox` and version `0.1.0`.

Only allowlisted tracked files were extracted from that commit. No ignored
profiles, keys, build output, private email or raw runtime logs were copied.
The app source, generated main/Glance programs, tools, agent instructions,
triage skill, icon and two listing PNGs are byte-identical to that source.
The PNGs are historical native captures of explicitly fictional offline states,
not screenshots of live Google mail or a new signed release.

Modified for standalone ymote packaging: `bundle/listing.json` replaces
publisher/support/privacy placeholders and describes the developer-preview
limits; `bundle/manifest.json` is restamped. Standalone README, privacy,
review answers, developer instructions and ignore rules are supplied here.
The local verifier now requires an explicit binary instead of guessing the
old workspace layout; the collector docstring points to immutable evidence.
These metadata changes change the digest; old receipts retain their own
original digests and are never restamped or relabelled.

The host reference is [OctoSense commit 26b9fe9f](https://github.com/OctoSense-org/OctoSense/tree/26b9fe9fa51ef3c1fe6f833743144a2e12cf54e3),
including the connected-services work in PR #347, with App Hub PR #119.
Historical test binaries and source hashes remain documented in the immutable
[Flow evidence](https://github.com/OctoSense-org/OctoScript-App-Design-Flow/blob/5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95/examples/connected-apps/inbox/evidence/soak/README.md).
[Source audit](review/SOURCE-AUDIT.json) compares the copied application files.

The bundle redistributes no Makepad, octos, OctoSense host executable or Google
SDK, and no upstream font directory. References to Gmail/Google identify the
provider integration, not an endorsement.
