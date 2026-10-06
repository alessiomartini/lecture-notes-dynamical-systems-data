# Future work, half-done work, things tried

## Status (6 Oct 2026)
- Setup done: transcripts of all 24 videos, book downloaded, skeleton from the Mehrling repo.
- Chapters 1–5 written and checked (scripts in code/, figures in lecture-notes/figures/); chapters 6–8 (Koopman, Koopman control, HAVOK) to do.
- GitHub: private repo alessiomartini/lecture-notes-dynamical-systems-data.

## Ideas
- Figures from the Python demos (Lorenz attractor, logistic bifurcation diagram, DMD modes of the
  cylinder wake): generate with matplotlib into `lecture-notes/figures/` or redo in pgfplots.
- The cylinder-wake data used in the DMD videos is on databookuw.com (`CYLINDER_ALL.mat`): could be
  downloaded to run the DMD demo on the real data.
- Appendix: map video -> chapter -> book section (generate from `materials/videos.csv`).

## Tried and changed
- yt-dlp also writes `en` captions; they are identical to `en-orig` (auto) except for video 2, so
  only `en-orig` is kept.
- Bash heredocs collapse `\\` to `\`: LaTeX edits go through the Edit/Write tools.
