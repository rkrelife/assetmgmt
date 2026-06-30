# XO Digital — CVM 88 Compliance

> Operational checklist, not legal advice. Validate every point with qualified Brazilian
> counsel / a compliance specialist before launch.

## Why this is urgent
The platform is the regulated party under CVM 88. Today **no one owns this full-time**.
A regulated investment platform cannot launch with compliance as a shared side-duty.
This document exists to make the gap concrete and assignable.

## What CVM 88 requires the platform to do (operational view)
1. **Investor onboarding & limits**
   - Verify identity (KYC) and collect the data needed to enforce investment limits.
   - Enforce per-investor annual investment caps (income/asset-based) for retail
     investors; identify "investidor qualificado" status where it lifts caps.
   - Track each investor's cumulative investments across offers to stay within limits.
2. **Suitability**
   - Administer a suitability assessment and ensure offers shown/sold are appropriate.
3. **Offer / issuer review**
   - Conduct due diligence on issuers and offers before listing.
   - Publish the standardized offer material (lâmina) with mandatory disclosures.
   - Enforce per-issuer annual fundraising limits.
4. **Investor rights**
   - Honor the withdrawal / cooling-off right within the regulated window.
   - Provide clear risk warnings.
5. **Funds handling**
   - Segregate investor funds appropriately during the offer period; ensure proper
     flow on success/cancellation (confirm escrow/segregation mechanics with counsel).
6. **Recordkeeping & reporting**
   - Maintain records of investors, offers, and transactions.
   - File periodic reports to CVM and meet ongoing platform-obligation requirements.
   - AML/PLD program: monitoring, suspicious-activity reporting (COAF).

## WhatsApp-specific compliance questions (resolve before building chat-only)
- Does a suitability questionnaire administered **in chat** satisfy CVM 88?
- Is **e-signature/consent inside WhatsApp** legally valid for subscriptions?
- Are mandatory disclosures (lâmina, risk warnings) adequately delivered in a chat UI,
  or is a document/web fallback required for certain steps?
- Audit trail: can every regulated interaction in WhatsApp be logged and reproduced for
  CVM on request? (Build logging in from day one.)

## Ownership
- **Single named owner required:** Head of Compliance & Risk (founder Funding 2, or
  first external hire if no founder can own it full-time).
- This owner signs off before any offer goes live and owns the CVM relationship jointly
  with the CEO.

## Immediate actions
1. Assign the compliance owner (founder or hire) — this week.
2. Engage Brazilian securities counsel to validate the WhatsApp-native flows.
3. Map each CVM 88 obligation above to a system feature or manual control before launch.
4. Stand up AML/PLD + audit logging as part of the MVP, not as a later add-on.
