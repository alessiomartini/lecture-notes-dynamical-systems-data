import numpy as np
from scipy.linalg import expm

A = np.array([[0.0, 1.0], [-1.0, 0.0]])     # harmonic oscillator, flow map exp(A t)
f = lambda x: A @ x
x0 = np.array([1.0, 0.0]); T = 2 * np.pi

def euler(x, dt):
    return x + dt * f(x)

def rk4(x, dt):
    k1 = f(x); k2 = f(x + dt / 2 * k1); k3 = f(x + dt / 2 * k2); k4 = f(x + dt * k3)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

exact = expm(A * T) @ x0                    # true flow map F_T
for dt in [0.1, 0.01, 0.001]:
    n = round(T / dt); dt = T / n             # land exactly on T
    for step in (euler, rk4):
        x = x0.copy()
        for _ in range(n):
            x = step(x, dt)
        print(f'dt={dt:.4f} {step.__name__:5} error={np.linalg.norm(x - exact):.1e}')
