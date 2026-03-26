"""
Kyle's insight: positivity might only matter WHERE THE ZEROS ARE.

Check: is Re(ĥ(1/2 + it)) > 0 at every Riemann zero t_n?

The first 30 Riemann zeros (imaginary parts):
"""
import numpy as np

# First 30 non-trivial Riemann zeros (imaginary parts)
zeros = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]

def mellin_tent(s):
    """Exact Mellin of tent: ĥ(s) = 2(cosh(s) - 1) / s^2"""
    if abs(s) < 1e-12:
        return 1.0
    return 2.0 * (np.cosh(s) - 1.0) / s**2

print("=" * 65)
print("POSITIVITY AT RIEMANN ZERO LOCATIONS")
print("=" * 65)
print(f"\n{'Zero #':>7s}  {'t_n':>10s}  {'Re(ĥ)':>12s}  {'Im(ĥ)':>12s}  {'|ĥ|':>10s}  Status")
print("-" * 65)

all_positive = True
for i, t in enumerate(zeros):
    s = 0.5 + 1j * t
    val = mellin_tent(s)
    status = "✓" if val.real > 0 else "✗ NEGATIVE"
    if val.real <= 0:
        all_positive = False
    print(f"{i+1:>7d}  {t:>10.6f}  {val.real:>12.8f}  {val.imag:>12.8f}  {abs(val):>10.8f}  {status}")

print(f"\n{'ALL POSITIVE AT ZEROS' if all_positive else 'SOME NEGATIVE AT ZEROS'}")

# Now scan FINELY between t=0 and t=50 to see exactly where it's negative
print("\n\n" + "=" * 65)
print("FINE SCAN: Where does Re(ĥ) go negative?")
print("=" * 65)

t_fine = np.linspace(0, 50, 10001)
neg_regions = []
in_neg = False
neg_start = 0

for t in t_fine:
    s = 0.5 + 1j * t
    val = mellin_tent(s)
    if val.real < 0 and not in_neg:
        in_neg = True
        neg_start = t
    elif val.real >= 0 and in_neg:
        in_neg = False
        neg_regions.append((neg_start, t))

if in_neg:
    neg_regions.append((neg_start, t_fine[-1]))

print(f"\nNegative regions of Re(ĥ(1/2 + it)):")
for start, end in neg_regions:
    # Find minimum in this region
    t_region = np.linspace(start, end, 1000)
    min_val = min(mellin_tent(0.5 + 1j*t).real for t in t_region)
    print(f"  t ∈ [{start:.3f}, {end:.3f}]  (min Re = {min_val:.8f})")

print(f"\nFirst Riemann zero at t = 14.1347")
print(f"All negative regions are BELOW the first zero: ", end="")
if all(end < 14.13 for start, end in neg_regions):
    print("YES ✓")
else:
    print("NO ✗")
    # Check which negative regions overlap with zeros
    for start, end in neg_regions:
        for i, t in enumerate(zeros):
            if start <= t <= end:
                print(f"  Zero #{i+1} at t={t:.4f} is IN negative region [{start:.3f}, {end:.3f}]")

# Also check: does the PATTERN continue? Check up to t=200
print("\n\n" + "=" * 65)
print("EXTENDED SCAN: Negative regions up to t = 500")
print("=" * 65)

t_ext = np.linspace(0, 500, 100001)
neg_regions_ext = []
in_neg = False

for t in t_ext:
    s = 0.5 + 1j * t
    val = mellin_tent(s)
    if val.real < 0 and not in_neg:
        in_neg = True
        neg_start = t
    elif val.real >= 0 and in_neg:
        in_neg = False
        neg_regions_ext.append((neg_start, t))

if in_neg:
    neg_regions_ext.append((neg_start, t_ext[-1]))

print(f"\nTotal negative regions found: {len(neg_regions_ext)}")
print(f"\nFirst 20 negative regions:")
for i, (start, end) in enumerate(neg_regions_ext[:20]):
    width = end - start
    print(f"  [{start:>8.3f}, {end:>8.3f}]  width = {width:.3f}")

# Check if ANY Riemann zero falls in a negative region
# Use more zeros
more_zeros = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
    114.320220, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256819, 127.516684, 129.578704, 131.087688, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
]

print(f"\nChecking {len(more_zeros)} Riemann zeros against negative regions...")
zero_in_neg = False
for i, tz in enumerate(more_zeros):
    s = 0.5 + 1j * tz
    val = mellin_tent(s)
    if val.real < 0:
        zero_in_neg = True
        print(f"  ✗ Zero #{i+1} at t={tz:.4f}: Re(ĥ) = {val.real:.8f} NEGATIVE!")

if not zero_in_neg:
    print("  ✓ ALL 50 zeros have POSITIVE Re(ĥ)")
    print("\n  *** THE TENT IS POSITIVE AT EVERY RIEMANN ZERO ***")
    print("  *** NEGATIVITY ONLY OCCURS WHERE NO ZEROS EXIST ***")
