# HarmoniQCI T5.1 monitor

Keeps the T5.1 map of open-source QKD tools (`data/HARMONIQCI_open_source_tools.xlsx`) up to
date. Every week it reads each tool where it is published (GitHub, GitLab, the ETSI Forge, Zenodo,
PyPI), writes what changed into the Excel file, searches the same places for new ETSI QKD tools
and opens an issue with a report for the expert review. The process around it (who reviews what
and when) is in [PROCESS.md](PROCESS.md).

## Features

1. **Additions.** Candidates that an expert marked `Add` in the sheet `Candidates` become
   rows of `Tool map` and of `Scoring`, with the expert columns set to
   `To be checked` / `To evaluate`.
2. **Update.** Every tool is read from where its link points:

   | Link | Read from | Fields |
   | --- | --- | --- |
   | `github.com/...` | GitHub API | last commit, latest release, license, Docker files in the root, archived, stars, language |
   | `gitlab.com/...`, `forge.etsi.org/rep/...` and the other hosts in `config.yaml` | GitLab API | the same |
   | `zenodo.org/records/...`, `doi.org/10.5281/zenodo...` | Zenodo API | latest version and its date, license |
   | `pypi.org/project/...` | PyPI JSON API | latest version and its date, license |
   | anything else (QuKayDee, NetSquid) | the page itself | whether it is online |

3. **Discovery.** The searches in `config.yaml` on GitHub, on each GitLab host, on Zenodo (software
   records) and, when `LIBRARIES_IO_KEY` is set, on Libraries.io for packages (PyPI has no search
   API of its own). A result is proposed when it is not in the map yet (also not as the GitHub
   repository behind a Zenodo record or a package), is not a fork, is not archived, was updated
   within `max_age_days` and its name or description is about QKD networks or ETSI. A source that
   cannot be reached is listed in the report and the run goes on with the others.
4. **Output.** The Excel file is saved, every change is logged in the sheet `Changes` (date, tool,
   field, old value, new value) and `reports/latest.md` lists the changes, the flags for review and
   the new candidates.

## Excel columns

| Written by the monitor | Written by the experts only |
| --- | --- |
| `Last commit`, `Latest release`, `Archived`, `Stars`, `Flags`, `Last checked` | `Category / Layer`, `What it does`, `ETSI APIs`, `Test status`, `Findings / Notes`, `Test priority`, the sheet `Scoring` |
| `License`, `Language`, `Docker`: only when the cell is empty or `To be checked`, the license also when it is an SPDX ID that changed, Docker also from `No` to `Yes` | free text in these cells (e.g. `BSD-style (Argonne)`) stays as written |
| `Link`: when the repository moved | |

`Flags` holds what needs a look: archived, no commit for `stale_days`, new release,
license changed, repository moved or missing, Docker files no longer in the root, page offline.

## Usage

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GITHUB_TOKEN=<GitHub token>        # optional: higher rate limits, private repositories
export GITLAB_TOKEN=<gitlab.com token>     # optional
export LIBRARIES_IO_KEY=<API key>          # optional: search of PyPI packages (free key on libraries.io)
python monitor.py                  # update, discover, save
python monitor.py --dry-run        # report only, Excel file unchanged
python monitor.py --no-discovery   # only the tools already in the map
python -m pytest -q                # tests, against a fake GitHub API
```

Close the Excel file before a run: the monitor saves over it.

## GitHub Actions

`.github/workflows/monitor.yml` runs every Monday and on demand (Actions, "Run workflow"). It
commits the updated Excel file and report, and opens an issue when something changed or a new
candidate turned up. It uses the token GitHub gives every workflow, which reads public
repositories only. For a private repository in the map (such as `swtoskon33/qkd-simulator` while
it is private), add a repository secret `MONITOR_TOKEN`: a fine-grained token with read access to
the contents and metadata of that repository. `LIBRARIES_IO_KEY`, `GITLAB_TOKEN` and `ZENODO_TOKEN`
can be added as secrets the same way.

## Configuration

`config.yaml`: the Excel file and sheet names, `stale_days`, the relevance filter and the searches
of each source (GitHub search syntax, plain words for GitLab, Elasticsearch syntax for Zenodo),
and the GitLab hosts.
