# Lifecycle sweep evidence: t_c71a7e66

Manual validation evidence for Couchbase-Ecosystem/couchbase-voltagent branch `chore/lifecycle-sweep-20260928` (commit d1a477a).
Couchbase Server enterprise-8.0.2 in Docker, bucket `voltagent`, scope/collection `support_demo.knowledge` created by `npm run example:customer-support`.

- `up.sh` / `run.sh`: harness mirroring `scripts/with-couchbase-docker.sh` (host 11210 was taken by another container, so tests run in the container's network namespace).
- `capture.py`: Playwright script that produced the screenshots and `couchbase-web-console-walkthrough.mp4`.
- Not part of the product; do not merge.
