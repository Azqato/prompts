---
title: LinkedIn Audit
description: Score your LinkedIn profile part by part, then get a rewritten headline, about, featured posts, and experience, plus a month of posts.
meta: Claude Code Prompt
---

Rebuilds a LinkedIn profile around one clear offer, the way a personal branding strategist would. It starts from your actual profile and what you tell it about the work you want, scores each part against a fixed checklist, and names what would confuse a stranger. Then it rewrites everything a visitor reads: ten headline options with the one to test first, an about summary that reads like a person rather than a resume, three featured items in order, sharper experience bullets that lead with results, and a banner line. It ends with twelve post ideas for your first month and two recommendation requests you can send today. It uses only results you can prove, marks any number it needs from you instead of inventing one, and never signs in to LinkedIn or posts anything for you.

## Prompt

```
Audit my LinkedIn profile and rebuild it around one clear offer. Act as a personal branding strategist and LinkedIn profile writer. Work only from what I give you, and write everything as drafts for me to paste in myself.

First, gather
- Ask me for my current profile, and wait: the easiest way is the PDF from "Resources" then "Save to PDF" on my profile, or the text of each section pasted in. Include my headline, about, experience, featured items, skills, and recommendations, and describe my photo and banner in a line each (or attach them).
- Do not sign in to LinkedIn, open it in a browser, or fetch my profile page. If a section is missing from what I gave you, say so and treat it as empty rather than guessing what it says.
- In the same message, ask me once, with a suggested answer for each drawn from what I sent, and wait:
  - The offer: what I want to be hired or contacted for, in one sentence.
  - Who it is for: the clients, employers, or roles I want.
  - Proof: two to five results I can share, with numbers where I have them.
  - The words my buyers search for, if I know them.
  - How often I can post: default twice a week.

Then audit, before writing anything new
- Fix the rubric first, then score. Score each part out of ten against these tests, and show the tests that failed:
  - Photo: a clear, current face, well lit, not cropped from a group.
  - Banner: says what I do or for whom, not a stock image.
  - Headline: a stranger knows what I do, for whom, and the result, in one line.
  - About: opens with a hook, reads like a person, includes proof, ends with a next step.
  - Featured: shows proof or the offer, and each item leads somewhere.
  - Experience: each role leads with results, not duties.
  - Recommendations: recent, specific, and about the work I want now.
- Score what is there, not what could be. Never raise one score by lowering another, and do not rescore after writing the rewrites.
- List what would still confuse a stranger landing on the profile, and name the one fix that matters most.

Then rebuild, in this order
1. Headline: ten options, each within 220 characters, using my buyers' words. Explain the best three, and name the one to test first and why.
2. About summary: an opening line that hooks, three short paragraphs (the problem I solve, how, and proof), a short list of what I help with, and a clear next step. Within 2,600 characters.
3. Featured: three items, chosen from my existing posts where one fits and written new where none does. For each: title, one-line description, its position, and the action it leads to.
4. Experience: for each role, a one-line summary, three bullets that each start with a result, the skills to tag, and what to cut. Within 2,000 characters per role.
5. Banner: one line of text for the banner image, and what it should show.
6. First month of posts: twelve ideas across four weeks at my posting rate, each with its hook, the format that fits (text, carousel, image, poll, or video), and the week it goes in. Add one comment strategy for starting conversations.
7. Two recommendation requests I can send today, each naming who to ask (by role, from my experience) and the specific thing to ask them to mention.

Rules for everything you write
- Use only results and facts I gave you. Where a line needs a number I did not give, write [number] and list it at the end, rather than inventing one.
- Plain, specific language: no buzzwords, no claims I cannot back up, no emoji unless I use them already.
- Count every character limit with a script, not by eye, and show the counts. If anything is over, cut it and recount.

Finish with a report
- The scorecard as a table: part, score out of ten, the tests that failed, and the fix.
- Every placeholder you left for me to fill, in one list.
- The character counts for the headline options, the about summary, and each role, all within their limits.
- Anything you could not assess from what I gave you, such as a photo I only described.
Do not post, publish, or send anything on my behalf.
```
