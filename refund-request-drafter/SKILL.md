---
name: refund-request-drafter
description: Draft clear, persuasive refund, cancellation, or billing-dispute requests from purchase receipts, timelines, and vendor policies. Use when the user asks to write a refund email, dispute a charge, cancel a subscription, or escalate an unresolved support ticket.
allowed-tools: client
---
# Refund Request Drafter

Draft concise, policy-grounded refund, cancellation, or billing-dispute messages tailored to the vendor's published policy and the user's purchase details.

## When to Use

- The user wants to request a refund for a product, SaaS subscription, flight/hotel, or service.
- The user needs to escalate an ignored support ticket or prepare a clear paper trail for a card dispute/chargeback.
- The user provides a receipt, order number, or screenshot and asks Claude to write the request.

## Steps

### 1. Collect Key Facts

Extract from the user's message or files (ask only for missing essentials):

- Vendor/merchant name and order/invoice/booking ID.
- Purchase date, amount, and payment method (last 4 digits if relevant, never full card numbers).
- Reason for refund (defective, cancelled within window, unauthorized renewal, service not delivered) and prior support attempts.

### 2. Check the Vendor's Refund Policy

- If the vendor's policy URL or text is available, read it to cite exact eligibility windows, cancellation rules, or statutory rights.
- Do not fabricate policy terms or guarantees not verified in the vendor's policy.

### 3. Draft the Request

Write a polite, firm, scannable message ready to paste or send:

- **Subject line**: Clear and specific (`Refund Request - Order #<ID> - <Product/Service>`).
- **Opening**: State the request and order details in the first two sentences.
- **Basis**: Summarize the timeline and why it qualifies under the policy (or consumer protection rules).
- **Ask & Deadline**: Request confirmation of the refund amount, original payment method, and a specific response timeframe (for example, 5 business days).

## Gotchas

- **Protect sensitive data**: Never ask for or include full credit card numbers, CVVs, or passwords in drafts.
- **Keep tone factual**: Firm, polite, and chronological messages get resolved faster than angry or threatening ones.
- **Confirm before sending**: Show the user the final subject, recipient, and body, and send only after they approve. A refund request sent by mistake can create a dispute the user did not intend.
- **Consumer-rights references are jurisdiction-specific**: Cite a statute only when the user's country or state is known and the rule has been checked. Otherwise, cite the vendor's own policy text.
- **Leave no `[Insert ...]` blanks**: Pre-fill every known detail from the user's context; only flag genuinely missing fields.
