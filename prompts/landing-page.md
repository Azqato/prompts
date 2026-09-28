---
title: Landing Page
description: Plan and write a landing or pricing page around one action: the questions to answer first, the section order, the copy, the FAQ, and indexing advice.
meta: Claude Code Prompt
---

Writes a page that is built to win one thing. A landing page is not a home page: it has one offer, one audience, and one main action, whether that is a trial, a demo, a purchase, a waitlist, or a download. Claude asks the few questions that decide everything else (the action, who it is for, what stops them today, what proof exists, and where visitors arrive from), then picks a layout that suits the offer and writes the page section by section: the hero, the problem and solution, benefits written as outcomes, how it works in three steps, proof placed next to the claim it supports, an FAQ that answers real objections, and a closing call to action.

In pricing mode it writes the page that helps a visitor choose a plan: one value metric, three plans at most with one recommended, a monthly and annual toggle, limits and inclusions that matter, a readable comparison, and FAQs on cancellation, limits, and security.

It never invents proof. Testimonials, logos, and numbers you do not have are left as clearly marked placeholders. It writes the plan and the copy first, and builds the page in the project only when you ask.

## Prompt

```
Help me plan and write a page that wins one action. Two modes: landing (a single offer) or pricing (choosing a plan). Ask which if I have not said.

Ask first, in one message, with your suggested answer for each drawn from this project where you can:
- The one primary action, and what counts as a conversion.
- The offer: exactly what the visitor gets.
- Who it is for, the problem they have, and the three objections that stop them today.
- The proof that actually exists: customers, testimonials, numbers, screenshots, a demo video.
- Where visitors arrive from (ads, search, social, email) and what they already know.
- The risk reversal on offer: free trial, free plan, no card required, cancel anytime, a guarantee.
- For pricing: the value metric (seats, usage, projects), the plans and prices, their limits, and what makes people upgrade.
Wait for my answers.

Landing mode
- Recommend a layout and say why: a classic hero with sections (the product is clear from a screenshot), a long-form story (visitors need convincing), a minimal page (visitors already intend to act), or a comparison page (they are searching for alternatives).
- Above the fold: a headline naming the outcome and the audience, a one or two sentence subheadline saying what it is and how, one primary call to action (a verb plus what they get, never "Learn more" or "Submit"), one proof signal, and a real product visual.
- Then: problem to solution, three to five benefits written as outcomes with a detail each, how it works in three steps, proof placed beside the claim it supports, six to twelve FAQs that answer the real objections, the risk reversal, and the same call to action again.
- If the traffic comes from an ad, mirror its promise in the headline.

Pricing mode
- Recommend a layout: three plans (natural tiers), a usage slider (price scales with use, with the median customer as the default), two paths (individuals and teams), or self-serve plus enterprise.
- Three plans at most, one marked recommended without shouting, a monthly and annual toggle with the saving shown, three to six limits and inclusions per plan written as outcomes, consistent call-to-action wording across plans, a comparison grouped into a few headings rather than one giant grid, stacked cards on phones rather than a sideways-scrolling table, and FAQs on cancellation, hitting limits, discounts, who each plan is for, and security.
- Keep one value metric throughout, and no surprise fees.

Rules for both
- Be specific: "cut weekly reporting from 4 hours to 15 minutes", not "save time". No empty superlatives.
- Never invent proof. Anything I do not have is a marked placeholder, such as [testimonial needed].
- Choose sections from how this product is bought, not from a template; leave out any section that has nothing true to say.
- Indexing: say whether the page should be indexed (evergreen offers that match search intent) or kept out of search (ad-only or time-limited offers), and if indexed, give a title and meta description, and write the FAQ in plain question-and-answer form.

Output: the page outline in order, the hero copy, each section's copy, the FAQ, the indexing advice, and the layout recommendation with its reason. Then ask whether I want it built in this project. If I do, build it section by section in the project's existing style, starting with the hero, and show me each section before the next.
```
