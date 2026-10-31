from dataclasses import asdict, dataclass, field


@dataclass
class Finding:
    category: str
    severity: str
    score: int
    evidence: list[str] = field(default_factory=list)
    suggestion: str = "Review the cited solver evidence."


@dataclass
class DiagnosticReport:
    source: str
    status: str
    warnings: list[str]
    errors: list[str]
    findings: list[Finding]

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "status": self.status,
            "warnings": self.warnings,
            "errors": self.errors,
            "findings": [asdict(item) for item in self.findings],
        }
