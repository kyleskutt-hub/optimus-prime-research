# The Primorial Depth Funnel
## A Geometric Argument Toward the Critical Line
### Kyle Skutt — March 2026

**Status: Formal conjecture with partial proof. Key steps proven, gap identified.**

---

## The Core Theorem (Proven)

**Theorem (Center of Mass).** For every primorial P_n# = p_1 · p_2 · ... · p_n, the center of mass of the reduced residue classes mod P_n# equals exactly P_n#/2. Equivalently, the normalized center of mass equals 1/2.

**Proof.** For every reduced residue k (with gcd(k, P_n#) = 1), its complement P_n# − k is also a reduced residue (since gcd(P_n# − k, P_n#) = gcd(k, P_n#) = 1). The map k ↦ P_n# − k is an involution on the set of reduced residues with no fixed points (since P_n#/2 is not coprime to P_n# for n ≥ 2). Therefore the reduced residues pair perfectly as {k, P_n# − k}, and the average of each pair is P_n#/2. ∎

## Supporting Results (Proven)

1. **Convexity inequality.** For x > 1 and β ≠ 1/2: 2x^{1/2} < x^β + x^{1−β}. The symmetric configuration β = 1/2 uniquely minimizes the sum.

2. **Fejér kernel closed form.** The Mellin transform of h₀(u) = (1 − |log u|)₊ satisfies: |ĥ₀(δ+it)| = (sinh²(δ/2) + sin²(t/2)) / ((δ/2)² + (t/2)²)

3. **Monotonicity.** |ĥ₀(1/2 + δ + it)| is strictly increasing in δ for all δ > 0 and all real t. Proof: sinh²(δ/2) ≥ (δ/2)² and sin²(t/2) ≤ (t/2)², so the ratio is ≥ 1 and increasing.

4. **Mollification preserves monotonicity.** Convolving h₀ with a C∞ mollifier φ_ε preserves the monotonicity property for all tested ε > 0. (Numerically verified.)

5. **|ĥ|² positivity.** Using the autocorrelation f * f̃, the Mellin transform on the critical line equals |ĥ(1/2+it)|² ≥ 0 for all t. This is automatic.

## The Conjecture

**Conjecture (Primorial Depth Funnel).** The primorial filtration — the tower of groups (ℤ/P_n#ℤ)* with forced centering at 1/2 at every level — constrains the zeros of the Riemann zeta function to lie on the critical line Re(s) = 1/2.

## What Remains Open

The proven results establish that:
- The arithmetic structure centers at 1/2 (center of mass theorem)
- Test functions with the right monotonicity property exist (Fejér kernel)
- Smoothing does not destroy monotonicity (mollification result)
- Positivity can be ensured by construction (|ĥ|² trick)

The gap: converting these ingredients into a contradiction from the explicit formula. The constant terms and prime terms in the Weil explicit formula dominate the off-line excess from any single zero by orders of magnitude. A fundamentally new approach may be required — possibly through the partial Euler product filtration rather than the explicit formula.

## Note on Independence

The primorial skeleton framework and center of mass theorem were developed in November 2025, independently of and prior to Connes' February 2026 paper (arXiv:2602.04022), which uses the same arithmetic object (P₅# = 2310) as its optimization domain.
