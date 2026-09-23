---
name: landing-page-copywriter
description: Writes conversion-focused landing page copy - headlines, subheads, value propositions, feature and benefit blocks, social proof, FAQs, and CTA button text - using PAS, AIDA, or StoryBrand. Use when the user wants words for a landing page, sales page, product or pricing page, waitlist page, homepage hero, or ad-to-page flow, including rewriting weak copy, generating headline or CTA variants for A/B tests, or turning a product description into page sections. Use landing-page-optimizer instead for auditing an existing page's performance, and a frontend skill for building the page itself.
---

# Landing Page Copywriter

Write landing page copy that makes one reader take one action. The copy is the deliverable; layout and code are out of scope unless asked.

## Workflow

1. **Build the brief.** Pull these from the conversation, attached docs, or the product's existing site before asking anything. Ask only for what is missing and blocking:
   - Product and the one action the page drives (buy, book, sign up, join waitlist)
   - Who lands here and where they came from (ad, search, email, referral) - this sets how much context the hero must carry
   - The problem in the reader's words, and what they use today instead
   - The real differentiator versus that alternative
   - Proof that actually exists: numbers, named customers, reviews, guarantees

2. **Write the message hierarchy before any sections.** One sentence each:
   - Promise: the outcome the reader gets
   - Mechanism: why this product delivers it when alternatives do not
   - Proof: the strongest real evidence
   - Action: the CTA and what happens right after clicking

   If you cannot fill one of these, flag the gap instead of papering over it. Every section below expands one of these four lines.

3. **Pick the framework** from the reader's awareness:
   - Reader feels the pain but has not looked for fixes: **PAS**
   - Reader is comparing options or cold from an ad: **AIDA**
   - Brand-led, story-heavy, or services business: **StoryBrand**

   Section-by-section guidance for each framework is in [references/frameworks.md](references/frameworks.md).

4. **Draft the page** in the order hero, problem, solution/features, how it works, proof, pricing (if relevant), FAQ, final CTA. Cut sections the product does not need; a waitlist page may be hero + three benefits + CTA.

5. **Write variants where they matter**: 3 headline options (different angles: outcome, pain, mechanism) and 2 CTA options. Say which you would test first and why.

6. **Run the checks below**, fix what fails, then deliver using [references/output-template.md](references/output-template.md).

## Checks before delivering

- **No invented proof.** Never make up testimonials, customer names, logos, user counts, or percentages. Use a labeled placeholder like `[TESTIMONIAL: ops lead at a customer, quote about time saved]` and list every placeholder at the end.
- **Headline test.** Could a competitor paste your headline onto their page unchanged? If yes, it is too generic. Anchor it to the mechanism or a specific outcome.
- **Benefit test.** Every feature line answers "so what?" for the reader. "Real-time sync" becomes "Your team sees the same numbers, no more version-hunting."
- **One primary action.** Every CTA on the page points to the same action. Secondary links (docs, pricing) stay visually secondary in your notes.
- **CTA text** starts with a verb and names the outcome ("Get my audit", "Start free trial"). Never "Submit" or "Click here". State friction reducers under it when true ("No card required").
- **Urgency only if real.** Deadlines, limited seats, and price changes must be true. Fake scarcity costs trust; omit urgency instead.
- **Reading level.** Short sentences, second person, present tense. Read the hero aloud; if it takes more than one breath, cut it.
- **Voice.** Match the brand voice from any existing copy the user shared. If none, default to plain and direct over hype. Drop filler adjectives (revolutionary, seamless, cutting-edge, unlock, elevate).

## Worked example

Brief: scheduling tool for independent physical therapy clinics; action is "book a demo"; readers come from a Google search for "PT clinic no-show software"; proof is one clinic that cut no-shows from 18% to 7%.

Message hierarchy:
- Promise: fewer empty appointment slots
- Mechanism: two-way text reminders that let patients reschedule in one tap instead of silently skipping
- Proof: one clinic went from 18% to 7% no-shows in 60 days
- Action: book a 20-minute demo

Hero (PAS, since searchers already feel the pain):
- Headline: "Stop losing a fifth of your schedule to no-shows"
- Subhead: "Patients reschedule by text in one tap, so the slot gets refilled instead of sitting empty."
- CTA: "Book a 20-minute demo" / under it: "See it with your own calendar"
- Proof line: "One clinic cut no-shows from 18% to 7% in 60 days" (real, from the brief)

Note what it avoids: no "revolutionary", no invented clinic count, and the headline only works for this product.

## Common failure modes

- Writing sections before the message hierarchy, which produces a page of disconnected claims.
- Opening the hero with the product name or category ("Acme is an AI-powered platform...") instead of the reader's outcome.
- An FAQ full of softballs. FAQ entries should answer the real objections: price, switching cost, setup time, security, "will this work for my case".
- Treating every page as long-form. Match length to price and risk: a free signup needs less persuasion than a five-figure contract.
