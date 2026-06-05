# Inputs

Collect from the user, or extract from conversation context.

## Required Inputs
- `client_name` -- The prospect company name
- `contact_name` -- Primary contact (who receives the proposal)
- `problem_description` -- What problem they need solved (even a vague description works)
- `your_company` -- The firm name (or default to what is in the user's context)

## Optional Inputs (inferred or defaulted if not provided)
- `rough_scope` -- Any known scope details (timeline, budget range, team size)
- `your_services` -- Description of the service offerings
- `pricing_model` -- fixed | retainer | milestone | hourly | hybrid (default: 3-tier fixed)
- `proposal_tone` -- consultative | enterprise | startup | technical (default: consultative)
- `include_case_studies` -- boolean (default: false, since fabricated case studies are worse than none)
- `output_path` -- Where to write the file (default: current directory)
- `currency` -- USD | EUR | GBP | etc. (default: USD)

If the user gives a one-liner like "Write a proposal for Acme Corp about redesigning their data pipeline," extract what is available and infer the rest.
