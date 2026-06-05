# Visual Representation and Reporting

## Visual Workflow Representation

When presenting workflows to users, render them as text-based diagrams.

### Sequential

```
[1. Researcher] --> [2. Pain Identifier] --> [3. Pricing] --> [4. Writer] --> [5. Reviewer]
```

### Parallel Fan-Out/Fan-In

```
                    /--> [2a. Firmographic Scorer] --\
[1. Prepare Data] -+--> [2b. Technographic Scorer] --+--> [3. Aggregator]
                    \--> [2c. Intent Scorer] --------/
```

### Conditional

```
                        /--> [3a. Hot Lead Handler] (score >= 80)
[1. Research] --> [2. Score] --+--> [3b. Warm Lead Handler] (40 <= score < 80)
                        \--> [3c. Cold Lead Handler] (score < 40)
```

### Loop

```
[1. Writer] --> [2. Reviewer] --PASS--> [3. Deliver]
     ^                |
     |              FAIL
     \--- feedback ---/
     (max 3 iterations)
```

## Execution Report Template

After workflow completion, present the results in this format.

```
## Workflow Execution Report: [workflow name]

### Execution Summary
- Status: COMPLETE / PARTIAL / FAILED
- Total steps: N
- Steps completed: N
- Steps failed: N
- Steps skipped: N
- Total agents deployed: N
- Total time: Xm Ys
- Retries used: N

### Step-by-Step Results
| Step | Agent | Status | Duration | Retries | Output Size |
|------|-------|--------|----------|---------|-------------|
| 1 | researcher | SUCCESS | 45s | 0 | 2.1KB |
| 2 | pain_identifier | SUCCESS | 30s | 0 | 1.4KB |
| 3 | pricing | SUCCESS | 35s | 1 | 1.8KB |
| 4 | writer | SUCCESS | 90s | 0 | 8.2KB |
| 5 | reviewer | SUCCESS | 40s | 0 | 0.9KB |

### Final Output
[The workflow's final deliverable]

### Issues and Warnings
- [Any retries, fallbacks, or validation warnings]
- [Agent notes or flags]
```
