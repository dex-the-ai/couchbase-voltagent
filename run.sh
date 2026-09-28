#!/usr/bin/env bash
# Run a command inside the Couchbase container's network namespace using node:24 with the repo mounted.
cleanup_flag=${CB_CLEANUP:-1}
exec docker run --rm --network container:couchbase-voltagent-test -v /home/ubuntu/github/couchbase-ecosystem/couchbase-voltagent:/w -w /w \
  -e CB_LIVE_TEST=1 -e CB_CONNECTION_STRING=couchbase://127.0.0.1 -e CB_USERNAME=Administrator -e CB_PASSWORD=password -e CB_BUCKET=voltagent -e CB_CLEANUP=$cleanup_flag \
  node:24 "$@"
