"""Persistent clarification runner; questions come from the current OQ register.

Usage: python -I clarify.py <docs> next [--limit 3] [--source source.md]
       python -I clarify.py <docs> asked|reply|applied OQ-01 ... --evidence <reference>
       python -I clarify.py <docs> defer OQ-01 ... --evidence <user reply> --reason <decision>

next exit codes: 0 complete, 1 repair, 3 ask, 4 wait, 5 apply_reply,
6 draft, 7 deliver_draft. Mutations record evidence; they never answer an OQ.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


SPEC = importlib.util.spec_from_file_location("requirements_validator", Path(__file__).with_name("validate.py"))
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
STATE_NAME = ".clarification-state.json"
EXIT_CODES = {"complete": 0, "repair": 1, "ask": 3, "wait": 4,
              "apply_reply": 5, "draft": 6, "deliver_draft": 7}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def context(docs):
    errors = []
    activities = VALIDATOR.read_activities(VALIDATOR.read(docs / "00-activity-list.md"), errors)
    question_text = VALIDATOR.read(docs / "pertanyaan-terbuka.md")
    questions, _ = VALIDATOR.check_questions(question_text, activities, errors)
    answers = {c[0]: c for header, rows in VALIDATOR.tables(
        VALIDATOR.h2_text(question_text, "catatan jawaban"))
        if header == VALIDATOR.ANSWER_HEADER for c in rows if len(c) == len(header)}
    if errors:
        raise ValueError("; ".join(errors))
    return questions, answers


def load_state(docs):
    path = docs / STATE_NAME
    if not path.exists():
        return {"version": 1, "questions": {}, "history": []}
    state = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(state, dict) or state.get("version") != 1
            or not isinstance(state.get("questions"), dict) or not isinstance(state.get("history"), list)):
        raise ValueError("State klarifikasi tidak valid; pertahankan berkas dan periksa isinya.")
    phases = {"waiting", "reply_received", "followup", "closed", "deferred"}
    for rid, entry in state["questions"].items():
        if (not isinstance(rid, str) or not isinstance(entry, dict) or entry.get("phase") not in phases
                or not isinstance(entry.get("evidence"), str) or not entry["evidence"].strip()
                or not isinstance(entry.get("question"), str)):
            raise ValueError(f"State {rid} tidak valid; periksa bukti dan fase klarifikasi.")
    return state


def save_state(docs, state):
    path = docs / STATE_NAME
    pending = path.with_suffix(".json.tmp")
    pending.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pending.replace(path)


def item(rid, row, answer=None):
    return {"id": rid, "question": row[1], "activities": row[2], "affects": row[3],
            "priority": row[4], "answer_so_far": answer[1] if answer else None}


def next_action(docs, limit=3, source=None):
    if limit < 1:
        raise ValueError("limit minimal 1")
    questions, answers = context(docs)
    state = load_state(docs)
    entries = state["questions"]
    opened = {rid: row for rid, row in questions.items() if row[6] == "Terbuka"}
    base = {"open_count": len(opened), "closed_count": len(questions) - len(opened)}

    # Receive -> apply -> validate -> advance. A received reply must never be bypassed.
    unapplied = []
    for rid, row in questions.items():
        entry = entries.get(rid, {})
        answer = answers.get(rid)
        changed = answer is not None and fingerprint(answer) != entry.get("applied_answer")
        if entry.get("phase") == "reply_received" or changed:
            unapplied.append(item(rid, row, answer))
    if unapplied:
        return {**base, "action": "apply_reply", "questions": unapplied,
                "instruction": "Baca bukti jawaban, terapkan ke semua bagian terdampak, "
                               "tutup hanya yang lengkap, lalu catat applied dan jalankan next lagi."}

    complete_inputs = all((docs / name).exists() for name in ("FRD.md", "NFRD.md"))
    if complete_inputs:
        errors, warnings, stats, _ = VALIDATOR.lint(docs, source)
        if errors or stats.get("quality_gaps"):
            return {**base, "action": "repair", "errors": errors, "warnings": warnings,
                    "instruction": "Perbaiki dokumen atau daftarkan kesenjangan mutu sebelum melanjutkan."}
        if not opened and stats.get("tbd"):
            return {**base, "action": "repair", "errors": ["TBD masih tersisa meskipun OQ sudah ditutup."]}

    waiting, fresh, followup, deferred = [], [], [], []
    for rid, row in opened.items():
        entry = entries.get(rid, {})
        current = fingerprint(row[1:4])
        evidence = item(rid, row, answers.get(rid))
        if entry.get("phase") == "waiting":
            waiting.append(evidence)
        elif entry.get("phase") == "deferred" and entry.get("question") == current:
            deferred.append({**evidence, "decision": entry["reason"], "evidence": entry["evidence"]})
        elif entry.get("phase") == "followup":
            followup.append(evidence)
        else:
            fresh.append(evidence)
    if waiting:
        return {**base, "action": "wait", "questions": waiting, "unasked_count": len(fresh),
                "instruction": "Tunggu jawaban yang sudah diminta; jangan ulangi atau tandai selesai."}
    # Cover unseen gaps before returning to a partially answered question indefinitely.
    queue = fresh if fresh else followup
    if queue:
        queue.sort(key=lambda q: (q["priority"] != "Penghambat", q["id"]))
        return {**base, "action": "ask", "questions": queue[:limit], "remaining_count": len(queue),
                "instruction": "Ajukan pertanyaan ini dalam bahasa pengguna, hanya bagian yang belum dijawab. "
                               "Setelah benar-benar dikirim, catat asked beserta rujukan pengirimannya."}
    if deferred:
        return {**base, "action": "deliver_draft", "questions": deferred,
                "instruction": "Pengguna menunda keputusan ini. Laporkan draft dan penundaannya; jangan klaim SIAP."}
    missing = [name for name in getattr(VALIDATOR, "REQUIRED", VALIDATOR.TEMPLATES) if not (docs / name).exists()]
    if not complete_inputs or missing:
        return {**base, "action": "draft", "missing": missing,
                "instruction": "Lengkapi keluaran tahap ini dari jawaban yang tercatat, lalu validasi dan next lagi."}
    return {**base, "action": "complete", "instruction": "Tidak ada keputusan terbuka atau cacat struktural. "
            "Lakukan tinjauan makna akhir; hasil ini bukan persetujuan stakeholder."}


def record(docs, command, question_ids, evidence, reason=None):
    if not evidence or not evidence.strip():
        raise ValueError("Rujukan bukti wajib diisi")
    if command == "defer" and (not reason or not reason.strip()):
        raise ValueError("Penundaan memerlukan keputusan eksplisit pengguna dan alasannya")
    if not question_ids or len(set(question_ids)) != len(question_ids):
        raise ValueError("Berikan ID OQ unik yang hendak diperbarui")
    questions, answers = context(docs)
    state = load_state(docs)
    # Validate the whole batch before writing any state.
    for rid in question_ids:
        if rid not in questions:
            raise ValueError(f"{rid} tidak terdaftar")
        row, old = questions[rid], state["questions"].get(rid, {})
        if command in {"asked", "defer"} and row[6] != "Terbuka":
            raise ValueError(f"{rid} sudah Terjawab; jangan ditanyakan atau ditunda kembali")
        if command == "asked" and old.get("phase") == "waiting":
            raise ValueError(f"{rid} sedang menunggu jawaban; jangan kirim ulang")
        if command in {"asked", "defer"} and old.get("phase") == "reply_received":
            raise ValueError(f"{rid}: terapkan balasan yang diterima sebelum mengganti tindak lanjutnya")
        if command == "reply" and old.get("phase") == "reply_received":
            raise ValueError(f"{rid}: terapkan jawaban sebelumnya sebelum mencatat balasan berikutnya")
        if command == "applied":
            if rid not in answers:
                raise ValueError(f"{rid}: catatan jawaban dan bukti belum tersedia")
            if (old.get("phase") == "reply_received" and
                    old.get("before_reply_answer") == fingerprint(answers[rid])):
                raise ValueError(f"{rid}: catatan jawaban belum diperbarui setelah balasan baru")
    if command == "applied" and all((docs / name).exists() for name in ("FRD.md", "NFRD.md")):
        errors = VALIDATOR.lint(docs)[0]
        if errors:
            raise ValueError("Jawaban belum dapat diakui diterapkan: " + "; ".join(errors))
    for rid in question_ids:
        row = questions[rid]
        old = state["questions"].get(rid, {})
        entry = {**old, "question": fingerprint(row[1:4]), "evidence": evidence}
        if command == "asked":
            entry["phase"] = "waiting"
        elif command == "reply":
            entry.update(phase="reply_received", before_reply_answer=fingerprint(answers.get(rid)))
        elif command == "applied":
            entry.update(phase="closed" if row[6] == "Terjawab" else "followup",
                         applied_answer=fingerprint(answers[rid]))
        elif command == "defer":
            entry.update(phase="deferred", reason=reason)
        else:
            raise ValueError("Perintah tidak dikenal")
        state["questions"][rid] = entry
    state["history"].append({"command": command, "ids": question_ids, "evidence": evidence,
                             **({"reason": reason} if reason else {})})
    save_state(docs, state)
    return {"recorded": command, "ids": question_ids}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    query = sub.add_parser("next")
    query.add_argument("--limit", type=int, default=3)
    query.add_argument("--source", type=Path)
    for name in ("asked", "reply", "applied", "defer"):
        action = sub.add_parser(name)
        action.add_argument("ids", nargs="+")
        action.add_argument("--evidence", required=True)
        if name == "defer":
            action.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "next":
            result = next_action(args.docs, args.limit, args.source)
            code = EXIT_CODES[result["action"]]
        else:
            result = record(args.docs, args.command, args.ids, args.evidence, getattr(args, "reason", None))
            code = 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        result, code = {"action": "repair", "error": str(error)}, 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
