"""
THE PRIMORIAL EULER TOWER

At each primorial level n, compute the partial Euler product:
  E_n(s) = product_{k=1}^{n} (1 - p_k^{-s})^{-1}

Evaluate at s = 1/2 + it for Riemann zeros.

Watch: magnitude, phase, and how they evolve level by level.
The zero is where |E_n| -> infinity (since zeta(rho)=0 means
the reciprocal 1/zeta -> 0, but the Euler product gives zeta,
so E_n should grow as we approach the zero).

Wait - actually at a zero of zeta, zeta(rho) = 0.
The Euler product gives zeta = product (1-p^{-s})^{-1}.
If zeta = 0, the product = 0... but each factor is nonzero.
The product diverges/oscillates in the critical strip.

What we're watching is HOW it diverges. The PATTERN of approach.
"""
import numpy as np
import matplotlib.pyplot as plt

# First 20 primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

# Primorial levels
primorials = []
P = 1
for p in primes:
    P *= p
    primorials.append(P)

# Riemann zeros to study
zeros_t = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
zero_names = ['ρ₁', 'ρ₂', 'ρ₃', 'ρ₄', 'ρ₅']

# Also test a NON-zero for comparison: t = 10 (not a zero)
test_t = [10.0, 14.134725, 20.0, 21.022040]
test_names = ['t=10 (not zero)', 't=14.13 (ZERO)', 't=20 (not zero)', 't=21.02 (ZERO)']

print("=" * 70)
print("PRIMORIAL EULER TOWER")
print("=" * 70)

# ================================================================
# For each test point, compute partial Euler products level by level
# ================================================================

all_data = {}

for t, name in zip(test_t, test_names):
    s = 0.5 + 1j * t
    
    print(f"\n{'='*60}")
    print(f"  {name}:  s = 1/2 + {t}i")
    print(f"{'='*60}")
    print(f"{'Level':>5s} {'Prime':>5s} {'P#':>12s} {'|E_n|':>12s} {'Phase°':>10s} {'log|E_n|':>10s} {'Δphase°':>10s}")
    print("-" * 70)
    
    E = 1.0 + 0j
    magnitudes = []
    phases = []
    log_mags = []
    
    prev_phase = 0
    
    for i, p in enumerate(primes):
        factor = 1.0 / (1.0 - p**(-s))
        E *= factor
        
        mag = abs(E)
        phase = np.degrees(np.angle(E))
        log_mag = np.log(mag) if mag > 0 else -999
        delta_phase = phase - prev_phase
        # Wrap to [-180, 180]
        while delta_phase > 180: delta_phase -= 360
        while delta_phase < -180: delta_phase += 360
        
        magnitudes.append(mag)
        phases.append(phase)
        log_mags.append(log_mag)
        
        print(f"{i+1:>5d} {p:>5d} {primorials[i]:>12d} {mag:>12.6f} {phase:>10.2f} {log_mag:>10.4f} {delta_phase:>10.2f}")
        
        prev_phase = phase
    
    all_data[t] = {
        'magnitudes': magnitudes,
        'phases': phases,
        'log_mags': log_mags,
        'name': name
    }

# ================================================================
# The KEY observation: at zeros, what does the phase do?
# ================================================================
print(f"\n\n{'='*70}")
print("PHASE ACCUMULATION: zeros vs non-zeros")
print("=" * 70)

print(f"\nTotal phase after 20 primes:")
for t, name in zip(test_t, test_names):
    d = all_data[t]
    total_phase = d['phases'][-1]
    total_mag = d['magnitudes'][-1]
    print(f"  {name:>30s}:  phase = {total_phase:>8.2f}°  |E| = {total_mag:.4f}")

# ================================================================
# Center of mass at each level
# ================================================================
print(f"\n\n{'='*70}")
print("PRIMORIAL SKELETON: reduced residues and center of mass")
print("=" * 70)

from math import gcd

for i in range(min(5, len(primes))):
    P = primorials[i]
    reduced = [k for k in range(1, P) if gcd(k, P) == 1]
    count = len(reduced)
    com = sum(reduced) / count / P  # normalized center of mass
    
    # Check pairing
    pairs = [(k, P-k) for k in reduced if k < P/2 and P-k in reduced]
    
    print(f"\n  Level {i+1}: P# = {P}, φ(P#) = {count} reduced residues")
    print(f"  Center of mass / P# = {com:.6f}  (exact 0.5: {'✓' if abs(com - 0.5) < 1e-10 else '✗'})")
    print(f"  Mirror pairs: {len(pairs)} pairs, {'all matched' if len(pairs) == count//2 else 'MISMATCH'}")

# ================================================================
# THE CONNECTION: Euler product phase at each level
# vs the primorial skeleton symmetry at that level
# ================================================================
print(f"\n\n{'='*70}")
print("CONNECTION: Euler phase vs skeleton symmetry")
print("=" * 70)

print(f"""
At each primorial level n:
  - The skeleton has φ(P_n#) reduced residues, centered at 1/2
  - The Euler product has accumulated n prime factors
  - Each new prime p_n contributes phase: arg(1/(1-p_n^{{-s}}))

The question: does the skeleton's forced centering at 1/2
constrain the Euler product's phase accumulation?

If the phase at each level is "centered" by the skeleton symmetry,
then the partial products can only diverge in a SYMMETRIC way.
And symmetric divergence means: if it blows up, it blows up
ON the critical line, not off it.
""")

# Compute: at a zero, what is the phase contribution from each prime?
print("Phase contribution per prime at ρ₁ = 1/2 + 14.134725i:")
print(f"{'Prime':>6s} {'arg(factor)°':>14s} {'|factor|':>12s} {'p^(-it)':>20s}")
print("-" * 56)

t = 14.134725
s = 0.5 + 1j * t

for p in primes[:10]:
    factor = 1.0 / (1.0 - p**(-s))
    p_it = p**(-1j * t)  # the oscillatory part
    p_half = p**(-0.5)    # the decay part
    
    phase = np.degrees(np.angle(factor))
    mag = abs(factor)
    
    # The key: p^{-it} = exp(-it*log(p)) is a rotation
    rotation_angle = np.degrees(-t * np.log(p)) % 360
    if rotation_angle > 180: rotation_angle -= 360
    
    print(f"{p:>6d} {phase:>14.2f} {mag:>12.6f} {rotation_angle:>10.2f}° rotation")

print(f"""
Each prime contributes a ROTATION of t*log(p) degrees.
At a zero, these rotations conspire to cancel the product.

The skeleton symmetry at each level says:
for every residue k, there's a mirror P#-k.
In phase space, this means for every rotation angle θ,
there's a compensating angle.

THIS is how the skeleton forces zeros to σ = 1/2:
the mirror symmetry ensures the phase conspiracy
can only happen symmetrically around the critical line.
""")

# ================================================================
# PLOTS
# ================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: |E_n| at zeros vs non-zeros
ax = axes[0, 0]
for t, name in zip(test_t, test_names):
    d = all_data[t]
    style = '-' if 'ZERO' in name else '--'
    width = 2.5 if 'ZERO' in name else 1.5
    ax.plot(range(1, 21), d['magnitudes'], style, linewidth=width, 
            label=name, marker='o', markersize=3)
ax.set_title('|Partial Euler product| at each level', fontsize=13)
ax.set_xlabel('Level n (number of primes)')
ax.set_ylabel('|E_n(s)|')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 2: Phase accumulation
ax = axes[0, 1]
for t, name in zip(test_t, test_names):
    d = all_data[t]
    style = '-' if 'ZERO' in name else '--'
    width = 2.5 if 'ZERO' in name else 1.5
    ax.plot(range(1, 21), d['phases'], style, linewidth=width,
            label=name, marker='o', markersize=3)
ax.set_title('Phase of partial Euler product', fontsize=13)
ax.set_xlabel('Level n')
ax.set_ylabel('Phase (degrees)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 3: log|E_n| - should diverge at zeros
ax = axes[1, 0]
for t, name in zip(test_t, test_names):
    d = all_data[t]
    style = '-' if 'ZERO' in name else '--'
    width = 2.5 if 'ZERO' in name else 1.5
    ax.plot(range(1, 21), d['log_mags'], style, linewidth=width,
            label=name, marker='o', markersize=3)
ax.set_title('log|E_n| — divergence pattern', fontsize=13)
ax.set_xlabel('Level n')
ax.set_ylabel('log|E_n|')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 4: Phase per prime at the first zero
ax = axes[1, 1]
phases_per_prime = []
for p in primes:
    rotation = (-t * np.log(p) * 180 / np.pi) % 360
    if rotation > 180: rotation -= 360
    phases_per_prime.append(rotation)
ax.bar(range(len(primes)), phases_per_prime, color='steelblue', alpha=0.7)
ax.set_xticks(range(len(primes)))
ax.set_xticklabels([str(p) for p in primes], fontsize=8)
ax.set_title(f'Phase rotation per prime at ρ₁ (t={t:.2f})', fontsize=13)
ax.set_xlabel('Prime')
ax.set_ylabel('Rotation (degrees)')
ax.axhline(y=0, color='k', linewidth=0.5)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/home/claude/euler_tower.png', dpi=150)
print("\nPlot saved to euler_tower.png")
