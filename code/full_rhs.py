"""
THE REAL TEST: Full RHS computation

For tent h_A(u) = (1 - |log u|/A)+, using f = h*h~ so F(s) = |h-hat(s)|^2:

The explicit formula (Weil) says:
  sum_rho F(rho) = integral_term + prime_term + constant_terms

We compute each piece and check if F(off-line) can exceed the total RHS.

RHS has:
1. Archimedean integral: integral of F(1/2+it) * K(t) dt
   where K(t) = Re(psi(1/4 + it/2)) / (2*pi) + (log(pi) + gamma)/(2*pi)
   psi = digamma function

2. Prime sum: sum over prime powers p^m of
   log(p) * (f*f~)(p^m) / p^(m/2)
   For tent: (f*f~)(p^m) = (h*h)(p^m) in multiplicative convolution
   = autocorrelation of tent evaluated at p^m
   The autocorrelation of tent_A is the B-spline: 
   g*g(x) where g(x)=(1-|x|/A)+
   This is nonzero for |x| < 2A, i.e. p^m < e^{2A}

3. Constant terms: F(0) + F(1) = h-hat(0)^2 + h-hat(1)^2
   (from the poles of zeta at s=0 and s=1)

Let's compute everything properly.
"""
import numpy as np
from scipy import integrate, special
import matplotlib.pyplot as plt

def mellin_tent_A(s, A):
    """Mellin of width-A tent"""
    As = A * s
    if abs(As) < 1e-12:
        return A + 0j
    return 2.0 * A * (np.cosh(As) - 1.0) / (As)**2

def F_A(s, A):
    return abs(mellin_tent_A(s, A))**2

def tent_autocorr(x, A):
    """Autocorrelation of tent_A on log scale: (g*g)(x) where g(y)=(1-|y|/A)+
    This is a B-spline of order 2, support [-2A, 2A]
    Explicit formula:
      For |x| <= A: (2A^2 - x^2 - ... ) -- let me compute via integral
    Actually easier to use: Mellin(autocorr)(s) = |Mellin(tent)(s)|^2
    But for the prime sum we need position-space values.
    
    g*g(x) = integral g(y)g(x-y) dy
    = integral_{max(-A,x-A)}^{min(A,x+A)} (1-|y|/A)(1-|x-y|/A) dy
    """
    x = abs(x)  # symmetric
    if x >= 2*A:
        return 0.0
    
    # Numerical integration
    def integrand(y):
        if abs(y) >= A:
            return 0.0
        if abs(x - y) >= A:
            return 0.0
        return (1.0 - abs(y)/A) * (1.0 - abs(x-y)/A)
    
    lo = max(-A, x - A)
    hi = min(A, x + A)
    if lo >= hi:
        return 0.0
    
    val, _ = integrate.quad(integrand, lo, hi)
    return val

def archimedean_integral(A, t_max=300):
    """
    Archimedean contribution:
    W_R(f*f~) = integral_{-inf}^{inf} F(1/2+it) * w(t) dt
    
    where w(t) = -1/(2*pi) * Re[psi(1/4 + it/2)] + log(pi)/(2*pi)
    
    But more precisely, for the completed zeta function:
    The archimedean term from the explicit formula is:
    -integral F(1/2+it) * [psi(1/4+it/2) + psi(1/4-it/2)]/(4*pi) dt
    + log(pi) * integral F(1/2+it) dt/(2*pi)
    + (gamma/2) * something...
    
    Let me use the standard form: for f*f~ with Mellin F(s),
    the archimedean W_inf = integral_R F(1/2+it) * phi(t) dt
    where phi(t) = [log(pi) - Re(psi(1/4+it/2))] / (2*pi)
    
    This is a standard formula from Bombieri's formulation.
    """
    t_grid = np.linspace(0.01, t_max, 6000)
    dt = t_grid[1] - t_grid[0]
    
    total = 0.0
    for t in t_grid:
        f_val = F_A(0.5 + 1j * t, A)
        # Kernel: phi(t) = [log(pi) - Re(psi(1/4 + it/2))] / (2*pi)
        psi_val = special.digamma(0.25 + 0.5j * t)
        kernel = (np.log(np.pi) - psi_val.real) / (2 * np.pi)
        total += f_val * kernel * dt
    
    # Factor of 2 for negative t (F is even in t for real f)
    total *= 2
    
    # Add t=0 neighborhood
    f0 = F_A(0.5, A)
    kernel0 = (np.log(np.pi) - special.digamma(0.25).real) / (2 * np.pi)
    # small correction for t near 0
    
    return total

def prime_sum(A):
    """
    Prime sum: sum over prime powers p^m with p^m < e^{2A}:
    sum log(p)/p^{m/2} * (h*h~)(p^m)
    
    where (h*h~)(p^m) = autocorrelation evaluated at log(p^m)
    
    For f*f~: the explicit formula prime term is:
    sum_{p^m} log(p) * [f*f~(p^{m/2}) + f*f~(p^{-m/2})] / 2
    
    Actually for the standard explicit formula with F(s) = |h-hat(s)|^2:
    prime_term = sum_{p^m} log(p) * g*g(m*log(p)) / p^{m/2}
    
    where g*g is the autocorrelation on log scale.
    
    Wait - I need to be more careful about the exact formula.
    The explicit formula for the test function phi(x) = g*g(x) is:
    
    sum_rho phi-hat(rho-1/2) = phi-hat(-1/2) + phi-hat(1/2) 
                               + W_inf(phi)
                               - sum_{p^m} Lambda(p^m)/p^{m/2} * phi(m*log(p))
    
    where Lambda(p^m) = log(p), and phi-hat(s) = integral phi(x) e^{sx} dx = F(1/2+s).
    
    The prime sum has a MINUS sign! It goes to the other side:
    
    sum_rho F(rho) + sum_{p^m} log(p)/p^{m/2} * phi(m*log(p)) = 
        F(0) + F(1) + W_inf
    """
    # Primes up to e^{2A}
    def sieve(n):
        is_prime = [True] * (n+1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n**0.5)+1):
            if is_prime[i]:
                for j in range(i*i, n+1, i):
                    is_prime[j] = False
        return [p for p in range(2, n+1) if is_prime[p]]
    
    max_prime_power = np.exp(2*A)
    primes = sieve(min(int(max_prime_power) + 10, 10000))
    
    total = 0.0
    for p in primes:
        m = 1
        while p**m < max_prime_power + 1:
            x = m * np.log(p)
            if x < 2*A:
                ac = tent_autocorr(x, A)
                contribution = np.log(p) / p**(m/2.0) * ac
                total += contribution
            m += 1
    
    return total

# Also for f*f~, we need the constant terms
def constant_terms(A):
    """F(0) + F(1) from the poles of zeta"""
    F0 = F_A(0.0, A)  # = |h-hat(0)|^2 = A^2
    F1 = F_A(1.0, A)  # = |h-hat(1)|^2
    return F0 + F1

# ================================================================
# MAIN COMPUTATION
# ================================================================
print("=" * 70)
print("FULL RHS COMPUTATION")
print("=" * 70)

t0 = 14.134725
delta = 0.1

A_values = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0]

print(f"\nFixed delta = {delta}, t0 = {t0}")
print(f"\n{'A':>5s} {'F(off)':>12s} {'F(on)':>12s} {'Primes':>12s} {'Arch.':>12s} {'Const':>12s} {'Full RHS':>12s} {'F(off)/RHS':>12s} {'Verdict':>10s}")
print("-" * 105)

all_data = []

for A in A_values:
    f_off = F_A(0.5 + delta + 1j * t0, A)
    f_on = F_A(0.5 + 1j * t0, A)
    
    p_sum = prime_sum(A)
    arch = archimedean_integral(A)
    const = constant_terms(A)
    
    # The explicit formula says:
    # sum_rho F(rho) + prime_sum = const + arch
    # So: sum_rho F(rho) = const + arch - prime_sum
    # The RHS that the zero sum must equal is: const + arch - prime_sum
    
    rhs = const + arch - p_sum
    
    ratio = f_off / rhs if rhs > 0 else float('inf')
    verdict = "CHECK" if ratio > 0.5 else "no"
    if f_off > rhs and rhs > 0:
        verdict = "!!! WIN"
    
    print(f"{A:>5.1f} {f_off:>12.4e} {f_on:>12.4e} {p_sum:>12.4e} {arch:>12.4e} {const:>12.4e} {rhs:>12.4e} {ratio:>12.6f} {verdict:>10s}")
    
    all_data.append({
        'A': A, 'f_off': f_off, 'f_on': f_on,
        'primes': p_sum, 'arch': arch, 'const': const, 'rhs': rhs
    })

print(f"\n\nNote: The zero sum includes ALL zeros, not just rho0.")
print(f"F(off) is the contribution from ONE off-line zero.")
print(f"For the argument to work, we need the EXCESS from one off-line")
print(f"zero to create a contradiction. The excess is F(off) - F(on).")
print(f"\nExcess = F(off) - F(on) vs total RHS:")
print(f"\n{'A':>5s} {'Excess':>12s} {'RHS':>12s} {'Excess/RHS':>12s}")
print("-" * 45)
for d in all_data:
    excess = d['f_off'] - d['f_on']
    ratio = excess / d['rhs'] if d['rhs'] > 0 else 0
    print(f"{d['A']:>5.1f} {excess:>12.4e} {d['rhs']:>12.4e} {ratio:>12.6e}")
