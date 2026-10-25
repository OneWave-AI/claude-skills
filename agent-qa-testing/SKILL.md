---
name: agent-qa-testing
description: Run selected agent-qa web tests and interpret their recorded results. Use when a project already uses agent-qa or the user chooses it to verify a browser flow, investigate a failed or healed run, or inspect the memory used by a test.
---

# agent-qa testing

[agent-qa](https://github.com/vostride/agent-qa) combines natural-language testing with advanced memidex memory and self-improvement. Use it to gather evidence for the requested user flow. A selected test passing does not establish that the whole application works.

## Establish the target

Read the project's instructions, `agent-qa.config.yaml`, and requested tests. Match the selected target to the authorized URL, environment, and app revision. Preserve the project's provider, test data, and expected outcomes.

Use the installed CLI through the project's package manager. The npm examples use `--no-install` to avoid downloading another version. agent-qa 0.2.3 requires Node.js 24+; live web runs also need the configured browser and model provider. If setup is missing, name the prerequisite instead of installing or initializing a project as a side effect.

```bash
npx --no-install agent-qa --version
npx --no-install agent-qa run --help
```

Run from the configuration directory. Put a global `--config <path>` before the command. The printed version is output, not a subcommand. If installed help differs, check the [current CLI reference](https://vostride.com/docs/agent-qa/cli) before using an option.

## Validate and select

Replace `tests/checkout.yaml` with the requested test path:

```bash
npx --no-install agent-qa validate tests/checkout.yaml
npx --no-install agent-qa run tests/checkout.yaml --dry-run
```

Validation checks structure. Dry run discovers tests without exercising the app. Confirm the selected test IDs and target; neither command proves the flow passes. An empty selection stays unresolved rather than expanding to every test.

## Execute within the agreed scope

Live runs can change application data and incur provider costs. Use authorized test accounts and disposable fixtures. Keep external actions, payments, and messages within the user's requested scope.

For authorized execution, keep the same selection and choose a report path that preserves prior evidence:

```bash
npx --no-install agent-qa run tests/checkout.yaml --junit-output results.xml
```

Keep the exit status and run ID before retrying. Verify the report exists; a successful dry run does not establish a JUnit artifact. `doctor` can contact the model provider, so it is not an offline validation command.

## Read the result and its memory

```bash
npx --no-install agent-qa runs list --json
npx --no-install agent-qa runs overview RUN_ID --json
npx --no-install agent-qa runs knowledge RUN_ID --json
```

Bind `RUN_ID` to the selected test, target, and inspected app revision.

| Evidence | Interpretation |
|---|---|
| Exit `0` | Passed or healed. Read the verdict and explain any healing. |
| Exit `1` | A test failed or timed out, or a required file was missing. Inspect the cause before calling it an app defect. |
| Exit `2` | Execution could not start. |
| Exit `130` | Cancelled; retain partial evidence. |
| No completed verdict or `evidence-incomplete` | Unverified. A partial run is not a completed result. |

An empty failed-only list does not prove success. A healed run needs an explanation of the correction and confirmation that the original expected outcome still holds.

The knowledge view shows what memidex supplied or learned. Use `knowledge inspect --json` and the [memory inspection guide](https://vostride.com/docs/agent-qa/memory/inspect) for a relevant record. Memory is diagnostic context, not independent acceptance evidence.

## Correct and report

Distinguish an application defect, an incorrect expectation, and an environment or provider failure. Keep the first failure and its evidence. After an authorized correction, rerun only the affected selection. Stop when no new evidence supports another attempt.

Never weaken assertions or erase memory/cache records to obtain a pass. Clean up only the fixtures created for this check. Keep credentials and sensitive application data out of shared findings.

Report the selected flow and target, exact command and exit, run ID, verdict, available evidence/report paths, and remaining checks. State whether the app actually ran. Preserve uncertainty when evidence is incomplete, and keep visual, accessibility, and other untested claims separate.
