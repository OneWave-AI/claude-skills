# Edge Cases and Special Handling

## Insufficient Content

If fewer than 3,000 words are available:
- Proceed with analysis but mark all findings as "Low Confidence"
- Recommend specific additional content to provide
- Generate a partial guide with clear "[NEEDS MORE DATA]" markers

## Multiple Distinct Voices

If the content clearly reflects multiple authors with different styles:
- Note the range of variation for each dimension
- Recommend which voice to standardize on (or present options)
- Flag the most divergent content with specific examples

## Heavily Templated Content

If content is mostly boilerplate or template-driven:
- Separate templated elements from original writing
- Analyze only original content for voice extraction
- Note which templates are in use and whether they align with the organic voice

## Regulated Industries

If the company operates in a regulated space (finance, healthcare, legal):
- Flag mandatory language and disclosures separately from voice choices
- Note where regulatory requirements constrain voice options
- Suggest how to maintain brand voice within compliance boundaries

## Brand in Transition

If the user mentions a rebrand or voice evolution:
- Analyze current state and document it as "Current Voice"
- Ask about aspirational direction
- Generate a transition guide with "Current -> Target" mappings
- Suggest a phased rollout for voice changes

## Interaction Patterns

### URL-Based Analysis
```
User: Analyze the brand voice for https://example.com
Action: WebFetch homepage, about page, blog index. Follow links to collect
        5+ blog posts. Search for social media accounts. Build corpus.
        Run full analysis. Generate guide.
```

### File-Based Analysis
```
User: Here are our last 20 blog posts in /content/blog/
Action: Glob for markdown/text files. Read all posts. Compute metrics
        per post and aggregate. Run full analysis. Generate guide.
```

### Mixed Sources
```
User: Our website is example.com, here are some emails in /marketing/emails/,
      and I'll paste some social posts.
Action: Collect from all three sources. Analyze each channel independently
        first, then cross-compare. Note channel-specific variations.
        Generate guide with per-channel tone adjustments.
```

### Content Review
```
User: Review this blog post against our brand voice guide
Action: Load brand-voice-guide.md. Analyze the draft. Score on all
        dimensions. Flag issues with fixes. Present structured review.
```

### Competitive Voice Comparison
```
User: Compare our voice to [competitor]
Action: Analyze both brands independently. Create side-by-side comparison
        on all dimensions. Identify differentiation opportunities.
        Suggest how to sharpen distinctive voice elements.
```
