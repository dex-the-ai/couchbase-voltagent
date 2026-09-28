#!/usr/bin/env bash
# Mirrors scripts/with-couchbase-docker.sh but avoids host port 11210 (in use by another task).
set -euo pipefail
c=couchbase-voltagent-test
B=http://127.0.0.1:28091
wait_for(){ local d=$1 n=$2; shift 2; for _ in $(seq 1 $n); do "$@" && return 0; sleep 1; done; echo "timeout $d" >&2; return 1; }
docker run -d --name $c -p 28091-28096:8091-8096 couchbase/server:enterprise-8.0.2 >/dev/null
wait_for ui 180 curl -fs -o /dev/null $B/ui/index.html
curl -fsS -X POST $B/clusterInit --data-urlencode username=Administrator --data-urlencode password=password --data-urlencode port=SAME --data-urlencode services=kv,n1ql,index --data-urlencode memoryQuota=512 --data-urlencode indexMemoryQuota=512 --data-urlencode indexerStorageMode=plasma --data-urlencode clusterName=voltagent-test --data-urlencode sendStats=false >/dev/null
wait_for init 120 curl -fs -o /dev/null -u Administrator:password $B/pools/default
curl -fsS -u Administrator:password -X POST $B/pools/default/buckets --data-urlencode name=voltagent --data-urlencode bucketType=couchbase --data-urlencode ramQuotaMB=256 --data-urlencode replicaNumber=0 --data-urlencode flushEnabled=1 >/dev/null
wait_for bucket 120 curl -fs -o /dev/null -u Administrator:password $B/pools/default/buckets/voltagent
wait_for query 180 curl -fs -o /dev/null -u Administrator:password -X POST http://127.0.0.1:28093/query/service --data-urlencode 'statement=SELECT 1 AS ready'
echo ready
