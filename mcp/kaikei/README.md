# kaikei MCP

This is the stdio MCP server for [kaikei](https://github.com/cloud-itonami/kaikei), an itonami dapp for accounting ledgers, invoices and bank statements. The dapp is also published at https://itonami.cloud/sites/app/kaikei/.

kaikei reads journal exports from MoneyForward クラウド会計, freee 会計, 弥生会計, QuickBooks Online and Xero, and builds a trial balance, P&L and balance sheet. It also handles invoices: it reads and writes Xero, QuickBooks Online, freee請求書 and MoneyForward クラウド請求書 invoices (JSON and import CSV), reads Zoho Invoice and FreshBooks invoices, checks the contents a Japanese qualified invoice must state, and posts invoices as receivable or payable entries. It reads bank and card statements the user downloaded and Ramp, Brex, Expensify and BILL exports, reconciles them against the ledger, and suggests invoice settlements, matches and journals for each line. It posts only the lines the user approved. Every tool is a pure function over the text or ledger the caller passes:

| tool | does |
|---|---|
| `kaikei_import` | Reads a journal or invoice export and returns a `kaikei.ledger.v1` ledger with checks and warnings. Journals: MoneyForward 仕訳帳 CSV, freee 仕訳 CSV, 弥生インポート形式, QuickBooks Online Account/JournalEntry JSON or journal CSV, Xero Accounts/Journals/ManualJournals JSON or manual journal CSV. Invoices: Xero Invoices JSON and invoice/bill CSV, QuickBooks Online Invoice/Bill JSON and invoice CSV, freee請求書 CSV and API JSON, MoneyForward クラウド請求書 CSV and API v3 JSON, Zoho Invoice JSON, FreshBooks invoice/bill JSON. Statements: OFX/QFX/QBO bank and card statements (SGML or XML), 全銀 入出金取引明細 and 振込入金明細 (fixed-length or CSV), freee, MoneyForward, Xero and QuickBooks Online statement CSV, and bank or card CSV recognised from its header. Expense and AP: Ramp transactions, reimbursements and bills JSON, Brex card transactions and reimbursement expenses JSON, Expensify CSV exported with kaikei's template, BILL v3 bills JSON. Also a kaikei ledger. Shift_JIS files go in as `bytes_base64`. Invoices and statement lines are imported, not posted. |
| `kaikei_validate` | Checks that the balance sheet balances and lists unclassified accounts and invalid entries. Invalid means unbalanced, negative, missing an account or with a bad date. |
| `kaikei_report` | Returns a trial balance, P&L or balance sheet for a period, in kaikei's own JSON or in the shape of the QuickBooks Online Report or Xero Reports responses. |
| `kaikei_export` | Writes a ledger in the journal and invoice formats above, or one statement account (`statement_account`) as freee, MoneyForward, Xero or QuickBooks Online statement CSV. Shift_JIS output comes back in base64, and fields the format cannot hold are listed in `notes`. |
| `kaikei_convert` | Runs import followed by export. |
| `kaikei_invoice_totals` | Per-rate consideration and consumption tax for invoice lines, rounded once per invoice per rate (消費税法施行令 70 条の 10), and each line's share of the tax. Needs no ledger. |
| `kaikei_invoice_check` | For each invoice in a ledger: missing qualified-invoice contents, differences between the stated tax and one rounding per rate, the transitional deduction percent for purchases from unregistered sellers, and whether it can be posted. |
| `kaikei_invoice_post` | Posts issued or paid invoices as receivable / sales / output tax (or the purchase side) entries and returns the new ledger. Skips drafts, voids, invoices with withholding and invoices already in the ledger. |
| `kaikei_statement_check` | For each statement account: line counts by status (open, posted, matched, excluded), the statement's last balance against the ledger account's balance on that date, and the first line where the running balance breaks. Also a receivable and payable aging in 30-day buckets from the due date. |
| `kaikei_statement_suggest` | Candidates for each open line, without changing the ledger: invoices the payment settles (exact, short by a bank fee, partial, or several invoices of one customer), journal entries to match, transfers between statement accounts, and journals from the user's rules and from rules learned from the user's own past journals. Each has a strength (3 strong, 2 medium, 1 weak), its reasons and a `choice`. |
| `kaikei_statement_post` | Posts only the approved lines, each with its `choice`: settle invoices, match an entry, post a transfer, post to an account with consumption tax split at the date's rate, or exclude the line. `"preselected"` takes the single strong candidate. Returns the new ledger; lines without an approval are untouched. |

How these tools handle the data:

- Nothing is sent to an accounting service or anywhere else, and nothing is stored.
- Amounts are integers in the currency's minor unit, using ISO 4217 exponents. A value with more decimal places than the currency allows is rejected, not rounded.
- An account kaikei cannot classify stays unclassified and is left out of the P&L and balance sheet; it is never guessed.
- The class mapping and the staged-profit and retained-earnings rules are kaikei's own. They do not reproduce any vendor's calculation.
- A registration number is checked for its form (T + 13 digits) only. The NTA publication site is not queried, and an invoice is never certified as qualified.
- Statements come only from files the user downloaded. kaikei connects to no bank, card issuer, Ramp, Brex, Expensify or BILL, does no account aggregation and makes no payment. Ramp, Brex, Expensify and BILL data is read only.
- Only the MUFG BizSTATION CSV preset is checked against the bank's published layout. The other bank and card presets are marked unverified, and an import with one says so in `warnings`.
- A short payment's difference is booked as a bank fee by the ledger's setting: by default as a return of the sale's consideration (account 支払手数料, NTA インボイス Q&A 問 30), or as a purchase or a discount, per customer. A date without a confirmed rate (before 2014-04-01, or reduced-rate items from 2027-04-01) is not guessed; the line is skipped as `rate-unknown` until the choice gives a rate.
- `kaikei_import` reads one file into a new ledger and does not merge into an existing one. To reconcile a statement against books, pass a kaikei ledger exported from the browser app, which holds the journals, invoices, statement lines and rules together.
- Learned rules come from the user's own past journals in the ledger, by a fixed counting rule. Nothing is inferred by a model, and a suggestion is never posted without an approval.
- The tools run on the same `.cljk` adapter as the browser app. That adapter agrees with the wasm guest `aiueos/kaikei_journal.cljk` on the repository's 192-row parity table (journal checks, financial statements, invoice tax, consumption-tax rates by date, statement balances and matching levels). The guest itself is not loaded here.

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

Status: source-inspected and protocol-tested through the itonami-agent MCP client (`discover`/`call`) on synthetic fixtures, all 11 tools. A model-driven agent turn has not been tested.
