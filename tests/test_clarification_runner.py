"""Exercise the clarification lifecycle, not a particular domain questionnaire."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("clarification_runner", ROOT / "skills/generate-activity/scripts/clarify.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".runner-", dir=ROOT / "tests")
        self.assertTrue(Path(self.temp.name).resolve().is_relative_to((ROOT / "tests").resolve()))
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name)
        (self.docs / "00-activity-list.md").write_text(
            "| ID | Ref SOP | Aktivitas | Aktor |\n|---|---|---|---|\n"
            "| AL-001 | - | Petugas mencatat hasil pemeriksaan. | Petugas |\n", encoding="utf-8")
        self.questions = {
            "OQ-01": ["OQ-01", "Pada pemeriksaan, hasil apa yang dicatat?", "AL-001", "FRD", "Penghambat", "Pengguna", "Terbuka"],
            "OQ-02": ["OQ-02", "Adakah sasaran mutu tambahan atau pembatasan untuk contoh pemeriksaan ini?",
                      "AL-001", "NFRD", "Penghambat", "Pengguna", "Terbuka"],
        }
        self.answers = {}
        self.write_register()

    def write_register(self):
        rows = ["## Daftar pertanyaan", "", "| " + " | ".join(RUNNER.VALIDATOR.OQ_HEADER) + " |",
                "|---|---|---|---|---|---|---|"]
        rows += ["| " + " | ".join(q) + " |" for q in self.questions.values()]
        pending = any(q[6] == "Terbuka" for q in self.questions.values())
        rows += ["", "## Tinjauan aktivitas", "", "| Aktivitas | Hasil tinjauan | OQ terkait | Dasar tinjauan |",
                 "|---|---|---|---|", "| AL-001 | " + ("Perlu konfirmasi" if pending else "Cukup dari sumber") +
                 " | " + ", ".join(self.questions) + " | Makna dan sasaran pemeriksaan ditelusuri ke jawaban. |",
                 "", "## Catatan jawaban", "", "| " + " | ".join(RUNNER.VALIDATOR.ANSWER_HEADER) + " |",
                 "|---|---|---|---|---|"]
        rows += ["| " + " | ".join(row) + " |" for row in self.answers.values()]
        (self.docs / "pertanyaan-terbuka.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

    def answer(self, rid, complete=True, text="Keputusan pengguna pada contoh uji."):
        self.questions[rid][6] = "Terjawab" if complete else "Terbuka"
        self.answers[rid] = [rid, text, "Pengguna pengujian", "2026-10-28", f"Balasan uji {rid}: {text}"]
        self.write_register()

    def send(self, *ids):
        return RUNNER.record(self.docs, "asked", list(ids), "Pesan pertanyaan pada sesi pengujian")

    def receive(self, rid):
        RUNNER.record(self.docs, "reply", [rid], f"Pesan jawaban pengguna untuk {rid}")

    def applied(self, rid):
        RUNNER.record(self.docs, "applied", [rid], f"Jawaban dan dokumen pengujian diperbarui untuk {rid}")

    def completed_decisions(self):
        for rid in list(self.questions):
            self.answer(rid)
            self.applied(rid)

    def write_outputs(self):
        """Build a small valid stage from the supplied output templates for a readiness check."""
        for name in ("FRD", "NFRD"):
            text = (ROOT / f"skills/generate-activity/assets/{name}.template.md").read_text(encoding="utf-8")
            text = re.sub(r"^> .*\n?", "", text, flags=re.M)
            text = text.replace("<Nama Proyek>", "Contoh Uji").replace("YYYY-MM-DD", "2026-10-28")
            if name == "FRD":
                module = '''## 3. Kebutuhan Fungsional

### 3.1 Modul Pemeriksaan

Sumber aktivitas: AL-001.

| ID | Pernyataan | Sumber | Alasan | Kriteria Penerimaan | Basis | Verif. |
|---|---|---|---|---|---|---|
| FR-001 | Sistem harus memungkinkan Petugas mencatat hasil pemeriksaan. | AL-001 | Jawaban OQ-01 | Diberikan pemeriksaan selesai, ketika Petugas mencatat hasil, maka hasil tersimpan. | Eksplisit | U |

'''
                text = re.sub(r"^## 3\. Kebutuhan Fungsional\n.*?(?=^## 4\.)", module, text, flags=re.M | re.S)
                text = text.replace("## 4. Keterlacakan", "## 4. Keterlacakan\n\n| Aktivitas | Modul | FR |\n|---|---|---|\n| AL-001 | 3.1 | FR-001 |")
            else:
                text = re.sub(r"(^### 3\.\d+ [^\n]+\n).*?(?=^#{2,3} |\Z)",
                              lambda m: m[1] + "\nTidak berlaku sesuai keputusan pengguna untuk contoh ini, lihat OQ-02.\n\n",
                              text, flags=re.M | re.S)
                text = text.replace("## 4. Kepatuhan dan Regulasi", "## 4. Kepatuhan dan Regulasi\n\nTidak berlaku sesuai keputusan pengguna untuk contoh ini, lihat OQ-02.")
            path = self.docs / f"{name}.md"
            path.write_text(text, encoding="utf-8")
            RUNNER.VALIDATOR.write_toc(path)

    def test_questions_are_derived_from_current_register(self):
        self.questions["OQ-01"][1] = "Pada kegiatan unik ini, apa arti fragmen yang belum jelas?"
        self.write_register()
        result = RUNNER.next_action(self.docs, limit=1)
        self.assertEqual(result["action"], "ask")
        self.assertEqual(result["questions"][0]["question"], self.questions["OQ-01"][1])

    def test_waiting_batch_is_not_resent_even_with_unasked_questions(self):
        self.send("OQ-01")
        self.assertEqual(RUNNER.next_action(self.docs)["action"], "wait")
        with self.assertRaises(ValueError):
            self.send("OQ-01")

    def test_reply_must_be_applied_before_next_batch(self):
        self.send("OQ-01")
        self.receive("OQ-01")
        self.assertEqual(RUNNER.next_action(self.docs)["action"], "apply_reply")
        with self.assertRaises(ValueError):
            self.send("OQ-01")
        self.answer("OQ-01")
        self.applied("OQ-01")
        result = RUNNER.next_action(self.docs)
        self.assertEqual(result["action"], "ask")
        self.assertEqual([q["id"] for q in result["questions"]], ["OQ-02"])

    def test_full_cycle_needs_outputs_before_completion(self):
        for rid in list(self.questions):
            self.assertEqual(RUNNER.next_action(self.docs, limit=1)["questions"][0]["id"], rid)
            self.send(rid)
            self.receive(rid)
            self.answer(rid)
            self.applied(rid)
        self.assertEqual(RUNNER.next_action(self.docs)["action"], "draft")
        self.write_outputs()
        self.assertEqual(RUNNER.next_action(self.docs)["action"], "complete")

    def test_partial_reply_stays_open_and_unseen_gap_is_not_starved(self):
        self.send("OQ-01")
        self.receive("OQ-01")
        self.answer("OQ-01", complete=False, text="Baru sebagian hasil dijelaskan.")
        self.applied("OQ-01")
        result = RUNNER.next_action(self.docs)
        self.assertEqual([q["id"] for q in result["questions"]], ["OQ-02"])
        self.answer("OQ-02")
        self.applied("OQ-02")
        result = RUNNER.next_action(self.docs)
        self.assertEqual(result["questions"][0]["id"], "OQ-01")
        self.assertIn("sebagian", result["questions"][0]["answer_so_far"])

    def test_explicit_deferral_does_not_close_questions_or_complete(self):
        with self.assertRaises(ValueError):
            RUNNER.record(self.docs, "defer", ["OQ-01"], "", "Belum diputuskan")
        with self.assertRaises(ValueError):
            RUNNER.record(self.docs, "defer", ["OQ-01"], "Pengguna meminta draft", "")
        for rid in self.questions:
            RUNNER.record(self.docs, "defer", [rid], "Balasan pengguna meminta menunda", "Tunda untuk draft")
        self.assertEqual(RUNNER.next_action(self.docs)["action"], "deliver_draft")
        self.assertEqual(RUNNER.context(self.docs)[0]["OQ-01"][6], "Terbuka")

    def test_state_is_persistent_and_bad_batch_does_not_write(self):
        self.send("OQ-01")
        before = (self.docs / RUNNER.STATE_NAME).read_bytes()
        with self.assertRaises(ValueError):
            self.send("OQ-02", "OQ-99")
        self.assertEqual((self.docs / RUNNER.STATE_NAME).read_bytes(), before)
        self.assertEqual(RUNNER.load_state(self.docs)["questions"]["OQ-01"]["phase"], "waiting")

    def test_applied_requires_an_updated_answer_log(self):
        with self.assertRaises(ValueError):
            self.applied("OQ-01")
        self.answer("OQ-01", complete=False)
        self.applied("OQ-01")
        self.send("OQ-01")
        self.receive("OQ-01")
        with self.assertRaises(ValueError):
            self.applied("OQ-01")

    def test_stale_tbd_blocks_application_and_completion(self):
        self.completed_decisions()
        self.write_outputs()
        path = self.docs / "FRD.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n[TBD: hasil, lihat OQ-01]\n", encoding="utf-8")
        self.assertEqual(RUNNER.next_action(self.docs)["action"], "repair")
        with self.assertRaises(ValueError):
            self.applied("OQ-01")

    def test_strict_validator_rejects_a_valid_but_unfinished_draft(self):
        self.completed_decisions()
        self.write_outputs()
        self.questions["OQ-03"] = ["OQ-03", "Apa keputusan tambahan ini?", "AL-001", "FRD", "Lanjutan", "Pengguna", "Terbuka"]
        self.write_register()
        command = [sys.executable, "-I", "-B", str(ROOT / "skills/generate-activity/scripts/validate.py"), str(self.docs)]
        regular = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        strict = subprocess.run(command + ["--require-ready"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(regular.returncode, 0, regular.stdout)
        self.assertEqual(strict.returncode, 3, strict.stdout)
        self.assertIn("BELUM SIAP", strict.stdout)

    def test_specification_final_gate_requires_its_own_outputs(self):
        self.completed_decisions()
        self.write_outputs()
        command = [sys.executable, "-I", "-B", str(ROOT / "skills/generate-fsd/scripts/validate.py"),
                   str(self.docs), "--require-ready"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("keluaran tahap ini belum dibuat", result.stdout)

    def test_runner_cli_exit_codes_are_actionable(self):
        command = [sys.executable, "-I", "-B", str(ROOT / "skills/generate-activity/scripts/clarify.py"), str(self.docs), "next"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 3, result.stdout)
        self.send("OQ-01")
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 4, result.stdout)

    def test_corrupt_state_fails_closed(self):
        state = {"version": 1, "questions": {"OQ-01": []}, "history": []}
        (self.docs / RUNNER.STATE_NAME).write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaises(ValueError):
            RUNNER.next_action(self.docs)

    def test_changed_decision_is_not_silently_kept_deferred(self):
        RUNNER.record(self.docs, "defer", ["OQ-01"], "Pengguna menunda keputusan lama", "Tunda")
        self.answer("OQ-02")
        self.applied("OQ-02")
        self.questions["OQ-01"][1] = "Apa arti fragmen baru yang mengubah keputusan sebelumnya?"
        self.write_register()
        result = RUNNER.next_action(self.docs)
        self.assertEqual(result["action"], "ask")
        self.assertEqual(result["questions"][0]["id"], "OQ-01")

    def test_current_source_failure_prevents_completion(self):
        self.completed_decisions()
        self.write_outputs()
        source = self.docs / "sop.md"
        source.write_text("1. Aktivitas berbeda dari ekstraksi yang disimpan.\n", encoding="utf-8")
        self.assertEqual(RUNNER.next_action(self.docs, source=source)["action"], "repair")


if __name__ == "__main__":
    unittest.main()
