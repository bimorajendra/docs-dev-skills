# Behavioral review scenarios

Use these to review `generate-activity`'s clarification behavior. Evaluate whether the questions follow the supplied input and conversation, rather than matching a particular sentence or question count. These scenarios test interpretation; passing the Python validator alone does not demonstrate these behaviors.

## Ambiguous activity

User input:

```text
Tolong petakan activities ini menjadi kebutuhan:
1. Admin memproses pengajuan yang sesuai.
2. Admin meneruskan hasilnya ke petugas.
```

Expected behavior: identify the unclear meaning of `memproses`, `yang sesuai` and the referent of `hasilnya` only as needed for an accurate mapping. Ask a focused, contextual clarification before treating a particular check or output as established. Explain which activity mapping depends on the reply. Do not invent approval, rejection, an SLA or a new application screen. Preserve the source wording.

## Context already resolves the activity

User input:

```text
Semua pemeriksaan dilakukan petugas; sistem dipakai untuk mencatat hasilnya.
1. Petugas memeriksa apakah nomor permintaan pada formulir sama dengan nomor permintaan pada surat pesanan.
2. Jika sama, petugas mencatat hasil Cocok pada sistem; jika berbeda, petugas mencatat hasil Tidak cocok.
```

Expected behavior: use the stated actor, comparison and two results. No clarification about the meaning of the comparison, actor or system boundary is needed. Do not manufacture ownership, migration or quality-level questions. Reflect the understood flow and invite correction without treating silence as agreement. An empty question register is valid.

## Follow-up narrows the remaining gap

Previous source:

```text
1. Admin memproses pengajuan yang sesuai.
2. Admin meneruskan hasilnya ke petugas.
```

User clarification:

```text
Memproses di sini mengecek kelengkapan nomor dan tanggal pengajuan. Sesuai artinya kedua data itu terisi.
```

Expected behavior: apply the defined check and criterion; do not ask them again. If the output sent to the petugas still cannot be identified, ask specifically what `hasilnya` in the second activity refers to. Do not close an OQ that also covers the still-undefined output. Revisit affected mappings after the next reply.

## List order does not establish process order

User input:

```text
Ini daftar pekerjaan, urutannya belum disusun:
1. Koordinator memeriksa hasil pengajuan.
2. Admin mencatat pengajuan baru.
```

Expected behavior: preserve numbering in the Activity List without asserting that review occurs before creation. Clarify the relationship and the meaning of the reviewed result if those prevent constructing the requested flow. Do not create a misleading linear diagram merely to complete the document.

## Continue without a user reminder

The current register contains several unanswered decisions. The agent sends a small first batch; the user answers it without mentioning the other document sections.

Expected behavior: the runner yields `apply_reply`, the agent applies the answers and records the evidence, and the next runner call chooses the next unasked decisions. The agent does not end the interview at a successful draft validation, wait for the user to point out missing sections, or resend the batch already waiting for a reply. A partial answer stays open; previously unseen topics are not starved by repeated attempts to obtain the same missing number.

## User prioritizes harness repair

User input:

```text
Perbaiki harness-nya dulu. Jangan lanjut bertanya tentang contoh aplikasinya sekarang.
```

Expected behavior: preserve any incoming domain replies and the clarification state, work on the harness, and do not send the next domain batch. A queue is not permission to disregard task steering. Tests can exercise the queue with fixtures while the real interview is suspended.
