# Instructions for Claude — Brunton data-driven dynamical systems notes

Talk to Alessio in Italian; the notes, code and docs are in English.
Global preferences (`~/.claude/rules/alessio-preferences.md`, section "Lecture notes") apply in full:
fixed box colours, screen layout with right column, notes/answers/requests system, history boxes,
"New concepts" definition boxes, etymology of new terms, enumerations one item per line, exercises
without solutions, `mysolution` never edited (comments go in `\feedback`); standalone exercises (self-contained, practising one section) go in the text right after that section, as early as possible; exercises forming a connected series with a global sense (consecutive problems referring to each other, e.g. "the matrix of the previous exercise") stay together at the end of the chapter in their original order, together with integrative ones needing the whole chapter (2026-10-06, refined 2026-10-07).
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
- Keep the pace (2026-10-15): a repetition of earlier material goes in a right-column `recall` box (cyan) with a
  `\cref` to the original; long exercises (> ~15-20 min, open projects, substantial programming) go verbatim to
  `appendices/appA-exam.tex` ("Pseudo-exam and second reading"), with a short core in the text; nothing is
  deleted (passages taken out of the text go to a `\section*{Set aside}` at the chapter end).
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
`cd lecture-notes && python build.py` (full build, latexmk, refreshes `build/book.pdf`; the VS Code per-chapter build was archived in `lecture-notes/archive/vscode/`, 2026-11-05). Page is 16:9 (32x18 cm): check figures/tables taller than ~14.5 cm and right-column boxes running off the page. Then grep `build/main.log` for
`\.tex:[0-9]+:`, `undefined`, `Overfull`; look at the rendered pages (Read tool on `build/main.pdf`).
Commit and push after each verified chapter, on main (no branch/PR).

## Roadmap, idee e progressi

`ROADMAP.md` nella root è l'**unico** file per todo, idee, decisioni e diario del progetto
(niente `FUTURE-ARCHITECTURE.md`, `IDEE.md`, `TODO.md`). È letto da https://alessiomartini.github.io/projects-overview/.
Sezioni: `## <fase>` (checkbox, contano nella percentuale), `## Idee` (checkbox, non contano),
`## Decisioni e cose provate` (prosa: scartato/rimandato e perché, provato e annullato, limiti e bug noti), `## Log`.

- Alla fine di ogni sessione di lavoro (prima del commit finale), aggiorna `ROADMAP.md`:
  - spunta (`- [x]`) i punti completati in questa sessione;
  - aggiungi come `- [ ]` i nuovi compiti nella fase giusta, e le idee non decise in `## Idee`;
  - annota in `## Decisioni e cose provate` ciò che è stato scartato, rimandato o annullato, col perché;
  - aggiungi in cima a `## Log` una riga `- AAAA-MM-GG: <cosa è stato fatto, in una frase>`
    (se esiste già una riga con la data di oggi, estendila invece di crearne un'altra).
- Non riscrivere né riordinare le voci esistenti senza motivo; non cancellare le voci completate.
- Se `ROADMAP.md` non esiste, crealo da `templates/ROADMAP.md` di projects-overview.
- Includi l'aggiornamento di `ROADMAP.md` nello stesso commit del lavoro.

## Scroll book (2026-11-05)

`build/book.pdf` is a **continuous-scroll** book: one long page per chapter (no page breaks inside a chapter), bookmarks per chapter; chapter PDFs are in `lecture-notes/build/scroll/`. `python build.py` recompiles only the chapters whose .tex changed and reassembles (a few seconds to a minute); `python build.py ch05` forces a chapter; `python build.py all` = full latexmk build + all chapters; `python build.py pages` = old paged book (`build/book-pages.pdf`, use it to check Overfull boxes). Mechanism: `scroll.py` + `\ifdefined\scrollmode` in `preamble.tex` (100 cm tall header-free pages, cut to the inked part and stacked; PDF viewers stop around 508 cm, longer chapters are split). Links between chapters are not kept.
