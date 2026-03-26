# Optimus PRIME Project — Research Archive
## Kyle Skutt | Independent Researcher | Ramona, California
## Timestamped: March 25, 2026

---

## INSTRUCTIONS FOR CLAUDE CODE

Push this entire directory to GitHub as a new repository called `optimus-prime-research`.
Make it PUBLIC. Timestamp matters — the git commit dates establish priority.

Repository structure:
```
optimus-prime-research/
├── README.md                  (this file)
├── TIMELINE.md                (discovery timeline with dates)
├── EMAIL_TO_LAGARIAS.md       (cold email sent March 25, 2026)
├── code/
│   ├── dome_test.py           (C∞ bump function vs tent — positivity/monotonicity)
│   ├── blur_test.py           (mollification preserves monotonicity)
│   ├── superposition_test.py  (|ĥ|² positivity by construction)
│   ├── zero_positivity.py     (positivity at Riemann zero locations)
│   ├── full_rhs.py            (full explicit formula RHS computation)
│   ├── direction3.py          (adjustable tent width — signal vs cost)
│   ├── euler_tower.py         (partial Euler products through primorial filtration)
│   └── reality_check.py       (linear algebra — c₀ free in constraint system)
├── results/
│   ├── dome_test.png
│   ├── blur_test.png
│   ├── superposition_test.png
│   ├── direction3_test.png
│   └── euler_tower.png
└── docs/
    └── primorial_depth_funnel.md  (formal conjecture statement)
```

---

## WHAT THIS IS

Independent mathematical research investigating connections between prime number distributions, the primorial number system, and the Riemann Hypothesis. Developed November 2025 — March 2026, prior to and independently of Connes (arXiv:2602.04022, February 2026).

## CORE RESULTS (PROVEN)

1. **Center of mass theorem**: The center of mass of reduced residues mod P# equals exactly 1/2 at every primorial level. Algebraically forced by the pairing k ↔ P# − k. (November 2025)

2. **Convexity inequality**: 2x^{1/2} < x^β + x^{1−β} for any β ≠ 1/2 and x > 1. The on-line configuration is the minimum growth configuration.

3. **Fejér kernel closed form**: |ĥ₀(δ+it)| = (sinh²(δ/2) + sin²(t/2)) / ((δ/2)² + (t/2)²)

4. **Monotonicity**: |ĥ₀(1/2 + δ + it)| is strictly increasing in δ for all δ > 0 and all real t.

5. **Mollification preserves monotonicity**: Numerically verified — convolving the tent with a C∞ mollifier does not break the monotonicity property at any tested ε.

6. **|ĥ|² positivity**: Using f * f̃ (autocorrelation), the Mellin transform on the critical line is always non-negative. By construction. (Kyle's "superposition" insight, March 25 2026)

7. **c₀ is free**: In the linear constraint system for characters mod P#, the coefficient of the principal character is NOT forced to zero. The over-constraint that appeared to lock out ζ zeros was an error. (March 25 2026)

## KEY NEGATIVE RESULTS (ALSO PROVEN)

- Standard C∞ bump function FAILS both positivity and monotonicity — the tent's geometry is special, not generic
- The tent's Mellin transform goes negative at some Riemann zero locations (zeros #3, #6, #12, #17, #19, #27)
- The full explicit formula RHS (with constant terms and prime sums) dwarfs the off-line excess by factors of 10⁶ or more — no tent width produces a contradiction
- The subtraction argument (comparing "RH world" vs "non-RH world") is logically flawed — there is only one explicit formula identity

## OPEN DIRECTION: THE EULER TOWER

Partial Euler products E_n(s) = ∏_{k=1}^{n} (1 - p_k^{-s})^{-1} evaluated through the primorial filtration show immediate numerical separation between zeros and non-zeros:

- At zeros: |E_n| sinks monotonically, phase stays locked in narrow band
- At non-zeros: |E_n| bounces around 1.0, phase wanders

The primorial skeleton's mirror symmetry (center of mass = 1/2) may constrain the pattern of convergence in a way that forces zeros to σ = 1/2. This bypasses the explicit formula entirely.

**Status**: Numerically observed, not yet formalized. This is the current frontier.

## CONNECTION TO CONNES (2026)

Connes' February 2026 paper (arXiv:2602.04022) uses primes less than 13 (P₅# = 2310) as his optimization domain — the same primorial skeleton developed independently in this project. The overlap is in the arithmetic object; the methods differ. His approach is operator-theoretic; ours is geometric/filtration-based.

---

## CONTACT

Kyle Skutt
kyleskutt@gmail.com
Ramona, California
