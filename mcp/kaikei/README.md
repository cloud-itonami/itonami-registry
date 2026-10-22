# kaikei MCP

This is the stdio MCP server for [kaikei](https://github.com/cloud-itonami/kaikei), an itonami dapp for accounting ledgers. The dapp is also published at https://itonami.cloud/sites/app/kaikei/.

kaikei reads journal exports from MoneyForward クラウド会計, freee 会計, 弥生会計, QuickBooks Online and Xero, and builds a trial balance, P&L and balance sheet. It also handles invoices: it reads and writes Xero, QuickBooks Online, freee請求書 and MoneyForward クラウド請求書 invoices (JSON and import CSV), reads Zoho Invoice and FreshBooks invoices, checks the contents a Japanese qualified invoice must state, and posts invoices as receivable or payable entries. Every tool is a pure function over the text or ledger the caller passes:

| tool | does |
|---|---|
| `kaikei_import` | Reads a journal or invoice export and returns a `kaikei.ledger.v1` ledger with checks and warnings. Journals: MoneyForward 仕訳帳 CSV, freee 仕訳 CSV, 弥生インポート形式, QuickBooks Online Account/JournalEntry JSON or journal CSV, Xero Accounts/Journals/ManualJournals JSON or manual journal CSV. Invoices: Xero Invoices JSON and invoice/bill CSV, QuickBooks Online Invoice/Bill JSON and invoice CSV, freee請求書 CSV and API JSON, MoneyForward クラウド請求書 CSV and API v3 JSON, Zoho Invoice JSON, FreshBooks invoice/bill JSON. Also a kaikei ledger. Shift_JIS files go in as `bytes_base64`. Invoices are imported, not posted. |
| `kaikei_validate` | Checks that the balance sheet balances and lists unclassified accounts and invalid entries. Invalid means unbalanced, negative, missing an account or with a bad date. |
| `kaikei_report` | Returns a trial balance, P&L or balance sheet for a period, in kaikei's own JSON or in the shape of the QuickBooks Online Report or Xero Reports responses. |
| `kaikei_export` | Writes a ledger in any of the formats above. Shift_JIS output comes back in base64, and fields the format cannot hold are listed in `notes`. |
| `kaikei_convert` | Runs import followed by export. |
| `kaikei_invoice_totals` | Per-rate consideration and consumption tax for invoice lines, rounded once per invoice per rate (消費税法施行令 70 条の 10), and each line's share of the tax. Needs no ledger. |
| `kaikei_invoice_check` | For each invoice in a ledger: missing qualified-invoice contents, differences between the stated tax and one rounding per rate, the transitional deduction percent for purchases from unregistered sellers, and whether it can be posted. |
| `kaikei_invoice_post` | Posts issued or paid invoices as receivable / sales / output tax (or the purchase side) entries and returns the new ledger. Skips drafts, voids, invoices with withholding and invoices already in the ledger. |

How these tools handle the data:

- Nothing is sent to an accounting service or anywhere else, and nothing is stored.
- Amounts are integers in the currency's minor unit, using ISO 4217 exponents. A value with more decimal places than the currency allows is rejected, not rounded.
- An account kaikei cannot classify stays unclassified and is left out of the P&L and balance sheet; it is never guessed.
- The class mapping and the staged-profit and retained-earnings rules are kaikei's own. They do not reproduce any vendor's calculation.
- A registration number is checked for its form (T + 13 digits) only. The NTA publication site is not queried, and an invoice is never certified as qualified.
- The tools run on the same `.cljk` adapter as the browser app. That adapter agrees with the wasm guest `aiueos/kaikei_journal.cljk` on the repository's 110-row parity table (journal checks, statements and invoice tax). The guest itself is not loaded here.

## Use from an itonami agent profile

```yaml
mcp_servers:
  kaikei:
    command: kbb
    args: ["/absolute/path/to/kaikei/bin/kaikei-mcp"]
```

The tools appear as `mcp__kaikei__kaikei_import` and so on. itonami-agent does not start MCP subprocesses on peer runs.

The tools are pure, but a model-driven agent turn is not local. A ledger passed to an agent whose inference rail is remote leaves the machine through that rail. Use synthetic or consented data there.

The first launch resolves the pinned `kotoba-lang/text` git dependency into `~/.gitlibs` over the network and creates a `.nbb/` cache in the checkout. Later launches only read.

Registering this entry enables nothing. A profile owner has to add the `mcp_servers` entry.

Status: source-inspected and protocol-tested through the itonami-agent MCP client (`discover`/`call`) on synthetic fixtures. A model-driven agent turn has not been tested.
