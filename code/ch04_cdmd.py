import numpy as np
from ch04_dmd import dmd, D, n            # same toy data (6400 pixels x 200 snapshots)

X, Xp = D[:, :-1], D[:, 1:]
lam_x, Phi_x, _ = dmd(X, Xp, r=2)         # DMD on the full data (reference)

rng = np.random.default_rng(2)
for p in [20, 100, 400]:                    # number of random pixels measured
    C = np.zeros((p, n * n)); C[np.arange(p), rng.choice(n * n, p, replace=False)] = 1
    Y, Yp = C @ X, C @ Xp                 # compressed data: p x (m-1)
    U, S, Vh = np.linalg.svd(Y, full_matrices=False)
    U, S, V = U[:, :2], S[:2], Vh[:2].conj().T
    lam_y, W = np.linalg.eig(U.conj().T @ Yp @ V / S)
    Phi = Xp @ V / S @ W                  # compressed DMD: modes from the full X'
    # compare with the reference (sort by frequency, normalise, remove the phase)
    ix, iy = np.argsort(np.angle(lam_x)), np.argsort(np.angle(lam_y))
    err = []
    for a, b in zip(Phi_x[:, ix].T, Phi[:, iy].T):
        a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
        err.append(np.linalg.norm(a - b * np.vdot(b, a) / abs(np.vdot(b, a))))
    print(f'p={p:3d}  |eig error|={np.abs(lam_x[ix] - lam_y[iy]).max():.1e}  mode errors={np.round(err, 3)}')
