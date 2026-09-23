# Categorization Rules

Categorize in this order and stop at the first that applies. Each step carries a confidence, and only `high` may be posted without review.

1. **Existing platform bank rule** (QBO Rules, Xero bank rules): `high`. The business already decided.
2. **Consistent history**: the same payee categorized to the same account in at least the last 3 occurrences with no exceptions: `high`.
3. **Vendor pattern table below**: `medium`. Patterns are generic; the business may use the vendor differently.
4. **Inference from description or amount alone**: `low`. Always goes to the review queue.

Note the reason with each proposal ("rule: Rent ACH", "history: 6 of 6 to Software", "pattern: fuel merchant"). A reviewer can accept a reasoned proposal in seconds; an unexplained one has to be redone.

## Chart of accounts mapping

Use the business's own chart. When mapping a description to it, target these common SMB accounts, and map to the closest existing account rather than creating new ones. Never create accounts without the owner or accountant agreeing.

| Type | Common accounts |
|---|---|
| Income | Sales / Service Revenue, Product Sales, Shipping Income, Refunds and Allowances (contra), Interest Income, Other Income |
| Cost of goods sold | Materials, Merchandise Purchases, Subcontractors (job-related), Freight In, Merchant/Processing Fees (some businesses put these in expenses) |
| Operating expense | Advertising and Marketing, Bank Service Charges, Contract Labor, Dues and Subscriptions, Insurance, Meals, Office Supplies, Payroll Expenses (wages, employer taxes, benefits), Professional Fees (legal, accounting), Rent or Lease, Repairs and Maintenance, Software and Subscriptions, Telephone and Internet, Travel, Utilities, Vehicle (fuel, maintenance) |
| Current asset | Checking, Savings, Undeposited Funds, Accounts Receivable, Prepaid Expenses, Inventory |
| Fixed asset | Equipment, Vehicles, Furniture, Accumulated Depreciation |
| Liability | Accounts Payable, Credit Cards (one per card), Payroll Liabilities, Sales Tax Payable, Customer Deposits / Deferred Revenue, Loans Payable (short and long term) |
| Equity | Owner Contributions, Owner Draws / Distributions, Retained Earnings |

## Vendor pattern table (confidence: medium)

| Description contains | Proposed account | Watch for |
|---|---|---|
| Payroll provider names, "PAYROLL", "DIR DEP" | Payroll clearing or Payroll Expenses | Net pay, taxes, and fees arrive as separate debits. Map each to the provider's register, not all to wages. |
| "IRS", "EFTPS", state tax agency | Payroll Liabilities, or accountant question | Could be payroll deposits, income tax, or penalties. Never expense by default. |
| Card processor or marketplace payout | Undeposited Funds / processor clearing | Payout is net of fees and refunds. Record gross sales and fees separately. |
| Card issuer name + "PAYMENT", "EPAYMENT", "AUTOPAY", "THANK YOU" | Credit card liability (transfer) | Never an expense. The charges were expensed on the card. |
| "TRANSFER", "XFER", "TO SAVINGS", own account last 4 | Transfer to the other own account | Never income or expense. Match the other leg. |
| Loan servicer, "LOAN PMT" | Loan payable (principal) + Interest Expense | Split per the lender statement. |
| "SERVICE FEE", "MAINTENANCE FEE", "WIRE FEE", "NSF" | Bank Service Charges | NSF may also mean a customer check bounced: reverse the deposit. |
| "INTEREST PAID", "INT EARNED" | Interest Income | |
| Fuel merchants, fleet cards | Vehicle: Fuel | Personal vehicle use: accountant question. |
| Software, SaaS, app stores | Software and Subscriptions | Annual prepayments above threshold may be prepaid assets. |
| Airlines, hotels, rideshare | Travel | Meals during travel go to Meals. |
| Restaurants, food delivery | Meals | Deductibility varies: accountant decides, bookkeeping just records Meals. |
| Online marketplaces (general retailers) | Office Supplies (low) | Generic retailers sell everything. Needs receipt or review. Always `low`. |
| Big-box hardware / home stores | Materials, Repairs, or Supplies (low) | Job materials vs repairs vs equipment depends on the purchase. |
| Utility companies | Utilities | |
| Telecom and ISP | Telephone and Internet | |
| Insurance carriers | Insurance, or Prepaid Insurance for annual premiums | Health insurance for owners: accountant question. |
| Landlord or property manager, "RENT" | Rent or Lease | |
| Advertising platforms | Advertising and Marketing | |
| Cash withdrawals, "ATM" | Owner Draws or Petty Cash (low) | Ask. Never expense cash withdrawals without support. |
| Zelle/Venmo/P2P to individuals | Contract Labor or Owner Draws (low) | Contractor payments need year-end reporting tracking; personal payments are draws. |

## Always human judgment (never above `low`, always on the review queue)

- Owner transactions: personal spending on business accounts, contributions, draws, loans to or from the owner.
- Anything that may be a fixed asset (equipment, vehicles, improvements) above the capitalization threshold.
- Transactions with related parties.
- Refunds and chargebacks (which sale do they reverse?).
- Lump deposits with no invoice: sale, loan proceeds, owner contribution, or refund?
- Tax payments of any kind.
- Large or unusual amounts versus the account's history (default: over 3x the payee's median).
- Anything where the description is only a reference number.

## Split transactions

A single bank line may cover several accounts (a card purchase of supplies and a meal, a loan payment of principal and interest, a payroll debit of net pay and fees). Split to the source document. If no document exists, categorize to the dominant account at `low` and note "split unknown". Never split by guessing percentages.

## Writing bank rules

When the same `high` categorization repeats monthly, propose a platform bank rule so the next close is faster. Keep conditions narrow (payee text plus amount range where stable), put the most specific rules first (both QBO and Xero apply rules in priority order), and do not enable auto-add/auto-confirm on rules for vendors that sell mixed goods.
