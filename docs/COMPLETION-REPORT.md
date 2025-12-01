PS C:\Users\姚东名> wsl docker ps -a
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
^CCONTAINER ID   IMAGE                      COMMAND            CREATED          STATUS         PORTS                                            NAMES
a88445208cf9   redis/redis-stack:latest   "/entrypoint.sh"   27 minutes ago   Up 3 seconds   0.0.0.0:6379->6379/tcp, 0.0.0.0:8001->8001/tcp   redis-stack
PS C:\Users\姚东名> docker logs redis-stack
docker : 无法将“docker”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确
保路径正确，然后再试一次。
所在位置 行:1 字符: 1
+ docker logs redis-stack
+ ~~~~~~
    + CategoryInfo          : ObjectNotFound: (docker:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

PS C:\Users\姚东名> wsl docker logs redis-stack
wsl: 无法配置网络 (networkingMode Nat)，回退到 networkingMode VirtioProxy。
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
9:C 30 Nov 2025 01:23:08.595 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
9:C 30 Nov 2025 01:23:08.596 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
9:C 30 Nov 2025 01:23:08.596 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=9, just started
9:C 30 Nov 2025 01:23:08.596 * Configuration loaded
9:M 30 Nov 2025 01:23:08.596 * Increased maximum number of open files to 10032 (it was originally set to 1024).
9:M 30 Nov 2025 01:23:08.596 * monotonic clock: POSIX clock_gettime
9:M 30 Nov 2025 01:23:08.597 * Running mode=standalone, port=6379.
9:M 30 Nov 2025 01:23:08.598 * Module 'RedisCompat' loaded from /opt/redis-stack/lib/rediscompat.so
9:M 30 Nov 2025 01:23:08.600 * <search> Redis version found by RedisSearch : 7.4.7 - oss
9:M 30 Nov 2025 01:23:08.600 * <search> RediSearch version 2.10.20 (Git=5c09b69)
9:M 30 Nov 2025 01:23:08.600 * <search> Low level api version 1 initialized successfully
9:M 30 Nov 2025 01:23:08.600 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  10000,
9:M 30 Nov 2025 01:23:08.600 * <search> Initialized thread pools!
9:M 30 Nov 2025 01:23:08.600 * <search> Subscribe to config changes
9:M 30 Nov 2025 01:23:08.600 * <search> Enabled role change notification
9:M 30 Nov 2025 01:23:08.601 * Module 'search' loaded from /opt/redis-stack/lib/redisearch.so
9:M 30 Nov 2025 01:23:08.602 * <timeseries> RedisTimeSeries version 11206, git_sha=cdcbe34f8e87e15ea700b737634be6bac6b6700b
9:M 30 Nov 2025 01:23:08.602 * <timeseries> Redis version found by RedisTimeSeries : 7.4.7 - oss
9:M 30 Nov 2025 01:23:08.602 * <timeseries> loaded default CHUNK_SIZE_BYTES policy: 4096
9:M 30 Nov 2025 01:23:08.602 * <timeseries> loaded server DUPLICATE_POLICY: block
9:M 30 Nov 2025 01:23:08.602 * <timeseries> loaded default IGNORE_MAX_TIME_DIFF: 0
9:M 30 Nov 2025 01:23:08.602 * <timeseries> loaded default IGNORE_MAX_VAL_DIFF: 0.000000
9:M 30 Nov 2025 01:23:08.602 * <timeseries> Setting default series ENCODING to: compressed
9:M 30 Nov 2025 01:23:08.602 * <timeseries> Detected redis oss
9:M 30 Nov 2025 01:23:08.602 * Module 'timeseries' loaded from /opt/redis-stack/lib/redistimeseries.so
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 30 Nov 2025 01:23:08.603 # <ReJSON> Skip register defrag callbacks as defrag callbacks is not supported on the current Redis server.
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Exported RedisJSON_V1 API
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Exported RedisJSON_V2 API
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Exported RedisJSON_V3 API
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Exported RedisJSON_V4 API
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Exported RedisJSON_V5 API
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Enabled diskless replication
9:M 30 Nov 2025 01:23:08.603 * <ReJSON> Initialized shared string cache, thread safe: false.
9:M 30 Nov 2025 01:23:08.603 * Module 'ReJSON' loaded from /opt/redis-stack/lib/rejson.so
9:M 30 Nov 2025 01:23:08.603 * <search> Acquired RedisJSON_V5 API
9:M 30 Nov 2025 01:23:08.604 * <bf> RedisBloom version 2.8.16 (Git=unknown)
9:M 30 Nov 2025 01:23:08.604 * Module 'bf' loaded from /opt/redis-stack/lib/redisbloom.so
9:M 30 Nov 2025 01:23:08.604 * <redisgears_2> Created new data type 'GearsType'
9:M 30 Nov 2025 01:23:08.605 * <redisgears_2> Detected redis oss
9:M 30 Nov 2025 01:23:08.605 # <redisgears_2> could not initialize RedisAI_InitError

9:M 30 Nov 2025 01:23:08.605 * <redisgears_2> Failed loading RedisAI API.
9:M 30 Nov 2025 01:23:08.605 * <redisgears_2> RedisGears v2.0.20, sha='9b737886bf825fe29ddc2f8da81f73cbe0b4e858', build_type='release', built_for='Linux-ubuntu22.04.x86_64', redis_version:'7.4.7', enterprise:'false'.
9:M 30 Nov 2025 01:23:08.606 * <redisgears_2> Registered backend: js.
9:M 30 Nov 2025 01:23:08.607 * Module 'redisgears_2' loaded from /opt/redis-stack/lib/redisgears.so
9:M 30 Nov 2025 01:23:08.620 * Server initialized
9:M 30 Nov 2025 01:23:08.620 * Ready to accept connections tcp
9:C 30 Nov 2025 01:23:38.866 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
9:C 30 Nov 2025 01:23:38.866 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
9:C 30 Nov 2025 01:23:38.866 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=9, just started
9:C 30 Nov 2025 01:23:38.866 * Configuration loaded
9:M 30 Nov 2025 01:23:38.867 * Increased maximum number of open files to 10032 (it was originally set to 1024).
9:M 30 Nov 2025 01:23:38.868 * monotonic clock: POSIX clock_gettime
9:M 30 Nov 2025 01:23:38.870 * Running mode=standalone, port=6379.
9:M 30 Nov 2025 01:23:38.873 * Module 'RedisCompat' loaded from /opt/redis-stack/lib/rediscompat.so
9:M 30 Nov 2025 01:23:38.900 * <search> Redis version found by RedisSearch : 7.4.7 - oss
9:M 30 Nov 2025 01:23:38.900 * <search> RediSearch version 2.10.20 (Git=5c09b69)
9:M 30 Nov 2025 01:23:38.901 * <search> Low level api version 1 initialized successfully
9:M 30 Nov 2025 01:23:38.902 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  10000,
9:M 30 Nov 2025 01:23:38.903 * <search> Initialized thread pools!
9:M 30 Nov 2025 01:23:38.905 * <search> Subscribe to config changes
9:M 30 Nov 2025 01:23:38.905 * <search> Enabled role change notification
9:M 30 Nov 2025 01:23:38.905 * Module 'search' loaded from /opt/redis-stack/lib/redisearch.so
9:M 30 Nov 2025 01:23:38.910 * <timeseries> RedisTimeSeries version 11206, git_sha=cdcbe34f8e87e15ea700b737634be6bac6b6700b
9:M 30 Nov 2025 01:23:38.910 * <timeseries> Redis version found by RedisTimeSeries : 7.4.7 - oss
9:M 30 Nov 2025 01:23:38.910 * <timeseries> loaded default CHUNK_SIZE_BYTES policy: 4096
9:M 30 Nov 2025 01:23:38.910 * <timeseries> loaded server DUPLICATE_POLICY: block
9:M 30 Nov 2025 01:23:38.910 * <timeseries> loaded default IGNORE_MAX_TIME_DIFF: 0
9:M 30 Nov 2025 01:23:38.910 * <timeseries> loaded default IGNORE_MAX_VAL_DIFF: 0.000000
9:M 30 Nov 2025 01:23:38.910 * <timeseries> Setting default series ENCODING to: compressed
9:M 30 Nov 2025 01:23:38.911 * <timeseries> Detected redis oss
9:M 30 Nov 2025 01:23:38.912 * Module 'timeseries' loaded from /opt/redis-stack/lib/redistimeseries.so
9:M 30 Nov 2025 01:23:38.921 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 30 Nov 2025 01:23:38.921 # <ReJSON> Skip register defrag callbacks as defrag callbacks is not supported on the current Redis server.
9:M 30 Nov 2025 01:23:38.922 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Exported RedisJSON_V1 API
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Exported RedisJSON_V2 API
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Exported RedisJSON_V3 API
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Exported RedisJSON_V4 API
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Exported RedisJSON_V5 API
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Enabled diskless replication
9:M 30 Nov 2025 01:23:38.923 * <ReJSON> Initialized shared string cache, thread safe: false.
9:M 30 Nov 2025 01:23:38.923 * Module 'ReJSON' loaded from /opt/redis-stack/lib/rejson.so
9:M 30 Nov 2025 01:23:38.923 * <search> Acquired RedisJSON_V5 API
9:M 30 Nov 2025 01:23:38.926 * <bf> RedisBloom version 2.8.16 (Git=unknown)
9:M 30 Nov 2025 01:23:38.927 * Module 'bf' loaded from /opt/redis-stack/lib/redisbloom.so
9:M 30 Nov 2025 01:23:38.937 * <redisgears_2> Created new data type 'GearsType'
9:M 30 Nov 2025 01:23:38.940 * <redisgears_2> Detected redis oss
9:M 30 Nov 2025 01:23:38.943 # <redisgears_2> could not initialize RedisAI_InitError

9:M 30 Nov 2025 01:23:38.943 * <redisgears_2> Failed loading RedisAI API.
9:M 30 Nov 2025 01:23:38.943 * <redisgears_2> RedisGears v2.0.20, sha='9b737886bf825fe29ddc2f8da81f73cbe0b4e858', build_type='release', built_for='Linux-ubuntu22.04.x86_64', redis_version:'7.4.7', enterprise:'false'.
9:M 30 Nov 2025 01:23:38.964 * <redisgears_2> Registered backend: js.
9:M 30 Nov 2025 01:23:38.972 * Module 'redisgears_2' loaded from /opt/redis-stack/lib/redisgears.so
9:M 30 Nov 2025 01:23:38.999 * Server initialized
9:M 30 Nov 2025 01:23:39.000 * Ready to accept connections tcp
9:C 30 Nov 2025 01:27:32.745 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
9:C 30 Nov 2025 01:27:32.746 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
9:C 30 Nov 2025 01:27:32.746 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=9, just started
9:C 30 Nov 2025 01:27:32.746 * Configuration loaded
9:M 30 Nov 2025 01:27:32.746 * Increased maximum number of open files to 10032 (it was originally set to 1024).
9:M 30 Nov 2025 01:27:32.746 * monotonic clock: POSIX clock_gettime
9:M 30 Nov 2025 01:27:32.748 * Running mode=standalone, port=6379.
9:M 30 Nov 2025 01:27:32.750 * Module 'RedisCompat' loaded from /opt/redis-stack/lib/rediscompat.so
9:M 30 Nov 2025 01:27:32.766 * <search> Redis version found by RedisSearch : 7.4.7 - oss
9:M 30 Nov 2025 01:27:32.766 * <search> RediSearch version 2.10.20 (Git=5c09b69)
9:M 30 Nov 2025 01:27:32.767 * <search> Low level api version 1 initialized successfully
9:M 30 Nov 2025 01:27:32.768 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  10000,
9:M 30 Nov 2025 01:27:32.768 * <search> Initialized thread pools!
9:M 30 Nov 2025 01:27:32.769 * <search> Subscribe to config changes
9:M 30 Nov 2025 01:27:32.769 * <search> Enabled role change notification
9:M 30 Nov 2025 01:27:32.769 * Module 'search' loaded from /opt/redis-stack/lib/redisearch.so
9:M 30 Nov 2025 01:27:32.772 * <timeseries> RedisTimeSeries version 11206, git_sha=cdcbe34f8e87e15ea700b737634be6bac6b6700b
9:M 30 Nov 2025 01:27:32.772 * <timeseries> Redis version found by RedisTimeSeries : 7.4.7 - oss
9:M 30 Nov 2025 01:27:32.772 * <timeseries> loaded default CHUNK_SIZE_BYTES policy: 4096
9:M 30 Nov 2025 01:27:32.772 * <timeseries> loaded server DUPLICATE_POLICY: block
9:M 30 Nov 2025 01:27:32.772 * <timeseries> loaded default IGNORE_MAX_TIME_DIFF: 0
9:M 30 Nov 2025 01:27:32.772 * <timeseries> loaded default IGNORE_MAX_VAL_DIFF: 0.000000
9:M 30 Nov 2025 01:27:32.772 * <timeseries> Setting default series ENCODING to: compressed
9:M 30 Nov 2025 01:27:32.773 * <timeseries> Detected redis oss
9:M 30 Nov 2025 01:27:32.773 * Module 'timeseries' loaded from /opt/redis-stack/lib/redistimeseries.so
9:M 30 Nov 2025 01:27:32.779 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 30 Nov 2025 01:27:32.779 # <ReJSON> Skip register defrag callbacks as defrag callbacks is not supported on the current Redis server.
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Exported RedisJSON_V1 API
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Exported RedisJSON_V2 API
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Exported RedisJSON_V3 API
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Exported RedisJSON_V4 API
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Exported RedisJSON_V5 API
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Enabled diskless replication
9:M 30 Nov 2025 01:27:32.780 * <ReJSON> Initialized shared string cache, thread safe: false.
9:M 30 Nov 2025 01:27:32.780 * Module 'ReJSON' loaded from /opt/redis-stack/lib/rejson.so
9:M 30 Nov 2025 01:27:32.780 * <search> Acquired RedisJSON_V5 API
9:M 30 Nov 2025 01:27:32.782 * <bf> RedisBloom version 2.8.16 (Git=unknown)
9:M 30 Nov 2025 01:27:32.782 * Module 'bf' loaded from /opt/redis-stack/lib/redisbloom.so
9:M 30 Nov 2025 01:27:32.788 * <redisgears_2> Created new data type 'GearsType'
9:M 30 Nov 2025 01:27:32.790 * <redisgears_2> Detected redis oss
9:M 30 Nov 2025 01:27:32.791 # <redisgears_2> could not initialize RedisAI_InitError

9:M 30 Nov 2025 01:27:32.791 * <redisgears_2> Failed loading RedisAI API.
9:M 30 Nov 2025 01:27:32.791 * <redisgears_2> RedisGears v2.0.20, sha='9b737886bf825fe29ddc2f8da81f73cbe0b4e858', build_type='release', built_for='Linux-ubuntu22.04.x86_64', redis_version:'7.4.7', enterprise:'false'.
9:M 30 Nov 2025 01:27:32.803 * <redisgears_2> Registered backend: js.
9:M 30 Nov 2025 01:27:32.808 * Module 'redisgears_2' loaded from /opt/redis-stack/lib/redisgears.so
9:M 30 Nov 2025 01:27:32.820 * Server initialized
9:M 30 Nov 2025 01:27:32.821 * Ready to accept connections tcp
9:C 30 Nov 2025 01:32:02.357 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
9:C 30 Nov 2025 01:32:02.358 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
9:C 30 Nov 2025 01:32:02.358 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=9, just started
9:C 30 Nov 2025 01:32:02.358 * Configuration loaded
9:M 30 Nov 2025 01:32:02.360 * Increased maximum number of open files to 10032 (it was originally set to 1024).
9:M 30 Nov 2025 01:32:02.360 * monotonic clock: POSIX clock_gettime
9:M 30 Nov 2025 01:32:02.364 * Running mode=standalone, port=6379.
9:M 30 Nov 2025 01:32:02.366 * Module 'RedisCompat' loaded from /opt/redis-stack/lib/rediscompat.so
9:M 30 Nov 2025 01:32:02.392 * <search> Redis version found by RedisSearch : 7.4.7 - oss
9:M 30 Nov 2025 01:32:02.393 * <search> RediSearch version 2.10.20 (Git=5c09b69)
9:M 30 Nov 2025 01:32:02.394 * <search> Low level api version 1 initialized successfully
9:M 30 Nov 2025 01:32:02.396 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  10000,
9:M 30 Nov 2025 01:32:02.397 * <search> Initialized thread pools!
9:M 30 Nov 2025 01:32:02.399 * <search> Subscribe to config changes
9:M 30 Nov 2025 01:32:02.399 * <search> Enabled role change notification
9:M 30 Nov 2025 01:32:02.400 * Module 'search' loaded from /opt/redis-stack/lib/redisearch.so
9:M 30 Nov 2025 01:32:02.407 * <timeseries> RedisTimeSeries version 11206, git_sha=cdcbe34f8e87e15ea700b737634be6bac6b6700b
9:M 30 Nov 2025 01:32:02.408 * <timeseries> Redis version found by RedisTimeSeries : 7.4.7 - oss
9:M 30 Nov 2025 01:32:02.408 * <timeseries> loaded default CHUNK_SIZE_BYTES policy: 4096
9:M 30 Nov 2025 01:32:02.408 * <timeseries> loaded server DUPLICATE_POLICY: block
9:M 30 Nov 2025 01:32:02.408 * <timeseries> loaded default IGNORE_MAX_TIME_DIFF: 0
9:M 30 Nov 2025 01:32:02.408 * <timeseries> loaded default IGNORE_MAX_VAL_DIFF: 0.000000
9:M 30 Nov 2025 01:32:02.408 * <timeseries> Setting default series ENCODING to: compressed
9:M 30 Nov 2025 01:32:02.409 * <timeseries> Detected redis oss
9:M 30 Nov 2025 01:32:02.410 * Module 'timeseries' loaded from /opt/redis-stack/lib/redistimeseries.so
9:M 30 Nov 2025 01:32:02.417 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 30 Nov 2025 01:32:02.418 # <ReJSON> Skip register defrag callbacks as defrag callbacks is not supported on the current Redis server.
9:M 30 Nov 2025 01:32:02.418 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Exported RedisJSON_V1 API
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Exported RedisJSON_V2 API
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Exported RedisJSON_V3 API
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Exported RedisJSON_V4 API
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Exported RedisJSON_V5 API
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Enabled diskless replication
9:M 30 Nov 2025 01:32:02.419 * <ReJSON> Initialized shared string cache, thread safe: false.
9:M 30 Nov 2025 01:32:02.419 * Module 'ReJSON' loaded from /opt/redis-stack/lib/rejson.so
9:M 30 Nov 2025 01:32:02.419 * <search> Acquired RedisJSON_V5 API
9:M 30 Nov 2025 01:32:02.422 * <bf> RedisBloom version 2.8.16 (Git=unknown)
9:M 30 Nov 2025 01:32:02.423 * Module 'bf' loaded from /opt/redis-stack/lib/redisbloom.so
9:M 30 Nov 2025 01:32:02.439 * <redisgears_2> Created new data type 'GearsType'
9:M 30 Nov 2025 01:32:02.443 * <redisgears_2> Detected redis oss
9:M 30 Nov 2025 01:32:02.444 # <redisgears_2> could not initialize RedisAI_InitError

9:M 30 Nov 2025 01:32:02.445 * <redisgears_2> Failed loading RedisAI API.
9:M 30 Nov 2025 01:32:02.445 * <redisgears_2> RedisGears v2.0.20, sha='9b737886bf825fe29ddc2f8da81f73cbe0b4e858', build_type='release', built_for='Linux-ubuntu22.04.x86_64', redis_version:'7.4.7', enterprise:'false'.
9:M 30 Nov 2025 01:32:02.464 * <redisgears_2> Registered backend: js.
9:M 30 Nov 2025 01:32:02.474 * Module 'redisgears_2' loaded from /opt/redis-stack/lib/redisgears.so
9:M 30 Nov 2025 01:32:02.490 * Server initialized
9:M 30 Nov 2025 01:32:02.491 * Ready to accept connections tcp
9:C 30 Nov 2025 01:50:18.290 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
9:C 30 Nov 2025 01:50:18.290 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
9:C 30 Nov 2025 01:50:18.290 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=9, just started
9:C 30 Nov 2025 01:50:18.290 * Configuration loaded
9:M 30 Nov 2025 01:50:18.291 * Increased maximum number of open files to 10032 (it was originally set to 1024).
9:M 30 Nov 2025 01:50:18.291 * monotonic clock: POSIX clock_gettime
9:M 30 Nov 2025 01:50:18.294 * Running mode=standalone, port=6379.
9:M 30 Nov 2025 01:50:18.296 * Module 'RedisCompat' loaded from /opt/redis-stack/lib/rediscompat.so
9:M 30 Nov 2025 01:50:18.315 * <search> Redis version found by RedisSearch : 7.4.7 - oss
9:M 30 Nov 2025 01:50:18.315 * <search> RediSearch version 2.10.20 (Git=5c09b69)
9:M 30 Nov 2025 01:50:18.316 * <search> Low level api version 1 initialized successfully
9:M 30 Nov 2025 01:50:18.317 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  10000,
9:M 30 Nov 2025 01:50:18.318 * <search> Initialized thread pools!
9:M 30 Nov 2025 01:50:18.319 * <search> Subscribe to config changes
9:M 30 Nov 2025 01:50:18.319 * <search> Enabled role change notification
9:M 30 Nov 2025 01:50:18.319 * Module 'search' loaded from /opt/redis-stack/lib/redisearch.so
9:M 30 Nov 2025 01:50:18.323 * <timeseries> RedisTimeSeries version 11206, git_sha=cdcbe34f8e87e15ea700b737634be6bac6b6700b
9:M 30 Nov 2025 01:50:18.323 * <timeseries> Redis version found by RedisTimeSeries : 7.4.7 - oss
9:M 30 Nov 2025 01:50:18.323 * <timeseries> loaded default CHUNK_SIZE_BYTES policy: 4096
9:M 30 Nov 2025 01:50:18.323 * <timeseries> loaded server DUPLICATE_POLICY: block
9:M 30 Nov 2025 01:50:18.323 * <timeseries> loaded default IGNORE_MAX_TIME_DIFF: 0
9:M 30 Nov 2025 01:50:18.323 * <timeseries> loaded default IGNORE_MAX_VAL_DIFF: 0.000000
9:M 30 Nov 2025 01:50:18.323 * <timeseries> Setting default series ENCODING to: compressed
9:M 30 Nov 2025 01:50:18.323 * <timeseries> Detected redis oss
9:M 30 Nov 2025 01:50:18.324 * Module 'timeseries' loaded from /opt/redis-stack/lib/redistimeseries.so
9:M 30 Nov 2025 01:50:18.330 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 30 Nov 2025 01:50:18.331 # <ReJSON> Skip register defrag callbacks as defrag callbacks is not supported on the current Redis server.
9:M 30 Nov 2025 01:50:18.331 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Exported RedisJSON_V1 API
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Exported RedisJSON_V2 API
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Exported RedisJSON_V3 API
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Exported RedisJSON_V4 API
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Exported RedisJSON_V5 API
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Enabled diskless replication
9:M 30 Nov 2025 01:50:18.332 * <ReJSON> Initialized shared string cache, thread safe: false.
9:M 30 Nov 2025 01:50:18.332 * Module 'ReJSON' loaded from /opt/redis-stack/lib/rejson.so
9:M 30 Nov 2025 01:50:18.332 * <search> Acquired RedisJSON_V5 API
9:M 30 Nov 2025 01:50:18.334 * <bf> RedisBloom version 2.8.16 (Git=unknown)
9:M 30 Nov 2025 01:50:18.334 * Module 'bf' loaded from /opt/redis-stack/lib/redisbloom.so
9:M 30 Nov 2025 01:50:18.341 * <redisgears_2> Created new data type 'GearsType'
9:M 30 Nov 2025 01:50:18.343 * <redisgears_2> Detected redis oss
9:M 30 Nov 2025 01:50:18.345 # <redisgears_2> could not initialize RedisAI_InitError

9:M 30 Nov 2025 01:50:18.345 * <redisgears_2> Failed loading RedisAI API.
9:M 30 Nov 2025 01:50:18.345 * <redisgears_2> RedisGears v2.0.20, sha='9b737886bf825fe29ddc2f8da81f73cbe0b4e858', build_type='release', built_for='Linux-ubuntu22.04.x86_64', redis_version:'7.4.7', enterprise:'false'.
9:M 30 Nov 2025 01:50:18.358 * <redisgears_2> Registered backend: js.
9:M 30 Nov 2025 01:50:18.364 * Module 'redisgears_2' loaded from /opt/redis-stack/lib/redisgears.so
9:M 30 Nov 2025 01:50:18.378 * Server initialized
9:M 30 Nov 2025 01:50:18.379 * Ready to accept connections tcp
9:C 30 Nov 2025 01:53:43.469 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
9:C 30 Nov 2025 01:53:43.470 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
9:C 30 Nov 2025 01:53:43.470 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=9, just started
9:C 30 Nov 2025 01:53:43.470 * Configuration loaded
9:M 30 Nov 2025 01:53:43.471 * Increased maximum number of open files to 10032 (it was originally set to 1024).
9:M 30 Nov 2025 01:53:43.471 * monotonic clock: POSIX clock_gettime
9:M 30 Nov 2025 01:53:43.474 * Running mode=standalone, port=6379.
9:M 30 Nov 2025 01:53:43.476 * Module 'RedisCompat' loaded from /opt/redis-stack/lib/rediscompat.so
9:M 30 Nov 2025 01:53:43.501 * <search> Redis version found by RedisSearch : 7.4.7 - oss
9:M 30 Nov 2025 01:53:43.502 * <search> RediSearch version 2.10.20 (Git=5c09b69)
9:M 30 Nov 2025 01:53:43.502 * <search> Low level api version 1 initialized successfully
9:M 30 Nov 2025 01:53:43.504 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  10000,
9:M 30 Nov 2025 01:53:43.504 * <search> Initialized thread pools!
9:M 30 Nov 2025 01:53:43.506 * <search> Subscribe to config changes
9:M 30 Nov 2025 01:53:43.506 * <search> Enabled role change notification
9:M 30 Nov 2025 01:53:43.506 * Module 'search' loaded from /opt/redis-stack/lib/redisearch.so
9:M 30 Nov 2025 01:53:43.511 * <timeseries> RedisTimeSeries version 11206, git_sha=cdcbe34f8e87e15ea700b737634be6bac6b6700b
9:M 30 Nov 2025 01:53:43.511 * <timeseries> Redis version found by RedisTimeSeries : 7.4.7 - oss
9:M 30 Nov 2025 01:53:43.512 * <timeseries> loaded default CHUNK_SIZE_BYTES policy: 4096
9:M 30 Nov 2025 01:53:43.512 * <timeseries> loaded server DUPLICATE_POLICY: block
9:M 30 Nov 2025 01:53:43.512 * <timeseries> loaded default IGNORE_MAX_TIME_DIFF: 0
9:M 30 Nov 2025 01:53:43.512 * <timeseries> loaded default IGNORE_MAX_VAL_DIFF: 0.000000
9:M 30 Nov 2025 01:53:43.512 * <timeseries> Setting default series ENCODING to: compressed
9:M 30 Nov 2025 01:53:43.512 * <timeseries> Detected redis oss
9:M 30 Nov 2025 01:53:43.513 * Module 'timeseries' loaded from /opt/redis-stack/lib/redistimeseries.so
9:M 30 Nov 2025 01:53:43.521 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 30 Nov 2025 01:53:43.522 # <ReJSON> Skip register defrag callbacks as defrag callbacks is not supported on the current Redis server.
9:M 30 Nov 2025 01:53:43.522 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Exported RedisJSON_V1 API
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Exported RedisJSON_V2 API
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Exported RedisJSON_V3 API
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Exported RedisJSON_V4 API
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Exported RedisJSON_V5 API
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Enabled diskless replication
9:M 30 Nov 2025 01:53:43.523 * <ReJSON> Initialized shared string cache, thread safe: false.
9:M 30 Nov 2025 01:53:43.523 * Module 'ReJSON' loaded from /opt/redis-stack/lib/rejson.so
9:M 30 Nov 2025 01:53:43.523 * <search> Acquired RedisJSON_V5 API
9:M 30 Nov 2025 01:53:43.526 * <bf> RedisBloom version 2.8.16 (Git=unknown)
9:M 30 Nov 2025 01:53:43.526 * Module 'bf' loaded from /opt/redis-stack/lib/redisbloom.so
9:M 30 Nov 2025 01:53:43.535 * <redisgears_2> Created new data type 'GearsType'
9:M 30 Nov 2025 01:53:43.538 * <redisgears_2> Detected redis oss
9:M 30 Nov 2025 01:53:43.539 # <redisgears_2> could not initialize RedisAI_InitError

9:M 30 Nov 2025 01:53:43.539 * <redisgears_2> Failed loading RedisAI API.
9:M 30 Nov 2025 01:53:43.539 * <redisgears_2> RedisGears v2.0.20, sha='9b737886bf825fe29ddc2f8da81f73cbe0b4e858', build_type='release', built_for='Linux-ubuntu22.04.x86_64', redis_version:'7.4.7', enterprise:'false'.
9:M 30 Nov 2025 01:53:43.557 * <redisgears_2> Registered backend: js.
9:M 30 Nov 2025 01:53:43.564 * Module 'redisgears_2' loaded from /opt/redis-stack/lib/redisgears.so
9:M 30 Nov 2025 01:53:43.578 * Server initialized
9:M 30 Nov 2025 01:53:43.580 * Ready to accept connections tcp
PS C:\Users\姚东名>
