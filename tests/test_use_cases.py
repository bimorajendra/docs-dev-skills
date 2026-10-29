"""Regression checks for the FSD use case list and scenarios, using temporary copies of the bundled example.

Run: python -I -B -m unittest discover -s tests -v
"""
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fsd_validator", ROOT / "skills/generate-fsd/scripts/validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class UseCaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".usecase-", dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name) / "docs"
        shutil.copytree(ROOT / "contoh/sop-keluhan/docs", self.docs)

    def edit(self, change, name="FSD.md"):
        path = self.docs / name
        path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")

    def errors(self):
        return VALIDATOR.lint(self.docs)[0]

    def assert_error(self, fragment):
        errors = self.errors()
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_example_has_one_use_case_per_activity(self):
        errors, _, stats, _ = VALIDATOR.lint(self.docs)
        self.assertEqual(errors, [])
        self.assertEqual(stats["uc"], stats["al"])

    def test_test_case_document_is_optional(self):
        (self.docs / "TEST-CASE.md").unlink()
        errors, _, stats, _ = VALIDATOR.lint(self.docs)
        self.assertEqual(errors, [])
        self.assertEqual(stats["tc"], 0)
        result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "skills/generate-fsd/scripts/validate.py"),
                                 str(self.docs), "--require-ready"], capture_output=True, text=True, encoding="utf-8")
        self.assertNotIn("keluaran tahap ini belum dibuat", result.stdout)
        (self.docs / "FSD.md").unlink()
        result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "skills/generate-fsd/scripts/validate.py"),
                                 str(self.docs), "--require-ready"], capture_output=True, text=True, encoding="utf-8")
        self.assertIn("FSD.md: keluaran tahap ini belum dibuat", result.stdout)

    def test_activity_without_use_case_is_rejected(self):
        self.edit(lambda text: re.sub(r"^\| UC-007 \|.*\n", "", text, flags=re.M))
        self.assert_error("AL-007: harus punya tepat satu use case")

    def test_use_case_must_sit_under_the_module_of_its_activity(self):
        self.edit(lambda text: text.replace("| UC-004 | Meneruskan tiket ke divisi terkait | 3.2 |",
                                            "| UC-004 | Meneruskan tiket ke divisi terkait | 3.1 |"))
        self.assert_error("UC-004: Modul harus modul dari AL-004")

    def test_every_use_case_needs_its_own_activity_diagram(self):
        def drop_diagram(text):
            start = text.index("**UC-002")
            at = text.index("```mermaid", start)
            return text[:at] + "```text" + text[at + len("```mermaid"):]
        self.edit(drop_diagram)
        self.assert_error("UC-002: diagram aktivitas")

    def test_two_tables_in_a_row_are_flagged(self):
        stacked = "\n".join(["| a |", "|---|", "| 1 |", "", "Alur:", "", "| b |", "|---|", "| 2 |", ""])
        self.assertEqual(VALIDATOR.stacked_tables(stacked), [7])
        spaced = stacked.replace("Alur:", "Tabel berikut memuat langkah dari awal sampai selesai.")
        self.assertEqual(VALIDATOR.stacked_tables(spaced), [])
        self.assertEqual(VALIDATOR.stacked_tables(stacked.replace("Alur:", "## Bagian")), [])

    def test_scenario_name_must_match_the_list(self):
        self.edit(lambda text: text.replace("**UC-005 — Memberikan solusi yang disetujui**", "**UC-005 — Nama lain**"))
        self.assert_error("UC-005: nama pada skenario berbeda")

    def test_use_case_without_scenario_is_rejected(self):
        self.edit(lambda text: text.replace("**UC-005 — Memberikan solusi yang disetujui**",
                                            "**UC-099 — Memberikan solusi yang disetujui**"))
        self.assert_error("UC-005 tidak punya skenario")

    def test_scenario_must_cite_every_rule_of_its_activity(self):
        self.edit(lambda text: text.replace("FR-003, FR-004, FR-005, BR-02 |", "FR-003, FR-004, BR-02 |"))
        self.assert_error("UC-001: FR-005 milik AL-001 belum dirujuk")

    def test_scenario_needs_its_attributes_and_main_flow(self):
        self.edit(lambda text: text.replace("| Pemicu | Pelanggan menyampaikan keluhan kepada CS |\n", ""))
        self.assert_error("UC-001: tabel Atribut harus memuat baris")


if __name__ == "__main__":
    unittest.main()
