# Roadmap

<!-- Single file for todo, ideas, decisions and log, read by Projects Overview (https://alessiomartini.github.io/projects-overview/). Protocol: templates/ROADMAP.md in projects-overview. -->

## To do
- [x] Transcripts of the 24 videos
- [x] All 8 chapters written and checked
- [x] Pace: RECALL box and pseudo-exam appendix for long exercises
- [x] Read my `\note{}` annotations: there are no unread `\note{` in the chapters (only the explanation in `ch00-requests.tex`) and the Log of 2026-11-05 says the annotations were read and answered.

## Ideas

- [ ] Figures from the Python demos (Lorenz attractor, logistic bifurcation diagram, DMD modes of the
  cylinder wake): generate with matplotlib into `lecture-notes/figures/` or redo in pgfplots.
- [ ] The cylinder-wake data used in the DMD videos is on databookuw.com (`CYLINDER_ALL.mat`): could be
  downloaded to run the DMD demo on the real data.
- [ ] Appendix: map video -> chapter -> book section (generate from `materials/videos.csv`).

## Decisions and things tried

### Initial status (6 Oct 2026, historical)

- Setup done: transcripts of all 24 videos, book downloaded, skeleton from the Mehrling repo.
- All 8 chapters written and checked (scripts in code/, figures in lecture-notes/figures/). Next at that date: read Alessio's `\note{}` annotations (done, see To do); possible appendix (video -> chapter -> book map, see Ideas).
- GitHub: private repo alessiomartini/lecture-notes-dynamical-systems-data.

### Tried and changed

- yt-dlp also writes `en` captions; they are identical to `en-orig` (auto) except for video 2, so
  only `en-orig` is kept.
- Bash heredocs collapse `\\` to `\`: LaTeX edits go through the Edit/Write tools.

## Log
- 2026-11-21: 🤖 Docs cleanup: ROADMAP translated to English, annotations item ticked, IT/EN duplicate items merged, README page size fixed to 31.5x18 cm (matches preamble.tex), CLAUDE.md condensed.
- 2026-11-05: tight margins and 12pt: geometry 31.5x18 cm with 0.9 left, 0.4+header top, 1.5 bottom, columns 18.8 + 10 cm, page number in the one-line header (no footer). Rebuilt; content that ran below the page edge fixed (history boxes moved or `\Needspace`, `\clearpage`, `\allowdisplaybreaks`).
- 2026-11-05: layout 16:9 (32x18 cm, PC screen), VS Code setup archived in `lecture-notes/archive/vscode/`, single build `python build.py`. Annotations read with `pdf-annotations.py` before the rebuild: none open in the current PDFs (the 4 of 2026-10-29 on Dynamical Systems were already answered on 2026-11-02). Checked the full build: no content running off the page; four tall history boxes (right column) fixed with `\Needspace`/page break.
- 2026-11-02: new flow: annotations on the PDF in Dropbox. Answered the 3 annotations on p.14-15 (Hartman-Grobman, Jacobian slot friction, longer eigenvectors in figure 2.1)
- 2026-10-18: FUTURE-ARCHITECTURE.md merged into ROADMAP.md (single protocol)
- 2026-10-16: RECALL box in the preamble; 3 long exercises (project, Feigenbaum, parametrized logistic map) moved to the pseudo-exam appendix
- 2026-10-15: created the roadmap for Projects Overview
