# Built-In Workflow Templates

Use these starting points to scaffold a workflow YAML for common shapes.

## Content Pipeline

```yaml
# Research -> Draft -> Review -> Publish
agents: [researcher, writer, editor, publisher]
pattern: sequential with review loop
use_when: "Creating any content that needs research and quality review"
```

## Multi-Angle Analysis

```yaml
# Fan-out to N analysts -> Aggregate
agents: [N domain analysts, aggregator]
pattern: parallel fan-out/fan-in
use_when: "Need multiple perspectives on a single topic"
```

## Qualify-and-Route

```yaml
# Classify -> Route to specialist
agents: [classifier, specialist_a, specialist_b, specialist_c]
pattern: conditional routing
use_when: "Different inputs need different handling"
```

## Iterative Refinement

```yaml
# Generate -> Validate -> Refine (loop) -> Deliver
agents: [generator, validator]
pattern: loop with validation
use_when: "Output must meet a quality bar and may need multiple passes"
```

## Map-Reduce

```yaml
# Split -> Process each -> Combine
agents: [splitter, processor, reducer]
pattern: map-reduce
use_when: "Large input needs to be chunked, processed, and recombined"
```
