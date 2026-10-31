import argparse
import json
from pathlib import Path

from .parser import parse_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract diagnostic evidence from an FEA solve.out file.")
    parser.add_argument("solve_out", help="Path to solve.out or another text solver log")
    parser.add_argument("--json", dest="json_path", help="Optional JSON report output path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = parse_file(args.solve_out)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 2

    payload = report.to_dict()
    print(f"Status: {report.status}")
    print(f"Warnings: {len(report.warnings)} | Errors: {len(report.errors)}")
    if report.findings:
        print("Ranked diagnostic findings:")
        for finding in report.findings:
            print(f"- {finding.category}: {finding.severity} ({finding.score}/100), evidence={len(finding.evidence)}")
    else:
        print("No diagnostic rule matched. Manual solver review is required.")

    if args.json_path:
        output = Path(args.json_path)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"JSON report written to: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
