import numpy as np
from itertools import combinations_with_replacement
from scipy.integrate import solve_ivp

def lorenz(t, x, s=10, r=28, b=8/3):
    return [s * (x[1] - x[0]), x[0] * (r - x[2]) - x[1], x[0] * x[1] - b * x[2]]

dt = 0.001
t = np.arange(0, 20, dt)
X = solve_ivp(lorenz, (0, 20), [-8, 8, 27], t_eval=t, rtol=1e-12, atol=1e-12).y.T
dX = np.gradient(X, dt, axis=0)                       # derivatives from the data (2nd-order FD)

def library(X, order=5, names='xyz'):
    """Theta(X): all monomials of the state up to the given order, and their names."""
    cols, labels = [np.ones(len(X))], ['1']
    for k in range(1, order + 1):
        for idx in combinations_with_replacement(range(X.shape[1]), k):
            cols.append(np.prod(X[:, idx], axis=1))
            labels.append(''.join(names[i] for i in idx))
    return np.column_stack(cols), labels

def stlsq(Theta, dX, lam=0.025, iters=10):
    """Sequentially thresholded least squares (Brunton, Proctor, Kutz 2016)."""
    Xi = np.linalg.lstsq(Theta, dX, rcond=None)[0]
    for _ in range(iters):
        small = abs(Xi) < lam                           # cut the small coefficients ...
        Xi[small] = 0
        for j in range(dX.shape[1]):                    # ... and refit on the survivors
            big = ~small[:, j]
            Xi[big, j] = np.linalg.lstsq(Theta[:, big], dX[:, j], rcond=None)[0]
    return Xi

Theta, labels = library(X)                            # 56 candidate functions
Xi = stlsq(Theta, dX)
for j, v in enumerate('xyz'):
    terms = [f'{Xi[i, j]:+.3f} {labels[i]}' for i in np.flatnonzero(Xi[:, j])]
    print(f'{v}\' =', ' '.join(terms))
print('least squares would keep', np.count_nonzero(abs(np.linalg.lstsq(Theta, dX, rcond=None)[0]) > 1e-6), 'of', Xi.size, 'terms')
