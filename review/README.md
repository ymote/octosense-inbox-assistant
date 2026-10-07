# Release review records

The current branch prepares **0.1.1**. The publisher must stamp and sign its exact
final bytes, check against the recorded public key and submit the new immutable
tag before official catalog publication. An unsigned gate is not admission.

[`releases/0.1.0/`](releases/0.1.0/RELEASE.json) preserves the previous release's
signed records. They do not verify the changed 0.1.1 bundle. Candidate packets
stay in ignored `build/`; the designated publisher adds the new signed records
here after signing. See [answers](ANSWERS.md) and the repository README.
