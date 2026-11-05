# Roadmap

<!--
Unico file per todo, idee, decisioni e diario, letto da Projects Overview
(https://alessiomartini.github.io/projects-overview/). Protocollo: templates/ROADMAP.md di projects-overview.
-->

## Da fare
- [x] Trascrizioni dei 24 video
- [x] Tutti gli 8 capitoli scritti e controllati
- [x] Ritmo: box RECALL e appendice pseudo-esame per gli esercizi lunghi
- [ ] Leggere le mie annotazioni `\note{}`

## Idee

- [ ] Figure dalle demo Python e appendice video → capitolo

- [ ] Figures from the Python demos (Lorenz attractor, logistic bifurcation diagram, DMD modes of the
  cylinder wake): generate with matplotlib into `lecture-notes/figures/` or redo in pgfplots.
- [ ] The cylinder-wake data used in the DMD videos is on databookuw.com (`CYLINDER_ALL.mat`): could be
  downloaded to run the DMD demo on the real data.
- [ ] Appendix: map video -> chapter -> book section (generate from `materials/videos.csv`).

## Decisioni e cose provate

### Status (6 Oct 2026)

- Setup done: transcripts of all 24 videos, book downloaded, skeleton from the Mehrling repo.
- All 8 chapters written and checked (scripts in code/, figures in lecture-notes/figures/). Next: read Alessio's `\note{}` annotations; possible appendix (video -> chapter -> book map).
- GitHub: private repo alessiomartini/lecture-notes-dynamical-systems-data.

### Tried and changed

- yt-dlp also writes `en` captions; they are identical to `en-orig` (auto) except for video 2, so
  only `en-orig` is kept.
- Bash heredocs collapse `\\` to `\`: LaTeX edits go through the Edit/Write tools.

## Log
- 2026-11-05: layout 16:9 (32x18 cm, PC screen), VS Code setup archived in `lecture-notes/archive/vscode/`, single build `python build.py`. Annotations read with `pdf-annotations.py` before the rebuild: none open in the current PDFs (the 4 of 2026-10-29 on Dynamical Systems were already answered on 2026-11-02). Checked the full build: no content running off the page; four tall history boxes (right column) fixed with `\Needspace`/page break.
- 2026-11-02: nuovo flusso: annotazioni sul PDF in Dropbox. Risposte alle 3 annotazioni di p.14-15 (Hartman-Grobman, slot friction della Jacobiana, autovettori più lunghi nella figura 2.1)
- 2026-10-18: FUTURE-ARCHITECTURE.md unito in ROADMAP.md (protocollo unico)
- 2026-10-16: box RECALL nel preambolo; 3 esercizi lunghi (progetto, Feigenbaum, mappa logistica parametrizzata) spostati nell'appendice pseudo-esame
- 2026-10-15: creata la roadmap per Projects Overview
