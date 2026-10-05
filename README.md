# Data-Driven Dynamical Systems — lecture notes

Personal LaTeX study notes of Steve Brunton's YouTube playlist
[Dynamical Systems (with Machine Learning)](https://www.youtube.com/playlist?list=PLMrJAkhIeNNR6DzT17-MM1GHLkuYVjhyt)
(24 videos, one by Nathan Kutz), companion to Brunton & Kutz, *Data-Driven Science and Engineering*
(Ch. 7; free chapters at http://databookuw.com). Same layout and conventions as the Mehrling and
MIT 18.642 notes: wide screen page, right column for notes/answers/history, `\ts` links to the video
at the second where each point is said. The Matlab demos are rewritten in Python.

## Layout
```
materials/
  playlist.json              yt-dlp --flat-playlist -J <playlist>
  transcripts/raw/*.json3    YouTube auto-captions (en-orig), one per video
  transcripts/CXX-VYY.txt    chapter XX, video YY: clean text, one line per ~20 s with m:ss
  videos.csv                 playlist index -> chapter, video, id, duration
  databook.pdf               the book (local only, gitignored)
tools/transcripts.py         builds videos.csv, CXX-VYY.txt and lecture-notes/videos.tex
lecture-notes/               main.tex, preamble.tex, chapters/, .vscode/ (fast build)
```

## Chapters (by topic; sections = videos)
1. Overview and anatomy (videos 1–2) · 2. Fundamentals: fixed points … chaos (video 24) ·
3. Simulation: Lorenz, discrete time, logistic map (3–5) · 4. DMD (6–9) · 5. SINDy, PDE-FIND (10–11) ·
6. Koopman spectral analysis (12–16) · 7. Koopman observable subspaces and control (17, 19, 20) ·
8. HAVOK (18, 21–23)

## Build
```
cd lecture-notes
python .vscode/build.py full      # whole book -> build/main.pdf and build/book.pdf
```
In VS Code (LaTeX Workshop) saving a chapter rebuilds only that chapter.

## Refresh the materials
```
python -m yt_dlp --flat-playlist -J "<playlist url>" > materials/playlist.json
python -m yt_dlp --skip-download --write-auto-subs --sub-langs en-orig --sub-format json3 \
  -o "materials/transcripts/raw/%(playlist_index)03d-%(id)s.%(ext)s" "<playlist url>"
python tools/transcripts.py
```
