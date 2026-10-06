import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import solve_continuous_are, expm

mu, lam = -0.1, 1.0                         # x2 direction unstable: control is needed
B = np.array([[0.0], [1.0]])                 # u acts on x2

def f(t, x, gain):                           # x1' = mu x1, x2' = lam (x2 - x1^2) + u
    u = -gain(x)
    return [mu * x[0], lam * (x[1] - x[0]**2) + u, x[0]**2 + x[1]**2 + u**2]   # 3rd: running cost

def lqr(A, B, Q, R):
    P = solve_continuous_are(A, B, Q, R)
    return np.linalg.solve(R, B.T @ P)       # u = -C x

R = np.array([[1.0]])
# (1) LQR on the linearization at the origin: A = df/dx(0)
C1 = lqr(np.array([[mu, 0], [0, lam]]), B, np.eye(2), R)
# (2) LQR on the Koopman linear system y = (x1, x2, x1^2), same cost (no weight on y3)
K = np.array([[mu, 0, 0], [0, lam, -lam], [0, 0, 2 * mu]])
C2 = lqr(K, np.vstack([B, [[0.0]]]), np.diag([1.0, 1.0, 0.0]), R)
print('linearized LQR gains:', C1.round(3), '\nKoopman LQR gains   :', C2.round(3))

x0 = [-5.0, 5.0, 0.0]                        # large initial condition, as in the paper
for name, gain in [('linearized', lambda x: (C1 @ x[:2]).item()),
                   ('Koopman   ', lambda x: (C2 @ [x[0], x[1], x[0]**2]).item())]:
    s = solve_ivp(f, (0, 50), x0, args=(gain,), rtol=1e-10, atol=1e-10)
    print(f'{name} total cost J = {s.y[2, -1]:.1f}')

# truncated Koopman models of x' = x^2 in the basis x, x^2, ..., x^N: y_k' = k y_{k+1}
x0, t = 0.5, np.linspace(0, 1.8, 10)          # blow-up at t = 1/x0 = 2
for N in (1, 2, 4, 8, 16):
    Kn = np.diag(np.arange(1, N), 1).astype(float)
    print(f'N={N:2d}: x(1.8) =', (expm(Kn * 1.8) @ x0 ** np.arange(1, N + 1))[0].round(3))
print('exact : x(1.8) =', round(x0 / (1 - x0 * 1.8), 3))
