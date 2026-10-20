# Harness benchmark report

Dated measurement on the provided OKE cluster (E5.Flex nodes); model replaced
by scripts/model_stub.py. Every figure from the captures in this directory.

## Validity per cell repeat

| repeat | valid | stub req / expected | unmatched | stock empty | errors | reasons |
|---|---|---|---|---|---|---|
| L0-r1-c1-r1 | yes | 326 / 326 | 0 | 0 | 0 |  |
| L0-r1-c1-r2 | yes | 326 / 326 | 0 | 0 | 0 |  |
| L0-r1-c2-r1 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L0-r1-c2-r2 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L0-r1-c4-r1 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L0-r1-c4-r2 | yes | 403 / 403 | 0 | 0 | 0 |  |
| L0-r2-c1-r1 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L0-r2-c1-r2 | yes | 347 / 347 | 0 | 0 | 0 |  |
| L0-r2-c2-r1 | yes | 396 / 396 | 0 | 0 | 0 |  |
| L0-r2-c2-r2 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L0-r2-c4-r1 | yes | 535 / 535 | 0 | 0 | 0 |  |
| L0-r2-c4-r2 | yes | 535 / 535 | 0 | 0 | 0 |  |
| L0-r4-c1-r1 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L0-r4-c1-r2 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L0-r4-c2-r1 | yes | 530 / 530 | 0 | 0 | 0 |  |
| L0-r4-c2-r2 | yes | 530 / 530 | 0 | 0 | 0 |  |
| L0-r4-c4-r1 | yes | 805 / 805 | 0 | 0 | 0 |  |
| L0-r4-c4-r2 | yes | 800 / 800 | 0 | 0 | 0 |  |
| L1-keda-c1-r1 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-keda-c1-r2 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r1-c1-r1 | yes | 326 / 326 | 0 | 0 | 0 |  |
| L1-r1-c1-r2 | yes | 326 / 326 | 0 | 0 | 0 |  |
| L1-r1-c2-r1 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L1-r1-c2-r2 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L1-r1-c4-r1 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r1-c4-r2 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r2-c1-r1 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L1-r2-c1-r2 | yes | 354 / 354 | 0 | 0 | 0 |  |
| L1-r2-c2-r1 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r2-c2-r2 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r2-c4-r1 | yes | 535 / 535 | 0 | 0 | 0 |  |
| L1-r2-c4-r2 | yes | 535 / 535 | 0 | 0 | 0 |  |
| L1-r4-c1-r1 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r4-c1-r2 | yes | 410 / 410 | 0 | 0 | 0 |  |
| L1-r4-c2-r1 | yes | 535 / 535 | 0 | 0 | 0 |  |
| L1-r4-c2-r2 | yes | 530 / 530 | 0 | 0 | 0 |  |
| L1-r4-c4-r1 | yes | 805 / 805 | 0 | 0 | 0 |  |
| L1-r4-c4-r2 | yes | 805 / 805 | 0 | 0 | 0 |  |
| L2-r4-c4-r1 | yes | 805 / 805 | 0 | 0 | 0 |  |
| L2-r4-c4-r2 | yes | 805 / 805 | 0 | 0 | 0 |  |

## Cells (mean of valid repeats)

| cell | R | c | valid | briefs/h | p50 s | p95 s | worker CPU-s/brief | CPU/wall | throttled | peak MiB/process | api CPU-s/brief | Little gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L0-r1-c1 | 1 | 1 | 2/2 | 3693.3 | 1.0 | 1.5 | 0.65 | 0.65 | 0.17 | 807 | 0.00 | 0% |
| L0-r1-c2 | 1 | 2 | 2/2 | 7614.0 | 0.9 | 1.5 | 0.78 | 0.89 | 0.15 | 699 | 0.00 | 1% |
| L0-r1-c4 | 1 | 4 | 2/2 | 6255.2 | 0.9 | 12.5 | 3.18 | 3.79 | 0.47 | 622 | 0.00 | 1% |
| L0-r2-c1 | 2 | 1 | 2/2 | 7308.3 | 1.0 | 1.5 | 0.79 | 0.78 | 0.17 | 789 | 0.00 | 1% |
| L0-r2-c2 | 2 | 2 | 2/2 | 16960.6 | 0.8 | 1.1 | 1.02 | 1.35 | 0.12 | 675 | 0.00 | 6% |
| L0-r2-c4 | 2 | 4 | 2/2 | 14071.9 | 1.0 | 12.7 | 5.63 | 5.53 | 0.54 | 624 | 0.00 | 53% |
| L0-r4-c1 | 4 | 1 | 2/2 | 16066.8 | 0.8 | 1.3 | 1.08 | 1.41 | 0.15 | 735 | 0.00 | 3% |
| L0-r4-c2 | 4 | 2 | 2/2 | 16124.4 | 0.8 | 8.4 | 2.63 | 3.37 | 0.32 | 649 | 0.00 | 40% |
| L0-r4-c4 | 4 | 4 | 2/2 | 25414.9 | 0.9 | 22.3 | 9.03 | 9.90 | 0.53 | 592 | 0.00 | 87% |
| L1-r1-c1 | 1 | 1 | 2/2 | 198.8 | 19.0 | 21.7 | 0.97 | 0.05 | 0.03 | 826 | 0.02 | 0% |
| L1-r1-c2 | 1 | 2 | 2/2 | 401.1 | 18.7 | 21.6 | 0.89 | 0.05 | 0.01 | 718 | 0.01 | 0% |
| L1-r1-c4 | 1 | 4 | 2/2 | 797.6 | 19.1 | 22.4 | 1.64 | 0.09 | 0.03 | 609 | 0.01 | 2% |
| L1-r2-c1 | 2 | 1 | 2/2 | 406.6 | 18.8 | 21.3 | 1.08 | 0.06 | 0.03 | 771 | 0.01 | 1% |
| L1-r2-c2 | 2 | 2 | 2/2 | 809.7 | 18.9 | 21.5 | 1.11 | 0.06 | 0.02 | 648 | 0.01 | 2% |
| L1-r2-c4 | 2 | 4 | 2/2 | 1621.1 | 18.8 | 21.7 | 2.04 | 0.11 | 0.04 | 592 | 0.00 | 2% |
| L1-r4-c1 | 4 | 1 | 2/2 | 816.7 | 18.9 | 21.6 | 1.30 | 0.07 | 0.03 | 724 | 0.01 | 3% |
| L1-r4-c2 | 4 | 2 | 2/2 | 1603.8 | 18.6 | 21.6 | 2.26 | 0.12 | 0.06 | 639 | 0.00 | 2% |
| L1-r4-c4 | 4 | 4 | 2/2 | 3062.6 | 18.6 | 21.5 | 3.06 | 0.16 | 0.06 | 602 | 0.00 | 5% |
| L1-keda-c1 | 1–4 (KEDA) | 1 | 2/2 | 704.0 | 18.7 | 21.4 | 0.77 | 0.04 | 0.04 | 750 | 0.01 | 14% |
| L2-r4-c4 | 4 | 4 | 2/2 | 286.3 | 177.5 | 202.3 | 4.32 | 0.02 | 0.01 | 586 | 0.01 | 16% |

## Reading rules (pre-registered)

```
{
 "Q1_overhead": {
  "latency_p50_s": 1.0045574307441711,
  "worker_cpu_s_per_brief": 0.6537015104166667
 },
 "Q2_wait_vs_work": {
  "(1,1)": {
   "cpu_over_wall": 0.05100477928442004,
   "reading": "waiting (supports the post)"
  },
  "(1,2)": {
   "cpu_over_wall": 0.04773437789847983,
   "reading": "waiting (supports the post)"
  },
  "(1,4)": {
   "cpu_over_wall": 0.08527182218410653,
   "reading": "waiting (supports the post)"
  },
  "(2,1)": {
   "cpu_over_wall": 0.05768184293170825,
   "reading": "waiting (supports the post)"
  },
  "(2,2)": {
   "cpu_over_wall": 0.05846235300989219,
   "reading": "waiting (supports the post)"
  },
  "(2,4)": {
   "cpu_over_wall": 0.10869609621383297,
   "reading": "waiting (supports the post)"
  },
  "(4,1)": {
   "cpu_over_wall": 0.06860136018089164,
   "reading": "waiting (supports the post)"
  },
  "(4,2)": {
   "cpu_over_wall": 0.12126305722816365,
   "reading": "waiting (supports the post)"
  },
  "(4,4)": {
   "cpu_over_wall": 0.16423875323920645,
   "reading": "waiting (supports the post)"
  }
 },
 "Q3_saturation": {
  "L0": {
   "doubling_gains": {
    "(1,1)": {
     "2x replicas": 0.9788251773928232,
     "2x concurrency": 1.0616058275913942
    },
    "(1,2)": {
     "2x replicas": 1.2275418495809585,
     "2x concurrency": -0.1784676139429624
    },
    "(1,4)": {
     "2x replicas": 1.2496482079751314
    },
    "(2,1)": {
     "2x replicas": 1.1984283708542436,
     "2x concurrency": 1.3207271217108545
    },
    "(2,2)": {
     "2x replicas": -0.04930275951102747,
     "2x concurrency": -0.170314640582658
    },
    "(2,4)": {
     "2x replicas": 0.8060710947310308
    },
    "(4,1)": {
     "2x concurrency": 0.0035846060707083183
    },
    "(4,2)": {
     "2x concurrency": 0.5761808087235833
    },
    "(4,4)": {}
   },
   "saturation_at": [
    "(2,2)",
    "(4,1)"
   ]
  },
  "L1": {
   "doubling_gains": {
    "(1,1)": {
     "2x replicas": 1.0449468573652765,
     "2x concurrency": 1.0173285739234013
    },
    "(1,2)": {
     "2x replicas": 1.018651747316722,
     "2x concurrency": 0.9886545538545706
    },
    "(1,4)": {
     "2x replicas": 1.032340360530546
    },
    "(2,1)": {
     "2x replicas": 1.0087363610543005,
     "2x concurrency": 0.991388595745311
    },
    "(2,2)": {
     "2x replicas": 0.9808150343287978,
     "2x concurrency": 1.0021397540827968
    },
    "(2,4)": {
     "2x replicas": 0.8892642986636763
    },
    "(4,1)": {
     "2x concurrency": 0.9637084020189117
    },
    "(4,2)": {
     "2x concurrency": 0.9096034171639
    },
    "(4,4)": {}
   },
   "saturation_at": "not reached within the sweep"
  }
 },
 "Q4_sizing": {
  "(1,1)": {
   "briefs_per_h": 198.8228339810932,
   "worker_vcpu": 0.05347460011931344,
   "worker_cpu_s_per_brief": 0.9682417083333332,
   "mem_peak_per_in_flight_brief_mib": 825.703125
  },
  "(1,2)": {
   "briefs_per_h": 401.0909841384879,
   "worker_vcpu": 0.09934810704654025,
   "worker_cpu_s_per_brief": 0.8917008846153847,
   "mem_peak_per_in_flight_brief_mib": 717.5
  },
  "(1,4)": {
   "briefs_per_h": 797.6314121170153,
   "worker_vcpu": 0.3628031149327839,
   "worker_cpu_s_per_brief": 1.6374621083333334,
   "mem_peak_per_in_flight_brief_mib": 609.25
  },
  "(2,1)": {
   "briefs_per_h": 406.58212952209465,
   "worker_vcpu": 0.12251116328815963,
   "worker_cpu_s_per_brief": 1.084750548076923,
   "mem_peak_per_in_flight_brief_mib": 771.46875
  },
  "(2,2)": {
   "briefs_per_h": 809.6630159641422,
   "worker_vcpu": 0.24898904193194935,
   "worker_cpu_s_per_brief": 1.1070785416666666,
   "mem_peak_per_in_flight_brief_mib": 648.0
  },
  "(2,4)": {
   "briefs_per_h": 1621.0585116723832,
   "worker_vcpu": 0.9207931827064183,
   "worker_cpu_s_per_brief": 2.0448709493670885,
   "mem_peak_per_in_flight_brief_mib": 592.0615234375
  },
  "(4,1)": {
   "briefs_per_h": 816.7163073259208,
   "worker_vcpu": 0.29450006221383307,
   "worker_cpu_s_per_brief": 1.29812545,
   "mem_peak_per_in_flight_brief_mib": 723.8984375
  },
  "(4,2)": {
   "briefs_per_h": 1603.7926747617703,
   "worker_vcpu": 1.006350322261364,
   "worker_cpu_s_per_brief": 2.2589335998052587,
   "mem_peak_per_in_flight_brief_mib": 638.728515625
  },
  "(4,4)": {
   "briefs_per_h": 3062.607972147508,
   "worker_vcpu": 2.599423517594165,
   "worker_cpu_s_per_brief": 3.055541142857143,
   "mem_peak_per_in_flight_brief_mib": 602.10546875
  }
 }
}
```

Measurement window under 10x the p95 latency (Little's-law check not supported, throughput imprecise): L0-r1-c4, L0-r2-c2, L0-r2-c4, L0-r4-c1, L0-r4-c2, L0-r4-c4, L1-keda-c1, L1-r1-c4, L1-r2-c2, L1-r2-c4, L1-r4-c1, L1-r4-c2, L1-r4-c4, L2-r4-c4
Peak memory source: sampled (kubectl top max / memory.current), a lower bound

