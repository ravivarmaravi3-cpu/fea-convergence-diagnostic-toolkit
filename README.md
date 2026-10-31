# FEA Convergence Diagnostic Toolkit

A work-in-progress Python toolkit for extracting and organizing convergence evidence from ANSYS Mechanical solver text output.

> Independent open-source project. Not affiliated with, endorsed by, or supported by Ansys, Inc. ANSYS is a trademark of its respective owner.

## Current V0.1 capability

- Parses `solve.out` text files
- Detects convergence success/failure phrases
- Extracts warning and error lines
- Classifies evidence into contact, mesh/element, constraint/rigid-body, material, load-stepping, and solver-resource categories
- Produces a ranked diagnostic summary with evidence
- Exports results as JSON from a command-line interface
- Includes unit tests and synthetic sample data

The classifier reports **diagnostic findings**, not guaranteed root causes. Engineering review remains necessary.

## Planned work

- Parse `ds.dat`, `.cnd`, and `.gst`
- Correlate contact real-constant IDs across files
- Extract load-step, substep, and equilibrium-iteration history
- Build an interactive dashboard
- Compare two solver runs
- Add sanitized fixtures covering more nonlinear failure modes

## Quick start

Requires Python 3.10 or newer.

```bash
python -m pip install -e .
fea-diagnose sample_data/sample_solve.out
```

Write JSON to a file:

```bash
fea-diagnose sample_data/sample_solve.out --json report.json
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Repository scope

Only synthetic or properly sanitized solver outputs should be committed. Do not upload confidential customer, employer, university, or proprietary simulation data.
