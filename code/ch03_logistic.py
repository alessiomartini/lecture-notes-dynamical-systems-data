import numpy as np
import matplotlib.pyplot as plt

betas, xs = [], []
for beta in np.arange(0, 4, 0.001):          # beta < 4: x stays in [0, 1]
    x = 0.5
    for _ in range(2000):              # transient: let x settle on the attractor
        x = (x - x**2) * beta            # x_{k+1} = beta x_k (1 - x_k)
    xss = x
    for _ in range(1000):              # store the steady state
        x = (x - x**2) * beta
        betas.append(beta); xs.append(x)
        if abs(x - xss) < 1e-3:        # back to the start: periodic, stop early
            break
print(len(xs), 'points')

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
for a, lim in zip(ax, [(0, 4), (3, 4)]):
    a.plot(betas, xs, ',', color='#1565C0', alpha=0.5)
    a.set_xlim(lim); a.set_xlabel(r'$\beta$'); a.set_ylabel(r'$x$')
plt.tight_layout()
plt.savefig('lecture-notes/figures/ch03-logistic.png', dpi=200)
