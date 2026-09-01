# MOVED: Candi Court Financial Discovery

**Do not add new case-specific financial discovery work in this folder.**

This package was created for the Candi Court matter and has been consolidated into the canonical legal repository:

`Satcomwarrior/candi-court/financial_discovery/`

The Candi Court copy now contains the financial-discovery code/schema, migration provenance, and the processed source statement migrated with an identical Git blob SHA.

## Status of this folder

This folder remains in `codex-comet-bridge` only as historical source/provenance. The broader `codex-comet-bridge` repository is a separate integration project and is **not** retired by this move.

Do not:

- add new Candi Court statements here;
- update case-specific reconciliation logic here;
- treat this folder's derived ledger as the canonical evidence source;
- create another case-specific financial repository.

For current case work, use `Satcomwarrior/candi-court/financial_discovery/`.

## Historical note

The legacy package ingested financial statements into a unified ledger and contained basic duplicate/reconciliation logic. Its source history is retained here so prior commits remain traceable, while current development belongs in Candi Court.
