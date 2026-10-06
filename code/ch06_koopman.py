import numpy as np
from itertools import combinations_with_replacement
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.special import ellipk
import matplotlib.pyplot as plt

mu, lam = -0.05, -1.0                       # slow (mu) and fast (lam) eigenvalues

def f(t, x):                                # x1' = mu x1, x2' = lam (x2 - x1^2)
    return [mu * x[0], lam * (x[1] - x[0]**2)]

# (a) the lifted system y = (x1, x2, x1^2) is exactly linear
K = np.array([[mu, 0, 0], [0, lam, -lam], [0, 0, 2 * mu]])
x0 = np.array([1.5, -1.0]); t = np.linspace(0, 20, 201)
x = solve_ivp(f, (0, 20), x0, t_eval=t, rtol=1e-12, atol=1e-12).y
y = np.array([expm(K * tk) @ [x0[0], x0[1], x0[0]**2] for tk in t]).T
print('(a) max |x - y[:2]| =', np.abs(x - y[:2]).max())

# (b) extended DMD: regress monomials of x at step k+1 on those at step k
def monomials(X, order=3):
    return np.array([np.prod(X[list(c)], axis=0) for k in range(order + 1)
                     for c in combinations_with_replacement(range(2), k)])
rng = np.random.default_rng(0)
dt = 0.1
X0 = rng.uniform(-2, 2, (2, 500))                                    # many short bursts
X1 = np.array([solve_ivp(f, (0, dt), p, rtol=1e-12, atol=1e-12).y[:, -1] for p in X0.T]).T
Psi0, Psi1 = monomials(X0), monomials(X1)                            # 10 x 500
Kd = Psi1 @ np.linalg.pinv(Psi0)                                     # EDMD matrix
ev = np.sort(np.log(np.linalg.eigvals(Kd)).real / dt)
print('(b) EDMD continuous-time eigenvalues:', ev.round(4))           # sums of mu, lam

# (c) continuous spectrum: the pendulum frequency depends on the energy
E = np.linspace(-0.999, 0.999, 300)                                  # E = w^2/2 - cos(theta), g/L = 1
k2 = (1 + E) / 2                                                     # modulus^2 of the elliptic integral
omega = np.pi / (2 * ellipk(k2))                                     # frequency of the libration
plt.figure(figsize=(4, 2.6)); plt.plot(E, omega, color='#C2185B')
plt.xlabel('energy $E$'); plt.ylabel(r'frequency $\omega(E)$')
plt.tight_layout(); plt.savefig('lecture-notes/figures/ch06-pendulum-omega.png', dpi=200)
print('(c) omega from', omega[0].round(3), 'to', omega[-1].round(3))
