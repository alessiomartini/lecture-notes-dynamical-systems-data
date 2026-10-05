# Future work, half-done work, things tried

## Status (6 Oct 2026)
- Setup done: transcripts of all 24 videos, book downloaded, skeleton from the Mehrling repo.
- Chapter 1 (videos 1–2) written and checked; chapters 2–8 to do, in order. Their `\include`
  lines (and the `\part`s II, III) are commented out in `main.tex` until they exist.
- No GitHub remote yet (to create: private `alessiomartini/lecture-notes-dynamical-systems-data`).

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
