# Monitoring process for T5.1

How the map of open-source QKD tools stays current for the rest of the project: automated checks
every week, expert review at fixed points, and one owner for each step. The repository and the
Excel file in it are the live resource of MS5.1; the WP5 reports cite a dated snapshot of them.

## Roles

| Role | Who | Responsibility |
| --- | --- | --- |
| Maintainer | one T5.1 partner | keeps the monitor running, triages the weekly issue, edits `config.yaml` |
| Reviewers | the T5.1 partners, one per category (KMS / ETSI 014–004, network simulation, SDN / control plane, libraries) | decide on candidates, re-test tools, fill in the expert columns and the scores |
| T5.1 lead | the task leader | approves the quarterly review and the snapshot for each WP5 report |

## Schedule

| When | What | Who |
| --- | --- | --- |
| Every Monday (automatic) | the monitor updates the Excel file and opens an issue if anything changed | GitHub Actions |
| Within a week of each issue | assign each flag and candidate to the reviewer of its category, close the issue when done | maintainer |
| Within two weeks | candidates: `Add` or `Reject` with a reason in `Comment`; flags: check and update `Test status` / `Findings / Notes` | reviewers |
| Every three months | review of the whole map: re-test the tools of high priority, update the scores, the ETSI APIs and the findings | reviewers, approved by the T5.1 lead |
| Before each WP5 report | tag a release of the repository (`ms5.1-YYYY-MM`) with the Excel file and the report; the report cites that tag | maintainer |

## Rules

- The monitor writes only the columns that can be read automatically (see the README). The expert
  columns change only through a reviewer, and every automated change is logged in `Changes`.
- A flag is resolved when a reviewer has looked at it: an archived or inactive tool moves to a
  lower priority or out of the map, a new release of a tested tool gets a new test.
- A candidate is added only through `Add`; the next run puts it in the map. A rejected
  candidate stays in `Candidates` with its reason and is not proposed again.
- New areas of interest (e.g. a new ETSI specification) become new searches in `config.yaml`.
- Edits to the Excel file go through pull requests (or straight to the main branch by the
  maintainer), so that the history of the file is the history of the review.
