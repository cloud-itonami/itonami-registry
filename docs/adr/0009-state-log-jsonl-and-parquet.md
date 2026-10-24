# ADR 0009: State is an append-only JSONL log, closed days compacted to Parquet

Status: proposed — 2026-10-24

## Context

ADR 0003 puts a profile's State (`sessions/`, `logs/`, `memories/`, `ledger/`) outside the
registry and outside definition repositories, in a data plane or a DataLad dataset. It does
not fix a file format. Today Hermes keeps sessions in one sqlite file per profile
(`~/.hermes/profiles/<p>/state.db`; 21 of 79 profiles on the host have one, the largest about
148 MB). A sqlite file is binary and uses a WAL, so git can neither diff nor merge it, and
every change stores the whole file again.

The aim is a format that is stored as plain files in git or a git-annex dataset, can be
queried with SQL, and can be signed.

## Decision

State that is a record of events (turns, tool calls, receipts, ledger entries) is written in
two layers.

1. **Open layer: JSONL.** One event per line in `log/open/<YYYY-MM-DD>.jsonl`, appended
   only. A line is never edited. Each event has at least `seq` (increasing within the file),
   `ts`, `profile`, `kind` and the event's own fields. JSONL diffs and merges by line, can
   be signed per line, and is read natively by the Kotoba engines.
2. **Closed layer: Parquet.** When a day is closed, its JSONL is compacted once into
   `log/closed/<YYYY-MM-DD>.parquet` (zstd, rows ordered by `seq`) and the file is never
   rewritten. The JSONL of that day stays; the Parquet file is derived.
3. **Query.** SQL runs over both layers at once, for example DuckDB's `read_json` on
   `log/open/*.jsonl` and `read_parquet` on `log/closed/*.parquet`. The same files can be read
   in a browser (duckdb-wasm) without a server.
4. **JSONL is the authority.** A closed day is valid only if its Parquet has the same rows as
   its JSONL (`EXCEPT` in both directions returns nothing). Signatures and checksums are over
   the JSONL. Parquet bytes are recorded with the writer's version but are not authoritative.
5. **A local sqlite file is allowed as a disposable index** (full-text search, aggregates).
   It is rebuilt from the log, never committed and never the source of truth.
6. **Placement follows ADR 0003.** Logs that hold conversation text, personal data or
   anything not published stay in the data plane or an encrypted annex, not in a definition
   repository and never in this registry. This ADR decides the format only; it moves no
   existing state and deletes none.

## Evidence

A proof of concept on synthetic data (3 days of 5,000 events, DuckDB 1.5.1):

- A day of JSONL (1.0 MB) compacted to 18 KB of Parquet. The ratio is overstated, because
  the synthetic bodies repeat; real logs will compress less.
- Writing the same input twice gave byte-identical Parquet (same SHA-256), so a closed
  day does not create a new git blob when it is regenerated with the same writer.
- The Parquet and the JSONL of a closed day had the same 5,000 rows (0 in `EXCEPT`).
- One query read closed Parquet and open JSONL together (15,000 rows, 100 sessions).

Byte-identical output was observed for one writer version only. A different DuckDB or
Arrow version may write different bytes for the same rows, which is why rule 4 makes the
rows, not the bytes, authoritative.

## Consequences

- A diff of recent activity is readable in git; history of closed days costs little.
- Compaction is a one-way, once-a-day step; a failed or interrupted one is simply redone from
  the JSONL.
- Nothing here changes how Hermes stores sessions today. Moving an existing `state.db` into
  this form needs an exporter and a verification of row counts; that is separate work.
- Not decided: the event schema beyond the common fields, the signing format (it depends on
  the key work in JUN-351), and the Itonami agent's own session format, which is not yet
  verified.
