#!/usr/bin/env python3
"""Skill guide generator: <src>/<slug>-guide.json -> <out>/<slug>.html + <out>/index.html

  py build.py --kit kit.json --src <folder of spec json> --out <folder>

Content lives in the specs (one per skill, written from the skill's own files).
Everything about YOUR center lives in kit.json. This script only supplies the chrome,
so every guide looks the same and the index never drifts.

Written for Maryland and points at Neoserra - check anything that touches your own CRM,
programs, or reporting rules before you lean on it. MIT and unsupported - fork it, change
it, don't wait on me.
"""
import argparse, datetime, glob, html, json, os, sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
TYPE_LABEL = {'conversation': 'Conversation skill', 'plugin': 'Plugin with setup', 'scheduled': 'Runs on a schedule'}
TYPE_BLURB = {
    'conversation': 'You start it by saying what you want; it asks for what it needs and hands back a deliverable in the same chat. Nothing to install beyond the plugin, nothing to configure.',
    'plugin': 'A one-time setup conversation creates a file that is yours; the skills then keep it current. Worth twenty minutes the first time.',
    'scheduled': 'It runs by itself on a schedule and leaves a report. Your job is to read the report and answer what it could not.'}

def e(s): return html.escape(str(s or ''), quote=True)
def li(items, rich=True): return ''.join('<li>' + (i if rich else e(i)) + '</li>' for i in items or [])
def say(items): return ''.join('<span class="say">' + e(i) + '</span>' for i in items or [])
def rows(items, cols): return ''.join('<tr>' + ''.join('<td>' + (r.get(c) or '') + '</td>' for c in cols) + '</tr>' for r in items or [])
def section(sid, eyebrow, h2, body): return '<section id="%s"><div class="wrap"><p class="eyebrow">%s</p><h2>%s</h2><span class="rule"></span>%s</div></section>' % (sid, eyebrow, h2, body)

def fill(tpl, kit, values):
    values.update({'FOR': kit['for'], 'MAINTAINER': e(kit['maintainer']), 'BADGE': kit['badge']})
    for k, v in values.items(): tpl = tpl.replace('{{' + k + '}}', v)
    return tpl

def render(spec, tpl, kit):
    t = spec.get('type', 'conversation'); plug = spec.get('plugin', {}); setup = spec.get('setup', {}); use = spec.get('use', {})
    parts = []
    # What you get
    body = ''.join('<p>' + p + '</p>' for p in spec.get('summary', []))
    body += '<p class="sub"><b>%s.</b> %s</p>' % (TYPE_LABEL[t], TYPE_BLURB[t])
    if spec.get('never'): body += '<div class="panel"><h3 style="margin-top:0;">What it never does</h3><ul>' + li(spec['never']) + '</ul></div>'
    parts.append(section('what', 'Start here', 'What you get', body))
    # Scan / have ready
    n = 1
    if spec.get('have'):
        body = '<p>It works with whatever you already have connected. Tick what applies:</p><div class="tablescroll"><table class="tt" style="min-width:0;"><thead><tr><th>Do you have&hellip;</th><th>How to tell</th><th>What it unlocks</th></tr></thead><tbody>' + rows(spec['have'], ['what', 'how', 'unlocks']) + '</tbody></table></div>' + ('<p style="margin-top:var(--s4);">' + spec['have_note'] + '</p>' if spec.get('have_note') else '')
        parts.append(section('scan', 'Step %d' % n, 'A scan of what you&rsquo;re currently using', body)); n += 1
    elif spec.get('have_ready'):
        parts.append(section('scan', 'Step %d' % n, 'What to have ready', '<ul>' + li(spec['have_ready']) + '</ul>')); n += 1
    # Connects
    if spec.get('connects'):
        body = '<p>' + (spec.get('connects_note') or 'Everything here is read-only unless the row says otherwise.') + '</p><div class="tablescroll"><table class="tt" style="min-width:0;"><thead><tr><th>Source</th><th>What it reads</th><th>What it does with it</th></tr></thead><tbody>' + rows(spec['connects'], ['source', 'reads', 'does']) + '</tbody></table></div>'
        parts.append(section('connects', 'Step %d' % n, 'What it connects to', body)); n += 1
    # Setup
    lead = kit.get('setup_lead') or 'The skill is plain instructions, so it runs wherever you already work. Pick your row:'
    body = '<div class="two"><div><h3>Getting it on your side</h3><p class="sub">' + lead + '</p><ol class="steps">'
    if kit.get('files_step'): body += '<li>' + kit['files_step'] + '</li>'
    if plug.get('install_cowork'):
        body += '<li><b>Claude desktop app:</b> download <code>%s</code> from %s, drag it into a chat, click <b>Accept</b>.</li>' % (e(plug['install_cowork']), kit['cowork_where'])
    gpt = spec.get('chatgpt_url') or plug.get('chatgpt_url')
    repo, only = kit.get('source_repo'), kit.get('only_plugin') or ''
    if gpt:
        chat = 'open the GPT: <a href="%s" target="_blank" rel="noopener">%s</a>. Same skill, same outputs.' % (e(gpt), e(gpt))
    elif spec.get('chatgpt_note'):
        chat = spec['chatgpt_note']
    elif repo:
        # A skill is a Markdown file, so any assistant that accepts custom instructions can run it. Link the actual file.
        src = spec.get('source', '')
        path = src.split('/', 1)[1] if only and src.startswith(only + '/') else src
        chat = ('this skill is a plain Markdown file, not Claude-specific. Open <a href="%s/blob/main/%s" target="_blank" '
                'rel="noopener">%s</a>, copy the whole file, and paste it into a ChatGPT Project&rsquo;s instructions or a '
                'custom GPT. Same instructions, same outputs.') % (e(repo), e(path), e(path))
    else:
        chat = spec.get('chatgpt_note') or plug.get('chatgpt_note') or kit['chatgpt_fallback']
    body += '<li><b>ChatGPT:</b> ' + chat + '</li>'
    if plug.get('install_code'): body += '<li><b>Claude Code:</b> ' + ' then '.join('<code>%s</code>' % e(c) for c in plug['install_code']) + '</li>'
    body += ''.join('<li>' + s + '</li>' for s in setup.get('steps', []))
    body += '</ol></div><div><h3>Your first conversation</h3>'
    if setup.get('first_say'): body += '<p>Open a new chat and say:</p>' + say([setup['first_say']])
    if setup.get('asks'): body += '<p>It will ask for:</p><ul>' + li(setup['asks']) + '</ul>'
    if setup.get('note'): body += '<p>' + setup['note'] + '</p>'
    body += '</div></div>'
    parts.append(section('setup', 'Step %d' % n, 'Setting it up', body)); n += 1
    # How to use
    left = '<h3>Say</h3>' + say(use.get('say', []))
    if use.get('returns'): left += '<h3>What comes back</h3><ul>' + li(use['returns']) + '</ul>'
    right = ''
    if use.get('then'): right += '<h3>Then</h3><ul>' + li(use['then']) + '</ul>'
    if use.get('tips'): right += '<h3>Tips from the field</h3><ul>' + li(use['tips']) + '</ul>'
    parts.append(section('use', 'Step %d' % n, 'How to use it', '<div class="two"><div>' + left + '</div><div>' + right + '</div></div>'))
    # FAQ
    if spec.get('faq'):
        parts.append(section('faq', 'Questions people ask', 'FAQ', '<dl class="faq">' + ''.join('<dt>' + e(f['q']) + '</dt><dd>' + f['a'] + '</dd>' for f in spec['faq']) + '</dl>'))
    toc = ''.join('<a href="#%s">%s</a>' % (sid, lbl) for sid, lbl in [('what', 'What you get'), ('scan', 'What you use'), ('connects', 'Connects to'), ('setup', 'Setup'), ('use', 'How to use'), ('faq', 'FAQ')] if ('id="%s"' % sid) in ''.join(parts))
    return fill(tpl, kit, {'DOCTITLE': e(spec['title']) + ' — Skill guide', 'TITLE': e(spec['title']), 'TAGLINE': e(spec.get('tagline', '')), 'PLUGIN': e(plug.get('label', plug.get('name', ''))),
                           'TYPE': TYPE_LABEL[t], 'UPDATED': e(spec.get('updated', datetime.date.today().isoformat())), 'VERSION': e(spec.get('version', '')),
                           'DESCRIPTION': e(spec.get('tagline', '')), 'TOC': toc, 'SECTIONS': ''.join(parts), 'SOURCE': e(spec.get('source', ''))})

def render_index(specs, tpl, kit):
    groups = {}
    for s in specs: groups.setdefault(s.get('plugin', {}).get('label', 'Other'), []).append(s)
    center = e(kit['center'])
    body = '<p>Every skill in the %s toolkit, one page each: what it does, what to have ready, what to say, what comes back. Open the guide before you open the skill.</p>' % center
    body += '<div class="panel" style="margin-top:var(--s4);">' + kit['files_panel'] + '</div>'
    for g, items in groups.items():
        body += '<h3 style="margin-top:var(--s6);">' + e(g) + '</h3><div class="dgrid">'
        for s in sorted(items, key=lambda x: x['title']):
            body += '<a class="dcard" href="%s.html" style="display:block;color:inherit;font-weight:400;"><div class="org">%s <span class="warm warm-known">%s</span></div><div class="tagline">%s</div></a>' % (e(s['slug']), e(s['title']), TYPE_LABEL[s.get('type', 'conversation')], e(s.get('tagline', '')))
        body += '</div>'
    sec = section('index', 'The rundown', 'Every skill, and how to actually use it', body)
    return fill(tpl, kit, {'DOCTITLE': 'Skill guides — ' + center, 'TITLE': 'Skill guides', 'TAGLINE': 'How to use every skill in the %s toolkit' % center,
                           'PLUGIN': kit['badge'], 'TYPE': '%d guide%s' % (len(specs), '' if len(specs) == 1 else 's'), 'UPDATED': datetime.date.today().isoformat(), 'VERSION': '',
                           'DESCRIPTION': 'Index of skill guides', 'TOC': '', 'SECTIONS': sec, 'SOURCE': ''})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default=os.path.join(HERE, 'kit.json'), help='your center settings')
    ap.add_argument('--src', required=True, help='folder of <slug>.json guide specs')
    ap.add_argument('--out', required=True, help='folder to write <slug>.html + index.html into')
    a = ap.parse_args()
    kit = json.load(open(a.kit, encoding='utf-8'))
    tpl = open(os.path.join(HERE, 'guide.template.html'), encoding='utf-8').read()
    os.makedirs(a.out, exist_ok=True)
    only, specs, skipped = kit.get('only_plugin'), [], 0
    for f in sorted(glob.glob(os.path.join(a.src, '*.json'))):
        s = json.load(open(f, encoding='utf-8')); s['slug'] = s.get('slug') or os.path.splitext(os.path.basename(f))[0]
        if only and (s.get('plugin') or {}).get('name') != only: skipped += 1; continue   # other plugins' guides never ship in this build
        specs.append(s)
        with open(os.path.join(a.out, s['slug'] + '.html'), 'w', encoding='utf-8', newline='\n') as fh: fh.write(render(s, tpl, kit))
    with open(os.path.join(a.out, 'index.html'), 'w', encoding='utf-8', newline='\n') as fh: fh.write(render_index(specs, tpl, kit))
    msg = 'rendered %d guides + index -> %s' % (len(specs), a.out)
    if skipped: msg += ' (skipped %d: plugin is not %s)' % (skipped, only)
    print(msg)
    if kit.get('netlify_allowlist'):
        update_redirects(os.path.join(os.path.dirname(os.path.abspath(a.out)), '_redirects'), [s['slug'] for s in specs])

BEGIN, END = '# -- GUIDES (generated by skill-guide/build.py; edit the specs, not this block) --', '# -- /GUIDES --'
def update_redirects(path, slugs):
    """Only for a Netlify site run as a default-closed allow-list (Maryland's wiki). A page is served only if it has a
    pretty-path 200 and an .html 301 ahead of the catch-all. Owns one marked block so a new guide can't be silently unpublished."""
    if not os.path.exists(path): print('no _redirects at', path, '- skipped'); return
    def rule(src, dst, code): return '%s  %s  %s' % (src.ljust(48), dst.ljust(52), code)   # always >= 2 spaces between columns
    lines = [BEGIN, rule('/guides', '/guides/index.html', '200!'), rule('/guides/', '/guides/index.html', '200!'), rule('/guides/index.html', '/guides', '301!')]
    for sl in sorted(slugs):
        lines += [rule('/guides/' + sl, '/guides/%s.html' % sl, '200!'), rule('/guides/%s.html' % sl, '/guides/' + sl, '301!')]
    lines.append(END)
    txt = open(path, encoding='utf-8').read()
    if BEGIN in txt:
        txt = txt[:txt.index(BEGIN)] + '\n'.join(lines) + txt[txt.index(END) + len(END):]
    else:
        marker = txt.index('# ── DENY EVERYTHING ELSE')
        txt = txt[:marker] + '\n'.join(lines) + '\n\n\n' + txt[marker:]
    with open(path, 'w', encoding='utf-8', newline='\n') as fh: fh.write(txt)
    print('updated allow-list in', path, '(%d guide rules)' % (len(lines) - 2))

if __name__ == '__main__':
    main()
