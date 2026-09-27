#!/usr/bin/env python3
"""Combine a folder of exported GPT instructions into one my-gpts.md for triage.

  py gpts-to-md.py "C:\\Users\\you\\Desktop\\My GPTs"          -> writes my-gpts.md next to that folder
  py gpts-to-md.py "Loan Coach.docx" "Notes Cleaner.docx"     -> just those files; my-gpts.md next to the first one
  py gpts-to-md.py "<folder or files>" -o "<file.md>"          -> writes where you say

Reads .docx, .md and .txt; one "## <file name>" section per file, so name each file after its GPT.
Runs entirely on your computer; nothing is uploaded. Python 3, nothing to install.

Written for Maryland and points at Neoserra — check anything that touches your own CRM, programs, or reporting
rules before you lean on it. MIT and unsupported — fork it, change it, don't wait on me.
"""
import argparse, os, sys, zipfile
import xml.etree.ElementTree as ET
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def docx_text(path):
    """One line per Word paragraph, in document order (table cells included)."""
    root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
    lines = []
    for p in root.iter(W + 'p'):
        bits = []
        for el in p.iter():
            if el.tag == W + 't': bits.append(el.text or '')
            elif el.tag == W + 'tab': bits.append('\t')
            elif el.tag in (W + 'br', W + 'cr'): bits.append('\n')
        lines.append(''.join(bits))
    return '\n'.join(lines)

def main():
    ap = argparse.ArgumentParser(description='Combine exported GPT instructions into one my-gpts.md.')
    ap.add_argument('paths', nargs='+', help='a folder holding one .docx / .md / .txt file per GPT, or the files themselves')
    ap.add_argument('-o', '--out', help='output file (default: my-gpts.md next to the folder, or next to the first file)')
    a = ap.parse_args()
    if len(a.paths) == 1 and os.path.isdir(a.paths[0]):
        folder = os.path.abspath(a.paths[0])
        files = [os.path.join(folder, n) for n in sorted(os.listdir(folder), key=str.lower)]
        label, default_out = os.path.basename(folder), os.path.join(os.path.dirname(folder), 'my-gpts.md')
    else:
        files = [os.path.abspath(p) for p in a.paths]
        label, default_out = '%d files' % len(files), os.path.join(os.path.dirname(files[0]), 'my-gpts.md')
    out = a.out or default_out
    sections, skipped, seen = [], [], {}
    for path in files:
        name = os.path.basename(path); stem, ext = os.path.splitext(name); ext = ext.lower()
        if name.startswith('~$') or ext == '.py' or not os.path.isfile(path): continue   # Word's lock files; the kit's own scripts
        try:
            if ext == '.docx': text = docx_text(path)
            elif ext in ('.md', '.txt'): text = open(path, encoding='utf-8-sig', errors='replace').read()
            else:
                skipped.append(name + (' (old Word format: open it and Save As .docx)' if ext == '.doc' else ' (not .docx, .md or .txt)'))
                continue
        except (zipfile.BadZipFile, KeyError, ET.ParseError):
            skipped.append(name + " (couldn't read it: open it and Save As .docx)"); continue
        text = text.strip()
        if not text: skipped.append(name + ' (empty)'); continue
        seen[stem] = seen.get(stem, 0) + 1
        if seen[stem] > 1: stem = '%s (%d)' % (stem, seen[stem])
        sections.append('## %s\n\n%s\n' % (stem, text))
    head = ('# My GPTs\n\nCombined from %s. One section per file; the file name is the GPT name. '
            'Add Description, Conversation starters, Knowledge file names and Capabilities under a heading '
            'if you have them; triage works on the instructions alone.\n\n' % label)
    with open(out, 'w', encoding='utf-8', newline='\n') as fh: fh.write(head + '\n'.join(sections))
    print('wrote %d GPTs -> %s' % (len(sections), out))
    for s in skipped: print('  skipped:', s)

if __name__ == '__main__':
    main()
