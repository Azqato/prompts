"""Generate dashboard/index.html, the progress dashboard, from its sources.

    python tools/dashboard.py

Never edit dashboard/index.html by hand: change a source and run this.
Each section reads exactly one source, so the page cannot disagree with
the project:

    Steps, questions, stuck   dashboard/state.json, kept by Claude
    Latest results            git: files changed since state.json's
                              start_commit, plus uncommitted changes
    Latest release            the newest entry in docs/PATCHNOTES.md
    Roadmap                   docs/PRD.md section 27, in full: every
                              milestone, its scoped findings, every
                              future update, every deferred item, and
                              the verification checklist
    Ideas waiting             docs/TODO.md

The top bar shows when progress was last recorded (state.json's
modification time), not when the page was generated, and a small inline
script warns when that is older than state.json's stale_minutes while the
task is open. The page is written atomically and only when its content,
ignoring the generation time, has changed. Styles are in
tools/dashboard.css. Python standard library only. See docs/PRD.md
section 20 and the Progress Dashboard prompt.
"""

import datetime
import html
import io
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, 'dashboard', 'state.json')
OUT = os.path.join(ROOT, 'dashboard', 'index.html')
CSS = os.path.join(ROOT, 'tools', 'dashboard.css')
PRD = os.path.join(ROOT, 'docs', 'PRD.md')
NOTES = os.path.join(ROOT, 'docs', 'PATCHNOTES.md')
TODO = os.path.join(ROOT, 'docs', 'TODO.md')
GEN = re.compile(r'<span class="pd-gen">[^<]*</span>')

e = html.escape
LABELS = {
    'done': ('done', 'Done'), 'progress': ('doing', 'In progress'),
    'todo': ('todo', 'Not started'), 'waiting': ('waiting', 'Waiting'),
}


def read(path):
    return io.open(path, encoding='utf-8').read()


def mtime(path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(path))


def stamp(t):
    return t.strftime('%Y-%m-%d %H:%M')


def git(*args):
    out = subprocess.run(['git'] + list(args), cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if out.returncode:
        raise RuntimeError(out.stderr.strip() or 'git failed')
    return out.stdout


def pill(kind, word):
    return '<span class="pd-status pd-status--%s">%s</span>' % (kind, e(word))


def table(cols, rows):
    return ('<div class="pd-table-wrap"><table class="pd-table"><thead><tr>'
            + ''.join('<th scope="col">%s</th>' % c for c in cols)
            + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')


def empty(text):
    return '<div class="pd-card pd-empty"><p class="pd-empty-title">Nothing here</p><p>%s</p></div>' % e(text)


def failed(source, err):
    return '<div class="pd-card pd-empty"><p class="pd-empty-title pd-error">Could not read %s</p><p>%s</p></div>' % (e(source), e(str(err)))


def source(text):
    return '<p class="pd-source">%s</p>' % text


def section(sid, title, body):
    return ('<section class="pd-section" id="%s" aria-labelledby="h-%s"><h2 class="pd-section-title" id="h-%s">%s</h2>%s</section>\n'
            % (sid, sid, sid, e(title), body))


# ---------- Sources ----------

def results(state):
    """(rows, count) from git since the task's start commit."""
    start = state.get('start_commit')
    files = {}
    if start:
        for line in git('log', '--format=%x00%s', '--name-only', start + '..HEAD').split('\n'):
            if line.startswith('\x00'):
                subject = line[1:]
            elif line.strip() and line.strip() not in files:
                files[line.strip()] = subject
    for line in git('status', '--porcelain').split('\n'):
        if line.strip():
            files.setdefault(line[3:].strip().strip('"'), 'Not yet committed')
    files.pop('dashboard/index.html', None)  # the page itself would churn
    rows = ['<tr><th scope="row"><code>%s</code></th><td>%s</td></tr>' % (e(f), e(m)) for f, m in sorted(files.items())]
    return rows, len(rows)


def release():
    notes = read(NOTES)
    m = re.search(r'^## (v[\d.]+) - (\d{4}-\d{2}-\d{2})\n(.*?)(?=^## v|\Z)', notes, re.M | re.S)
    if not m:
        raise ValueError('no "## vX.Y.Z - YYYY-MM-DD" entry found')
    heads = re.findall(r'^### (.+)$', m.group(3), re.M)
    items = len(re.findall(r'^- ', m.group(3), re.M))
    return ('<div class="pd-card"><div class="pd-card-head"><h3>%s</h3><p class="pd-card-note">%s</p></div>'
            '<p class="pd-summary">%s, %d item%s.</p></div>'
            % (e(m.group(1)), e(m.group(2)), e(', '.join(heads) or 'No headings'), items, '' if items == 1 else 's'))


def roadmap():
    """(rows, open_count, done_count, total) from PRD section 27, in full."""
    prd = read(PRD)
    s = prd[prd.index('## 27. Roadmap'):prd.index('## 28. Metrics')]
    part = lambda head: s.split(head, 1)[1].split('\n### ', 1)[0]
    rows, opened, done, total = [], 0, 0, 0

    def row(name, kind, kind_word, word, is_done, sub=False):
        nonlocal opened, done, total
        total += 1
        done += is_done
        opened += not is_done
        cls = ' class="%s"' % ' '.join(c for c in ('is-dim' if is_done else '', 'pd-sub' if sub else '') if c)
        return '<tr%s><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (
            cls if cls != ' class=""' else '', e(name), e(kind_word), pill(kind, word))

    scoped = dict(
        (t.strip().lower(), re.findall(r'^\*\*(\d+\..+?)\*\*', body, re.M))
        for t, body in re.findall(r'^### Scoped: (.+?)\n(.*?)(?=^### |\Z)', s, re.M | re.S))
    for name, when, status in re.findall(r'^\| (.+?) \| (.+?) \| (.+?) \|$', part('### Milestones'), re.M)[2:]:
        is_done = status.startswith('Complete')
        kind = 'done' if is_done else 'waiting' if status.startswith(('Ongoing', 'In Progress')) else 'todo'
        rows.append(row(name, kind, 'Milestone, ' + when, status, is_done))
        for finding in scoped.get(name.strip().lower(), []):
            rows.append(row(finding.rstrip('.'), kind, 'Scoped finding', 'Done' if is_done else 'Open', is_done, sub=True))
    for entry in re.split(r'^#### ', part('### Future updates'), flags=re.M)[1:]:
        title = entry.split('\n', 1)[0]
        built = re.search(r'\*\*Built in (v[\d.]+)', entry)
        declined = re.search(r'\*\*(Declined|Not built)', entry)
        num, _, name = title.partition('. ')
        word = 'Built ' + built.group(1).rstrip('.') if built else 'Declined' if declined else 'Proposed'
        rows.append(row(name, 'done' if built else 'todo' if declined else 'waiting', 'Future update ' + num, word, bool(built or declined)))
    for name in re.findall(r'^- \*\*(.+?)\.\*\*', part('### Deferred'), re.M):
        rows.append(row(name, 'todo', 'Deferred', 'Deferred', False))
    for name, title, status in re.findall(r'^\| ((?:PRD|DESIGN) [^|]+?) \| ([^|]+?) \| ([^|]+?) \|', part('### Verification checklist'), re.M):
        ok = status.startswith('Verified')
        rows.append(row('%s, %s' % (name, title), 'done' if ok else 'todo', 'Verification checklist', status.split(';')[0], ok))
    return rows, opened, done, total


def ideas():
    body = read(TODO).split('## Ideas', 1)[1]
    return len([l for l in body.split('\n') if l.startswith('- ') and '<Your idea' not in l])


# ---------- Page ----------

def build():
    state = json.loads(read(STATE))
    recorded = mtime(STATE)
    steps = state.get('steps', [])
    n = len(steps)
    done = sum(1 for x in steps if x['status'] == 'done')
    doing = sum(1 for x in steps if x['status'] == 'progress')
    questions = [q for q in state.get('questions', []) if not q.get('answered')]
    stuck = state.get('stuck', [])
    pct = round(100 * done / n) if n else 0
    finished = n > 0 and done == n

    step_rows = ['<tr class="is-%s"><td class="pd-num">%d</td><th scope="row">%s</th><td>%s</td><td class="pd-num">%s</td></tr>'
                 % (LABELS[x['status']][0], i + 1, e(x['name']), pill(*LABELS[x['status']]), e(x.get('at', '')))
                 for i, x in enumerate(steps)]
    q_rows = ['<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>'
              % (e(q['q']), e(q['default']), pill('done', 'Answered by default') if q.get('answered') else pill('waiting', 'Open'))
              for q in state.get('questions', [])]
    s_rows = ['<tr><th scope="row">%s</th><td>%s</td></tr>' % (e(x['what']), e(x.get('waiting', ''))) for x in stuck]

    try:
        r_rows, r_count = results(state)
        results_body = source('From git since commit <code>%s</code>, plus uncommitted changes.' % e(state.get('start_commit', 'none'))) + (table(['File', 'Last change'], r_rows) if r_rows else empty('No files changed yet.'))
    except Exception as err:
        r_count, results_body = 0, failed('git', err)
    try:
        release_body = source('From docs/PATCHNOTES.md, changed %s.' % stamp(mtime(NOTES))) + release()
    except Exception as err:
        release_body = failed('docs/PATCHNOTES.md', err)
    try:
        road_rows, road_open, road_done, road_total = roadmap()
        road_body = (source('From docs/PRD.md section 27, changed %s. Ideas waiting in docs/TODO.md: %d.' % (stamp(mtime(PRD)), ideas()))
                     + '<div class="pd-card pd-road-note"><div class="pd-card-head"><h3>Whole roadmap</h3><p class="pd-card-note">%d of %d done</p></div>'
                       '<span class="pd-meter" role="img" aria-label="%d of %d done"><span class="pd-meter-fill" style="width:%d%%"></span></span></div>'
                       % (road_done, road_total, road_done, road_total, round(100 * road_done / road_total) if road_total else 0)
                     + table(['Item', 'Kind', 'Status'], road_rows))
    except Exception as err:
        road_open, road_body = 0, failed('docs/PRD.md section 27', err)

    kpi = lambda label, value, note, tone: ('<li class="pd-kpi"><p class="pd-kpi-label">%s</p><p class="pd-kpi-value">%s</p><p class="pd-kpi-delta is-%s">%s</p></li>'
                                             % (label, value, tone, note))
    nav = ''.join('<a href="#%s">%s<span class="pd-nav-count">%d</span></a>' % (a, b, c) for a, b, c in [
        ('steps', 'Steps', n), ('questions', 'Questions', len(questions)), ('stuck', 'Stuck', len(stuck)),
        ('results', 'Results', r_count), ('release', 'Release', 1), ('roadmap', 'Roadmap', road_open)])
    stale = int(state.get('stale_minutes', 30))

    body = ('<body><div class="pd-shell">\n'
            '<aside class="pd-sidebar"><a class="pd-brand" href="#overview"><span class="pd-brand-mark" aria-hidden="true"><span></span><span></span></span>Progress</a>\n'
            '<p class="pd-org"><strong>Current task</strong>%s</p>\n'
            '<nav class="pd-nav" aria-label="Sections"><a href="#overview">Overview</a>%s</nav>'
            '<div class="pd-sidebar-foot"><span class="pd-avatar" aria-hidden="true">C</span><p><strong>Generated</strong>by tools/dashboard.py</p></div></aside>\n'
            '<div class="pd-main-wrap">\n<header class="pd-topbar"><div class="pd-topbar-title"><h1>%s</h1>'
            '<p class="pd-live"><span class="pd-live-dot" id="pd-dot" aria-hidden="true"></span>Progress recorded %s, refreshes every 10 seconds</p></div><span class="pd-chip">%d%%</span></header>\n'
            '<main class="pd-main">\n<p class="pd-stale" id="pd-stale" role="alert"></p>\n'
            % (e(state['task']), nav, e(state['task']), stamp(recorded), pct))
    body += section('overview', 'Overview',
                    '<ul class="pd-kpis">'
                    + kpi('Steps done', '%d/%d' % (done, n), '%d%% complete' % pct, 'good')
                    + kpi('In progress', doing, 'working now' if doing else 'nothing running', 'flat')
                    + kpi('Stuck', len(stuck), 'needs attention' if stuck else 'nothing blocked', 'bad' if stuck else 'good')
                    + kpi('Open questions', len(questions), 'defaults applied meanwhile' if questions else 'none waiting', 'flat' if questions else 'good')
                    + '</ul><div class="pd-card"><div class="pd-card-head"><h3>Progress</h3><p class="pd-card-note">%d of %d steps done</p></div>'
                      '<span class="pd-meter" role="img" aria-label="%d%% complete"><span class="pd-meter-fill" style="width:%d%%"></span></span><p class="pd-summary">%s</p></div>'
                    % (done, n, pct, pct, e(state.get('summary', ''))))
    body += section('steps', 'Steps', source('From dashboard/state.json.') + (table(['#', 'Step', 'Status', 'Time'], step_rows) if step_rows else empty('No steps yet.')))
    body += section('questions', 'Questions for you', table(['Question', 'Default I am taking', 'Status'], q_rows) if q_rows else empty('No questions waiting.'))
    body += section('stuck', 'Stuck', table(['What', 'Waiting for'], s_rows) if s_rows else empty('Nothing is blocked.'))
    body += section('results', 'Latest results', results_body)
    body += section('release', 'Latest release', release_body)
    body += section('roadmap', 'Roadmap', road_body)
    body += ('<footer class="pd-footer">A generated working page: run python tools/dashboard.py, never edit it by hand. <span class="pd-gen"></span> Not indexed. '
             'The published copy shows the state as of the last publish.</footer>\n</main></div></div>\n')
    # The only script: warns when no progress has been recorded for a while.
    # With it blocked the page still reads correctly; only the warning is lost.
    body += ('<script>(function(){var r=new Date("%s"),m=%d,open=%s;if(!open)return;'
             'var a=Math.floor((Date.now()-r.getTime())/60000);if(a<m)return;'
             'var b=document.getElementById("pd-stale");b.textContent="May be stale: no progress recorded for "+a+" minutes.";b.className="pd-stale is-on";'
             'document.getElementById("pd-dot").className="pd-live-dot is-stale";})();</script>\n</body></html>\n'
             % (recorded.strftime('%Y-%m-%dT%H:%M:%S'), stale, 'false' if finished else 'true'))

    head = ('<!DOCTYPE html>\n<!-- Generated by tools/dashboard.py from dashboard/state.json, git, and docs/. '
            'Do not edit by hand: change a source and run python tools/dashboard.py. -->\n'
            '<html lang="en"><head><meta charset="UTF-8"><meta http-equiv="refresh" content="10"><meta name="robots" content="noindex">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>%s - Progress</title>\n<style>\n%s</style>\n</head>\n'
            % (e(state['task']), read(CSS)))
    return head + body


def main():
    page = build()
    old = read(OUT) if os.path.exists(OUT) else ''
    blank = '<span class="pd-gen"></span>'
    if GEN.sub(blank, old) == page:
        print('dashboard: unchanged')
        return
    page = page.replace(blank, '<span class="pd-gen">Generated %s.</span>' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    tmp = OUT + '.tmp'
    io.open(tmp, 'w', encoding='utf-8', newline='\n').write(page)
    os.replace(tmp, OUT)
    print('dashboard: written')


if __name__ == '__main__':
    main()
