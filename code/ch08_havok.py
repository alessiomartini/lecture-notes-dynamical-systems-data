import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import lsim
import matplotlib.pyplot as plt

def lorenz(t, x, s=10, r=28, b=8/3):
    return [s * (x[1] - x[0]), x[0] * (r - x[2]) - x[1], x[0] * x[1] - b * x[2]]

dt = 0.001
t = np.arange(0, 200, dt)
x = solve_ivp(lorenz, (0, 200), [-8, 8, 27], t_eval=t, method='DOP853', rtol=1e-12, atol=1e-12).y[0]

# Hankel matrix of the single measurement x(t): q delayed copies as rows
q, r = 100, 15
H = np.array([x[i:len(x) - q + i + 1] for i in range(q)])          # q x (m - q + 1)
U, S, Vh = np.linalg.svd(H, full_matrices=False)
V = Vh[:r].T                                                       # eigen time-delay coordinates v1..vr
print('first singular values / s1:', (S[:r + 2] / S[0]).round(5))

# regression dv/dt = Xi v; the first r-1 rows are the linear model, v_r is the forcing
dV = (V[2:] - V[:-2]) / (2 * dt)                                   # central differences
Vc = V[1:-1]
Xi = np.linalg.lstsq(Vc, dV, rcond=None)[0].T                      # r x r
A, B = Xi[:r - 1, :r - 1], Xi[:r - 1, r - 1:]
res = lambda k: np.linalg.norm(dV[:, k] - Vc @ Xi[k]) / np.linalg.norm(dV[:, k])
print('relative fit residual: rows 1..r-1 max =', max(res(k) for k in range(r - 1)).round(4),
      ' row r =', res(r - 1).round(4))
print('A super-diagonal:', np.diag(A, 1)[:8].round(2))             # ~ multiples of 5 (antisymmetric)

# simulate the forced linear model with the measured forcing v_r
n = 50000                                                          # first 50 time units
tt = np.arange(n) * dt
_, Y, _ = lsim((A, B, np.eye(r - 1), 0 * B), V[:n, r - 1], tt, X0=V[0, :r - 1])
print('v1 model vs data, correlation:', np.corrcoef(Y[:, 0], V[:n, 0])[0, 1].round(4))

# forcing active (v_r^2 above a threshold) vs lobe switching (sign changes of x)
active = V[:, r - 1]**2 > 2e-5
fig, ax = plt.subplots(3, 1, figsize=(8, 5), sharex=True)
ax[0].plot(tt, V[:n, 0], 'k', lw=0.8, label='data'); ax[0].plot(tt, Y[:, 0], '--', color='#1565C0', lw=0.8, label='model')
ax[0].set_ylabel('$v_1$'); ax[0].legend(loc='upper right', fontsize=7)
ax[1].plot(tt, V[:n, r - 1], color='#D32F2F', lw=0.6); ax[1].set_ylabel('$v_r$ (forcing)')
ax[2].plot(tt, x[:n], 'k', lw=0.6)
ax[2].plot(tt[active[:n]], x[:n][active[:n]], '.', color='#D32F2F', ms=1)
ax[2].set_ylabel('$x$'); ax[2].set_xlabel('$t$')
plt.tight_layout(); plt.savefig('lecture-notes/figures/ch08-havok.png', dpi=200)

plt.figure(figsize=(3.2, 3)); m = abs(Xi).max()
plt.imshow(Xi[:r - 1], cmap='RdBu_r', vmin=-m, vmax=m); plt.title('[A | B]', fontsize=9)
plt.xticks([]); plt.yticks([]); plt.tight_layout()
plt.savefig('lecture-notes/figures/ch08-havok-A.png', dpi=200)
