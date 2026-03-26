# Why Our Models Fail — And What We Learned
**Kyle Skutt | Optimus PRIME Project | November 2025 — March 2026**

*"The primes do not scatter — they remember. But remembering is not the same as proving."*

---

## Philosophy

This document catalogs what DIDN'T work and why. In mathematics, knowing precisely where an approach fails is often more valuable than a vague claim of success. Every wall we hit is a wall we can describe.

---

## Failure 1: The Hamiltonian Operator (Nov–Dec 2025)

**What we built:** A finite Hamiltonian H = H_log + H_skel + γΓ on a space of 60 primes × 48 residue classes mod 210. H_log encoded prime gaps, H_skel was a Laplacian on the residue torus, Γ coupled them.

**What worked:** The operator reproduced GOE/GUE random matrix statistics. Level repulsion emerged. σ = 1/2 appeared as a stable attractor (σ* = 0.5065 ± 0.0372). The symmetry σ ↔ (1−σ) correctly forced the chaos peak to 0.5.

**What failed:** The eigenvalues did NOT match actual Riemann zeros. Score = 100/100 was achieved, but the F1 falsification test revealed this was an artifact of matrix dimension — a random antisymmetric matrix of the same size scores equally well. The match was density, not structure.

**Why it fails (5 reasons):**

1. **Finite primes, infinite product.** We used 60 primes. ζ(s) needs all of them. Any finite operator can only approximate the statistical behavior, never the exact zero locations.
2. **No true dynamical flow.** ζ(s) is governed by multiplicative structure (p^{-s} rotations), analytic continuation, and the functional equation. Our operator had additive potentials and a discrete Laplacian — wrong category of mathematics.
3. **Symmetry without substance.** We encoded σ ↔ (1−σ) in weights, but the functional equation contains the Gamma function, π-scaling, and sine terms. We captured the symmetry but not the equation.
4. **Too few degrees of freedom.** ~3000 matrix entries cannot encode a structure as rich as ζ(s), which requires infinite dimension, correct spectral growth (Riemann–von Mangoldt law), and perfect prime encoding simultaneously.
5. **The true operator may not exist.** The Hilbert–Pólya conjecture — that such an operator exists — remains unproven. We may be searching for something that isn't there.

**What we learned:** Statistics ≠ structure. Matching ⟨r⟩ ≈ 0.603 (GUE) is necessary but nowhere near sufficient. The F1 test (random null hypothesis) should be run on EVERY claimed match. This lesson saved months of false optimism.

---

## Failure 2: The Spectral Probe / MOD 12 Bridge (March 2026)

**What we built:** A probe using prime powers restricted to specific residue classes (≡ 1 mod 30030) to detect Riemann zeros from the Euler product side.

**What worked:** Experiment 2 located the 5th Riemann zero at T=32.935 from just 502 prime powers. Genuine resonance detection.

**What failed:** The signal at σ = 0.5 was n^{−σ} scaling artifacts, not genuine critical-line resonance. Multiple normalization approaches confirmed: the explicit formula's prime sum side cannot detect WHERE zeros sit (σ = 0.5). That information lives in the functional equation and analytic continuation, not in the sum's amplitude.

**Why it fails:** The explicit formula has two sides — zeros and primes. You can detect zero HEIGHTS (t-values) from the prime side, but not zero POSITIONS (σ-values). Position information is encoded in the functional equation, which is a global analytic object, not a local sum.

**What we learned:** The center-of-mass theorem holds for the principal character but not for non-trivial characters (S_dev grows across levels). The bridge to RH runs through the functional equation, not through direct character sum constraints.

---

## Failure 3: The Tent / Weil Positivity Approach (March 25, 2026)

**What we built:** A Fejér-type tent function h₀(u) = (1 − |log u|)₊ with proven monotonicity, mollified to C∞, using Weil's positivity criterion with f * f̃ for automatic positivity.

**What worked:**
- Monotonicity proven analytically via closed-form Mellin transform
- Mollification preserves monotonicity (numerically verified at 5 epsilon values)
- |ĥ|² positivity by construction (Kyle's "superposition" insight)
- c₀ ≠ 0 in the character constraint system (over-constraint error caught)

**What failed:** The constant terms F(0) + F(1) in the explicit formula grow like A² (tent width squared) and dwarf the off-line excess by factors of 10⁶ or more. No tent width A produces a contradiction. The ratio Excess/RHS actually gets WORSE as A grows (drops from 10⁻⁶ to 10⁻¹² as A goes from 0.5 to 20).

**Additional failure:** A subtraction argument ("compare RH-world vs non-RH-world") was proposed and shown to be logically flawed. There is only one explicit formula identity — both sides are always equal regardless of where zeros are. You cannot subtract two realities.

**Why it fails:** The explicit formula is an identity between huge quantities. The zero sum, prime sum, and constant terms are all large and nearly cancel. The excess from a single off-line zero is an infinitesimal perturbation on a mountain-sized balance. Detecting it requires test functions concentrated at a specific frequency — but the uncertainty principle means narrow frequency concentration requires wide position support, which increases the prime sum and constant terms. This is a fundamental tension, possibly the reason RH is hard.

**What we learned:**
- The standard C∞ bump function fails BOTH positivity and monotonicity — the tent's geometry is special, not generic
- Ancient tuning matters: the tent (Fejér kernel) has properties that generic smooth functions don't
- The character constraint system at level 5 (mod 2310) has 480 unknowns, 94 constraints, 386 degrees of freedom — ample room, but ample room doesn't produce a contradiction when the constant terms dominate

---

## Failure 4: Character Frequency Filtering (March 25, 2026)

**What we built:** Using Dirichlet characters mod P# as frequency filters inside Burnol's conductor operator framework. The idea: weight the test function by a character to concentrate energy near a specific zero height t₀.

**What worked:** The explicit formula for L(s, χ) is well-defined. Monotonicity carries over. The prime sum simplifies.

**What failed:** Characters with large conductor q introduce an archimedean term growing like log q. To cancel this, you need differences between characters at the same conductor — but the principal character (conductor 1) has no partner. Forcing c₀ = 0 locks you out of ζ zeros entirely.

**Partial recovery:** Kyle identified that the c₀ = 0 constraint was an over-constraint — conductor 1 terms are bounded (log(1/π) ≈ −1.14) and don't need cancellation. So c₀ IS free. But even with c₀ free, the signal-to-noise ratio remains hopelessly small (Failure 3).

**What we learned:** The primorial hierarchy gives enormous algebraic freedom (exponentially many characters, polynomially many constraints). But algebraic freedom doesn't help when the analytic signal is buried in noise.

---

## What Remains Open: The Euler Tower

After all four failures, one observation stands apart. It doesn't use the explicit formula, test functions, or Weil's criterion.

**The observation:** Partial Euler products E_n(s) = ∏_{k=1}^{n} (1 − p_k^{-s})^{-1}, computed at each primorial level, show immediate numerical separation between zeros and non-zeros of ζ(s):

- At zeros: |E_n| sinks monotonically, phase stays locked in a narrow band
- At non-zeros: |E_n| bounces around ~1.3, phase wanders widely

By 5 primes, the separation is already visible. By 20 primes, zeros are at |E_n| ≈ 0.1 while non-zeros are at |E_n| ≈ 1.3.

**The connection:** The primorial skeleton's mirror symmetry (center of mass = 1/2) constrains the phase accumulation of the Euler product at each level. This may force the partial products to "die" (converge toward zero) only when s is on the critical line.

**Status:** Numerically observed. Not formalized. Not proven. This is the frontier.

**The key question:** Can the forced symmetry of the primorial skeleton at each level prove that |E_n(s)| → 0 only when Re(s) = 1/2?

---

## Summary Table

| Approach | What Worked | What Failed | Root Cause |
|---|---|---|---|
| Hamiltonian operator | GOE statistics, σ=1/2 attractor | Eigenvalues ≠ actual zeros | Finite approx of infinite structure |
| Spectral probe | Found zero heights | Can't detect σ-position | Info lives in functional equation |
| Tent / Weil positivity | Monotonicity, \|ĥ\|² positivity | Constant terms dominate | Uncertainty principle tension |
| Character filtering | Algebraic freedom, c₀ free | Signal buried in noise | Same as above, from different angle |
| Euler tower | Immediate zero/non-zero separation | Not formalized | Open — this is the frontier |

---

*Last updated: March 25, 2026*
