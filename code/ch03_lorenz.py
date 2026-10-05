import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def lorenz(t, x, beta):                 # t first, like ode45 / solve_ivp expect
    sigma, rho, b = beta
    return [sigma * (x[1] - x[0]),
            x[0] * (rho - x[2]) - x[1],
            x[0] * x[1] - b * x[2]]

beta = (10, 28, 8 / 3)                  # Lorenz's chaotic parameters
x0 = [0, 1, 20]
dt = 0.001
t = np.arange(dt, 50 + dt / 2, dt)      # 50 000 samples, as in the video
sol = solve_ivp(lorenz, (0, 50), x0, args=(beta,), t_eval=t,
                method='DOP853', rtol=1e-12, atol=1e-12)
X = sol.y.T                             # rows = times, columns = x, y, z
print(X.shape)                          # (50000, 3)

# a small blob of initial conditions: sensitive dependence
x0b = np.array(x0) + 1e-3 * np.random.default_rng(0).standard_normal((200, 3))
ends = [solve_ivp(lorenz, (0, 15), p, args=(beta,), rtol=1e-10, atol=1e-10).y[:, -1]
        for p in x0b]
print('blob size: 1e-3 ->', np.ptp(np.array(ends), axis=0).round(1))

ax = plt.figure(figsize=(5, 4)).add_subplot(projection='3d')
ax.plot(*X.T, lw=0.3, color='k')
ax.scatter(*np.array(ends).T, s=4, color='#D32F2F')
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
plt.savefig('lecture-notes/figures/ch03-lorenz.png', dpi=200, bbox_inches='tight')
