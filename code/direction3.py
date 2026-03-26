"""
DIRECTION 3 EXPERIMENT: Vary tent width, find the sweet spot

Tent with width A: h_A(u) = (1 - |log u|/A)_+
Support: [e^{-A}, e^A]

Mellin transform: h-hat_A(s) = 2A(cosh(As) - 1) / (As)^2
  (scaled version of our tent)

For each A, compute:
  Signal:  F(1/2 + delta + it0) = |h-hat_A(1/2 + delta + it0)|^2
  On-line: F(1/2 + it0) = |h-hat_A(1/2 + it0)|^2
  Cost:    C(A) = integral of |h-hat_A(1/2 + it)|^2 against 
           the archimedean measure (approximated by spectral density)

The test: does Signal > Cost * On-line for any A and delta > 0?

If yes for some A: RH follows
If no for all A: tent isn't sharp enough
"""
import numpy as np
import matplotlib.pyplot as plt

def mellin_tent_A(s, A):
    """Mellin of width-A tent: h_A(u) = (1 - |log u|/A)_+"""
    As = A * s
    if abs(As) < 1e-12:
        return A + 0j
    return 2.0 * A * (np.cosh(As) - 1.0) / (As)**2

def F_A(s, A):
    """F = |h-hat|^2"""
    return abs(mellin_tent_A(s, A))**2

# First Riemann zero
t0 = 14.134725

print("=" * 70)
print("DIRECTION 3: Vary tent width A")
print(f"Target zero: t0 = {t0}")
print("=" * 70)

# Test range of widths
A_values = np.array([0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0])
delta_values = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]

# For each A, compute the "spectral cost" C(A)
# This is approximately the integral of F_A(1/2+it) weighted by 
# the density of states ~ log(t/(2*pi)) / (2*pi)
# For our purposes, we approximate:
# C(A) ~ sum of F_A(1/2+it) over a dense grid, weighted by spectral density

def spectral_cost(A, t_max=200):
    """Approximate integral of F_A on critical line against spectral measure"""
    t_grid = np.linspace(0.1, t_max, 4000)
    dt = t_grid[1] - t_grid[0]
    
    total = 0
    for t in t_grid:
        f_val = F_A(0.5 + 1j * t, A)
        # Spectral density ~ log(t/(2*pi)) / (2*pi) for large t
        density = max(np.log(t / (2 * np.pi)), 0.1) / (2 * np.pi)
        total += f_val * density * dt
    
    return total

print(f"\n{'A':>6s}  {'F(on-line)':>12s}  {'C(A)':>12s}  ", end="")
for d in delta_values:
    print(f"{'d='+str(d):>10s}", end="  ")
print()
print("-" * (36 + 12 * len(delta_values)))

results = {}

for A in A_values:
    f_online = F_A(0.5 + 1j * t0, A)
    cost = spectral_cost(A)
    
    row = {'online': f_online, 'cost': cost, 'ratios': {}}
    
    print(f"{A:>6.1f}  {f_online:>12.6e}  {cost:>12.6e}  ", end="")
    
    for d in delta_values:
        f_offline = F_A(0.5 + d + 1j * t0, A)
        # The ratio we need > 1 for contradiction:
        # F(offline) / (C(A) * F(online))
        # But this isn't quite right. Let me compute the excess ratio:
        # excess = F(offline) - F(online)
        # We need excess to be detectable against cost
        excess = f_offline - f_online
        ratio = f_offline / f_online if f_online > 0 else 0
        row['ratios'][d] = ratio
        print(f"{ratio:>10.4f}", end="  ")
    
    print()
    results[A] = row

# Now the key question: excess vs cost
print(f"\n\n{'='*70}")
print("KEY RATIO: F(offline) / F(online) — how much bigger is the off-line signal?")
print("(Need this to overcome the spectral cost)")
print("=" * 70)

print(f"\nFor delta = 0.1 (moderate off-line displacement):")
print(f"\n{'A':>6s}  {'F(off)/F(on)':>14s}  {'Excess':>14s}  {'C(A)':>14s}  {'Excess/C(A)':>14s}")
print("-" * 66)

for A in A_values:
    f_on = F_A(0.5 + 1j * t0, A)
    f_off = F_A(0.5 + 0.1 + 1j * t0, A)
    excess = f_off - f_on
    cost = spectral_cost(A)
    ratio = excess / cost if cost > 0 else 0
    
    print(f"{A:>6.1f}  {f_off/f_on if f_on > 0 else 0:>14.6f}  {excess:>14.6e}  {cost:>14.6e}  {ratio:>14.6e}")

# Now DeepSeek's specific question:
# Is there A where F(1/2+delta+it0) > C(A) * F(1/2+it0)?
print(f"\n\n{'='*70}")
print("DEEPSEEK'S TEST: F(offline) > C(A) * F(online)?")
print("=" * 70)

for d in [0.05, 0.1, 0.2, 0.5]:
    print(f"\ndelta = {d}:")
    for A in A_values:
        f_on = F_A(0.5 + 1j * t0, A)
        f_off = F_A(0.5 + d + 1j * t0, A)
        cost = spectral_cost(A)
        
        lhs = f_off
        rhs = cost * f_on
        
        verdict = "✓ SIGNAL WINS" if lhs > rhs else "✗ cost wins"
        ratio = lhs / rhs if rhs > 0 else float('inf')
        
        print(f"  A={A:>5.1f}: signal={lhs:.4e}  cost*online={rhs:.4e}  ratio={ratio:.6f}  {verdict}")

# PLOT
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: F(online) vs A
ax = axes[0, 0]
f_on_vals = [F_A(0.5 + 1j * t0, A) for A in A_values]
ax.semilogy(A_values, f_on_vals, 'bo-', linewidth=2)
ax.set_title(f'F(1/2 + it₀) vs tent width A', fontsize=13)
ax.set_xlabel('A (tent width)')
ax.set_ylabel('F (log scale)')
ax.grid(True, alpha=0.3)

# Plot 2: Ratio F(off)/F(on) vs A for various delta
ax = axes[0, 1]
for d in [0.01, 0.05, 0.1, 0.2, 0.5]:
    ratios = [F_A(0.5+d+1j*t0, A) / F_A(0.5+1j*t0, A) if F_A(0.5+1j*t0, A) > 1e-30 else 1 for A in A_values]
    ax.plot(A_values, ratios, 'o-', label=f'δ={d}')
ax.axhline(y=1, color='k', linestyle='--', alpha=0.3)
ax.set_title('Signal amplification: F(off)/F(on)', fontsize=13)
ax.set_xlabel('A')
ax.set_ylabel('Ratio')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Spectral cost vs A
ax = axes[1, 0]
costs = [spectral_cost(A) for A in A_values]
ax.semilogy(A_values, costs, 'ro-', linewidth=2)
ax.set_title('Spectral cost C(A) vs tent width', fontsize=13)
ax.set_xlabel('A')
ax.set_ylabel('C(A) (log scale)')
ax.grid(True, alpha=0.3)

# Plot 4: The money plot - ratio signal/(cost*online) vs A
ax = axes[1, 1]
for d in [0.05, 0.1, 0.2, 0.5]:
    money = []
    for A in A_values:
        f_on = F_A(0.5 + 1j * t0, A)
        f_off = F_A(0.5 + d + 1j * t0, A)
        c = spectral_cost(A)
        r = f_off / (c * f_on) if c * f_on > 1e-30 else 0
        money.append(r)
    ax.plot(A_values, money, 'o-', linewidth=2, label=f'δ={d}')
ax.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='WIN threshold')
ax.set_title('THE MONEY PLOT: signal / (cost × online)', fontsize=13)
ax.set_xlabel('A (tent width)')
ax.set_ylabel('Ratio (need > 1)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0, max(2, max(money) * 1.2) if money else 2)

plt.tight_layout()
plt.savefig('/home/claude/direction3_test.png', dpi=150)
print("\nPlot saved.")
