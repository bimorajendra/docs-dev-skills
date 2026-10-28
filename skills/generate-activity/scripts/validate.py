"""Validator Activity List, FRD, NFRD dan pertanyaan klarifikasi.
Pemakaian: python -I validate.py <docs> [--source sumber.md] [--intake] [--toc] [--matrix] [--require-ready]
--intake memeriksa ekstraksi dan pertanyaan sebelum dokumen kebutuhan selesai."""
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
TEMPLATES = {"FRD.md": "FRD.template.md", "NFRD.md": "NFRD.template.md"}
FRONT = {"riwayat revisi", "persetujuan", "daftar isi"}
P = {"AL": r"\bAL-\d{3}\b", "FR": r"\bFR-\d{3}\b", "NFR": r"\bNFR-[A-Z]{3}-\d{2}\b",
     "OQ": r"\bOQ-\d{2}\b"}
ANY = "(?:" + "|".join(P.values()) + ")"
CODES = {"functional suitability": "FUN", "performance efficiency": "PER", "compatibility": "COM",
         "interaction capability": "INT", "reliability": "REL", "security": "SEC",
         "maintainability": "MAI", "flexibility": "FLX", "safety": "SAF"}
BASIS = {"Eksplisit", "Turunan"}
VAGUE = re.compile(
    r"(?<!\w)(cepat|lambat|mudah|ramah pengguna|user-friendly|memadai|optimal|andal|fleksibel|secukupnya|"
    r"segera|secepatnya|jika perlu|bila perlu|sebaiknya|mungkin|dll|dsb|dan sebagainya)(?!\w)", re.I)
RANGE = re.compile(r"(?:AL|FR|OQ|NFR-[A-Z]{3})-\d+\s+(?:sampai|hingga|s\.d\.)\s+"
                   r"(?:AL|FR|OQ|NFR)-", re.I)
OQ_HEADER = ["ID", "Pertanyaan", "Aktivitas terkait", "Mempengaruhi", "Prioritas", "Penjawab", "Status"]
REVIEW_HEADER = ["Aktivitas", "Hasil tinjauan", "OQ terkait", "Dasar tinjauan"]
ANSWER_HEADER = ["OQ", "Jawaban", "Dikonfirmasi oleh", "Tanggal", "Rujukan bukti"]


def read(p):
    return Path(p).read_text(encoding="utf-8")


def norm(t):
    return re.sub(r"^\d+(\.\d+)*\.?\s+", "", t.strip()).lower()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def ids(pattern, text):
    return set(re.findall(pattern, text))


def width_ok(c, header, ctx, err):
    if len(c) != len(header):
        err.append(f"{ctx}: baris '{c[0] if c else ''}' punya {len(c)} kolom, seharusnya {len(header)}")
        return False
    return True


def no_tbd(s):
    return re.sub(r"\[TBD[^\]]*\]", "", s).strip()


def headings(text):
    out, fence = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"(#{1,6})\s+(.+?)\s*$", line)
        if m:
            out.append((len(m[1]), m[2], n))
    return out


def tables(text):
    blocks, cur = [], []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|"):
            cur.append(cells(line))
        elif cur:
            blocks.append(cur)
            cur = []
    return [(b[0], b[2:]) for b in blocks if len(b) >= 2 and all(re.fullmatch(r":?-{3,}:?", x) for x in b[1])]


def h2_text(text, prefix):
    lines, hs = text.splitlines(), headings(text)
    for j, h in enumerate(hs):
        if h[0] == 2 and norm(h[1]).startswith(prefix):
            end = next((x[2] for x in hs[j + 1:] if x[0] <= 2), len(lines) + 1)
            return "\n".join(lines[h[2]:end - 1])
    return ""


def modules(text, prefix):
    lines, hs, out, inside = text.splitlines(), headings(text), [], False
    for i, (lv, t, ln) in enumerate(hs):
        if lv == 2:
            inside = norm(t).startswith(prefix)
        if inside and lv == 3:
            m = re.match(r"(\d+\.\d+)\s+Modul\s+(.+)$", t)
            end = next((h[2] for h in hs[i + 1:] if h[0] <= 3), len(lines) + 1)
            body = "\n".join(lines[ln:end - 1])
            decl = next((x for x in body.splitlines() if x.startswith("Sumber aktivitas:")), "")
            subs = {}
            for h in hs[i + 1:]:
                if h[0] == 4 and ln < h[2] < end:
                    nxt = next((x[2] for x in hs if x[2] > h[2]), len(lines) + 1)
                    subs[norm(h[1])] = "\n".join(lines[h[2]:nxt - 1])
            out.append({"title": t, "ok": bool(m), "num": m[1] if m else t, "name": norm(m[2]) if m else "",
                        "als": ids(P["AL"], decl), "decl": bool(decl), "body": body, "subs": subs})
    return out


def template_headings(path):
    main, rep, inside = set(), set(), False
    for line in read(path).splitlines():
        if "ulang:mulai" in line:
            inside = True
        elif "ulang:selesai" in line:
            inside = False
        m = re.match(r"(#{2,6})\s+(.+?)\s*$", line)
        if m:
            (rep if inside else main).add((len(m[1]), norm(m[2])))
    return main, rep


def write_toc(path):
    text, hs = read(path), headings(read(path))
    h2 = [i for i, h in enumerate(hs) if h[0] == 2]
    items = []
    for k, i in enumerate(h2):
        nxt = h2[k + 1] if k + 1 < len(h2) else len(hs)
        subs = [x[1] for x in hs[i + 1:nxt] if x[0] == 3]
        items.append(f"- {hs[i][1]}" + (f" ({', '.join(subs)})" if subs else ""))
    new = re.sub(r"(^## Daftar Isi[ \t]*\n)(.*?)(?=^## )", lambda m: m[1] + "\n" + "\n".join(items) + "\n\n",
                 text, count=1, flags=re.M | re.S)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)


def check_trace(name, text, expected, err):
    """expected: AL -> {kolom: set}; kolom 1.. dibaca dari sel tabel Keterlacakan (pola per kolom)."""
    got = {}
    for header, rows in tables(h2_text(text, "keterlacakan")):
        for c in rows:
            if re.fullmatch(P["AL"], c[0]):
                got[c[0]] = c
    for a, cols in expected.items():
        for idx, (pat, exp) in cols.items():
            have = ids(pat, got[a][idx]) if a in got and len(got[a]) > idx else set()
            if exp and have != exp:
                err.append(f"{name}: tabel Keterlacakan {a} kolom {idx + 1} seharusnya {sorted(exp)}, tertulis {sorted(have)}")


def check_questions(text, al_rows, err):
    """Check register, per-activity coverage and evidence; do not infer business answers."""
    questions, reviews, answers = {}, {}, {}
    sections = (("daftar pertanyaan", OQ_HEADER, questions, "OQ"),
                ("tinjauan aktivitas", REVIEW_HEADER, reviews, "AL"),
                ("catatan jawaban", ANSWER_HEADER, answers, "OQ"))
    for section, expected, target, kind in sections:
        body = h2_text(text, section)
        if not any(lv == 2 and norm(title) == section for lv, title, _ in headings(text)):
            err.append(f"pertanyaan-terbuka.md: bagian '{section}' tidak ada (gunakan templat v1.2)")
        found = False
        for header, rows in tables(body):
            if header != expected:
                err.append(f"pertanyaan-terbuka.md {section}: kolom harus {' | '.join(expected)}")
                continue
            found = True
            for c in rows:
                if not width_ok(c, header, f"pertanyaan-terbuka.md {section}", err):
                    continue
                rid = c[0]
                if not re.fullmatch(P[kind], rid):
                    err.append(f"pertanyaan-terbuka.md {section}: ID '{rid}' tidak valid")
                    continue
                if rid in target:
                    err.append(f"pertanyaan-terbuka.md {section}: ID ganda: {rid}")
                target[rid] = c
                required = [v for i, v in enumerate(c) if i and not (target is reviews and i == 2 and v == "-")]
                if any(not v or v == "-" or re.search(r"<[^>]+>", v.replace("<br>", "")) for v in required):
                    err.append(f"{rid}: {section} masih berisi kolom kosong atau placeholder")
        if not found and section != "catatan jawaban":
            err.append(f"pertanyaan-terbuka.md: tabel {section} tidak ada")

    for rid, c in questions.items():
        related = ids(P["AL"], c[2])
        if not related and c[2] != "Lintas dokumen":
            err.append(f"{rid}: Aktivitas terkait harus AL atau Lintas dokumen")
        if related and not re.fullmatch(r"AL-\d{3}(?:[,;] AL-\d{3})*", c[2]):
            err.append(f"{rid}: tulis Aktivitas terkait sebagai daftar AL satu per satu")
        for a in sorted(related - set(al_rows)):
            err.append(f"{rid}: {a} tidak ada di Activity List")
        if c[4] not in {"Penghambat", "Lanjutan"}:
            err.append(f"{rid}: Prioritas harus Penghambat atau Lanjutan")
        if c[6] not in {"Terbuka", "Terjawab"}:
            err.append(f"{rid}: Status harus Terbuka atau Terjawab")
        if c[6] == "Terjawab" and rid not in answers:
            err.append(f"{rid}: Terjawab tanpa catatan jawaban dan bukti konfirmasi")
        for a in sorted(related):
            if a not in reviews or rid not in ids(P["OQ"], reviews[a][2]):
                err.append(f"{rid}: belum ditautkan pada tinjauan {a}")

    for a in al_rows:
        if a not in reviews:
            err.append(f"{a}: belum memiliki tinjauan aktivitas")
    for a, c in reviews.items():
        if a not in al_rows:
            err.append(f"Tinjauan {a}: tidak ada di Activity List")
        related = ids(P["OQ"], c[2])
        if c[2] != "-" and not re.fullmatch(r"OQ-\d{2}(?:[,;] OQ-\d{2})*", c[2]):
            err.append(f"Tinjauan {a}: OQ terkait harus daftar OQ satu per satu atau '-'")
        for q in sorted(related):
            if q not in questions:
                err.append(f"Tinjauan {a}: {q} tidak terdaftar")
            elif a not in ids(P["AL"], questions[q][2]):
                err.append(f"Tinjauan {a}: {q} tidak mencantumkan aktivitas ini")
        pending = any(q in questions and questions[q][6] == "Terbuka" for q in related)
        expected = "Perlu konfirmasi" if pending else "Cukup dari sumber"
        if c[1] != expected:
            err.append(f"Tinjauan {a}: Hasil tinjauan seharusnya {expected}")

    for rid, c in answers.items():
        if rid not in questions:
            err.append(f"Catatan jawaban: {rid} tidak terdaftar")
        if any(v.casefold() in {"tbd", "belum ditetapkan", "belum dijawab", "belum ada"} or "[TBD" in v
               for v in c[1:]):
            err.append(f"{rid}: catatan jawaban belum memuat jawaban dan bukti nyata")
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", c[3]):
                raise ValueError
            date.fromisoformat(c[3])
        except ValueError:
            err.append(f"{rid}: Tanggal konfirmasi harus tanggal valid YYYY-MM-DD")
    return questions, reviews


def read_activities(text, err):
    rows_by_id = {}
    for header, rows in tables(text):
        if header[:1] != ["ID"]:
            continue
        if header != ["ID", "Ref SOP", "Aktivitas", "Aktor"]:
            err.append("00-activity-list.md: kolom harus ID | Ref SOP | Aktivitas | Aktor")
            continue
        for c in rows:
            if not width_ok(c, header, "00-activity-list.md", err):
                continue
            if not re.fullmatch(P["AL"], c[0]):
                err.append(f"Activity List: ID '{c[0]}' tidak valid")
            if c[0] in rows_by_id:
                err.append(f"ID ganda: {c[0]}")
            rows_by_id[c[0]] = c
            if not c[2] or not c[3]:
                err.append(f"{c[0]}: Aktivitas atau Aktor kosong")
    if not rows_by_id:
        err.append("Activity List: belum ada aktivitas yang diekstrak")
    return rows_by_id


def check_activity_source(al_rows, source, err):
    if source is None:
        return
    source_text = read(source)
    items = []
    for line in source_text.splitlines():
        m = re.match(r"\s*\d+\.\s+(?:\((\d+(?:\.\d+)*)\)\s*)?(.+?)\s*$", line)
        if m:
            items.append((m[1] or "-", re.sub(r"\s+", " ", m[2])))
    if items:
        if len(items) != len(al_rows):
            err.append(f"Activity List: {len(al_rows)} baris, sumber {len(items)} butir")
        for (ref, txt), c in zip(items, al_rows.values()):
            if c[1] != ref or re.sub(r"\s+", " ", c[2]) != txt:
                err.append(f"{c[0]}: tidak sama persis dengan butir sumber {ref}")
    else:
        source_plain = re.sub(r"\s+", " ", source_text).strip()
        if not source_plain:
            err.append("Sumber narasi kosong")
        for rid, c in al_rows.items():
            fragment = re.sub(r"\s+", " ", c[2]).strip()
            if not fragment or fragment not in source_plain:
                err.append(f"{rid}: cuplikan aktivitas tidak ditemukan persis dalam narasi sumber")
            if c[1] not in {"Narasi", "-"}:
                err.append(f"{rid}: Ref SOP untuk narasi harus Narasi atau '-'")


def check_quality_review(text, questions, warn):
    """Track unreviewed areas without mistaking source silence for a scope decision."""
    lines, hs = text.splitlines(), headings(text)
    inside, seen, gaps = False, set(), 0
    for i, (level, title, line) in enumerate(hs):
        if level == 2:
            inside = norm(title).startswith("kebutuhan mutu per karakteristik")
        if not inside or level != 3:
            continue
        seen.add(norm(title))
        end = next((h[2] for h in hs[i + 1:] if h[0] <= 3), len(lines) + 1)
        body = "\n".join(lines[line:end - 1])
        has_rows = any(rows for header, rows in tables(body) if header[:1] == ["ID"])
        refs = ids(P["OQ"], body)
        pending = any(q in questions and questions[q][6] == "Terbuka" for q in refs)
        decided = bool(refs) and all(q in questions and questions[q][6] == "Terjawab" for q in refs)
        no_requirement = bool(re.search(r"^\s*(?:Tidak ada kebutuhan|Tidak berlaku)", body, re.I | re.M))
        confirmed_decision = bool(re.search(r"^\s*Keputusan mutu terkonfirmasi:", body, re.I | re.M))
        if no_requirement or confirmed_decision:
            covered = decided
        else:
            covered = has_rows or pending
        if not covered:
            gaps += 1
            warn.append(f"NFRD {title}: kajian mutu belum selesai; tanyakan kebutuhan atau keputusan tidak berlaku, "
                        "lalu tautkan OQ. Ketiadaan informasi sumber bukan keputusan pengguna.")
    missing = set(CODES) - seen
    for name in sorted(missing):
        gaps += 1
        warn.append(f"NFRD: kajian karakteristik '{name}' belum ada")
    regulations = h2_text(text, "kepatuhan dan regulasi")
    if (not regulations.strip() or re.search(r"Tidak disebut sumber|Tidak berlaku|Tidak ada (?:kebutuhan|regulasi|kebijakan)",
                                            regulations, re.I)) and not ids(P["OQ"], regulations):
        gaps += 1
        warn.append("NFRD Kepatuhan: penerapan kebijakan belum diklarifikasi atau diberi bukti keputusan; tautkan OQ.")
    return gaps


def lint(docs, source=None):
    err, warn, T = [], [], {}
    need = ["00-activity-list.md", "pertanyaan-terbuka.md", "FRD.md", "NFRD.md"]
    for name in need:
        if (docs / name).exists():
            T[name] = read(docs / name)
        else:
            err.append(f"{name}: berkas tidak ada")
    if err:
        return err, warn, {}, T

    al_text, frd, nfrd, oq_text = T["00-activity-list.md"], T["FRD.md"], T["NFRD.md"], T["pertanyaan-terbuka.md"]
    docs_text = {n: T[n] for n in ("FRD.md", "NFRD.md") if n in T}
    defined = {k: Counter() for k in P}

    # ---- Activity List
    al_rows = read_activities(al_text, err)
    defined["AL"].update(al_rows.keys())
    check_activity_source(al_rows, source, err)

    # ---- FRD
    fr_rows, mod_of_fr = {}, {}
    fmods = modules(frd, "kebutuhan fungsional")
    for m in fmods:
        if not m["ok"] or not m["decl"]:
            err.append(f"FRD {m['title']}: judul harus '3.n Modul <Nama>' dan ada baris 'Sumber aktivitas:'")
        if len(m["als"]) > 6:
            warn.append(f"FRD modul {m['num']}: lebih dari 6 aktivitas")
        for header, rows in tables(m["body"]):
            if header != ["ID", "Pernyataan", "Sumber", "Alasan", "Kriteria Penerimaan", "Basis", "Verif."]:
                err.append(f"FRD modul {m['num']}: kolom tabel salah")
                continue
            for c in rows:
                if not width_ok(c, header, f"FRD modul {m['num']}", err):
                    continue
                rid = c[0]
                defined["FR"][rid] += 1
                fr_rows[rid], mod_of_fr[rid] = c, m["num"]
                src = ids(P["AL"], c[2])
                if not src or not src <= m["als"]:
                    err.append(f"{rid}: Sumber harus berisi AL dari modul {m['num']}")
                if c[5] not in BASIS:
                    err.append(f"{rid}: Basis harus Eksplisit atau Turunan")
                if not re.fullmatch(r"[UDIA](, [UDIA])*", c[6]):
                    err.append(f"{rid}: Verif. harus U, D, I, atau A")
                if len(re.findall(r"\bharus\b", no_tbd(c[1]), re.I)) != 1:
                    warn.append(f"{rid}: pernyataan harus memuat tepat satu 'harus'")
                if not no_tbd(c[4]).replace("<br>", "").strip():
                    err.append(f"{rid}: Kriteria Penerimaan kosong atau hanya TBD")
                if c[5] == "Turunan" and c[3] in ("", "-"):
                    err.append(f"{rid}: Turunan wajib punya Alasan")
    per_al = Counter(a for m in fmods for a in m["als"])
    for a in al_rows:
        if per_al[a] != 1:
            err.append(f"{a}: harus masuk tepat satu modul FRD (ada di {per_al[a]})")
    err += [f"FRD: {a} dideklarasikan tetapi tidak ada di Activity List" for a in per_al if a not in al_rows]
    fr_src = ids(P["AL"], " ".join(c[2] for c in fr_rows.values()))
    err += [f"{a}: tidak punya FR" for a in al_rows if a not in fr_src]

    # ---- NFRD
    nfr_rows = {}
    lines, hs = nfrd.splitlines(), headings(nfrd)
    in3 = False
    for i, (lv, t, ln) in enumerate(hs):
        if lv == 2:
            in3 = norm(t).startswith("kebutuhan mutu per karakteristik")
        if in3 and lv == 3:
            end = next((h[2] for h in hs[i + 1:] if h[0] <= 3), len(lines) + 1)
            body = "\n".join(lines[ln:end - 1])
            code = CODES.get(norm(t), "")
            tbls = [x for x in tables(body) if x[0][:1] == ["ID"]]
            if not tbls and not re.search(r"Tidak ada kebutuhan|Tidak berlaku|Bergantung OQ-\d{2}|Keputusan mutu terkonfirmasi:", body):
                err.append(f"NFRD {t}: isi kebutuhan, klarifikasi OQ, atau keputusan mutu yang dibuktikan")
            for header, rows in tbls:
                if header != ["ID", "Sub-karakteristik", "Pernyataan", "Ukuran", "Target", "Sumber", "Basis", "Verif."]:
                    err.append(f"NFRD {t}: kolom tabel salah")
                    continue
                for c in rows:
                    if not width_ok(c, header, f"NFRD {t}", err):
                        continue
                    rid = c[0]
                    defined["NFR"][rid] += 1
                    nfr_rows[rid] = c
                    if not rid.startswith(f"NFR-{code}-"):
                        err.append(f"{rid}: kode ID tidak sesuai karakteristik {t}")
                    if not ids(P["AL"], c[5]) <= set(al_rows) or not ids(P["AL"], c[5]):
                        err.append(f"{rid}: Sumber AL tidak valid")
                    if c[6] not in BASIS:
                        err.append(f"{rid}: Basis harus Eksplisit atau Turunan")
                    if not re.fullmatch(r"[UDIA](, [UDIA])*", c[7]):
                        err.append(f"{rid}: Verif. harus U, D, I, atau A")
                    if not no_tbd(c[3]):
                        err.append(f"{rid}: Ukuran kosong")
                    if not no_tbd(c[4]):
                        err.append(f"{rid}: Target kosong atau hanya TBD (tulis 'Bergantung OQ-nn' di subbab)")
                    if len(re.findall(r"\bharus\b", no_tbd(c[2]), re.I)) != 1:
                        warn.append(f"{rid}: pernyataan harus memuat tepat satu 'harus'")

    # ---- traceability tables of FRD / NFRD
    mod_of_al = {a: m["num"] for m in fmods for a in m["als"]}
    check_trace("FRD.md", frd, {a: {1: (r"\d+\.\d+", {mod_of_al.get(a)} - {None}),
                                    2: (P["FR"], {r for r, c in fr_rows.items() if a in ids(P["AL"], c[2])})}
                                for a in al_rows}, err)
    check_trace("NFRD.md", nfrd, {a: {1: (P["NFR"], {r for r, c in nfr_rows.items() if a in ids(P["AL"], c[5])})}
                                  for a in al_rows}, err)

    # ---- ID unik dan rujukan
    for kind, ctr in defined.items():
        if kind != "OQ":
            err += [f"ID ganda: {i}" for i, n in ctr.items() if n > 1]
    questions, reviews = check_questions(oq_text, al_rows, err)
    quality_gaps = check_quality_review(nfrd, questions, warn)
    oq_rows = [(o, c[6]) for o, c in questions.items()]
    all_defined = set().union(*[set(c) for c in defined.values()]) | {o for o, _ in oq_rows}
    for name, text in {**docs_text, "pertanyaan-terbuka.md": oq_text}.items():
        for n, line in enumerate(text.splitlines(), 1):
            plain = re.sub(r"`[^`]*`", "", line)
            err += [f"{name}:{n}: {i} tidak terdaftar" for i in sorted(ids(ANY, plain) - all_defined)]

    # ---- OQ dan TBD
    open_oq = [o for o, s in oq_rows if not s.lower().startswith("terjawab")]
    referenced = set().union(*(ids(P["OQ"], c[2]) for c in reviews.values()))
    tbd = 0
    answered = {o for o, s in oq_rows if s == "Terjawab"}
    for name, text in docs_text.items():
        for n, line in enumerate(text.splitlines(), 1):
            plain = re.sub(r"`[^`]*`", "", line)
            refs = ids(P["OQ"], plain)
            referenced |= refs
            tbd += plain.count("[TBD")
            markers = re.findall(r"\[TBD[^\]]*\]", plain)
            if len(markers) != plain.count("[TBD"):
                err.append(f"{name}:{n}: penanda TBD tidak ditutup")
            for marker in markers:
                marker_refs = ids(P["OQ"], marker)
                if not marker_refs:
                    err.append(f"{name}:{n}: [TBD] tanpa OQ di dalam penanda")
                if marker_refs & answered:
                    err.append(f"{name}:{n}: TBD merujuk OQ yang sudah Terjawab")
    warn += [f"{o}: OQ terbuka tetapi tidak dirujuk dokumen mana pun" for o in open_oq if o not in referenced]

    # ---- daftar bab, daftar isi, sisa petunjuk, rentang, kata kabur, duplikasi
    for name, text in docs_text.items():
        hs = headings(text)
        if name in TEMPLATES:
            tpl = ASSETS / TEMPLATES[name]
            if not tpl.exists():
                err.append(f"{name}: templat {tpl.name} tidak ditemukan di assets/")
            else:
                main, rep = template_headings(tpl)
                have = {(lv, norm(t)) for lv, t, _ in hs if lv >= 2}
                err += [f"{name}: bab '{t}' (level {lv}) tidak ada" for lv, t in sorted(main - have)]
        m = re.search(r"^## Daftar Isi\s*$(.*?)(?=^## )", text, re.M | re.S)
        toc = (m[1] if m else "").lower()
        err += [f"{name}: Daftar Isi tidak memuat '{norm(t)}' (jalankan --toc)"
                for lv, t, _ in hs if lv == 2 and norm(t) not in FRONT and norm(t) not in toc]
        for n, line in enumerate(text.splitlines(), 1):
            if line.startswith("> Fill:") or "ulang:mulai" in line or "ulang:selesai" in line:
                err.append(f"{name}:{n}: petunjuk atau penanda template belum dihapus")
    for rid, c in {**fr_rows, **nfr_rows}.items():
        for w in sorted({m[1].lower() for m in VAGUE.finditer(no_tbd(" ".join(c)))}):
            warn.append(f"{rid}: kata kabur '{w}'")
    for a, c in al_rows.items():
        for w in sorted({m[1].lower() for m in VAGUE.finditer(c[2])}):
            warn.append(f"{a}: kata kabur '{w}' (dari sumber)")
    for rid, c in {**fr_rows, **nfr_rows}.items():
        if re.search(r"tidak boleh", no_tbd(c[1] if rid.startswith("FR") else c[2]), re.I):
            warn.append(f"{rid}: nyatakan pembatasan sebagai kemampuan positif dengan kriteria penerimaan")
    err += [f"{o}: Status harus Terbuka atau Terjawab (tertulis '{s}')" for o, s in oq_rows
            if s not in ("Terbuka", "Terjawab")]
    seen = {}
    for name, text in docs_text.items():
        for _, rows in tables(text):
            for c in rows:
                for cell in c:
                    key = re.sub(r"\s+", " ", no_tbd(cell).lower())
                    if len(key) >= 60:
                        seen.setdefault(key, set()).add(name)
    warn += [f"kalimat sama di {' dan '.join(sorted(v))}: '{k[:50]}...'" for k, v in seen.items() if len(v) > 1]
    for name, text in docs_text.items():
        for n, line in enumerate(text.splitlines(), 1):
            if RANGE.search(line):
                warn.append(f"{name}:{n}: rentang ID, tulis satu per satu")

    stats = dict(al=len(al_rows), fr=len(fr_rows), nfr=len(nfr_rows), modul=len(fmods), oq=len(open_oq),
                 tbd=tbd, quality_gaps=quality_gaps)
    return err, warn, stats, T


def matrix(docs, T):
    fr, nfr = {}, {}
    fmods = modules(T["FRD.md"], "kebutuhan fungsional")
    for m in fmods:
        for _, rows in tables(m["body"]):
            for c in rows:
                fr[c[0]] = c
    for _, rows in [t for t in tables(T["NFRD.md"]) if len(t[0]) == 8 and t[0][1] == "Sub-karakteristik"]:
        for c in rows:
            nfr[c[0]] = c
    out = ["# Matriks Keterlacakan", "", "Dibuat otomatis oleh `validate.py --matrix`. Jangan diedit manual.", "",
           "| Aktivitas | Modul | FR | NFR | OQ |",
           "|---|---|---|---|---|"]
    question_rows = [c for header, rows in tables(h2_text(T["pertanyaan-terbuka.md"], "daftar pertanyaan"))
                     if header == OQ_HEADER for c in rows]
    for line in T["00-activity-list.md"].splitlines():
        m = re.match(r"\|\s*(AL-\d{3})\s*\|", line)
        if not m:
            continue
        a = m[1]
        mod = next((x for x in fmods if a in x["als"]), None)
        frs = [r for r, c in fr.items() if a in ids(P["AL"], c[2])]
        nfs = [r for r, c in nfr.items() if a in ids(P["AL"], c[5])]
        row = f"| {a} | {mod['num'] if mod else ''} | {', '.join(frs)} | {', '.join(nfs)} |"
        row += " " + ", ".join(c[0] for c in question_rows if a in ids(P["AL"], c[2])) + " |"
        out.append(row)
    with open(docs / "traceability.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")


def lint_intake(docs, source=None):
    err = []
    texts = {}
    for name in ("00-activity-list.md", "pertanyaan-terbuka.md"):
        path = docs / name
        if path.exists():
            texts[name] = read(path)
        else:
            err.append(f"{name}: berkas tidak ada")
    if err:
        return err, [], {}, texts
    activities = read_activities(texts["00-activity-list.md"], err)
    check_activity_source(activities, source, err)
    questions, _ = check_questions(texts["pertanyaan-terbuka.md"], activities, err)
    stats = dict(al=len(activities), oq=sum(c[6] == "Terbuka" for c in questions.values()), tbd=0)
    return err, [], stats, texts


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) < 2:
        print(__doc__)
        return 2
    docs = Path(argv[1])
    source = Path(argv[argv.index("--source") + 1]) if "--source" in argv else None
    intake = "--intake" in argv
    if intake and ("--toc" in argv or "--matrix" in argv):
        print("Mode --intake memeriksa ekstraksi dan klarifikasi; jalankan --toc/--matrix setelah dokumen lengkap.")
        return 2
    if "--toc" in argv:
        for name in TEMPLATES:
            if (docs / name).exists():
                write_toc(docs / name)
        print("Daftar Isi ditulis ulang")
    err, warn, st, T = (lint_intake if intake else lint)(docs, source)
    if "--matrix" in argv and not err:
        matrix(docs, T)
        print("traceability.md ditulis ulang")
    for e in err:
        print("GALAT      ", e)
    for w in warn:
        print("PERINGATAN ", w)
    if st and intake:
        print(f"\nIntake: AL {st['al']} | OQ terbuka {st['oq']}")
    elif st:
        print(f"\nAL {st['al']} | FR {st['fr']} | NFR {st['nfr']} | modul {st['modul']} | "
              f"OQ terbuka {st['oq']} | penanda TBD {st['tbd']} | kajian mutu belum tertaut {st['quality_gaps']}")
    status = "GAGAL" if err else ("BELUM SIAP" if st["oq"] or st["tbd"] or st.get("quality_gaps") else "SIAP")
    print(f"{'Status intake' if intake else 'Status'}: {status}")
    return 1 if err else (3 if "--require-ready" in argv and status != "SIAP" else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
