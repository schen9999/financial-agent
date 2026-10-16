| Where | Device | Backend | Threads | GPU layers | pp512 tok/s | pp2048 tok/s | tg128 tok/s |
|---|---|---|---|---|---|---|---|
| AMD EPYC 9J14 (OKE E5), 4 vCPU | AMD EPYC 9J14 96-Core Processor | CPU | 4 | -1 | 45.7 (±27.21) † | 61.1 (±0.03) | 12.9 (±0.02) |
| AMD EPYC 9J14 (OKE E5), 8 vCPU | AMD EPYC 9J14 96-Core Processor | CPU | 8 | -1 | 79.6 (±55.76) † | 109.8 (±0.09) | 13.3 (±0.01) |
| AMD EPYC 9J14 (OKE E5), 15 vCPU | AMD EPYC 9J14 96-Core Processor | CPU | 15 | -1 | 75.2 (±49.66) † | 103.6 (±0.26) | 12.8 (±0.02) |
| Intel Xeon 8358 (A10.1 host), 4 vCPU | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | CPU | 4 | -1 | 44.3 (±0.25) | 43.8 (±0.04) | 10.8 (±0.01) |
| Intel Xeon 8358 (A10.1 host), 8 vCPU | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | CPU | 8 | -1 | 81.5 (±0.32) | 80.4 (±0.16) | 15.9 (±0.01) |
| Intel Xeon 8358 (A10.1 host), 15 vCPU | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | CPU | 15 | -1 | 122.8 (±3.18) | 122.5 (±1.23) | 20.8 (±0.10) |
| Intel Xeon 8358 (A10.1 host), 28 vCPU | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | CPU | 28 | -1 | 119.6 (±0.66) | 116.3 (±0.91) | 22.1 (±0.05) |
| NVIDIA A10, all layers | NVIDIA A10 | CUDA | 8 | 99 | 2289.3 (±81.90) | 2299.5 (±5.71) | 110.4 (±0.34) |

llama.cpp build(s): b11347. † repetitions spread wider than the cold threshold: not quoted.
