"""
DOME TEST: Can a C∞ bump function replace the tent?

We test the standard bump function on the multiplicative group:
  h(u) = exp(1/((log u)^2 - 1))  for |log u| < 1   (i.e. 1/e < u < e)
  h(u) = 0                        otherwise

This is C∞, compactly supported on [1/e, e], symmetric around u=1.

We numerically compute its Mellin transform:
  ĥ(s) = ∫₀^∞ h(u) u^(s-1) du

with s = 1/2 + δ + it

Then check:
  Property 4: ĥ(1/2 + it) > 0  for all real t  (positivity on critical line)
  Property 5: |ĥ(1/2 + δ + it)| is increasing in δ for δ > 0  (monotonicity off-line)
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

# === The bump function on multiplicative group ===
def bump(u):
    """C∞ bump: h(u) = exp(1/((log u)^2 - 1)) for |log u| < 1, else 0"""
    log_u = np.log(u)
    if abs(log_u) >= 1.0:
        return 0.0
    val = log_u**2 - 1.0
    if abs(val) < 1e-15:
        return 0.0
    return np.exp(1.0 / val)

# === Mellin transform: ĥ(s) = ∫ h(u) u^(s-1) du ===
def mellin_transform(s, h_func):
    """Compute Mellin transform numerically. s is complex."""
    def integrand_real(u):
        if u <= 0:
            return 0.0
        hval = h_func(u)
        if hval == 0:
            return 0.0
        power = u**(s - 1)
        return hval * np.real(power) / u  # du/u for multiplicative measure

    def integrand_imag(u):
        if u <= 0:
            return 0.0
        hval = h_func(u)
        if hval == 0:
            return 0.0
        power = u**(s - 1)
        return hval * np.imag(power) / u

    # Integration over support [1/e, e] = [0.3679, 2.7183]
    a, b = np.exp(-1) + 1e-10, np.exp(1) - 1e-10
    
    real_part, _ = integrate.quad(integrand_real, a, b, limit=200)
    imag_part, _ = integrate.quad(integrand_imag, a, b, limit=200)
    
    return real_part + 1j * imag_part

# === Also compute for the TENT for comparison ===
def tent(u):
    """Fejér tent: h(u) = (1 - |log u|)  for |log u| < 1, else 0"""
    log_u = np.log(u)
    if abs(log_u) >= 1.0:
        return 0.0
    return 1.0 - abs(log_u)

print("=" * 60)
print("DOME TEST: C∞ bump function vs. Tent (Fejér)")
print("=" * 60)

# === TEST 1: Positivity on the critical line (δ = 0) ===
print("\n--- TEST 1: POSITIVITY on critical line (δ=0) ---")
print("ĥ(1/2 + it) for various t values:\n")

t_values = np.linspace(0, 30, 61)
dome_on_line = []
tent_on_line = []

for t in t_values:
    s = 0.5 + 1j * t
    dome_val = mellin_transform(s, bump)
    tent_val = mellin_transform(s, tent)
    dome_on_line.append(dome_val)
    tent_on_line.append(tent_val)

print(f"{'t':>6s}  {'Dome Re':>12s}  {'Dome Im':>12s}  {'Tent Re':>12s}  {'Tent Im':>12s}")
print("-" * 58)
for i, t in enumerate(t_values[::5]):
    idx = i * 5
    d = dome_on_line[idx]
    tr = tent_on_line[idx]
    print(f"{t:6.1f}  {d.real:12.6f}  {d.imag:12.6f}  {tr.real:12.6f}  {tr.imag:12.6f}")

# Check positivity
dome_reals = [v.real for v in dome_on_line]
dome_imags = [v.imag for v in dome_on_line]
min_dome_real = min(dome_reals)
max_dome_imag_abs = max(abs(v) for v in dome_imags)

print(f"\nDome: min Re(ĥ) on critical line = {min_dome_real:.8f}")
print(f"Dome: max |Im(ĥ)| on critical line = {max_dome_imag_abs:.2e}")
if min_dome_real > 0 and max_dome_imag_abs < 1e-10:
    print("✓ POSITIVITY HOLDS — Mellin transform is real and positive on critical line!")
elif min_dome_real > -1e-10:
    print("~ POSITIVITY MARGINAL — very close to zero")
else:
    print("✗ POSITIVITY FAILS — goes negative on critical line")

# === TEST 2: Monotonicity in δ ===
print("\n\n--- TEST 2: MONOTONICITY in δ (off critical line) ---")
print("|ĥ(1/2 + δ + it)| should INCREASE as δ increases\n")

delta_values = np.linspace(0, 0.4, 21)
test_t_values = [0, 2, 5, 10, 14.13, 20]  # 14.13 ≈ first Riemann zero

monotonicity_ok = True
mono_results = {}

for t in test_t_values:
    mags = []
    for delta in delta_values:
        s = 0.5 + delta + 1j * t
        val = mellin_transform(s, bump)
        mags.append(abs(val))
    mono_results[t] = mags
    
    # Check monotonicity
    is_mono = all(mags[i+1] >= mags[i] - 1e-12 for i in range(len(mags)-1))
    
    print(f"t = {t:6.2f}: |ĥ| from {mags[0]:.6f} to {mags[-1]:.6f}  ", end="")
    if is_mono:
        print("✓ monotone increasing")
    else:
        # Find first violation
        for i in range(len(mags)-1):
            if mags[i+1] < mags[i] - 1e-12:
                print(f"✗ FAILS at δ={delta_values[i+1]:.3f} (drop: {mags[i]-mags[i+1]:.2e})")
                monotonicity_ok = False
                break

print(f"\nOverall monotonicity: {'✓ HOLDS for all tested t' if monotonicity_ok else '✗ FAILS'}")

# === TEST 3: Monotonicity with Gaussian penalty ===
print("\n\n--- TEST 3: MONOTONICITY with Gaussian penalty e^(λδ²/2) ---")
lam = 1.0
print(f"λ = {lam}\n")

mono_gauss_ok = True
for t in test_t_values:
    mags = []
    for delta in delta_values:
        s = 0.5 + delta + 1j * t
        val = mellin_transform(s, bump)
        F = abs(val) * np.exp(lam * delta**2 / 2)
        mags.append(F)
    
    is_mono = all(mags[i+1] >= mags[i] - 1e-12 for i in range(len(mags)-1))
    print(f"t = {t:6.2f}: F from {mags[0]:.6f} to {mags[-1]:.6f}  ", end="")
    if is_mono:
        print("✓ monotone")
    else:
        for i in range(len(mags)-1):
            if mags[i+1] < mags[i] - 1e-12:
                print(f"✗ FAILS at δ={delta_values[i+1]:.3f}")
                mono_gauss_ok = False
                break

print(f"\nWith Gaussian: {'✓ HOLDS' if mono_gauss_ok else '✗ FAILS'}")

# === PLOT ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Bump vs Tent shape
u_plot = np.linspace(0.37, 2.72, 500)
bump_vals = [bump(u) for u in u_plot]
tent_vals = [tent(u) for u in u_plot]
axes[0,0].plot(u_plot, bump_vals, 'b-', linewidth=2, label='Dome (C∞ bump)')
axes[0,0].plot(u_plot, tent_vals, 'r--', linewidth=2, label='Tent (Fejér)')
axes[0,0].set_title('Test Functions: Dome vs Tent', fontsize=13)
axes[0,0].set_xlabel('u')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# Plot 2: Mellin transform on critical line
axes[0,1].plot(t_values, dome_reals, 'b-', linewidth=2, label='Dome')
axes[0,1].plot(t_values, [v.real for v in tent_on_line], 'r--', linewidth=2, label='Tent')
axes[0,1].axhline(y=0, color='k', linestyle='-', alpha=0.3)
axes[0,1].set_title('Mellin transform on critical line (δ=0)', fontsize=13)
axes[0,1].set_xlabel('t')
axes[0,1].set_ylabel('Re(ĥ(1/2 + it))')
axes[0,1].legend()
axes[0,1].grid(True, alpha=0.3)

# Plot 3: |ĥ| vs δ for various t
colors = plt.cm.viridis(np.linspace(0, 1, len(test_t_values)))
for i, t in enumerate(test_t_values):
    axes[1,0].plot(delta_values, mono_results[t], '-o', color=colors[i], 
                   markersize=3, label=f't={t:.1f}')
axes[1,0].set_title('|ĥ_dome(1/2 + δ + it)| vs δ', fontsize=13)
axes[1,0].set_xlabel('δ (distance from critical line)')
axes[1,0].set_ylabel('|ĥ|')
axes[1,0].legend(fontsize=8)
axes[1,0].grid(True, alpha=0.3)

# Plot 4: With Gaussian penalty
for i, t in enumerate(test_t_values):
    F_vals = []
    for j, delta in enumerate(delta_values):
        s = 0.5 + delta + 1j * t
        val = mellin_transform(s, bump)
        F_vals.append(abs(val) * np.exp(lam * delta**2 / 2))
    axes[1,1].plot(delta_values, F_vals, '-o', color=colors[i],
                   markersize=3, label=f't={t:.1f}')
axes[1,1].set_title(f'F(δ,t) = |ĥ| · exp(λδ²/2), λ={lam}', fontsize=13)
axes[1,1].set_xlabel('δ')
axes[1,1].set_ylabel('F(δ,t)')
axes[1,1].legend(fontsize=8)
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/dome_test.png', dpi=150)
print("\nPlot saved to dome_test.png")
print("\n" + "=" * 60)
print("DONE")
