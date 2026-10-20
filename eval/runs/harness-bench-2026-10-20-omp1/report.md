# Harness benchmark report

Dated measurement on the provided OKE cluster (E5.Flex nodes); model replaced
by scripts/model_stub.py. Every figure from the captures in this directory.

## Validity per cell repeat

| repeat | valid | stub req / expected | unmatched | stock empty | errors | reasons |
|---|---|---|---|---|---|---|
| L0-r4-c4-r1 | yes | 790 / 790 | 0 | 0 | 0 |  |
| L0-r4-c4-r2 | yes | 790 / 790 | 0 | 0 | 0 |  |
| L1-r4-c4-r1 | yes | 800 / 800 | 0 | 0 | 0 |  |
| L1-r4-c4-r2 | yes | 805 / 805 | 0 | 0 | 0 |  |

## Cells (mean of valid repeats)

| cell | R | c | valid | briefs/h | p50 s | p95 s | worker CPU-s/brief | CPU/wall | throttled | peak MiB/process | api CPU-s/brief | Little gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L0-r4-c4 | 4 | 4 | 2/2 | 84292.0 | 0.8 | 1.2 | 1.04 | 1.45 | 0.00 | 554 | 0.00 | 15% |
| L1-r4-c4 | 4 | 4 | 2/2 | 2790.7 | 18.1 | 21.1 | 1.08 | 0.06 | 0.00 | 539 | 0.00 | 15% |

## Reading rules (pre-registered)

```
{
 "Q1_overhead": "not measured: L0 (1,1) has no valid repeat",
 "Q2_wait_vs_work": {
  "(4,4)": {
   "cpu_over_wall": 0.059861977921904924,
   "reading": "waiting (supports the post)"
  }
 },
 "Q3_saturation": {
  "L0": {
   "doubling_gains": {
    "(4,4)": {}
   },
   "saturation_at": "not reached within the sweep"
  },
  "L1": {
   "doubling_gains": {
    "(4,4)": {}
   },
   "saturation_at": "not reached within the sweep"
  }
 },
 "Q4_sizing": {
  "(4,4)": {
   "briefs_per_h": 2790.654802116528,
   "worker_vcpu": 0.8392240706596983,
   "worker_cpu_s_per_brief": 1.0826156829155391,
   "mem_peak_per_in_flight_brief_mib": 539.373046875
  }
 }
}
```

Measurement window under 10x the p95 latency (Little's-law check not supported, throughput imprecise): L0-r4-c4, L1-r4-c4
Peak memory source: sampled (kubectl top max / memory.current), a lower bound

