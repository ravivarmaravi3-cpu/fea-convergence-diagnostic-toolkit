from pathlib import Path
import re

from .models import DiagnosticReport, Finding

RULES = {
    "contact": {
        "patterns": [r"contact", r"penetration", r"pinball", r"CONTA\d+", r"TARGE\d+"],
        "suggestion": "Review contact status, initial gaps/penetration, formulation, stiffness, pinball, and scoping.",
    },
    "mesh_or_element": {
        "patterns": [r"element.*distort", r"negative.*jacobian", r"poor.*shape", r"mesh", r"highly distorted"],
        "suggestion": "Locate the reported element IDs and review local mesh quality, geometry, and element formulation.",
    },
    "constraint_or_rigid_body": {
        "patterns": [r"rigid body", r"insufficient.*constraint", r"zero pivot", r"singular", r"unconstrained"],
        "suggestion": "Check supports, joints, remote constraints, weak springs, and possible free rigid-body motion.",
    },
    "material_nonlinearity": {
        "patterns": [r"plastic", r"material", r"hyperelastic", r"creep", r"yield"],
        "suggestion": "Review material data, units, extrapolation, and nonlinear constitutive settings.",
    },
    "load_stepping": {
        "patterns": [r"time step", r"substep", r"bisection", r"cutback", r"equilibrium iteration"],
        "suggestion": "Review automatic time stepping, initial/minimum substep sizes, and the load history near divergence.",
    },
    "solver_resource": {
        "patterns": [r"out of memory", r"disk space", r"license", r"terminated", r"fatal"],
        "suggestion": "Check solver resources, licensing, termination conditions, and the earliest fatal message.",
    },
}

WARNING_RE = re.compile(r"\bwarning\b", re.IGNORECASE)
ERROR_RE = re.compile(r"\b(error|fatal)\b", re.IGNORECASE)
SUCCESS_PATTERNS = [r"solution is done", r"solve completed", r"converged"]
FAILURE_PATTERNS = [r"not converge", r"failed to converge", r"solution failed", r"analysis terminated"]


def _clean(line: str) -> str:
    return " ".join(line.strip().split())


def parse_text(text: str, source: str = "<memory>") -> DiagnosticReport:
    lines = [_clean(line) for line in text.splitlines() if line.strip()]
    warnings = [line for line in lines if WARNING_RE.search(line)]
    errors = [line for line in lines if ERROR_RE.search(line)]

    lowered = text.lower()
    failed = any(re.search(pattern, lowered) for pattern in FAILURE_PATTERNS)
    succeeded = any(re.search(pattern, lowered) for pattern in SUCCESS_PATTERNS)
    status = "failed" if failed else "converged" if succeeded else "unknown"

    findings = []
    for category, rule in RULES.items():
        evidence = []
        for line in lines:
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in rule["patterns"]):
                evidence.append(line)
        evidence = list(dict.fromkeys(evidence))[:10]
        if evidence:
            score = min(100, 25 + 15 * len(evidence))
            severity = "high" if score >= 70 else "medium" if score >= 40 else "low"
            findings.append(Finding(category, severity, score, evidence, rule["suggestion"]))

    findings.sort(key=lambda item: (-item.score, item.category))
    return DiagnosticReport(source, status, warnings, errors, findings)


def parse_file(path: str | Path) -> DiagnosticReport:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Solver output not found: {file_path}")
    text = file_path.read_text(encoding="utf-8", errors="replace")
    return parse_text(text, str(file_path))
