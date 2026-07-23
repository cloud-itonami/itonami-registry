# Atlas to bank-provider handoff

`com-stripe` owns Stripe and Stripe Atlas contracts. It does not own company
formation policy or a bank provider's approval policy.

## Boundaries

- company-formation workflow: `cloud-itonami-isic-6910`
- monetary-intermediation workflow: `cloud-itonami-isic-6419`
- Mercury adapter: `kotoba-lang/com-mercury`

## Payment-account cutover

Before moving an application from a predecessor Stripe seller account:

1. activate the target Stripe account for the intended legal entity
2. verify the payout destination through Stripe without exposing bank details
3. store live and webhook secrets only in the operator vault
4. pause checkout and record the predecessor account reconciliation cursor
5. recreate the production webhook in the target account
6. assert `/v1/account` country and normalized legal name against configuration
7. require charges and payouts enabled with no due requirements
8. perform an approved low-value purchase, payout, refund, and reconciliation
9. disable the predecessor webhook only after outstanding events reconcile

Every assertion fails closed. Provider names, legal names, callback URLs, and
hosting platforms are configuration rather than literals.
