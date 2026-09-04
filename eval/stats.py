"""Statistics for the grounding eval: Wilson score intervals and Fisher's
exact test. Pure stdlib on purpose — imported by the Argo aggregate pod,
which must start fast.

Why this module exists: at the eval's current scale (~65–85 claims per run)
a point estimate is not enough to call a gate pass meaningful. Every
reported unsupported rate should carry its 95% interval, and every two-arm
comparison should carry an exact p-value, so readers can see what the data
can and cannot resolve.
"""
import math
from math import comb

# z for a 95% two-sided interval
Z_95 = 1.959963984540054


def wilson_interval(successes: int, n: int, z: float = Z_95) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion.

    Returns (low, high) as proportions in [0, 1]. Preferred over the normal
    approximation at small n and extreme rates (it behaves sensibly at 0/n,
    where the normal interval collapses to a width of zero).
    """
    if n <= 0:
        return (0.0, 1.0)
    if successes < 0 or successes > n:
        raise ValueError(f"successes={successes} out of range for n={n}")
    p = successes / n
    z2 = z * z
    denom = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def fisher_exact(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact test p-value for the 2x2 table [[a, b], [c, d]].

    Convention (matches scipy/R): sum the hypergeometric probabilities of all
    tables with the same margins whose probability does not exceed that of
    the observed table (with a small relative tolerance for float ties).
    """
    for v in (a, b, c, d):
        if v < 0:
            raise ValueError("table entries must be non-negative")
    n = a + b + c + d
    if n == 0:
        return 1.0
    row1, col1 = a + b, a + c

    def p_k(k: int) -> float:
        return comb(col1, k) * comb(n - col1, row1 - k) / comb(n, row1)

    p_obs = p_k(a)
    lo = max(0, row1 - (n - col1))
    hi = min(row1, col1)
    tol = 1 + 1e-9
    return min(1.0, sum(p for p in (p_k(k) for k in range(lo, hi + 1)) if p <= p_obs * tol))


def format_rate_ci(successes: int, n: int) -> str:
    """'12.31% (95% CI 6.4–22.5%)' — the reporting format for eval output."""
    if n <= 0:
        return "n/a (0 claims)"
    lo, hi = wilson_interval(successes, n)
    return f"{successes / n * 100:.2f}% (95% CI {lo * 100:.1f}–{hi * 100:.1f}%)"
