---
title: E-commerce Site
description: Build an online shop: a landing page that sells, a filterable catalogue, product pages with options, and a cart drawer, with no invented reviews.
meta: Claude Code Prompt
---

Sets up an online shop in three parts that work together. A landing page that sells the shop and its best product to someone who has never heard of it. A catalogue where visitors filter, search, sort, and compare. A product page that answers a buyer's last questions beside the Add to cart button. A cart drawer runs across all three, so a buyer never loses their place.

Everything is described in the prompt itself, down to the small behaviors that make a shop feel trustworthy: sold-out options that stay visible and say so, delivery and returns answered under the button, a free-delivery threshold in the cart, filter chips you can remove one at a time, and focus that goes back where it was when a drawer closes. It works in whatever framework the project already uses, or a plain HTML, CSS, and JavaScript site if there is none.

Claude asks about the shop first and waits. It never invents reviews, ratings, customer counts, or logos: anything you do not have yet is a marked placeholder. Checkout is connected to the payment provider you choose, or left as a clear notice that nothing is charged until you connect one.

## Prompt

```
Build an online shop in this project: a landing page, a catalogue, product pages, and a cart that works across all of them. Goal: a visitor who has never heard of the shop understands what it sells, finds the right product, and buys it without leaving their place on the page.

1. Ask first, in one message, with your suggested answer for each drawn from this project where you can, then wait for my answers
- The shop: its name, what it sells, who buys it, and the one thing that makes it worth choosing.
- The products: how many, their categories, and the options each has (colour, size, material), with prices, sale prices, and stock. Ask for a file if there are many.
- The hero product or collection the landing page leads with, and the one action it asks for (usually "Shop now" or "Add to cart").
- The proof that actually exists: reviews and ratings, press, customer numbers, guarantees.
- Delivery: where you ship, costs, the free-delivery threshold, and how long it takes. Returns and repairs: the terms.
- Payments: the provider (Stripe, Shopify, Lemon Squeezy, or none yet). If none, the cart works and checkout says plainly that nothing is charged.
- Photos: whether real product photos exist, one per option, or placeholders are needed.
- Any subscription or repeat order: if so, the renewal terms.

2. Read the project
- Framework, styling approach, existing pages, and any design rules or brand. Build in the project's own style and conventions; with nothing there, use plain HTML, CSS, and JavaScript with no build step.
- Keep one product data file (JSON or a module) as the single source for every page: id, name, category, price, sale price, options with their own price and stock (in, low, out), rating, description, details, care, and photos with alt text. Every page reads from it.

3. Build the shared parts
- An announcement bar for one message (free delivery over the threshold, a sale).
- A header with the logo, section links, search, and a cart button showing the item count. The count is also in the button's accessible name, since a visual badge alone is not read out. Below about 860px the links fold into a Menu button.
- A cart drawer that opens over the page as a modal dialog. It lists each item with photo, chosen options, a quantity stepper, a remove button, and the line price; then the subtotal, how far the buyer is from free delivery, and the checkout button. Opening it moves focus into it; Tab stays inside; Escape and a click on the backdrop close it; closing returns focus to whatever opened it. Removing an item keeps focus in the drawer. The cart persists across pages and reloads.
- A short confirmation message (a toast, announced to screen readers) after adding to the cart.
- A footer with a newsletter sign-up (visible label, a status line for the result), links, delivery and returns, contact, and the small print.

4. The landing page (one action, asked twice)
- Hero: a headline naming what is sold and for whom, one sentence on why this shop, the main button, one proof signal, and a large real product image.
- Proof: real press mentions, reviews, or numbers, each with its source. If none exist, leave a marked placeholder or leave the section out.
- Featured products: three to eight cards from the data file, each with photo, name, price (sale price beside the crossed-out original), and quick add.
- Why it is better: three to four benefits written as outcomes, each with a detail.
- How it is made or how it works: three short steps.
- Questions: delivery, returns, sizing, care, and payment, as expandable answers.
- A final call to action that repeats the main action.

5. The catalogue
- A heading with the category name and a live result count, and "shop by type" buttons that set the filter.
- Filters in a side column (a full-screen sheet on phones, with the page behind it inactive and a "Show N products" button that says the result before closing): type, price range, option values (colour swatches), and in stock only. Each choice shows how many products it would leave.
- Search and a sort menu (featured, price low to high and high to low, rating, newest).
- Removable chips for every active filter, and "Clear all".
- Product cards: photo, name, price and sale price, colour swatches, rating with its count (only if real), stock word (low stock, sold out), save, quick view, and Add to cart.
- Show twelve, then a "Show more" button; after it, focus moves to the first new card.
- An empty state that says what to change, with a button to clear filters.
- After any filter, type button, search, or Clear all, focus moves to the results heading so a screen reader hears the new count. After removing a chip, focus moves to the next chip.
- Quick view: a dialog with photos, options, and Add to cart, behaving like the cart drawer.
- If sizes matter, a size guide that can set the size filter.

6. The product page
- Two columns: a gallery (a large image and thumbnails, sticky while scrolling on wide screens, stacked above the options under about 1000px) beside the name, rating, price, short summary, and the buy form.
- The buy form: each option is a real radio group (swatches and size cards), so the keyboard and screen readers work. Choosing a colour changes the gallery to that colour. Choosing a size updates the price. A sold-out option stays visible, disabled, and labelled sold out, with a "tell me when it is back" email field. A quantity stepper with a maximum that disables the plus button rather than failing silently. Add to cart adds the chosen options and opens the cart drawer.
- Directly under the button: three assurances (delivery time, free returns, guarantee), so the last questions are answered beside it.
- Details, care, and delivery as expandable sections.
- How it is made, if there is a real story.
- Reviews with a rating breakdown, only if reviews exist; the breakdown must add up to the average.
- Three or four "goes well with" products with quick add.

7. Rules
- Never invent proof: no made-up reviews, ratings, testimonials, customer counts, press logos, or statistics. Anything I have not given you is a placeholder such as [review needed], listed at the end.
- Prices, stock, and options come only from the data file; no page hard-codes them.
- Subscription products show the renewal price, how often it renews, and how to cancel right beside the subscribe button.
- Checkout: connect to the provider I chose using its own hosted checkout, with keys read from environment variables and never written into the code. With no provider, the checkout button shows a notice that nothing was ordered or charged.
- Every image has alt text naming the product and the option shown; decorative images have empty alt. Photos have width and height set and are served in WebP or AVIF at the size displayed.
- Works from 360px wide up with no sideways scrolling, buttons at least 44px tall, visible focus on everything, and colour contrast of at least 4.5:1 for text.
- Any motion respects reduced-motion settings.
- Each page has its own title and meta description, and product pages carry Product structured data with the real price and stock.
- Do not commit, push, or deploy.

8. Verify
- Run the site locally and walk through it at a phone width and a desktop width: land, filter, search, sort, open quick view, choose options on a product page, try a sold-out option, add to the cart, change quantity, remove an item, reload, and check out.
- Do the same walk with the keyboard only, and check where focus lands after each action.
- Fix what fails, and walk it again.

Report
1. The pages and files built, and where the product data lives.
2. How to add a product, change a price, or mark something sold out.
3. Every placeholder left for me to fill, by page.
4. What checkout does now, and what remains to connect it to real payments.
5. What could not be checked, and why.
```
