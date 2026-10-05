import numpy as np
from scipy.integrate import solve_ivp

# data: Burgers' equation u_t = -u u_x + nu u_xx, solved spectrally on a periodic domain
nu, L, n = 0.1, 16.0, 256
x = np.linspace(-L / 2, L / 2, n, endpoint=False)
k = 2 * np.pi * np.fft.fftfreq(n, d=L / n)
def burgers(t, u):
    uh = np.fft.fft(u)
    return np.real(-u * np.fft.ifft(1j * k * uh) - nu * np.fft.ifft(k**2 * uh))
t = np.linspace(0, 10, 201); dt = t[1] - t[0]
U = solve_ivp(burgers, (0, 10), np.exp(-(x + 2)**2), t_eval=t, rtol=1e-10, atol=1e-10).y   # n x m

# derivatives from the data with finite differences (clean data)
dx = x[1] - x[0]
Ut = np.gradient(U, dt, axis=1)
Ux = np.gradient(U, dx, axis=0)
Uxx = np.gradient(Ux, dx, axis=0)
Uxxx = np.gradient(Uxx, dx, axis=0)

# library: {1, u, u^2} x {1, u_x, u_xx, u_xxx}, every space-time point is one row
pw = {'': np.ones_like(U), 'u': U, 'u^2': U**2}
dv = {'': np.ones_like(U), 'u_x': Ux, 'u_xx': Uxx, 'u_xxx': Uxxx}
names = [(a + ' ' + b).strip() or '1' for a in pw for b in dv]
Theta = np.column_stack([(pw[a] * dv[b]).ravel() for a in pw for b in dv])
ut = Ut.ravel()

def stridge(Theta, y, lam=1e-5, tol=0.05, iters=10):
    """Sequential threshold ridge regression (Rudy et al. 2017), columns normalised."""
    norms = np.linalg.norm(Theta, axis=0); T = Theta / norms
    big = np.ones(T.shape[1], bool)
    for _ in range(iters):
        A = T[:, big]
        w = np.zeros(T.shape[1])
        w[big] = np.linalg.solve(A.T @ A + lam * np.eye(big.sum()), A.T @ y)
        big = abs(w / norms) > tol                     # threshold on the real coefficients
    w = np.zeros(T.shape[1]); w[big] = np.linalg.lstsq(T[:, big], y, rcond=None)[0]
    return w / norms

xi = stridge(Theta, ut)
print('u_t =', ' '.join(f'{c:+.4f} {s}' for c, s in zip(xi, names) if c != 0))
rows = np.random.default_rng(0).choice(len(ut), len(ut) // 100, replace=False)   # 1% of the data
xi1 = stridge(Theta[rows], ut[rows])
print('with 1% of the rows:', ' '.join(f'{c:+.4f} {s}' for c, s in zip(xi1, names) if c != 0))
