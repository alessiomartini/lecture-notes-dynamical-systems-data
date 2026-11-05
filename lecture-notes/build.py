"""Full build of the whole book: latexmk -> build/main.pdf, copied to build/book.pdf (what sync-pdfs.ps1 reads).

  python build.py          # run from lecture-notes/
Check overfull boxes afterwards:  grep "Overfull" build/main.log
"""
import shutil, subprocess, sys

code = subprocess.call(['latexmk', '-pdf', '-outdir=build', '-interaction=nonstopmode', '-file-line-error', 'main.tex'])
if code == 0:
    try:
        shutil.copyfile('build/main.pdf', 'build/book.pdf')  # book.pdf open in a viewer that locks it: retry
    except OSError as e:
        print(f'Could not update build/book.pdf: {e}')
sys.exit(code)
