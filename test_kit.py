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
    for top, copy in (('STANDARD.md', 'standard.md'), ('TESTING.md', 'testing.md')):
        a = open(os.path.join(HERE, top), 'rb').read()
        b = open(os.path.join(ref, copy), 'rb').read()
        assert a == b, '%s and references/%s differ - copy the top-level file over' % (top, copy)
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
    shutil.rmtree(tmp)

if __name__ == '__main__':
    test_generator()
    test_converter_own_guide_spec_renders()
    test_copies_in_sync()
    test_gpts_to_md()
    print('ok')
