# Working on Inbox Assistant

This is a standalone publisher repository for `org.octosense.samples.inbox`
0.1.1, derived from the immutable source in [ATTRIBUTION.md](ATTRIBUTION.md).
Read [README.md](README.md), [PRIVACY.md](PRIVACY.md), and the upstream
[App Hub publishing contract](https://github.com/OctoSense-org/OctoSense-App-Hub/blob/main/docs/PUBLISHING.md).

- Edit `src/workspace.splash`, then run `python3 build_bundle.py`; main and
  Glance share one controller. Do not change functional source merely to fix
  publisher metadata. Keep agent/data/account boundaries and physical approval.
- Use the matching host and Hub versions. Do not invent services or expose
  credentials in the app. `model.complete` is foreground AI sort; actual
  Chat/background work uses this app’s admitted account-bound peer and tools.
- Only `bundle/` is submitted. Stamp after bundle edits, then check and scan.
  A signed package needs a new signature after any edit. Never claim catalog
  admission or a reviewer approval from an unsigned gate pass.
- Keep build/scan packets, profiles, keys, state and real-mail captures outside
  Git. Historical evidence stays at its immutable upstream links. Keep the
  two README and privacy languages aligned and preserve attribution.
- Use owned hidden Makepad instances and distinct ports. Native read-back,
  original pixel review and external provider effects are separate checks.
  Close each owned instance via `/quit`; never replay uncertain actions.
- Publisher identity, signing, repository/tag/release and review submission
  follow the person’s explicit authorization. Do not invent that authorization
  or write directly to the App Hub signed catalog/artifact directories.
