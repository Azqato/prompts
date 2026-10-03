---
title: SEO Audit
description: Find why search engines miss your site, measure every page against the technical checklist, fix what code can fix, and list what only you can do.
meta: Claude Code Prompt
---

Works through the whole technical search checklist on your site: whether pages are rendered so a crawler sees the content, the sitemap and robots.txt, stray noindex tags, redirect chains, broken links, canonical tags, titles and meta descriptions, one H1 per page, breadcrumbs and structured data, orphan pages, image alt text and formats, layout shift, and load speed. Each item is measured on the built site first, not guessed from the source, and reported as pass or fail with the page and the evidence.

It then shows a plan and waits for your yes before changing anything. Small fixes it makes directly; anything large, such as moving a client-rendered site to server or static rendering, is proposed with its cost rather than done. It never removes a noindex tag without checking the page is meant to be found, never invents an author, a review, or a statistic, and never buys or asks for links.

It ends with the jobs that need you: submitting the sitemap in Google Search Console, writing a real author bio, earning links from other sites, and rewriting copy that reads as generic. No prompt can promise a ranking, and this one does not try.

## Prompt

```
Audit this site for search engines and fix what the code can fix. Goal: every page that should be found can be crawled, rendered, and indexed, and makes its case clearly. Ranking is not promised: it depends on content, links, and competition no code change controls.

1. Read and measure (change nothing yet)
- Read the project: framework, how pages are rendered (static, server, or client), the build command, the deploy target, and the live address if there is one. List every public page from the routes or the build output.
- Build the site and serve the built output locally. Measure the built pages, not the source. Use scripts and tools for every count, length, and timing; do not estimate by eye.
- Where a live address exists, you may also fetch its public pages and its robots.txt read-only, never signed in. Never run anything that changes the live site.

2. Check each item, per page, as pass, fail, or not applicable, with the evidence (file and line, URL, or the measured number)
- Rendering: fetch each page without running JavaScript. Is the main content, title, and links in the HTML? If not, the site depends on client rendering and crawlers may see an empty page.
- robots.txt: exists at the domain root and blocks nothing that should be found (a site served from a subfolder cannot set it; say so). Names the sitemap.
- Sitemap: sitemap.xml lists every page that should be found, with absolute URLs, and nothing that redirects, 404s, or is noindexed.
- noindex: list every page with a noindex meta tag or X-Robots-Tag header, and say whether each looks deliberate (an admin, draft, or internal page) or accidental.
- Redirects: follow every internal link and sitemap URL. Flag chains of more than one hop and any redirect loop.
- Broken links: every internal link and image resolves; list each 404 with the page that links to it.
- Canonical: each page has one absolute canonical URL, pointing to itself unless it is a deliberate duplicate.
- Title and meta description: every page has its own; titles about 60 characters or fewer, descriptions about 150 to 160, no duplicates across pages. Count with a script.
- Headings: exactly one H1 per page, saying what the page is; no skipped heading levels.
- Structured data: valid JSON-LD where it fits the content (Organization or Person, Article, Product, BreadcrumbList). FAQ markup no longer earns a rich result in Google; add it only where the page has a real FAQ, and never as a ranking tactic.
- Breadcrumbs: on any site more than one level deep, visible breadcrumbs with matching BreadcrumbList markup.
- Orphan pages: pages in the sitemap or routes that no other page links to.
- Images: every meaningful image has alt text describing it, decorative ones have empty alt. Large images are served in WebP or AVIF at the size displayed, with width and height set.
- Speed and stability: run Lighthouse (or the browser's performance tools) on the main page types at a phone size. Targets: Largest Contentful Paint 2.5s or less, Cumulative Layout Shift 0.1 or less, Interaction to Next Paint 200ms or less. Say these are lab numbers; real-user data comes from Search Console.
- Content signals (report only, do not rewrite): pages with very little text, near-duplicate pages, copy that is generic filler, and whether pages say who wrote them and why they can be trusted.

3. Plan, then wait
- Show a table: item, pages affected, the fix, its size (small, medium, large), and the risk. Small means a tag, a file, or an attribute. Large means a change to how the site renders or is built.
- Ask before: removing any noindex (some are deliberate), changing URLs (each old URL then needs a permanent redirect), and any large change. For rendering, propose the smallest fix that works in this framework (prerendering or static generation before a full server) with its cost.
- Stop and wait for my yes. Change nothing before it.

4. Fix
- Apply the approved fixes, smallest first. Follow the project's own rules and conventions; where a fix would break one (for example a no-build-step rule), say so and skip it.
- Never invent content: no made-up author, credentials, reviews, testimonials, or statistics. Where something only I can supply is missing, leave a marked placeholder and list it.
- Do not commit, push, or deploy.

5. Verify
- Rebuild, and rerun every check from step 2 with the same scripts. Every approved fix must now pass; show before and after for each, and for speed the numbers.

Report
1. The checklist: each item, pass or fail before and after, with evidence.
2. What was changed, by file.
3. What was proposed and not done, with why.
4. Jobs only I can do: submit the sitemap in Google Search Console (and Bing Webmaster Tools) and request indexing for key pages; write a real author bio; earn links from relevant sites (never buy them); rewrite any copy flagged as generic; fill each placeholder.
5. What could not be checked, and why.
```
