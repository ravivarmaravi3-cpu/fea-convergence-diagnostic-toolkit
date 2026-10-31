import unittest

from fea_diagnostics.parser import parse_text


class ParserTests(unittest.TestCase):
    def test_contact_failure_is_ranked(self):
        text = """
        WARNING: Contact pair 17 has excessive penetration.
        Bisection performed at substep 8.
        ERROR: Solution failed to converge.
        """
        report = parse_text(text)
        self.assertEqual(report.status, "failed")
        self.assertEqual(len(report.warnings), 1)
        self.assertEqual(len(report.errors), 1)
        categories = [finding.category for finding in report.findings]
        self.assertIn("contact", categories)
        self.assertIn("load_stepping", categories)

    def test_success_status(self):
        report = parse_text("The solve completed. The solution is done.")
        self.assertEqual(report.status, "converged")

    def test_unknown_status(self):
        report = parse_text("Solver initialization information only.")
        self.assertEqual(report.status, "unknown")


if __name__ == "__main__":
    unittest.main()
