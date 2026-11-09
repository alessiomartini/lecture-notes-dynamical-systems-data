# Instructions for Claude — Brunton data-driven dynamical systems notes

@~/.claude/templates/lecture-notes/RULES.md
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

## LaTeX conventions (preamble.tex)
- Long exercises go verbatim to `appendices/appA-exam.tex` ("Pseudo-exam and second reading"), with a short core in the text; passages taken out of the text go to a `\section*{Set aside}` at the chapter end.
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
`cd lecture-notes && python build.py` (full build, latexmk, refreshes `build/book.pdf`; the VS Code per-chapter build was archived in `lecture-notes/archive/vscode/`, 2026-11-05). Page is 31.5×18 cm: check figures/tables taller than ~15 cm and right-column boxes running off the page. Then grep `build/main.log` for
`\.tex:[0-9]+:`, `undefined`, `Overfull`; look at the rendered pages (Read tool on `build/main.pdf`).

## Scroll book

`build/book.pdf` is the continuous-scroll book; chapter PDFs are in `lecture-notes/build/scroll/`. `python build.py` recompiles only the chapters whose .tex changed and reassembles; `python build.py ch05` forces a chapter; `python build.py all` = full latexmk build + all chapters; `python build.py pages` = paged book (`build/book-pages.pdf`, use it to check Overfull boxes). Longer chapters are split into several PDF pages. Links between chapters are not kept.
