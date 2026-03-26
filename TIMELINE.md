# OPTIMUS PRIME PROJECT — Discovery Timeline

## Priority Record

---

### November 2025
- **Center of mass theorem discovered**: Reduced residues mod P# have center of mass exactly 1/2, forced by mirror symmetry k ↔ P# − k
- Primorial skeleton framework developed independently
- H_skel operator with energy formula E(χ) = ω(cond(χ))/r on 480 characters of (ℤ/2310ℤ)*
- Phase 6F attractor theorem: σ* = 0.5065 ± 0.0372

### December 2025
- Scaling/falsification harness built and tested
- Character-weighted Hamiltonians plateau at ⟨r⟩ ≈ 0.48, below GUE target
- Key insight: GUE statistics driven by magnetic flux geometry, not primality
- Score=100/100 shown to be artifact of matrix dimension, not structural correspondence
- F1 falsification test designed (random antisymmetric matrix as null hypothesis)
- Discovery: primes determine zero locations, not the reverse
- Zeros identified as 180° phase discontinuities, not conventional solutions

### January–February 2026
- Residual calculus historical investigation
- Euler product truncation methods explored
- Comprehensive research summary compiled for cross-AI verification

### February 2026
- Connes posts arXiv:2602.04022 using P₅# = 2310 (same primorial skeleton)
- Independent parallel development confirmed

### March 17, 2026
- Connection to Connes recognized and documented
- Primorial Depth Funnel formal conjecture document written
- Burnol conductor operator framework identified as bridge
- Fejér kernel closed form derived: |ĥ₀(δ+it)| = (sinh²(δ/2) + sin²(t/2)) / ((δ/2)² + (t/2)²)
- Monotonicity of unsmoothed case proven via sin²b ≤ b²
- Smoothing gap identified as single remaining obstacle
- Cold email drafted to Jeffrey Lagarias at University of Michigan

### March 25, 2026
- **Cold email sent to Professor Jeffrey Lagarias** (lagarias@umich.edu)
- Burnol's full paper trail researched (math/9810169, math/9811040, math/9902080)
- Burnol confirmed at University of Lille, 37 papers, 290 citations
- Connection mapped: Burnol's conductor operator → Connes' Sonin spaces → prolate wave operators

#### Smoothing investigation (March 25):
- Standard C∞ bump function tested: FAILS both positivity and monotonicity
- Mollification of tent tested at ε = 0.2, 0.1, 0.05, 0.02, 0.01
- **Result: Monotonicity survives mollification at all ε values**
- **Result: Positivity already fails for the exact tent** (min Re = -0.00667)
- Tent's Mellin transform goes negative in periodic bands of width ~0.96, period ~2π

#### Superposition insight (March 25):
- Kyle's idea: use |ĥ|² instead of Re(ĥ) — "make it superposition so neg and pos don't matter"
- **Result: |ĥ|² is always positive (by construction) AND preserves monotonicity**
- All 30 tested Riemann zeros show positive |ĥ|² values
- Autocorrelation f * f̃ gives |ĥ|² in Weil's framework — matches Kyle's intuition

#### Weil positivity investigation (March 25):
- Three-part structure identified: positivity, monotonicity, contradiction
- DeepSeek two-lane analysis: Lane 1 (heavy machinery) and Lane 2 (elementary) hit same wall
- Wall identified: isolating single zero's contribution from total sum
- Character filtering via Dirichlet characters mod P# explored
- **Key error caught by Kyle**: DeepSeek's over-constraint forcing c₀ = 0 was unnecessary
- Principal character has conductor 1, log(1/π) is bounded, doesn't need cancellation
- **Result: c₀ is free** — 386 degrees of freedom with 94 constraints at level 5
- Subtraction argument identified as logically flawed by Claude (only one reality exists)
- Full RHS computation shows constant terms dwarf off-line excess by 10⁶+

#### Euler Tower discovery (March 25):
- Kyle's vision: "horizontal branches converging right to a singular event"
- Partial Euler products computed at each primorial level for zeros vs non-zeros
- **Immediate numerical separation**: zeros sink (|E_n| → 0), non-zeros bounce (~1.3)
- Phase-locking observed at zeros: phase stays in narrow band (0° to 20°)
- Phase wandering at non-zeros: phase spans -100° to +10°
- Connection to primorial skeleton: mirror symmetry constrains phase accumulation
- **New direction identified**: study Euler product through primorial filtration directly
- Bypasses explicit formula, test functions, and archimedean kernel entirely

---

## Verification

All computations from March 25, 2026 session are reproducible via the Python scripts in the code/ directory. Git commit timestamps establish priority dates.
