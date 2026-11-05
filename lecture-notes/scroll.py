r"""Continuous-scroll build of the book: one long PDF page per chapter (no page breaks inside a chapter).

  python scroll.py            # recompile the chapters whose .tex changed (or all if never built), reassemble
  python scroll.py ch05 ch07  # recompile just these (substring of the file name), reassemble
  python scroll.py all        # recompile every chapter, reassemble
  python scroll.py assemble   # only reassemble build/scroll/*.pdf into build/book.pdf

Each chapter is typeset with `\includeonly` in "scroll mode" (preamble: 100 cm tall pages, no header), reading the
cross-reference aux files of the last full build (python build.py pages), then every page is cut to its inked part and
the pages are stacked into long pages (<= 480 cm: PDF viewers stop around 508 cm). The chapter PDFs live in
build/scroll/, build/book.pdf is their concatenation with bookmarks. Links between chapters are not kept.
Needs: pdflatex, pypdf, pypdfium2, Pillow.
"""
import os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

B = 'build'
S = os.path.join(B, 'scroll')


def includes():
    """[(path-without-.tex, title)] in main.tex order (ignores commented lines)."""
    out = []
    for line in open('main.tex', encoding='utf-8', errors='ignore'):
        m = re.match(r'\s*\\include\{([^}]+)\}', line)
        if m:
            p = m.group(1)
            t = ''
            try:
                src = open(p + '.tex', encoding='utf-8', errors='ignore').read()
                c = re.search(r'\\(?:chapter|section)\*?\{([^}]*)\}', src)
                t = c.group(1) if c else ''
            except OSError:
                pass
            out.append((p, t or os.path.basename(p)))
    return out


def stem(p):
    return os.path.basename(p)


def compile_chapter(p):
    d = os.path.join(S, 'tmp-' + stem(p))
    shutil.rmtree(d, ignore_errors=True)
    for sub in ('', 'chapters', 'appendices'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    for root, _, fs in os.walk(B):
        if root.startswith(S):
            continue
        for f in fs:
            if f.endswith(('.aux', '.toc', '.out', '.lof', '.lot', '.bbl', '.idx', '.ind')):
                dst = os.path.join(d, os.path.relpath(os.path.join(root, f), B))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(root, f), dst)
    cmd = ['pdflatex', '-interaction=nonstopmode', '-file-line-error', f'-output-directory={d}', '-jobname=main',
           r'\def\scrollmode{}\includeonly{' + p + r'}\input{main}']
    for _ in range(2):   # the right-column alignment needs two runs
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = os.path.join(d, 'main.pdf')
    if not os.path.exists(pdf):
        print('FAILED', p, '(see', os.path.join(d, 'main.log') + ')')
        return None
    rng = os.path.join(d, 'main.scrollpages')
    first, last = 1, None
    if os.path.exists(rng):
        nums = [int(x) for x in open(rng).read().split()]
        if nums and not p.endswith('ch00-requests'):
            first = nums[0]   # the chapter is the last thing typeset: its pages run to the end of the PDF
    out = os.path.join(S, stem(p) + '.pdf')
    n = stitch(pdf, out, first, last)
    print(f'{stem(p)}: {n} long page(s)')
    shutil.rmtree(d, ignore_errors=True)
    return out


def stitch(inp, out, first=1, last=None, maxcm=480, gap=3.0, pad=12.0):
    import pypdfium2 as pdfium
    from PIL import ImageOps
    from pypdf import PdfReader, PdfWriter, PageObject, Transformation
    doc, rd, w = pdfium.PdfDocument(inp), PdfReader(inp), PdfWriter()
    last = last or len(doc)
    items = []
    for i in range(first - 1, min(last, len(doc))):
        pg = doc[i]
        bb = ImageOps.invert(pg.render(scale=1).to_pil().convert('L')).point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb:
            H = pg.get_size()[1]
            items.append((i, H - bb[3] - 1.0, H - bb[1] + 1.0))
    W = float(rd.pages[0].mediabox.width)
    chunks, cur, h = [], [], 0.0
    for it in items:
        if cur and h + (it[2] - it[1]) + gap > maxcm / 2.54 * 72:
            chunks.append(cur); cur, h = [], 0.0
        cur.append(it); h += it[2] - it[1] + gap
    chunks.append(cur)
    for ch in chunks:
        T = sum(hi - lo + gap for _, lo, hi in ch) + 2 * pad
        pg = PageObject.create_blank_page(width=W, height=T)
        y = T - pad
        for i, lo, hi in ch:
            src = rd.pages[i]
            if '/Annots' in src:
                del src['/Annots']
            pg.merge_transformed_page(src, Transformation().translate(0, y - hi))
            y -= hi - lo + gap
        w.add_page(pg)
    w.write(out)
    return len(chunks)


def assemble():
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for p, title in includes():
        f = os.path.join(S, stem(p) + '.pdf')
        if not os.path.exists(f):
            continue
        first = len(w.pages)
        for pg in PdfReader(f).pages:
            w.add_page(pg)
        w.add_outline_item(title, first)
    w.add_metadata({'/Title': os.path.basename(os.getcwd())})
    out = os.path.join(B, 'book.pdf')
    try:
        w.write(out)
        print('->', out, len(w.pages), 'long pages')
    except OSError as e:
        print('could not write', out, e)


if __name__ == '__main__':
    os.makedirs(S, exist_ok=True)
    args = sys.argv[1:]
    inc = [p for p, _ in includes()]
    if args == ['assemble']:
        todo = []
    elif args == ['all']:
        todo = inc
    elif args:
        todo = [p for p in inc if any(a in p for a in args)]
    else:
        todo = [p for p in inc if not os.path.exists(os.path.join(S, stem(p) + '.pdf'))
                or os.path.getmtime(p + '.tex') > os.path.getmtime(os.path.join(S, stem(p) + '.pdf'))
                or os.path.getmtime('preamble.tex') > os.path.getmtime(os.path.join(S, stem(p) + '.pdf'))]
    if not os.path.exists(os.path.join(B, 'main.aux')):
        sys.exit('no build/main.aux: run "python build.py pages" (full latexmk build) once first')
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(compile_chapter, todo))
    assemble()
