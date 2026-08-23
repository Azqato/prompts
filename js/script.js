/* ============================================================
   Prompts - client logic
   Reads prompt content embedded in prompts-data.js (mirrors the
   .md files in /prompts), parses frontmatter + body, and renders
   the home list and per prompt detail views with hash based
   routing. No fetch, no server, no external libraries: the site
   runs by opening index.html directly (file://).
   ============================================================ */

const SITE_INTRO =
  'A personal library of reusable Claude Code prompts. Each prompt lives in its own ' +
  'markdown file: a plain description of what it does and a copyable block with the full ' +
  'prompt text. Pick one, copy it, drop it into Claude Code.';

let PROMPTS = [];

/* ---------- Parsing ---------- */

function parsePrompt(raw, slug) {
  let title = slug;
  let description = '';
  let meta = 'Claude Code Prompt';
  let hidden = false;
  let body = raw;

  const fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (fm) {
    body = fm[2];
    fm[1].split(/\r?\n/).forEach(function (line) {
      const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
      if (!m) return;
      const key = m[1].toLowerCase();
      const value = m[2].trim();
      if (key === 'title') title = value;
      else if (key === 'description') description = value;
      else if (key === 'meta') meta = value;
      else if (key === 'hidden') hidden = /^(true|yes|1)$/i.test(value);
    });
  }

  // The first fenced code block is the prompt text. Everything
  // before it (minus a trailing "## Prompt" heading) is the description.
  let prompt = '';
  let descSource = body;
  const fence = body.match(/```[^\n]*\n([\s\S]*?)```/);
  if (fence) {
    prompt = fence[1].replace(/\n$/, '');
    descSource = body.slice(0, fence.index);
  }
  descSource = descSource.replace(/#{2,}\s*Prompt\s*$/i, '').trim();

  return {
    slug: slug,
    title: title,
    description: description,
    meta: meta,
    hidden: hidden,
    prompt: prompt,
    descHtml: renderMarkdown(descSource)
  };
}

/* ---------- Minimal markdown for descriptions ---------- */

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function renderInline(text) {
  let out = escapeHtml(text);
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  return out;
}

function renderMarkdown(src) {
  if (!src) return '';
  const blocks = src.split(/\r?\n\r?\n+/);
  return blocks.map(function (block) {
    const lines = block.split(/\r?\n/);
    const heading = block.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      const level = Math.min(heading[1].length, 6);
      return '<h' + level + '>' + renderInline(heading[2]) + '</h' + level + '>';
    }
    if (lines.every(function (l) { return /^\s*[-*]\s+/.test(l); })) {
      const items = lines.map(function (l) {
        return '<li>' + renderInline(l.replace(/^\s*[-*]\s+/, '')) + '</li>';
      });
      return '<ul>' + items.join('') + '</ul>';
    }
    return '<p>' + renderInline(lines.join(' ')) + '</p>';
  }).join('\n');
}

/* ---------- Rendering ---------- */

function findPrompt(slug) {
  for (let i = 0; i < PROMPTS.length; i++) {
    if (PROMPTS[i].slug === slug) return PROMPTS[i];
  }
  return null;
}

function buildSidebar() {
  const nav = document.getElementById('sidebar-nav');
  let html = '<a href="#/" data-slug="">Home</a>';
  PROMPTS.forEach(function (p) {
    if (p.hidden) return; // hidden prompts stay reachable by direct link, but off the nav
    html += '<a href="#/' + p.slug + '" data-slug="' + p.slug + '">' + escapeHtml(p.title) + '</a>';
  });
  nav.innerHTML = html;
}

function setActiveLink(slug) {
  const links = document.querySelectorAll('#sidebar-nav a');
  links.forEach(function (a) {
    a.classList.toggle('active', a.getAttribute('data-slug') === slug);
  });
}

function renderHome() {
  let html = '';
  html += '<section class="hero">';
  html += '<h1>Claude Code Prompts<span class="accent-dot">.</span></h1>';
  html += '<p class="lead">' + escapeHtml(SITE_INTRO) + '</p>';
  html += '</section>';
  html += '<h2>Prompts</h2>';
  html += '<div class="prompt-list">';
  PROMPTS.forEach(function (p) {
    if (p.hidden) return; // hidden prompts stay reachable by direct link, but off the home list
    html += '<a class="prompt-list-item" href="#/' + p.slug + '">';
    html += '<span class="prompt-list-title">' + escapeHtml(p.title) + '</span>';
    html += '<span class="prompt-list-desc">' + escapeHtml(p.description) + '</span>';
    html += '</a>';
  });
  html += '</div>';
  document.getElementById('content').innerHTML = html;
  document.title = "Azqato's Prompts";
}

function renderDetail(p) {
  let html = '';
  html += '<div class="prompt-header">';
  html += '<h1>' + escapeHtml(p.title) + '</h1>';
  html += '<span class="prompt-meta">' + escapeHtml(p.meta) + '</span>';
  html += '</div>';
  html += '<div class="prompt-description">' + p.descHtml + '</div>';
  html += '<div class="code-block-wrapper">';
  html += '<div class="code-block-header">';
  html += '<span class="code-label">Prompt</span>';
  html += '<button class="copy-btn" aria-label="Copy prompt to clipboard">Copy</button>';
  html += '</div>';
  html += '<pre><code>' + escapeHtml(p.prompt) + '</code></pre>';
  html += '</div>';
  document.getElementById('content').innerHTML = html;
  document.title = p.title;
  wireCopyButton();
}

function renderError(err) {
  const html =
    '<div class="prompt-header"><h1>Could not load prompts</h1></div>' +
    '<div class="prompt-description"><p>' + escapeHtml(err.message) + '</p></div>' +
    '<div class="status-message">' +
    '<p>Make sure <code>prompts-data.js</code> is present next to <code>index.html</code> ' +
    'and is loaded before <code>script.js</code>.</p>' +
    '</div>';
  document.getElementById('content').innerHTML = html;
}

/* ---------- Copy button ---------- */

function wireCopyButton() {
  const btn = document.querySelector('.copy-btn');
  if (!btn) return;
  btn.addEventListener('click', function () {
    const code = document.querySelector('.code-block-wrapper pre code');
    if (!code) return;
    navigator.clipboard.writeText(code.textContent).then(function () {
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      btn.setAttribute('aria-label', 'Copied!');
      setTimeout(function () {
        btn.textContent = 'Copy';
        btn.classList.remove('copied');
        btn.setAttribute('aria-label', 'Copy prompt to clipboard');
      }, 2000);
    });
  });
}

/* ---------- Redirects ---------- */

/* Retired address -> current slug. Deliberately empty.

   The public surface of this site is the deployed page, not the source
   that builds it. A prompt is authored as a .md file in prompts/, and its
   slug is derived from that filename, so renaming or removing a prompt is
   an internal change to source and needs no redirect. An unknown slug
   falls through to the home view, which is the right outcome for one.

   The mechanism is kept for a genuine public-facing address, should one
   ever be retired. Any entry added here is permanent, never chains, and
   is never reused to point at different content. See docs/PRD.md,
   "Renaming Prompts" and "Removing Prompts". */
const REDIRECTS = {};

/* ---------- Routing ---------- */

function currentSlug() {
  const hash = window.location.hash.replace(/^#\/?/, '');
  return hash.trim();
}

function route() {
  const slug = currentSlug();
  if (!slug) {
    renderHome();
    setActiveLink('');
    return;
  }
  // A retired slug rewrites the hash to the current one, which fires
  // hashchange and re-enters route() with the canonical slug. Guarded on
  // the target existing so a stale redirect can never bounce the reader
  // into a dead end; if it does not resolve, fall through to the home view.
  if (Object.prototype.hasOwnProperty.call(REDIRECTS, slug) && findPrompt(REDIRECTS[slug])) {
    window.location.replace('#/' + REDIRECTS[slug]);
    return;
  }

  const p = findPrompt(slug);
  if (p) {
    renderDetail(p);
    setActiveLink(slug);
  } else {
    renderHome();
    setActiveLink('');
  }
  window.scrollTo(0, 0);
}

/* ---------- Init ---------- */

function init() {
  const data = window.PROMPTS_DATA;
  if (!Array.isArray(data) || data.length === 0) {
    renderError(new Error('No prompt data was loaded from prompts-data.js.'));
    return;
  }
  try {
    PROMPTS = data.map(function (entry) {
      return parsePrompt(entry.raw, entry.slug);
    });
  } catch (err) {
    renderError(err);
    return;
  }
  buildSidebar();
  window.addEventListener('hashchange', route);
  route();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
