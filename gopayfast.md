
# GoPayFast — Project Audit Checklist

## Current Codebase vs. Required Pages

> Stack: Django · SQLite · Vanilla CSS/JS · Tailwind
> Audited: April 2026

---

## Quick Summary

| Status                                           | Count   |
| ------------------------------------------------ | ------- |
| ✅ Done (template + view exists)                 | 14      |
| ⚠️ Template exists — content needs SBP review | 4       |
| 🔴 Missing — template + view both needed        | 11      |
| 📁 Excluded from tree (dashboard dir)            | Unknown |

---

## CATEGORY A — Legal / Compliance Pages

| Page                          | Template                    | View                        | Status                       | Action                                                                             |
| ----------------------------- | --------------------------- | --------------------------- | ---------------------------- | ---------------------------------------------------------------------------------- |
| Terms & Conditions (Consumer) | `landing/terms.html`✅    | `extra_pages.py`(assumed) | ⚠️**Content Review** | Add SBP jurisdiction clause, ETO 2002 reference, transaction limits, liability cap |
| Merchant Agreement            | ❌                          | ❌                          | 🔴**Missing**          | New page:`/merchant-agreement/`— separate from consumer T&C                     |
| Privacy Policy                | `landing/privacy.html`✅  | `extra_pages.py`(assumed) | ⚠️**Content Review** | Add: PCI DSS data handling, AML record retention (10 years), SBP CPD reference     |
| AML / KYC Policy              | ❌                          | ❌                          | 🔴**Missing**          | New page:`/aml-policy/`— required by SBP AML/CFT Regulations                    |
| Refund & Dispute Policy       | `landing/return.html`✅   | `extra_pages.py`(assumed) | ⚠️**Content Review** | Add: 7-day auto-refund timeline, 10–12 day processing, dispute escalation path    |
| Acceptable Use Policy         | ❌                          | ❌                          | 🔴**Missing**          | New page:`/acceptable-use/`— define prohibited merchants/transactions           |
| Cookie Policy                 | ❌                          | ❌                          | 🔴**Missing**          | New page:`/cookie-policy/`— add cookie banner JS too                            |
| Shipping Policy               | `landing/shipping.html`✅ | `extra_pages.py`(assumed) | ✅**Done**             | OK — not GoPayFast-specific but good to have                                      |

---

## CATEGORY B — Transaction Flow Pages

| Page                           | Template                             | View                                     | Status                      | Action                                                                                                            |
| ------------------------------ | ------------------------------------ | ---------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Payment Checkout               | `landing/checkout.html`✅          | `views/checkout.py`✅                  | ⚠️**Needs Review**  | Verify: HTTPS enforced, 3DS OTP shown, merchant name + amount summary visible, cancel button                      |
| Payment Confirmation (Success) | ❌                                   | ❌                                       | 🔴**Missing**         | New:`landing/payment_success.html`+ route in `checkout.py`— show TXN ID, amount, timestamp, receipt download |
| Payment Failure / Declined     | `landing/error.html`✅ (generic)   | `views/not_found.py`or `checkout.py` | ⚠️**Needs Upgrade** | Rename/add `payment_failed.html`— show failure reason, auto-refund notice (7 days), retry button               |
| Payment Pending                | ❌                                   | ❌                                       | 🔴**Missing**         | New:`landing/payment_pending.html`— spinner, TXN ref, "do not close" warning                                   |
| Transaction Receipt            | ❌                                   | ❌                                       | 🔴**Missing**         | New:`landing/receipt.html`+`views/checkout.py`GET route — printable, TXN ID, masked payer, download PDF      |
| Refund Status                  | ❌                                   | ❌                                       | 🔴**Missing**         | New:`landing/refund_status.html`— lookup by TXN ID, status stages, expected date                               |
| Order Confirmation Email       | `emails/order_confirmation.html`✅ | signals.py (assumed)                     | ✅**Done**            | Good — verify it includes TXN ID and GoPayFast reference                                                         |

---

## CATEGORY C — Merchant-Facing Pages

| Page                          | Template                                   | View                    | Status                      | Action                                                                                              |
| ----------------------------- | ------------------------------------------ | ----------------------- | --------------------------- | --------------------------------------------------------------------------------------------------- |
| Merchant Signup / Get Started | `landing/register.html`✅                | `views/register.py`✅ | ⚠️**Needs Upgrade** | Add: NTN, CNIC, Utility Bill upload fields. Add merchant type selector. Wire to KYC flow            |
| Merchant Login                | `landing/login.html`✅                   | `views/login.py`✅    | ⚠️**Needs Upgrade** | Add: 2FA/OTP step. Add session timeout (15 min). Add brute-force lockout                            |
| Merchant KYC / Documents      | ❌                                         | ❌                      | 🔴**Missing**         | New:`landing/kyc.html`— document upload, status tracker (Pending/Approved/Rejected)              |
| Merchant Dashboard            | 📁**In excluded `/dashboard/`dir** | Likely exists           | ❓**Unverified**      | Run `find ./dashboard -name "*.html"`to confirm — verify settlement, refund, reports pages exist |
| Transaction History           | 📁 In dashboard                            | Likely exists           | ❓**Unverified**      | Confirm export (CSV/PDF) works                                                                      |
| Settlement Reports            | 📁 In dashboard                            | Likely exists           | ❓**Unverified**      | Confirm T+2/T+3 breakdown is visible                                                                |
| Pricing                       | `landing/`— ❌ not found                | ❌                      | 🔴**Missing**         | New:`landing/pricing.html`— per-method fee table, settlement fees, chargeback fees               |

---

## CATEGORY D — Public Information Pages

| Page                  | Template                              | View                                     | Status              | Action                                                                                  |
| --------------------- | ------------------------------------- | ---------------------------------------- | ------------------- | --------------------------------------------------------------------------------------- |
| Home / Landing        | `landing/body.html`/`base.html`✅ | `views/main.py`✅                      | ✅**Done**    | Add SBP PSO/PSP badge + PCI-DSS badge to footer                                         |
| About Us              | `landing/about.html`✅              | `views/main.py`or `extra_pages.py`✅ | ✅**Done**    | Add: SECP registration, physical Karachi address, SBP license milestone                 |
| Contact Us            | `landing/contact.html`✅            | `views/extra_pages.py`(assumed) ✅     | ✅**Done**    | Add: Compliance Officer email, office address, BMP escalation link                      |
| FAQ                   | `landing/faq.html`✅                | `views/extra_pages.py`✅               | ✅**Done**    | Add sections: Failed payments, Refund timelines, Unauthorized TXN, 3DS/OTP              |
| Payment Methods       | `landing/payment_methods.html`✅    | Likely in `extra_pages.py`✅           | ✅**Done**    | Add: Transaction limits per method, currency conversion note for intl cards             |
| Products / Services   | `landing/products.html`✅           | `views/products.py`✅                  | ✅**Done**    | This is e-commerce products — also add a GoPayFast Services page if needed             |
| Security / Trust Page | ❌                                    | ❌                                       | 🔴**Missing** | New:`landing/security.html`— PCI-DSS v4.0.1 badge, 3DS, encryption, fraud monitoring |

---

## CATEGORY E — Support & Grievance Pages

| Page                       | Template                           | View                         | Status              | Action                                                                                                                             |
| -------------------------- | ---------------------------------- | ---------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Complaint / Grievance Form | ❌ (contact.html partially covers) | ❌                           | 🔴**Missing** | New dedicated:`landing/complaints.html`— complaint form, ref number, 48hr SLA, BMP escalation info.**SBP § 5 Mandatory** |
| 404 Not Found              | `landing/not_found.html`✅       | `views/not_found.py`✅     | ✅**Done**    | OK                                                                                                                                 |
| Error Page                 | `landing/error.html`✅           | Likely in `not_found.py`✅ | ✅**Done**    | Repurpose for generic 500 errors, make separate `payment_failed.html`                                                            |
| Status Page                | ❌                                 | ❌                           | 🔴**Missing** | New:`/status/`or external (UptimeRobot embed) — real-time gateway status                                                        |

---

## CATEGORY F — Developer / Integration

| Page                         | Template                          | View | Status              | Action                                                                                                     |
| ---------------------------- | --------------------------------- | ---- | ------------------- | ---------------------------------------------------------------------------------------------------------- |
| PayFast API Service          | `services/payfast_service.py`✅ | —   | ✅**Done**    | Verify: hash/HMAC signing, error handling, retry logic                                                     |
| Checkout JS                  | `static/js/checkout.js`✅       | —   | ✅**Done**    | Review: is 3DS redirect handled? Is payment status polled?                                                 |
| Webhook Handler              | ❌ in views                       | ❌   | 🔴**Missing** | Add `views/webhooks.py`— handle payment.success, payment.failed, refund.processed events from GoPayFast |
| API Docs / Integration Guide | ❌                                | ❌   | 🔴**Missing** | Add `landing/docs.html`or link to `gopayfast.com/docs`                                                 |

---

## File-Level Action Items

### Files that need changes (not new files)

```
views/checkout.py
  → Add: payment_success view (GET + context)
  → Add: payment_failed view
  → Add: payment_pending view
  → Add: receipt view (by transaction_id)
  → Handle PayFast callback/redirect URL

views/register.py
  → Add: NTN, CNIC, Utility Bill fields to merchant signup
  → Add: KYC document upload handling

views/extra_pages.py
  → Add routes for: AML policy, Acceptable Use, Cookie Policy, Complaints, Security, Pricing

app/urls.py
  → Wire all new views above

landing/terms.html
  → Add: Pakistani jurisdiction, ETO 2002 reference, transaction limit disclosures

landing/privacy.html
  → Add: PCI DSS section, AML record retention (10 years), SBP CPD reference

landing/return.html
  → Add: 7-day auto-refund, 10–12 day processing, dispute escalation, BMP info

landing/checkout.html
  → Add: security badge, payment method icons, 3DS OTP step visibility

landing/register.html
  → Add: document upload UI, merchant type selector, KYC disclaimer
```

### New files to create

```
templates/landing/
  ├── payment_success.html      🔴 HIGH
  ├── payment_failed.html       🔴 HIGH
  ├── payment_pending.html      🔴 HIGH
  ├── receipt.html              🔴 HIGH
  ├── complaints.html           🔴 HIGH (SBP mandatory)
  ├── aml_policy.html           🔴 HIGH
  ├── acceptable_use.html       🔴 HIGH
  ├── merchant_agreement.html   🔴 HIGH
  ├── pricing.html              🟡 MEDIUM
  ├── kyc.html                  🟡 MEDIUM
  ├── refund_status.html        🟡 MEDIUM
  ├── security.html             🟡 MEDIUM
  ├── cookie_policy.html        🟠 LOW
  └── status.html               🟠 LOW

app/views/
  ├── webhooks.py               🔴 HIGH
  └── (extend extra_pages.py)   🔴 HIGH

static/js/
  └── cookie_banner.js          🟠 LOW
```

---

## Build Order (Sprint Plan)

### Sprint 1 — Compliance & Legal (Do this week)

> These block SBP compliance and merchant trust.

* [ ] **`payment_success.html`** + view in `checkout.py`
* [ ] **`payment_failed.html`** + view in `checkout.py` (upgrade `error.html`)
* [ ] **`payment_pending.html`** + view in `checkout.py`
* [ ] **`complaints.html`** + route — SBP § 5 mandatory
* [ ] **`aml_policy.html`** + route in `extra_pages.py`
* [ ] **`merchant_agreement.html`** + route in `extra_pages.py`
* [ ] **`acceptable_use.html`** + route in `extra_pages.py`
* [ ] Update **`terms.html`** — add SBP content
* [ ] Update **`privacy.html`** — add PCI DSS + AML sections
* [ ] Update **`return.html`** — add SBP-compliant refund timelines

### Sprint 2 — Transaction Flow (Next week)

> These complete the payment UX and reduce disputes.

* [ ] **`receipt.html`** + view — printable, TXN ID, download PDF
* [ ] **`refund_status.html`** + view — lookup by TXN ID
* [ ] **`webhooks.py`** — handle GoPayFast callbacks
* [ ] Update **`checkout.html`** — security badge, 3DS OTP step
* [ ] Verify **`payfast_service.py`** — hash signing, error handling, retry

### Sprint 3 — Merchant Onboarding (Week 3)

> These enable proper SBP-compliant merchant KYC.

* [ ] **`kyc.html`** — document upload, status tracker
* [ ] Update **`register.html`** — NTN, CNIC, Utility Bill fields
* [ ] **`pricing.html`** — per-method fee table
* [ ] **`security.html`** — PCI-DSS badge, fraud monitoring
* [ ] Audit **`/dashboard/`** directory — verify settlement + reports pages

### Sprint 4 — Polish (Week 4)

* [ ] **`cookie_policy.html`** + cookie banner JS
* [ ] **`status.html`** — or embed UptimeRobot
* [ ] Update **`about.html`** — SECP registration, Karachi address
* [ ] Update **`contact.html`** — Compliance Officer email, BMP link
* [ ] Update **`faq.html`** — payment-specific Q&As
* [ ] Add SBP + PCI-DSS badges to footer in **`base.html`**

---

## One-Line Dashboard Audit Command

Run this to see what's inside your excluded dashboard dir:

```bash
find ./dashboard -type f -name "*.html" | sort
```

Then paste the output — I'll map those too.

---

*Audit date: April 2026 | Based on project tree + GOPAYFAST_REQUIRED_PAGES.md*
