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

if __name__ == '__main__':
    test_generator()
    test_copies_in_sync()
    print('ok')
