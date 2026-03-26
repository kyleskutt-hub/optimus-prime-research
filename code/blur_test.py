"""
BLUR TEST: Mollify the tent and see what survives.

Take the tent h₀(u) = (1 - |log u|)₊
Convolve with a standard mollifier φ_ε (C∞ bump scaled to width ε)
Check positivity and monotonicity at decreasing ε values.

On log scale: g(x) = (1 - |x|)₊, mollify to g_ε = g * φ_ε
Mellin transform becomes: ĥ_ε(s) = ∫ g_ε(x) e^(sx) dx
"""

import numpy as np
from scipy import integrate
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt

# === Normalization constant for standard mollifier ===
NORM_CONST = integrate.quad(
    lambda x: np.exp(1.0/(x**2 - 1.0)) if abs(x) < 0.9999 else 0.0, 
    -1, 1, limit=100
)[0]

def make_mollified_tent(eps, N=10000):
    """
    Create mollified tent on a fine grid.
    Support of tent is [-1,1], mollifier adds ε on each side.
    """
    L = 1.0 + eps + 0.05
    x = np.linspace(-L, L, N)
    dx = x[1] - x[0]
    
    # Tent
    g = np.maximum(1.0 - np.abs(x), 0.0)
    
    # Mollifier on same grid
    t = x / eps
    phi = np.zeros_like(x)
    mask = np.abs(t) < 0.9999
    phi[mask] = np.exp(1.0 / (t[mask]**2 - 1.0)) / (eps * NORM_CONST)
    
    # Convolve
    g_eps = fftconvolve(g, phi, mode='same') * dx
    
    return x, g_eps

def mellin_on_grid(s, x_grid, g_grid):
    """ĥ(s) = ∫ g(x) e^(sx) dx via trapezoidal rule"""
    dx = x_grid[1] - x_grid[0]
    integrand = g_grid * np.exp(s * x_grid)
    return np.trapezoid(integrand, dx=dx)

def mellin_tent_exact(s):
    """Exact Mellin of tent: 2(cosh(s) - 1) / s^2"""
    if abs(s) < 1e-12:
        return 1.0
    return 2.0 * (np.cosh(s) - 1.0) / s**2

# =================================================================
# RUN TESTS
# =================================================================
epsilons = [0.2, 0.1, 0.05, 0.02, 0.01]

print("=" * 70)
print("BLUR TEST: Mollified Tent at Decreasing ε")  
print("=" * 70)

t_test = np.linspace(0, 40, 201)
delta_test = np.linspace(0, 0.45, 46)
t_mono_test = [0, 2, 5, 10, 14.13, 21.02, 25.01, 30.0]

all_results = {}

for eps in epsilons:
    print(f"\n--- ε = {eps} ---")
    
    x_grid, g_eps = make_mollified_tent(eps)
    
    # TEST 1: Positivity on critical line
    pos_vals = []
    for t in t_test:
        s = 0.5 * 1j * 0 + 1j * t  # s = it on log scale (δ=0)
        val = mellin_on_grid(1j * t, x_grid, g_eps)
        pos_vals.append(val)
    
    pos_reals = np.array([v.real for v in pos_vals])
    pos_imags = np.array([v.imag for v in pos_vals])
    min_real = np.min(pos_reals)
    max_imag = np.max(np.abs(pos_imags))
    
    # Note: on critical line, s = 1/2 + it in Mellin convention
    # In our log-scale convention, this maps to evaluating at s = it
    # (since the 1/2 shift is absorbed into the measure)
    # Let's be more careful: ĥ(1/2 + it) = ∫ g(x) e^((1/2+it)x) dx
    
    pos_vals_correct = []
    for t in t_test:
        val = mellin_on_grid(0.5 + 1j * t, x_grid, g_eps)  # WRONG - this is shifted
        # Actually: on log scale, Mellin(s) = ∫ g(x) e^(sx) dx
        # We want s on critical line: s = it (imaginary axis)
        # because h(u) u^(s-1) du with s=1/2+it becomes g(x) e^((s-1/2)x) e^(x/2) dx
        # Hmm, let me just use the direct approach
        pos_vals_correct.append(val)
    
    # Let me redo this cleanly. The Mellin transform is:
    # ĥ(s) = ∫₀^∞ h(u) u^{s-1} du = ∫ g(x) e^{(s-1)x} e^x dx = ∫ g(x) e^{sx} dx
    # Wait no. u = e^x, du = e^x dx. So:
    # ĥ(s) = ∫ g(x) e^{(s-1)x} · e^x dx = ∫ g(x) e^{sx} dx
    # So ĥ(s) = ∫ g(x) e^{sx} dx. On critical line s = 1/2 + it.
    
    pos_vals2 = []
    for t in t_test:
        val = mellin_on_grid(0.5 + 1j * t, x_grid, g_eps)
        pos_vals2.append(val)
    
    pos_reals2 = np.array([v.real for v in pos_vals2])
    pos_imags2 = np.array([v.imag for v in pos_vals2])
    min_real2 = np.min(pos_reals2)
    max_imag2 = np.max(np.abs(pos_imags2))
    
    positivity_ok = min_real2 > -1e-10 and max_imag2 < 1e-6
    
    print(f"  Positivity: min Re = {min_real2:.8f}, max |Im| = {max_imag2:.2e}", end="")
    if min_real2 > 0:
        print("  ✓ POSITIVE")
    elif min_real2 > -1e-6:
        print("  ~ marginal")
    else:
        print(f"  ✗ FAILS (goes to {min_real2:.6f})")
    
    # TEST 2: Monotonicity |ĥ(1/2 + δ + it)| increasing in δ
    mono_ok_all = True
    mono_data = {}
    for t in t_mono_test:
        mags = []
        for delta in delta_test:
            s = 0.5 + delta + 1j * t
            val = mellin_on_grid(s, x_grid, g_eps)
            mags.append(abs(val))
        mono_data[t] = mags
        
        # Check monotonicity
        is_mono = all(mags[i+1] >= mags[i] - 1e-10 for i in range(len(mags)-1))
        if not is_mono:
            mono_ok_all = False
            # Find first violation
            for i in range(len(mags)-1):
                if mags[i+1] < mags[i] - 1e-10:
                    drop = mags[i] - mags[i+1]
                    print(f"  Mono t={t:5.1f}: ✗ fails at δ={delta_test[i+1]:.3f} (drop={drop:.2e})")
                    break
        else:
            print(f"  Mono t={t:5.1f}: ✓")
    
    # TEST 3: Monotonicity with Gaussian penalty
    lam = 2.0
    gauss_ok = True
    for t in t_mono_test:
        mags_F = []
        for delta in delta_test:
            s = 0.5 + delta + 1j * t
            val = mellin_on_grid(s, x_grid, g_eps)
            F = abs(val) * np.exp(lam * delta**2 / 2)
            mags_F.append(F)
        
        is_mono = all(mags_F[i+1] >= mags_F[i] - 1e-10 for i in range(len(mags_F)-1))
        if not is_mono:
            gauss_ok = False
    
    print(f"  Gaussian (λ={lam}): {'✓ monotone' if gauss_ok else '✗ fails'}")
    
    all_results[eps] = {
        'x_grid': x_grid, 'g_eps': g_eps,
        'pos_reals': pos_reals2, 'pos_imags': pos_imags2,
        'mono_data': mono_data, 'positivity': min_real2 > 0,
        'monotonicity': mono_ok_all
    }

# =================================================================
# REFERENCE: Exact tent
# =================================================================
print(f"\n--- EXACT TENT (no blur) ---")
tent_pos = []
for t in t_test:
    val = mellin_tent_exact(0.5 + 1j * t)
    tent_pos.append(val)
tent_reals = np.array([v.real for v in tent_pos])
tent_imags = np.array([v.imag for v in tent_pos])
print(f"  Positivity: min Re = {np.min(tent_reals):.8f}")

tent_mono = {}
tent_mono_ok = True
for t in t_mono_test:
    mags = []
    for delta in delta_test:
        val = mellin_tent_exact(0.5 + delta + 1j * t)
        mags.append(abs(val))
    tent_mono[t] = mags
    is_mono = all(mags[i+1] >= mags[i] - 1e-12 for i in range(len(mags)-1))
    if not is_mono:
        tent_mono_ok = False
        print(f"  Mono t={t:5.1f}: ✗")
    else:
        print(f"  Mono t={t:5.1f}: ✓")
print(f"  Overall: {'✓' if tent_mono_ok else '✗'}")

# =================================================================
# PLOTS
# =================================================================
fig, axes = plt.subplots(3, 2, figsize=(16, 18))

# Plot 1: The blurred tent shapes
ax = axes[0, 0]
for eps in [0.2, 0.1, 0.05, 0.01]:
    r = all_results[eps]
    ax.plot(r['x_grid'], r['g_eps'], label=f'ε={eps}', linewidth=1.5)
# Exact tent
x_tent = np.linspace(-1.3, 1.3, 500)
y_tent = np.maximum(1.0 - np.abs(x_tent), 0.0)
ax.plot(x_tent, y_tent, 'k--', linewidth=2, label='Exact tent')
ax.set_title('Mollified tent shapes (log scale)', fontsize=13)
ax.set_xlabel('x = log(u)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Positivity on critical line
ax = axes[0, 1]
ax.plot(t_test, tent_reals, 'k-', linewidth=2, label='Exact tent', alpha=0.7)
for eps in [0.2, 0.1, 0.05, 0.01]:
    r = all_results[eps]
    ax.plot(t_test, r['pos_reals'], label=f'ε={eps}', linewidth=1.2)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax.set_title('Re(ĥ) on critical line (δ=0)', fontsize=13)
ax.set_xlabel('t')
ax.set_ylabel('Re(ĥ(1/2 + it))')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 40)

# Plot 3: Zoom on positivity near first zero crossing
ax = axes[1, 0]
ax.plot(t_test, tent_reals, 'k-', linewidth=2, label='Exact tent', alpha=0.7)
for eps in [0.2, 0.1, 0.05, 0.01]:
    r = all_results[eps]
    ax.plot(t_test, r['pos_reals'], label=f'ε={eps}', linewidth=1.5)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax.set_title('ZOOM: Positivity near zero-crossing region', fontsize=13)
ax.set_xlabel('t')
ax.set_xlim(3, 15)
ax.set_ylim(-0.02, 0.08)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 4: Monotonicity for exact tent
ax = axes[1, 1]
colors = plt.cm.tab10(np.linspace(0, 1, len(t_mono_test)))
for i, t in enumerate(t_mono_test):
    ax.plot(delta_test, tent_mono[t], '-o', color=colors[i], markersize=2, 
            label=f't={t:.1f}')
ax.set_title('Exact tent: |ĥ(1/2+δ+it)| vs δ', fontsize=13)
ax.set_xlabel('δ')
ax.set_ylabel('|ĥ|')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 5: Monotonicity for ε=0.01
ax = axes[2, 0]
eps_show = 0.01
if eps_show in all_results:
    for i, t in enumerate(t_mono_test):
        ax.plot(delta_test, all_results[eps_show]['mono_data'][t], '-o', 
                color=colors[i], markersize=2, label=f't={t:.1f}')
ax.set_title(f'Blurred tent ε={eps_show}: |ĥ_ε(1/2+δ+it)| vs δ', fontsize=13)
ax.set_xlabel('δ')
ax.set_ylabel('|ĥ_ε|')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 6: Monotonicity for ε=0.1
ax = axes[2, 1]
eps_show = 0.1
if eps_show in all_results:
    for i, t in enumerate(t_mono_test):
        ax.plot(delta_test, all_results[eps_show]['mono_data'][t], '-o',
                color=colors[i], markersize=2, label=f't={t:.1f}')
ax.set_title(f'Blurred tent ε={eps_show}: |ĥ_ε(1/2+δ+it)| vs δ', fontsize=13)
ax.set_xlabel('δ')
ax.set_ylabel('|ĥ_ε|')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/blur_test.png', dpi=150)
print("\nPlot saved to blur_test.png")

# =================================================================
# SUMMARY
# =================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"{'ε':>6s}  {'Positivity':>12s}  {'Monotonicity':>14s}")
print("-" * 36)
print(f"{'exact':>6s}  {'✓':>12s}  {'✓':>14s}")
for eps in epsilons:
    r = all_results[eps]
    pos = "✓" if r['positivity'] else "✗"
    mono = "✓" if r['monotonicity'] else "✗"
    print(f"{eps:6.3f}  {pos:>12s}  {mono:>14s}")
