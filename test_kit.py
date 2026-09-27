"""The one runnable check for this repo:  py test_kit.py
Renders the example spec through the generator and checks the kit.json contract."""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, 'generator', 'build.py')

def build(kit, specs):
    tmp = tempfile.mkdtemp()
    src, out = os.path.join(tmp, 'src'), os.path.join(tmp, 'out')
    os.makedirs(src)
    for s in specs:
        json.dump(s, open(os.path.join(src, s['slug'] + '.json'), 'w', encoding='utf-8'))
    kp = os.path.join(tmp, 'kit.json')
    json.dump(kit, open(kp, 'w', encoding='utf-8'))
    subprocess.run([sys.executable, GEN, '--kit', kp, '--src', src, '--out', out], check=True, capture_output=True)
    return tmp, out

def read(out, name): return open(os.path.join(out, name), encoding='utf-8').read()

def test_generator():
    spec = json.load(open(os.path.join(HERE, 'generator', 'example-spec.json'), encoding='utf-8'))
    private = dict(spec, slug='private-thing', title='Private Thing', plugin={'name': 'private', 'label': 'Private'})
    kit = json.load(open(os.path.join(HERE, 'generator', 'kit.json'), encoding='utf-8'))

    # only_plugin filters out other plugins' guides
    tmp, out = build(kit, [spec, private])
    assert os.path.exists(os.path.join(out, spec['slug'] + '.html'))
    assert not os.path.exists(os.path.join(out, 'private-thing.html'))
    page, index = read(out, spec['slug'] + '.html'), read(out, 'index.html')
    for html in (page, index):
        assert '{{' not in html, 'unfilled placeholder'
        assert kit['badge'] in html and kit['maintainer'] in html
    assert 'Skill guides — Maryland SBDC' in index
    assert '/blob/main/skills/transcript-to-action-plan-client-email/SKILL.md' in page  # source_repo link
    shutil.rmtree(tmp)

    # another center, no filter, no source repo: its own names, both guides, fallback text
    hi = dict(kit, center='Hawaii SBDC', maintainer='Joe Burnes', badge='Hawaii SBDC',
              only_plugin=None, source_repo=None, chatgpt_fallback='ask Joe.')
    hi['for'] = 'Hawaii SBDC advisors'   # 'for' is a Python keyword, so it can't be a dict() kwarg
    tmp, out = build(hi, [spec, private])
    page, index = read(out, spec['slug'] + '.html'), read(out, 'index.html')
    assert os.path.exists(os.path.join(out, 'private-thing.html'))
    assert 'Hawaii SBDC advisors' in page and 'Joe Burnes' in page and 'ask Joe.' in page
    assert 'Skill guides — Hawaii SBDC' in index and 'Maryland SBDC toolkit' not in index
    shutil.rmtree(tmp)

    # a kit with no files_step and its own lead-in; a spec with its own ChatGPT row
    own = dict(spec, chatgpt_note='paste it into a new Project.')
    k2 = dict(kit, files_step='', setup_lead='On ChatGPT, do row 1.')
    tmp, out = build(k2, [own])
    page = read(out, spec['slug'] + '.html')
    assert 'On ChatGPT, do row 1.' in page and 'paste it into a new Project.' in page
    assert kit['files_step'] not in page and 'Pick your row' not in page
    shutil.rmtree(tmp)

    # a kit with doors renders them on the index (and drops files_panel); without doors the panel still renders
    doors = {'heading': 'Which one is you?', 'buttons': ['Button one', 'Thirty to sort'],
             'doors': [{'title': 'Door 1: You have the button', 'steps': ['<b>Press</b> it', 'Test it', 'Get a receipt'],
                        'receipt': {'caption': 'This is what you get.', 'columns': ['#', 'Rule', 'Where'], 'rows': [['C1', 'never guess one', 'Guardrails']]},
                        'have': 'plugins', 'policy': 'Advisors stay on the plugin.'},
                       {'title': 'Door 2: Thirty to sort', 'steps': ['Attach', 'Paste', 'Read'], 'have': 'a table'}],
             'shelf': 'STANDARD.md and TESTING.md'}
    tmp, out = build(dict(kit, doors=doors), [spec])
    index = read(out, 'index.html')
    for needle in ('Which one is you?', 'href="#door-1"', 'id="door-2"', 'Door 1: You have the button', '<b>Press</b> it',
                   'never guess one', 'Advisors stay on the plugin.', 'STANDARD.md and TESTING.md'):
        assert needle in index, needle
    assert kit['files_panel'] not in index
    shutil.rmtree(tmp)
    tmp, out = build(kit, [spec])
    assert kit['files_panel'] in read(out, 'index.html')
    shutil.rmtree(tmp)

def test_converter_own_guide_spec_renders():
    """The converter's own worked-example guide spec must render, not just parse (Important 2)."""
    spec_path = os.path.join(HERE, 'examples', 'transcript-to-action-plan', 'after',
                              'transcript-to-action-plan-client-email-guide.json')
    spec = json.load(open(spec_path, encoding='utf-8'))
    kit = dict(json.load(open(os.path.join(HERE, 'generator', 'kit.json'), encoding='utf-8')), only_plugin=None)
    tmp, out = build(kit, [spec])
    assert os.path.exists(os.path.join(out, spec['slug'] + '.html'))
    shutil.rmtree(tmp)

def test_copies_in_sync():
    """The converter must be self-contained when zipped, so it carries copies. They may not drift."""
    ref = os.path.join(HERE, 'skills', 'gpt-to-skill', 'references')
    for top, copy in (('STANDARD.md', os.path.join('references', 'standard.md')),
                      ('TESTING.md', os.path.join('references', 'testing.md')),
                      (os.path.join('tools', 'gpts-to-md.py'), os.path.join('scripts', 'gpts-to-md.py'))):
        a = open(os.path.join(HERE, top), 'rb').read()
        b = open(os.path.join(HERE, 'skills', 'gpt-to-skill', copy), 'rb').read()
        assert a == b, '%s and skills/gpt-to-skill/%s differ - copy the top-level file over' % (top, copy)
    tmpl = json.load(open(os.path.join(ref, 'guide-spec-template.json'), encoding='utf-8'))
    for key in ('slug', 'title', 'tagline', 'type', 'source', 'summary', 'never', 'have_ready', 'setup', 'use', 'faq'):
        assert key in tmpl, 'guide-spec-template.json missing ' + key

def test_gpts_to_md():
    """A folder of Word/text exports becomes one my-gpts.md with a ## section per file."""
    import zipfile
    tmp = tempfile.mkdtemp()
    folder = os.path.join(tmp, 'My GPTs')
    os.makedirs(folder)
    W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    xml = ('<w:document %s><w:body><w:p><w:r><w:t>You write social posts.</w:t></w:r></w:p>'
           '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Never</w:t></w:r><w:r><w:t xml:space="preserve"> invent results.</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
           '</w:body></w:document>') % W
    with zipfile.ZipFile(os.path.join(folder, 'Marketing Helper.docx'), 'w') as z: z.writestr('word/document.xml', xml)
    open(os.path.join(folder, 'Loan Check.txt'), 'w', encoding='utf-8').write('Ask for net operating income.')
    open(os.path.join(folder, '~$rketing Helper.docx'), 'wb').write(b'lock')   # Word's lock file: skipped
    open(os.path.join(folder, 'Old One.doc'), 'wb').write(b'\xd0\xcf')          # legacy .doc: reported, not read
    r = subprocess.run([sys.executable, os.path.join(HERE, 'tools', 'gpts-to-md.py'), folder], check=True, capture_output=True, text=True)
    md = open(os.path.join(tmp, 'my-gpts.md'), encoding='utf-8').read()
    assert '## Loan Check\n\nAsk for net operating income.' in md
    assert '## Marketing Helper\n\nYou write social posts.\nNever invent results.' in md
    assert md.index('## Loan Check') < md.index('## Marketing Helper')      # sorted by name
    assert '~$' not in md and 'Old One' not in md
    assert 'Old One.doc' in r.stdout and '2 GPTs' in r.stdout
    # explicit file list: only the named files are combined, a SKILL.md and a .py in the same folder are left alone,
    # and a duplicate stem gets " (2)"
    open(os.path.join(folder, 'SKILL.md'), 'w', encoding='utf-8').write('# not a GPT')
    open(os.path.join(folder, 'gpts-to-md.py'), 'w', encoding='utf-8').write('print(1)')
    dup = os.path.join(tmp, 'elsewhere'); os.makedirs(dup)
    open(os.path.join(dup, 'Loan Check.txt'), 'w', encoding='utf-8').write('Second copy.')
    out2 = os.path.join(tmp, 'listed.md')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'tools', 'gpts-to-md.py'),
                        os.path.join(folder, 'Loan Check.txt'), os.path.join(folder, 'Marketing Helper.docx'),
                        os.path.join(dup, 'Loan Check.txt'), os.path.join(folder, 'nope.docx'), '-o', out2],
                       check=True, capture_output=True, text=True)
    md2 = open(out2, encoding='utf-8').read()
    assert '## Loan Check\n' in md2 and '## Marketing Helper\n' in md2 and '## Loan Check (2)\n' in md2
    assert 'not a GPT' not in md2 and 'print(1)' not in md2
    assert '3 GPTs' in r.stdout
    assert 'skipped: nope.docx (not found)' in r.stdout
    assert r.stdout.count('skipped:') == 1
    assert 'Combined from 3 files.' in md2
    # file mode with nothing to combine writes nothing and fails loudly
    keep = os.path.join(tmp, 'keep', 'my-gpts.md'); os.makedirs(os.path.dirname(keep))
    open(keep, 'w', encoding='utf-8').write('hand edited')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'tools', 'gpts-to-md.py'), os.path.join(tmp, 'keep', 'My GPT')],
                       capture_output=True, text=True)
    assert r.returncode != 0 and 'nothing to combine' in (r.stdout + r.stderr) and 'skipped: My GPT (not found)' in r.stdout
    assert open(keep, encoding='utf-8').read() == 'hand edited'
    # a folder handed to file mode is "(not a file)"; the default output lands next to the first real file
    r = subprocess.run([sys.executable, os.path.join(HERE, 'tools', 'gpts-to-md.py'), folder, os.path.join(dup, 'Loan Check.txt')],
                       check=True, capture_output=True, text=True)
    assert 'skipped: %s (not a file)' % os.path.basename(folder) in r.stdout
    assert os.path.exists(os.path.join(dup, 'my-gpts.md'))
    # a folder run stays quiet about the .py sitting in it, and never re-ingests its own prior output
    open(os.path.join(folder, 'my-gpts.md'), 'w', encoding='utf-8').write('## Old Output\n\nstale')
    folder_out = os.path.join(tmp, 'folder.md')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'tools', 'gpts-to-md.py'), folder, '-o', folder_out],
                       check=True, capture_output=True, text=True)
    assert 'gpts-to-md.py' not in r.stdout
    assert 'Old Output' not in open(folder_out, encoding='utf-8').read()
    shutil.rmtree(tmp)

def test_skill_text():
    """SKILL.md carries Collect mode and points at the combiner where the skill ships it."""
    s = open(os.path.join(HERE, 'skills', 'gpt-to-skill', 'SKILL.md'), encoding='utf-8').read()
    assert '## Collect' in s and 'scripts/gpts-to-md.py' in s
    assert "say 'that's all'" in s and 'fenced block headed `my-gpts.md`' in s
    assert 'tools/gpts-to-md.py' not in s
    assert s.index('A conversion card, or a request') < s.index('→ **Collect**'), 'Convert must outrank Collect'
    assert 'never run it on the whole folder' in s and 'Take the first line that fits.' in s
    assert 'Attach only the GPT files, not their Knowledge files.' in s

def test_readme_block():
    """The README's doors block is generated from the same kit.json object as the site index."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('build', GEN); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    doors = {'heading': 'Which one is you?', 'buttons': ['Button one', 'Thirty to sort'],
             'doors': [{'title': 'Door 1: You have the button', 'steps': ['<b>Press</b> <code>Migrate</code>', 'See <a href="https://x.test/T.md">TESTING.md</a>'],
                        'receipt': {'caption': 'What you get.', 'columns': ['#', 'Rule', 'Where'], 'rows': [['C1', 'never guess one', 'Guardrails']]},
                        'have': 'plugins', 'policy': 'Advisors stay on the plugin.'},
                       {'title': 'Door 2: Thirty to sort, or no button', 'steps': ['Attach'], 'have': 'a table'}],
             'shelf': '<b>The shelf:</b> STANDARD.md'}
    md = mod.render_doors_md(doors)
    assert md.startswith('## Which one is you?\n')
    assert '- [Button one](#door-1-you-have-the-button)' in md and '- [Thirty to sort](#door-2-thirty-to-sort-or-no-button)' in md
    assert '### Door 1: You have the button\n' in md and '1. **Press** `Migrate`' in md and '2. See [TESTING.md](https://x.test/T.md)' in md
    assert '| # | Rule | Where |' in md and '| C1 | never guess one | Guardrails |' in md
    assert "**You'll have:** plugins" in md and 'Advisors stay on the plugin.' in md and '**The shelf:** STANDARD.md' in md
    tmp = tempfile.mkdtemp(); p = os.path.join(tmp, 'README.md')
    open(p, 'w', encoding='utf-8', newline='\n').write('# Kit\n\nintro\n\n<!-- doors:start -->\nold\n<!-- doors:end -->\n\n## After\n')
    mod.update_readme(p, doors)
    txt = open(p, encoding='utf-8').read()
    assert 'old' not in txt and '## Which one is you?' in txt and txt.startswith('# Kit\n\nintro\n\n<!-- doors:start -->\n') and txt.endswith('<!-- doors:end -->\n\n## After\n')
    assert '\r' not in txt
    assert '|---|---|---|' in md and md.endswith('**The shelf:** STANDARD.md\n')   # separator row; end marker gets its own line
    bad = dict(doors, doors=[dict(doors['doors'][0], receipt={'caption': 'x', 'columns': ['#'], 'rows': [[1]]})] + doors['doors'][1:])
    before = open(p, encoding='utf-8').read()
    try:
        mod.update_readme(p, bad); assert False, 'expected a failure on a non-string cell'
    except AttributeError:
        pass
    assert open(p, encoding='utf-8').read() == before   # a failed render must not touch the file
    shutil.rmtree(tmp)

if __name__ == '__main__':
    test_generator()
    test_converter_own_guide_spec_renders()
    test_copies_in_sync()
    test_gpts_to_md()
    test_skill_text()
    test_readme_block()
    print('ok')
