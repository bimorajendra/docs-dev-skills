"""Regression checks for confirmation coverage and answer evidence, using temporary documents.

Run: python -I -B -m unittest discover -s tests -v
"""
import importlib.util
from pathlib import Path
import re
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "skills/generate-activity/scripts/validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ConfirmationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".confirmation-", dir=ROOT / "tests")
        self.assertTrue(Path(self.temp.name).resolve().is_relative_to((ROOT / "tests").resolve()))
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name) / "docs"
        shutil.copytree(ROOT / "contoh/sop-keluhan/docs", self.docs)

    def edit(self, name, change):
        path = self.docs / name
        path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")

    def question(self, rid, change):
        def rewrite(text):
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if line.startswith(f"| {rid} |"):
                    c = VALIDATOR.cells(line)
                    # Only register rows; the answer log uses five columns.
                    if len(c) == len(VALIDATOR.OQ_HEADER):
                        change(c)
                        lines[i] = "| " + " | ".join(c) + " |"
            return "\n".join(lines) + "\n"
        self.edit("pertanyaan-terbuka.md", rewrite)

    def evidence(self, rid="OQ-05", when="2026-10-28", proof="Percakapan uji, balasan pengguna tentang sumber pembanding"):
        self.edit("pertanyaan-terbuka.md", lambda text: text +
                  f"| {rid} | Data dibandingkan dengan catatan transaksi yang dirujuk nomor order. | "
                  f"Pengguna dalam percakapan | {when} | {proof} |\n")

    def errors(self):
        return VALIDATOR.lint(self.docs)[0]

    def assert_error(self, fragment):
        errors = self.errors()
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_both_examples_and_both_standalone_validators(self):
        for skill in ("generate-activity", "generate-fsd"):
            spec = importlib.util.spec_from_file_location(skill, ROOT / "skills" / skill / "scripts/validate.py")
            validator = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validator)
            for name, count in (("sop-keluhan", 7), ("sop-pengadaan", 17)):
                with self.subTest(skill=skill, example=name):
                    base = ROOT / "contoh" / name
                    errors, _, stats, _ = validator.lint(base / "docs", base / "sop.md")
                    self.assertEqual(errors, [])
                    self.assertEqual(stats["al"], count)
                    self.assertGreater(stats["oq"], 0)

    def test_missing_activity_review_is_rejected(self):
        self.edit("pertanyaan-terbuka.md", lambda text: re.sub(r"^\| AL-003 \|.*\n", "", text, flags=re.M))
        self.assert_error("AL-003: belum memiliki tinjauan aktivitas")

    def test_closed_question_requires_answer_evidence(self):
        self.question("OQ-05", lambda c: c.__setitem__(6, "Terjawab"))
        self.assert_error("Terjawab tanpa catatan jawaban")

    def test_answered_question_cannot_leave_stale_tbd(self):
        self.question("OQ-05", lambda c: c.__setitem__(6, "Terjawab"))
        self.evidence()
        self.assert_error("TBD merujuk OQ yang sudah Terjawab")

    def test_partial_answer_can_remain_open(self):
        self.evidence()
        self.assertEqual(self.errors(), [])

    def test_confirmed_answer_can_close_after_affected_tbds_are_updated(self):
        self.question("OQ-05", lambda c: c.__setitem__(6, "Terjawab"))
        self.evidence()
        for name in ("FRD.md", "NFRD.md", "FSD.md", "TEST-CASE.md"):
            self.edit(name, lambda text: re.sub(
                r"\[TBD[^\]]*\bOQ-05\b[^\]]*\]",
                "sesuai catatan transaksi yang dirujuk nomor order (lihat OQ-05)", text))
        errors, _, stats, _ = VALIDATOR.lint(self.docs)
        self.assertEqual(errors, [])
        self.assertEqual(stats["oq"], 25)

    def test_invalid_evidence_date_is_rejected(self):
        self.evidence(when="2026-02-30")
        self.assert_error("Tanggal konfirmasi harus tanggal valid")

    def test_missing_evidence_is_rejected(self):
        self.evidence(proof="-")
        self.assert_error("catatan jawaban masih berisi kolom kosong")

    def test_duplicate_answer_is_rejected(self):
        self.evidence()
        self.evidence()
        self.assert_error("catatan jawaban: ID ganda: OQ-05")

    def test_activity_links_must_be_reciprocal(self):
        self.question("OQ-25", lambda c: c.__setitem__(2, "AL-004"))
        self.assert_error("OQ-25: belum ditautkan pada tinjauan AL-004")
        self.assert_error("Tinjauan AL-003: OQ-25 tidak mencantumkan aktivitas ini")

    def test_unknown_activity_and_priority_are_rejected(self):
        self.question("OQ-25", lambda c: (c.__setitem__(2, "AL-999"), c.__setitem__(4, "Tinggi")))
        self.assert_error("AL-999 tidak ada di Activity List")
        self.assert_error("Prioritas harus Penghambat atau Lanjutan")

    def test_tbd_needs_its_own_oq_even_when_line_has_other_citations(self):
        self.edit("FRD.md", lambda text: text + "\n[TBD: sumber pembanding] (lihat OQ-05).\n")
        self.assert_error("[TBD] tanpa OQ di dalam penanda")

    def test_sufficient_activity_needs_no_fabricated_question(self):
        text = """## Daftar pertanyaan
| ID | Pertanyaan | Aktivitas terkait | Mempengaruhi | Prioritas | Penjawab | Status |
|---|---|---|---|---|---|---|

## Tinjauan aktivitas
| Aktivitas | Hasil tinjauan | OQ terkait | Dasar tinjauan |
|---|---|---|---|
| AL-001 | Cukup dari sumber | - | Aktor, input dan hasil sudah disebut sumber. |

## Catatan jawaban
Belum ada jawaban yang diterima.
"""
        errors = []
        questions, _ = VALIDATOR.check_questions(text, {"AL-001": []}, errors)
        self.assertEqual(errors, [])
        self.assertEqual(questions, {})

    def test_matrix_links_new_question_to_its_activity(self):
        errors, _, _, texts = VALIDATOR.lint(self.docs)
        self.assertEqual(errors, [])
        VALIDATOR.matrix(self.docs, texts)
        matrix = (self.docs / "traceability.md").read_text(encoding="utf-8")
        rows = [VALIDATOR.cells(line) for line in matrix.splitlines() if line.startswith("| AL-")]
        linked = [row[0] for row in rows if "OQ-25" in row[-1]]
        self.assertEqual(linked, ["AL-003"])

    def test_requirements_stage_ignores_unfinished_later_documents(self):
        self.edit("FSD.md", lambda _: "# Belum disusun\n")
        self.edit("TEST-CASE.md", lambda _: "# Belum disusun\n")
        self.assertEqual(self.errors(), [])
        self.assertEqual(set(VALIDATOR.TEMPLATES), {"FRD.md", "NFRD.md"})

    def test_specification_stage_still_checks_its_outputs(self):
        spec = importlib.util.spec_from_file_location("spec_validator", ROOT / "skills/generate-fsd/scripts/validate.py")
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        self.edit("FSD.md", lambda _: "# Belum disusun\n")
        errors, _, _, _ = validator.lint(self.docs)
        self.assertTrue(any("FSD" in error for error in errors), errors)
        self.assertEqual(set(validator.TEMPLATES), {"FSD.md", "TEST-CASE.md"})

    def test_real_narrative_example_applies_confirmed_answers(self):
        example = ROOT / "contoh/web-penilaian"
        errors, _, stats, texts = VALIDATOR.lint_intake(example / "docs", example / "sumber.md")
        self.assertEqual(errors, [])
        self.assertEqual(stats["al"], 6)
        self.assertGreater(stats["oq"], 0)
        self.assertNotIn("FRD.md", texts)
        self.assertNotIn("NFRD.md", texts)
        errors, _, stats, _ = VALIDATOR.lint(example / "docs", example / "sumber.md")
        self.assertEqual(errors, [])
        self.assertGreater(stats["oq"], 0)
        self.assertEqual(stats["quality_gaps"], 0)

    def test_unresolved_narrative_can_be_checked_before_requirements_exist(self):
        example = ROOT / "contoh/web-penilaian"
        shutil.copytree(example / "docs", self.docs, dirs_exist_ok=True)
        initial = VALIDATOR.lint_intake(self.docs, example / "sumber.md")[2]["oq"]
        self.question("OQ-04", lambda c: c.__setitem__(6, "Terbuka"))
        self.edit("pertanyaan-terbuka.md", lambda text: re.sub(
            r"(^\| AL-002 \| )Cukup dari sumber", r"\1Perlu konfirmasi", text, flags=re.M))
        for name in ("FRD.md", "NFRD.md"):
            (self.docs / name).unlink()
        errors, _, stats, _ = VALIDATOR.lint_intake(self.docs, example / "sumber.md")
        self.assertEqual(errors, [])
        self.assertEqual(stats["oq"], initial + 1)

    def test_source_silence_is_an_unfinished_quality_review(self):
        example = ROOT / "contoh/web-penilaian"
        text = (example / "docs/NFRD.md").read_text(encoding="utf-8")
        questions = VALIDATOR.check_questions(
            (example / "docs/pertanyaan-terbuka.md").read_text(encoding="utf-8"),
            {f"AL-{i:03}": [] for i in range(1, 7)}, [])[0]
        text = re.sub(r"(### 3\.2 Performance Efficiency\n).*?(?=### 3\.3)",
                      r"\1\nTidak ada kebutuhan yang diturunkan dari sumber.\n\n", text, flags=re.S)
        warnings = []
        self.assertEqual(VALIDATOR.check_quality_review(text, questions, warnings), 1)
        self.assertTrue(any("Performance Efficiency" in warning for warning in warnings))

    def test_not_applicable_quality_needs_a_confirmed_decision(self):
        example = ROOT / "contoh/web-penilaian"
        text = (example / "docs/NFRD.md").read_text(encoding="utf-8")
        questions = VALIDATOR.check_questions(
            (example / "docs/pertanyaan-terbuka.md").read_text(encoding="utf-8"),
            {f"AL-{i:03}": [] for i in range(1, 7)}, [])[0]
        questions["OQ-99"] = list(questions["OQ-16"])
        text = re.sub(r"(### 3\.9 Safety\n).*?(?=## 4\.)",
                      r"\1\nTidak berlaku sesuai keputusan pengguna, lihat OQ-99.\n\n", text, flags=re.S)
        self.assertEqual(VALIDATOR.check_quality_review(text, questions, []), 1)
        questions["OQ-99"][6] = "Terjawab"
        self.assertEqual(VALIDATOR.check_quality_review(text, questions, []), 0)

    def test_contextual_quality_decision_needs_confirmed_answer(self):
        text = "## 3. Kebutuhan Mutu per Karakteristik\n"
        for title in VALIDATOR.CODES:
            text += f"### {title}\nKeputusan mutu terkonfirmasi: Evaluasi mengikuti FR-001, lihat OQ-99.\n"
        text += "## 4. Kepatuhan dan Regulasi\nKebijakan dikonfirmasi pada OQ-99.\n"
        questions = {"OQ-99": ["OQ-99", "Apa tujuan hasil?", "AL-001", "NFRD", "Penghambat", "Pengguna", "Terbuka"]}
        for name in ("generate-activity", "generate-fsd"):
            spec = importlib.util.spec_from_file_location(name, ROOT / "skills" / name / "scripts/validate.py")
            validator = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validator)
            with self.subTest(validator=name):
                questions["OQ-99"][6] = "Terbuka"
                self.assertGreater(validator.check_quality_review(text, questions, []), 0)
                questions["OQ-99"][6] = "Terjawab"
                self.assertEqual(validator.check_quality_review(text, questions, []), 0)
                self.assertGreater(validator.check_quality_review(text.replace(", lihat OQ-99", ""), questions, []), 0)

    def test_narrative_provenance_rejects_invented_activity(self):
        source = self.docs.parent / "sumber.md"
        source.write_text("Mentor mengisi nilai peserta bimbingannya.", encoding="utf-8")
        errors = []
        rows = {"AL-001": ["AL-001", "Narasi", "Sistem mengirim email otomatis.", "Sistem"]}
        VALIDATOR.check_activity_source(rows, source, errors)
        self.assertTrue(any("tidak ditemukan persis" in error for error in errors), errors)

    def test_numbered_source_cannot_be_silently_split(self):
        source = self.docs.parent / "sop.md"
        source.write_text("1. Mentor memeriksa dan mencatat nilai.", encoding="utf-8")
        errors = []
        rows = {"AL-001": ["AL-001", "-", "Mentor memeriksa", "Mentor"],
                "AL-002": ["AL-002", "-", "mencatat nilai.", "Mentor"]}
        VALIDATOR.check_activity_source(rows, source, errors)
        self.assertTrue(any("sumber 1 butir" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
