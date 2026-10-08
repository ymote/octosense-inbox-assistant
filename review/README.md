# Current review: 0.2.1 publication guidance update

See [0.2.1 source gate](releases/0.2.1/GATE.txt), [preparation](releases/0.2.1/PREPARATION.json) and [answers](ANSWERS.md). App UI, permissions and storage remain unchanged. The [0.2.0 genuine release installation](releases/0.2.0/PUBLISHING.json) is prior-version evidence; the 0.2.1 update is validated separately after release. Official catalog admission is a maintainer decision.

## Historical 0.1.x records

# Release review records

**0.1.1 is publisher-signed.** `GATE.txt` / `GATE.json` verify the final signed
bundle against the recorded ymote public key and existing official catalog.
`QUESTIONS.json` contains the eight emitted scan questions; `ANSWERS.md` is the
publisher self-review, not a maintainer verdict. `RELEASE.json` binds these
checks to the exact bundle files and the Hub tool used.

Official catalog admission remains a separate maintainer decision. The immutable
`v0.1.1` source tag identifies this release once published. The previous signed
records in [`releases/0.1.0/`](releases/0.1.0/RELEASE.json) and unsigned preparation
record `VALIDATION-0.1.1.json` remain historical; they do not replace the final
signed check or claim new native/provider execution. Raw scan packets stay in
ignored `build/` outside the bundle.
