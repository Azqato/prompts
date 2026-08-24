#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check or resync the prompts-data.js mirror.

js/prompts-data.js holds a verbatim copy of every file in prompts/, because
browsers block fetch() on file:// and the site has to run by opening
index.html from disk. Nothing in the site enforces that the two copies
agree. If they drift, the page silently serves the stale copy while the .md
file that looks authoritative is not what anyone reads. This script is the
check that catches it.

    python tools/prompts-mirror.py            check, exit 1 on any problem
    python tools/prompts-mirror.py --sync     rewrite the data file from source

This is a maintenance tool, not part of the site. It never runs in a
browser, is not loaded by index.html, and is not a build step: delete it and
the site is unchanged. It has no third-party dependencies, only the Python
standard library, so it does not breach the project's no-dependency rule.
See docs/PRD.md sections 12, 29, and 30.
"""

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'js', 'prompts-data.js')
PROMPTS = os.path.join(ROOT, 'prompts')


def read(path):
    """Read UTF-8, normalizing every line ending to LF.

    The normalization is not cosmetic, it is what makes the comparison
    correct. This repository stores LF and has no .gitattributes, while
    core.autocrlf is true by default on Windows, so a fresh clone puts CRLF
    in the working tree. The raw values inside prompts-data.js are JSON
    escapes rather than real line breaks, so git never rewrites them and
    they stay LF forever. Comparing the two literally would report drift on
    every prompt in a fresh Windows clone with nothing actually wrong.

    Line endings are a property of the checkout, not of the content, so they
    are normalized away on both sides. Leaving newline at its default gives
    universal-newline translation, which is exactly that normalization.
    Writing is done with newline='' so nothing is translated back on the way
    out and the data file is always LF.
    """
    return io.open(path, encoding='utf-8').read()


def write(path, text):
    io.open(path, 'w', encoding='utf-8', newline='').write(text)


def load_data():
    """Return (prologue, entries, epilogue) from js/prompts-data.js."""
    src = read(DATA)
    start = src.index('[')
    end = src.rindex(']') + 1
    return src[:start], json.loads(src[start:end]), src[end:]


def source_slugs():
    return sorted(
        name[:-3] for name in os.listdir(PROMPTS)
        if name.endswith('.md')
    )


def render(entries):
    """Serialize entries in the file's existing two-space-indented style."""
    body = ',\n'.join(
        '  ' + json.dumps(e, ensure_ascii=False, indent=2).replace('\n', '\n  ')
        for e in entries
    )
    return '[\n' + body + '\n]'


def check():
    problems = []
    prologue, entries, epilogue = load_data()

    data_slugs = [e['slug'] for e in entries]
    files = source_slugs()

    for slug in sorted(set(data_slugs)):
        if data_slugs.count(slug) > 1:
            problems.append('duplicate entry in prompts-data.js: %s' % slug)
    for slug in sorted(set(data_slugs) - set(files)):
        problems.append('entry with no source file: prompts/%s.md is missing' % slug)
    for slug in sorted(set(files) - set(data_slugs)):
        problems.append('source file with no entry: prompts/%s.md is not in prompts-data.js' % slug)

    for entry in entries:
        slug = entry['slug']
        path = os.path.join(PROMPTS, slug + '.md')
        if not os.path.exists(path):
            continue
        if read(path) != entry['raw']:
            problems.append('DRIFT: prompts/%s.md does not match its entry' % slug)

    # Frontmatter and structure the renderer depends on. parsePrompt() falls
    # back silently for each of these, so a missing one ships as a page
    # titled with its slug, or with an empty code block, rather than as an
    # error anyone would notice.
    for entry in entries:
        raw = entry['raw']
        fm = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', raw, re.S)
        if not fm:
            problems.append('prompts/%s.md has no frontmatter block' % entry['slug'])
            continue
        keys = re.findall(r'^([A-Za-z0-9_-]+):', fm.group(1), re.M)
        for required in ('title', 'description'):
            if required not in keys:
                problems.append('prompts/%s.md frontmatter has no %s' % (entry['slug'], required))
        if not re.search(r'```[^\n]*\n.*?```', raw[fm.end():], re.S):
            problems.append('prompts/%s.md has no fenced prompt block' % entry['slug'])

    if problems:
        print('FAIL: %d problem(s)' % len(problems))
        for problem in problems:
            print('  - ' + problem)
        print('')
        print('Run with --sync to rewrite prompts-data.js from prompts/*.md.')
        return 1

    print('OK: %d prompt(s) mirrored, no orphans, all frontmatter present.' % len(entries))
    for slug in data_slugs:
        print('  %s' % slug)
    return 0


def sync():
    prologue, entries, epilogue = load_data()
    files = source_slugs()

    known = set(e['slug'] for e in entries)
    missing = [s for s in files if s not in known]
    orphans = [e['slug'] for e in entries if e['slug'] not in files]

    if orphans:
        print('Refusing to sync. These entries have no source file:')
        for slug in orphans:
            print('  - %s' % slug)
        print('')
        print('Deleting a prompt is a deliberate act with a documented procedure')
        print('(docs/PRD.md section 12, "Removing Prompts"). Remove the entry by')
        print('hand so the README and the patch notes are updated in the same pass.')
        return 1

    changed = []
    for entry in entries:
        raw = read(os.path.join(PROMPTS, entry['slug'] + '.md'))
        if raw != entry['raw']:
            entry['raw'] = raw
            changed.append(entry['slug'])

    # New prompts append, because array order is display order and a new
    # prompt belongs last in the sidebar. See docs/PRD.md section 12 step 4.
    for slug in missing:
        entries.append({'slug': slug, 'raw': read(os.path.join(PROMPTS, slug + '.md'))})

    if not changed and not missing:
        print('Nothing to do. Already in sync.')
        return 0

    write(DATA, prologue + render(entries) + epilogue)
    for slug in changed:
        print('resynced: %s' % slug)
    for slug in missing:
        print('added:    %s' % slug)
    print('')
    print('prompts-data.js written. Remember the rest of the procedure:')
    print('  - update README.md if the prompt list changed')
    print('  - add a docs/PATCHNOTES.md entry and a version history row')
    print('  - open index.html from disk and check the page')
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--sync':
        sys.exit(sync())
    if len(sys.argv) > 1:
        print(__doc__)
        sys.exit(2)
    sys.exit(check())
