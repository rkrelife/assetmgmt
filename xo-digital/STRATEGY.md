# XO Digital — Strategy

## 1. Regulatory frame (the box we operate in)
CVM Resolution 88 governs investment crowdfunding in Brazil. Key constraints that
shape product and strategy:
- Offers are capped per issuer (annual fundraising limit per company).
- Retail investors have per-investor annual investment limits tied to income/assets,
  unless they qualify as "investidor qualificado."
- Mandatory disclosure, a standardized "lâmina"/offer sheet, and a cooling-off /
  withdrawal right for investors.
- The platform is responsible for investor suitability and for verifying limits.

Implication: compliance is a **core platform constraint**, not overhead. The
per-investor limit directly bounds how much each of the "millions of customers" can
deploy — the R$1,000–10,000 ticket fits retail caps well, which validates the model.

## 2. Wedge: WhatsApp-native investing
Be among the first platforms where the **full regulated loop** lives in WhatsApp:
registration, KYC, suitability questionnaire, investing, signed subscription,
portfolio, statements, and support.

Why it fits this segment:
- WhatsApp is the default interface for Brazilian retail; near-universal penetration.
- Removes the highest-friction step for first-time investors — downloading/learning an app.
- Conversational onboarding can make a regulated, intimidating product feel approachable.

What this actually requires (this is a real engineering + compliance bet, not a chatbot):
- WhatsApp Business / Cloud API at scale, with templated + session messaging.
- Conversational KYC with document capture and liveness, feeding a real identity check.
- Suitability questionnaire and limit enforcement inside the chat flow.
- Legally valid e-signature / consent for subscriptions within WhatsApp.
- PIX integration for funding and redemptions.
- Accurate ledger + portfolio statements deliverable in-chat and as documents.

## 3. Target customer & unit economics
- Retail / middle-market Brazilian investors, R$1,000–10,000 per offer.
- Volume thesis (millions of customers) means **cost-per-user must be tiny**:
  - CAC via WhatsApp/Instagram virality and referral, not paid app-install funnels.
  - KYC cost-per-user matters at millions of users — negotiate per-check pricing.
  - Support must be largely automated; WhatsApp conversation costs scale with volume
    and must be modeled into the P&L (this can quietly become a major cost line).
- Revenue: platform/structuring fees on offers (supply side) + possible spread/fees.
  Confirm what CVM 88 permits the platform to charge and to whom.

## 4. Two sides — sequencing
The classic marketplace chicken-and-egg. Demand (investors) is the visible bet, but
**supply (quality offers) is the binding constraint**:
- You can acquire millions of investors and have nothing compelling to offer them.
- Recommend: secure a credible **launch pipeline of offers** (the 2 funding founders'
  job) *before* opening the demand floodgates. Quality and timely repayment of the
  first offers define platform trust forever.

## 5. Go-to-market phases
- **Phase 0 — Pre-launch (now):** lock team roles, name a compliance owner, build the
  WhatsApp MVP for one full offer end-to-end, line up the first 2–3 issuers.
- **Phase 1 — Soft launch:** invite-only / waitlist via Instagram; first offers with a
  controlled investor cohort; instrument everything; prove the WhatsApp loop and repayment.
- **Phase 2 — Scale demand:** referral mechanics, content, Instagram growth, press the
  "first fully-WhatsApp investing platform in Brazil" story.
- **Phase 3 — Broaden supply:** more issuers, more offer types, deeper underwriting.

## 6. Open risks to resolve before launch
1. **Offer pipeline depth** vs. demand ambition — is there enough supply for scale?
2. **WhatsApp API cost at scale** — model conversation costs into unit economics.
3. **Chat-native KYC/suitability** — confirm with legal it satisfies CVM 88 as the
   *sole* channel; may need a web fallback for certain regulated steps.
4. **First-offer repayment risk** — early defaults would kill trust; underwrite the
   launch cohort conservatively.
5. **Differentiation durability** — "WhatsApp-first" can be copied; the moat is
   execution speed, brand trust, and supply relationships.
