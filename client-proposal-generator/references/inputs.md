# Inputs

Collect from the user or extract from conversation context.

## Required
- `client_name` -- The prospect company name (the one truly required field)
- `contact_name` -- Primary contact who receives the proposal
- `problem_description` -- What problem they need solved (a vague description works)
- `your_company` -- The firm name (default to the user's context)

## Optional (infer or default if absent)
- `rough_scope` -- Known scope details (timeline, budget range, team size)
- `your_services` -- Description of service offerings
- `pricing_model` -- fixed | retainer | milestone | hourly | hybrid (default: 3-tier fixed)
- `proposal_tone` -- consultative | enterprise | startup | technical (default: consultative)
- `include_case_studies` -- boolean (default: false; fabricated case studies are worse than none)
- `output_path` -- Where to write the file (default: current directory)
- `currency` -- USD | EUR | GBP | etc. (default: USD)

For a one-liner such as "Write a proposal for Acme Corp about redesigning their data pipeline," extract what is given and infer the rest.
