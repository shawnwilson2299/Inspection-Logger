import unittest

from inspection_logger import Inspection, acceptance_limits, verdict_for


def defects(severity: str, count: int) -> list[dict[str, str]]:
    return [{"severity": severity, "description": f"test defect {n}"} for n in range(count)]


class VerdictTests(unittest.TestCase):
    # The six required cases from the brief.
    def test_45_with_3_major_is_accepted(self):
        self.assertEqual(verdict_for(45, defects("major", 3)), "ACCEPT")

    def test_45_with_4_major_is_rejected(self):
        self.assertEqual(verdict_for(45, defects("major", 4)), "REJECT")

    def test_44_with_3_major_is_rejected(self):
        self.assertEqual(verdict_for(44, defects("major", 3)), "REJECT")

    def test_159_with_6_major_is_rejected(self):
        self.assertEqual(verdict_for(159, defects("major", 6)), "REJECT")

    def test_160_with_6_major_is_accepted(self):
        self.assertEqual(verdict_for(160, defects("major", 6)), "ACCEPT")

    def test_70_with_critical_is_rejected(self):
        self.assertEqual(verdict_for(70, defects("critical", 1)), "REJECT")

    def test_no_defects_is_accepted(self):
        self.assertEqual(verdict_for(45, []), "ACCEPT")

    def test_sample_size_below_one_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "at least 1"):
            verdict_for(0, [])

    def test_minor_count_exactly_at_limit_is_accepted(self):
        self.assertEqual(verdict_for(45, defects("minor", 7)), "ACCEPT")

    def test_minor_count_over_limit_is_rejected(self):
        self.assertEqual(verdict_for(45, defects("minor", 8)), "REJECT")

    def test_boundary_row_selection(self):
        self.assertEqual(acceptance_limits(44), (1, 3))
        self.assertEqual(acceptance_limits(45), (3, 7))
        self.assertEqual(acceptance_limits(159), (3, 7))
        self.assertEqual(acceptance_limits(160), (6, 14))
        self.assertEqual(acceptance_limits(900), (12, 28))


class InspectionTests(unittest.TestCase):
    def test_recorded_defect_is_listable_and_used_for_verdict(self):
        inspection = Inspection("BATCH-1", 45)
        inspection.record_defect(" Major ", "rough edge")
        self.assertEqual(inspection.defects[0]["description"], "rough edge")
        self.assertEqual(inspection.verdict(), "ACCEPT")

    def test_invalid_severity_is_refused(self):
        inspection = Inspection("BATCH-1", 45)
        with self.assertRaisesRegex(ValueError, "critical, major, or minor"):
            inspection.record_defect("low", "rough edge")


if __name__ == "__main__":
    unittest.main()
