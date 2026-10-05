import numpy as np
import matplotlib.pyplot as plt

def dmd(X, Xp, r):
    """Exact DMD (Tu et al. 2014): eigenvalues and modes of the best-fit A with Xp ~ A X."""
    U, S, Vh = np.linalg.svd(X, full_matrices=False)       # economy SVD
    U, S, V = U[:, :r], S[:r], Vh[:r].conj().T              # rank-r truncation
    Atilde = U.conj().T @ Xp @ V / S                        # r x r: U* A U
    lam, W = np.linalg.eig(Atilde)
    Phi = Xp @ V / S @ W                                    # exact DMD modes
    return lam, Phi, S

# toy "video" (after B. W. Brunton): an 80x80 square blinking fast and a Gaussian blinking slowly
n, m, dt = 80, 200, 0.05
xx, yy = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, n))
square = ((abs(xx - 0.15) < 0.3) & (abs(yy - 0.15) < 0.3)).astype(float)
gauss = np.exp(-((xx + 0.1)**2 + (yy + 0.1)**2) / 0.15)   # overlapping shapes
t = np.arange(m) * dt
w1, w2 = 2 * np.pi * 2.0, 2 * np.pi * 0.4                   # fast and slow frequencies
D = (np.outer(square.ravel(), np.exp(1j * w1 * t))
     + np.outer(gauss.ravel(), np.exp(1j * w2 * t)))         # 6400 x 200 snapshots
D = D + 0.3 * np.random.default_rng(1).standard_normal(D.shape)   # noise

X, Xp = D[:, :-1], D[:, 1:]                                 # the two shifted matrices
lam, Phi, S = dmd(X, Xp, r=2)
omega = np.log(lam) / dt                                    # continuous-time eigenvalues
print('DMD frequencies (Hz):', np.sort(omega.imag / (2 * np.pi)).round(3))   # ~[0.4, 2.0]
print('growth rates      :', omega.real.round(3))                           # ~0

U, s, _ = np.linalg.svd(X, full_matrices=False)            # POD/PCA modes, for comparison
fig, ax = plt.subplots(1, 5, figsize=(12, 2.6))
ax[0].semilogy(s[:10], 'o-')                                # rank 2 + noise floor
ax[0].set_title('singular values')
for k in range(2):
    ax[1 + k].imshow(U[:, k].real.reshape(n, n), cmap='RdBu'); ax[1 + k].set_title(f'POD mode {k+1}')
    ax[3 + k].imshow(abs(Phi[:, k]).reshape(n, n), cmap='viridis')
    ax[3 + k].set_title(f'DMD mode, {omega[k].imag / (2*np.pi):.2f} Hz')
for a in ax[1:]:
    a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig('lecture-notes/figures/ch04-dmd-toy.png', dpi=200)
