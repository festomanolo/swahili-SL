### table_runtime_benchmark

REVIEWER B COMMENT 14. Measured latency of every stage, with percentiles, on this runtime. Landmark extraction dominates: it is a CPU-bound per-frame cost, whereas classification runs once per clip. Two rules for the manuscript: quote the CPU figures, because the deployment argument in Section 4.7.2 is about commodity hardware; and name the device, because a Colab GPU is neither a phone nor a low-cost laptop. Only claim real-time operation if the per-frame verdict row says "within budget" on the TARGET device.

