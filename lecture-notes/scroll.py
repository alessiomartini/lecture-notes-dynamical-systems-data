r"""Continuous-scroll build of the book: one long PDF page per chapter (no page breaks inside a chapter).

  python scroll.py            # recompile the chapters whose .tex changed (or all if never built), reassemble
  python scroll.py ch05 ch07  # recompile just these (substring of the file name), reassemble
  python scroll.py all        # recompile every chapter, reassemble
  python scroll.py assemble   # only reassemble build/scroll/*.pdf into build/book.pdf

Each chapter is typeset with `\includeonly` in "scroll mode" (preamble: 100 cm tall pages, no header), reading the
cross-reference aux files of the last full build (python build.py pages), then every page is cut to its inked part and
the pages are stacked into long pages (<= 480 cm: PDF viewers stop around 508 cm). The chapter PDFs live in
build/scroll/, build/book.pdf is their concatenation with bookmarks. Internal links and URLs are carried over (named destinations are merged into one name space).
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


import threading
LOCK = threading.Lock()


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
    first, last, breaks = 1, None, ()
    if os.path.exists(rng):
        nums = [int(x) for x in open(rng).read().split()]
        if nums and not p.endswith('ch00-requests'):
            first = nums[0]   # the chapter is the last thing typeset: its pages run to the end of the PDF
            breaks = tuple(nums[1:])   # page numbers where \scrollbreak started a new long page
            # The shipout counter can run ahead of the real page number (e.g. after a \part page), which would cut the
            # top of the chapter: take the first page that starts with the chapter/appendix heading instead.
            import pypdfium2 as pdfium
            doc = pdfium.PdfDocument(pdf)
            for i in range(len(doc)):
                head = doc[i].get_textpage().get_text_range()[:12].lstrip()
                if head.startswith(('Chapter', 'Appendix')):
                    delta = (i + 1) - first
                    first, breaks = i + 1, tuple(b + delta for b in breaks)
                    break
            doc.close()
    out = os.path.join(S, stem(p) + '.pdf')
    with LOCK:   # pdfium is not thread-safe: stitch one chapter at a time (pdflatex runs stay parallel)
        n = stitch(pdf, out, first, last, breaks)
    print(f'{stem(p)}: {n} long page(s)', flush=True)
    shutil.rmtree(d, ignore_errors=True)
    return out


def resolve_links(w, dest_map):
    """Turn named-destination links into explicit [page /XYZ left top null] ones: works in every viewer."""
    from pypdf.generic import ArrayObject, FloatObject, NameObject, NullObject
    for pg in w.pages:
        for ref in pg.get('/Annots') or []:
            a = ref.get_object()
            act = a.get('/A')
            if act is None or str(act.get('/S')) != '/GoTo' or not isinstance(act.get('/D'), str):
                continue
            hit = dest_map.get(str(act['/D']))
            if hit:
                k, left, top = hit
                act[NameObject('/D')] = ArrayObject([w.pages[k].indirect_reference, NameObject('/XYZ'),
                                                     FloatObject(left), FloatObject(top), NullObject()])


def stitch(inp, out, first=1, last=None, breaks=(), maxcm=480, gap=3.0, pad=12.0, meta=None, resolve=False,
           bigblank=70.0, runblank=24.0):
    """Stack the pages first..last of `inp` into long pages (<= maxcm; a new one also starts at the 1-based page
    numbers in `breaks`). Every page is cut to its inked part, and a blank band taller than `bigblank` pt inside a
    page (title page, part pages...) is shortened to `runblank` pt. Link annotations and named destinations are
    carried over (positions translated), so cross-references keep working."""
    import pypdfium2 as pdfium
    from PIL import ImageOps
    from pypdf import PdfReader, PdfWriter, PageObject, Transformation
    from pypdf.generic import (ArrayObject, DictionaryObject, FloatObject, NameObject, NumberObject, TextStringObject,
                               Destination, Fit)
    doc, rd, w = pdfium.PdfDocument(inp), PdfReader(inp), PdfWriter()
    last = last or len(doc)
    items = []   # (source page, lo, hi, first run of its page) in PDF coordinates
    for i in range(first - 1, min(last, len(doc))):
        pg = doc[i]
        ink = ImageOps.invert(pg.render(scale=1).to_pil().convert('L')).point(lambda v: 255 if v > 8 else 0)
        rows = ink.getprojection()[1]   # 1 for every pixel row that has ink
        H = pg.get_size()[1]
        runs, start, blank = [], None, 0
        for r, v in enumerate(rows):
            if v:
                if start is None:
                    start = r
                elif blank > bigblank:
                    runs.append((start, r - blank - 1)); start = r
                blank = 0
            elif start is not None:
                blank += 1
        if start is not None:
            runs.append((start, len(rows) - 1 - blank))
        for n, (a, b) in enumerate(runs):
            items.append((i, H - b - 2.0, H - a + 1.0, n == 0))
    W = float(rd.pages[0].mediabox.width)
    chunks, cur, h = [], [], 0.0
    for it in items:
        if cur and ((it[3] and (it[0] + 1) in breaks) or h + (it[2] - it[1]) + gap > maxcm / 2.54 * 72):
            chunks.append(cur); cur, h = [], 0.0
        cur.append(it); h += it[2] - it[1] + gap
    chunks.append(cur)
    placed = {}   # source page index -> [(lo, hi, long page index, vertical shift)]
    for k, ch in enumerate(chunks):
        T = sum(hi - lo + gap for _, lo, hi, _ in ch) + 2 * pad
        pg = PageObject.create_blank_page(width=W, height=T)
        y = T - pad
        links = ArrayObject()
        prev = None
        for i, lo, hi, _ in ch:
            if prev == i:
                y -= runblank - gap   # same page, a long blank band was cut out here
            src = rd.pages[i]
            ty = y - hi
            for ref in src.get('/Annots') or []:
                a = ref.get_object()
                if str(a.get('/Subtype')) != '/Link':
                    continue
                x0, y0, x1, y1 = [float(v) for v in a['/Rect']]
                if not (lo <= (y0 + y1) / 2 <= hi):
                    continue
                act = a.get('/A')
                target = a.get('/Dest') if '/Dest' in a else (act.get('/D') if act is not None and str(act.get('/S')) == '/GoTo' else None)
                uri = act.get('/URI') if act is not None and str(act.get('/S')) == '/URI' else None
                if isinstance(target, str):
                    new_a = DictionaryObject({NameObject('/S'): NameObject('/GoTo'), NameObject('/D'): TextStringObject(str(target))})
                elif uri is not None:
                    new_a = DictionaryObject({NameObject('/S'): NameObject('/URI'), NameObject('/URI'): TextStringObject(str(uri))})
                else:
                    continue
                links.append(DictionaryObject({
                    NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Link'),
                    NameObject('/Rect'): ArrayObject([FloatObject(x0), FloatObject(y0 + ty), FloatObject(x1), FloatObject(y1 + ty)]),
                    NameObject('/Border'): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]), NameObject('/A'): new_a}))
            run = PageObject.create_blank_page(width=W, height=hi - lo)   # its page box clips to this run
            run.merge_transformed_page(src, Transformation().translate(0, -lo))
            pg.merge_transformed_page(run, Transformation().translate(0, y - (hi - lo)))
            placed.setdefault(i, []).append((lo, hi, k, ty))
            y -= hi - lo + gap
            prev = i
        if len(links):
            pg[NameObject('/Annots')] = links
        w.add_page(pg)
    dest_map = {}
    for name, d in rd.named_destinations.items():
        if name.startswith('page.') or name == 'Doc-Start':
            continue
        try:
            i = rd.get_destination_page_number(d)
        except Exception:
            continue
        if i in placed:
            top0 = float(d.top) if d.top is not None else float(rd.pages[i].mediabox.height)
            runs = placed[i]
            lo, hi, k, ty = next((r for r in runs if r[0] - 20 <= top0 <= r[1] + 20), min(runs, key=lambda r: abs(r[1] - top0)))
            top, left = min(max(top0, lo), hi) + ty, (float(d.left) if d.left is not None else 0.0)
            w.add_named_destination_object(Destination(name, w.pages[k].indirect_reference, Fit.xyz(left, top, 0)))
            dest_map[name] = (k, left, top)
    if resolve:
        resolve_links(w, dest_map)
    if meta:
        w.add_metadata(meta)
    w.write(out)
    return len(chunks)


def assemble():
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import Destination, Fit
    w = PdfWriter()
    dest_map = {}
    for p, title in includes():
        f = os.path.join(S, stem(p) + '.pdf')
        if not os.path.exists(f):
            continue
        first = len(w.pages)
        rd = PdfReader(f)
        for pg in rd.pages:
            w.add_page(pg)
        for name, d in rd.named_destinations.items():   # one name space for the whole book: cross-chapter links
            try:
                i = rd.get_destination_page_number(d)
                w.add_named_destination_object(Destination(name, w.pages[first + i].indirect_reference,
                                                            Fit.xyz(float(d.left or 0), float(d.top or 0), 0)))
                dest_map[name] = (first + i, float(d.left or 0), float(d.top or 0))
            except Exception:
                pass
        w.add_outline_item(title, first)
    resolve_links(w, dest_map)
    w.add_metadata({'/Title': os.path.basename(os.getcwd())})
    out = os.path.join(B, 'book.pdf')
    try:
        w.write(out)
        print('->', out, len(w.pages), 'long pages')
    except OSError as e:
        print('could not write', out, e)


if __name__ == '__main__':
    os.makedirs(S, exist_ok=True)
    from pypdf import PdfReader
    for f in [x for x in os.listdir(S) if x.endswith('.pdf')]:   # a killed run leaves truncated PDFs: drop them
        try:
            PdfReader(os.path.join(S, f))
        except Exception:
            os.remove(os.path.join(S, f)); print('removed truncated', f)
    for d in [x for x in os.listdir(S) if x.startswith('tmp-')]:
        shutil.rmtree(os.path.join(S, d), ignore_errors=True)
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
    with ThreadPoolExecutor(max_workers=int(os.environ.get('SCROLL_WORKERS', 3))) as ex:
        list(ex.map(compile_chapter, todo))
    assemble()
