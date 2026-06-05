# Monitoring Dimensions

Six dimensions, each with what to monitor, an analysis framework, a detection protocol, and a snapshot output format.

## 1. Pricing Intelligence

Monitor:
- Pricing tiers and their features
- Price points for each tier
- Free tier limitations
- Enterprise/custom pricing indicators
- Discount patterns (annual vs monthly)
- Add-on pricing
- Usage-based pricing thresholds

Analysis framework:
- Price positioning relative to the user's company (premium, parity, value)
- Price-to-feature ratio comparison
- Recent price changes (increases signal confidence, decreases signal desperation or competitive pressure)
- Packaging strategy (all-in-one vs modular)
- Free tier strategy (generous free tier = land-and-expand, restrictive = enterprise focus)

Detection protocol:
1. Fetch the competitor's pricing page using WebFetch.
2. Extract all pricing data points into structured format.
3. Compare against the most recent pricing snapshot.
4. Flag any changes with magnitude and direction.
5. Classify changes: minor adjustment, major restructure, new tier, removed tier.

Output format:
```markdown
## Pricing Snapshot: [Competitor Name] - [Date]

### Current Pricing
| Tier | Price (Monthly) | Price (Annual) | Key Features |
|------|----------------|----------------|--------------|
| ... | ... | ... | ... |

### Changes Detected
- [CHANGE] [Tier]: [Old price] -> [New price] ([% change])
- [NEW] [Tier name]: [Details]
- [REMOVED] [Tier name]: [Was priced at X]

### Analysis
[What this pricing change signals about their strategy]
```

## 2. Feature Intelligence

Monitor:
- Product feature lists on marketing pages
- Feature comparison tables
- Changelog/release notes
- Integration pages
- API documentation updates

Analysis framework:
- Feature parity: which features do they have that the user does not, and vice versa?
- Feature velocity: how fast are they shipping new features?
- Feature direction: what categories of features are they investing in?
- Integration strategy: which platforms are they integrating with?
- Technical differentiation: any unique technical capabilities?

Detection protocol:
1. Fetch feature pages, changelog, and integration pages.
2. Extract feature lists into structured format.
3. Compare against previous snapshot.
4. Identify new features, removed features, and upgraded features.
5. Categorize features by product area.

Output format:
```markdown
## Feature Snapshot: [Competitor Name] - [Date]

### New Features (since last check)
- [Feature name]: [Description] - [Product area]

### Feature Comparison
| Feature Area | Us | Them | Gap |
|-------------|-----|------|-----|
| ... | ... | ... | ... |

### Analysis
[What their feature roadmap signals about strategic direction]
```

## 3. Content Intelligence

Monitor:
- Blog posts (titles, topics, frequency)
- Case studies and customer stories
- Whitepapers and reports
- Webinar announcements
- Documentation changes
- Press releases

Analysis framework:
- Content velocity: how often are they publishing?
- Topic focus: what themes dominate their content?
- Audience targeting: who are they writing for (persona, industry, role)?
- SEO strategy: what keywords are they targeting?
- Thought leadership positioning: what narrative are they building?
- Customer proof: which logos and industries are they showcasing?

Detection protocol:
1. Fetch blog/resource pages using WebFetch.
2. Search for recent content using WebSearch with site-specific queries.
3. Extract titles, dates, topics, and summaries.
4. Compare against previous content snapshot.
5. Identify new content, content themes, and publishing cadence.

Output format:
```markdown
## Content Snapshot: [Competitor Name] - [Date]

### New Content (since last check)
| Date | Type | Title | Topic/Theme | Target Audience |
|------|------|-------|-------------|-----------------|
| ... | ... | ... | ... | ... |

### Content Strategy Analysis
- Publishing frequency: [X posts/week]
- Top themes: [list]
- Target personas: [list]
- Notable content: [any standout pieces]

### Gaps and Opportunities
[Content themes they cover that the user does not, and vice versa]
```

## 4. Hiring Intelligence

Monitor:
- Open job postings (roles, departments, locations)
- Role descriptions and requirements
- Seniority levels being hired
- Technical stack mentioned in job postings
- Growth rate of team (if visible)

Analysis framework:
- Hiring velocity: how many open roles? Growing or shrinking?
- Department focus: where are they investing? (Engineering, Sales, Marketing, Support)
- Technical signals: what technologies appear in job descriptions?
- Seniority signals: hiring senior leaders = new initiative. Hiring junior = scaling.
- Geographic signals: new offices, remote expansion, market entry.
- Role titles: new roles (e.g., "AI Product Manager") signal strategic bets.

Detection protocol:
1. Search for job postings using WebSearch: "[Company] careers", "[Company] jobs".
2. Fetch their careers page if available.
3. Extract role titles, departments, locations, and key requirements.
4. Compare against previous hiring snapshot.
5. Identify new roles, filled roles, and pattern changes.

Output format:
```markdown
## Hiring Snapshot: [Competitor Name] - [Date]

### Open Roles
| Role | Department | Location | Seniority | Key Skills |
|------|-----------|----------|-----------|------------|
| ... | ... | ... | ... | ... |

### Hiring Patterns
- Total open roles: [X]
- Department breakdown: Engineering [X], Sales [X], Marketing [X], Other [X]
- New roles since last check: [list]
- Filled/removed roles: [list]

### Strategic Signals
[What their hiring tells us about their plans]
```

## 5. Social/PR Intelligence

Monitor:
- Funding announcements
- Partnership announcements
- Award wins
- Executive changes
- Conference appearances
- Media coverage

Detection protocol:
1. Search recent news using WebSearch: "[Company] news", "[Company] announcement".
2. Check for funding rounds, partnerships, and executive moves.
3. Note any conference/event mentions.

## 6. Technical Intelligence

Monitor:
- Technology stack changes (visible in job postings, documentation, or technical blog posts)
- API changes and versioning
- Infrastructure signals (status pages, CDN changes)
- Open source contributions
- Patent filings
