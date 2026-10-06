# Instructions for Claude — Brunton data-driven dynamical systems notes

Talk to Alessio in Italian; the notes, code and docs are in English.
Global preferences (`~/.claude/rules/alessio-preferences.md`, section "Lecture notes") apply in full:
fixed box colours, screen layout with right column, notes/answers/requests system, history boxes,
"New concepts" definition boxes, etymology of new terms, enumerations one item per line, exercises
without solutions, `mysolution` never edited (comments go in `\feedback`); short exercises (practising one section) go right after that section in the text; only integrative exercises needing the whole chapter stay in the final "Exercises" section (2026-10-06).
The setup is copied from `../lecture-notes-economics-of-money-and-banking-Perry-Mehrling` (same
preamble machinery, `build.py`, `tools/transcripts.py`): when in doubt, do as that repo does.

## Sources and how to use them
- Chapters are by topic; each section is one video. Map in `tools/transcripts.py` (`CHAPTERS`) and
  `materials/videos.csv`. Chapter 2 is the last video of the playlist (fundamentals), moved forward.
- Read `materials/transcripts/CXX-VYY.txt` (auto-captions, no punctuation): paraphrase in clean
  English, fix mis-hearings ("Brenton" -> Brunton, "Lorentz" -> Lorenz, "kootman"/"coopman" ->
  Koopman, "havoc" -> HAVOK, "Navy or Stokes" -> Navier–Stokes). Never drop content of a video.
  When two videos repeat each other (V1.1/V1.2, HAVOK FULL/SHORT), merge and tag both.
- Every point gets `\ts{C}{V}{m:ss}` with the time of the transcript line where it is said;
  `\seg{C}{V}{text}` links a whole video (Sources box).
- Check notation and facts against the book: `materials/databook.pdf` (gitignored; text dump with
  `pdftotext -layout materials/databook.pdf materials/databook.txt`, also gitignored). Chapter 7
  = DMD, SINDy, Koopman; Ch. 3 = compressed sensing/sparse regression; Ch. 1 = SVD.
- History boxes: fact-checked, with a References line.

## LaTeX conventions (preamble.tex)
- Boxes: `intuition`, `application` (orange), `casestudy`, `reading` (book sections), `keyformulas`,
  `secondary`, `history`, `aside`, `coursenote`, `example` (right column), `code` (Python listing,
  text column only).
- Python code: rewrite the Matlab demos with numpy/scipy/matplotlib; run every listing in the
  scratchpad before putting it in the notes.
- Use `nfigure` (non-floating) instead of `figure`. `\vb x` = bold vector.
- `\flushside` before a `\section*` if a right-column item is still queued.
- When writing LaTeX through the shell, backslashes get mangled (heredocs collapse `\\`): use the
  Edit/Write tools.

## Build and check
`cd lecture-notes && python .vscode/build.py full`, then grep `build/main.log` for
`\.tex:[0-9]+:`, `undefined`, `Overfull`; look at the rendered pages (Read tool on `build/main.pdf`).
Commit and push after each verified chapter, on main (no branch/PR).
