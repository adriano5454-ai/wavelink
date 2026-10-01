# Wavelink UI85 — Authentic Contribution Badges

**Prepared:** 1 October 2026  
**Core:** 1.34.19  
**Parent:** exact cumulative UI84 repository  
**Runtime variant:** `workspace-ui85-authentic-contribution-badges-2026-10-01`

## Why this release exists

The first Wavelink badge set was visually polished but too glossy, ornate and synthetic. UI85 replaces it with a quieter, hand-authored maritime medallion system that feels closer to real survey, vessel and offshore work.

The badge system remains cosmetic recognition. It does not represent competency, rank, safety approval, employment performance or authority.

## Included

- Thirty newly drawn badge assets: ten cumulative tiers × three choices per tier.
- Restrained navy, aged-brass, steel and tier-accent palette.
- Clean vector-style maritime symbols with consistent 300 × 300 transparent app exports.
- Editable SVG and PNG masters supplied as a separate asset pack.
- Existing stable badge IDs retained so saved profile choices and backups continue to resolve.
- Human badge titles and short symbolic descriptions in Profile, Team and the permanent top-bar badge surface.
- Badge artwork shown directly without the earlier glossy CSS medallion behind it.
- UI85 service-worker cache replacement for all thirty images.

## Badge choice and progression remain unchanged

- Tiers remain Starter, Bronze, Silver, Gold, Platinum, Emerald, Diamond, Master, Grandmaster and Legend.
- Thresholds remain 0, 25, 50, 100, 150, 225, 325, 500, 750 and 1,000 contribution points.
- Each tier still unlocks three selectable choices.
- Previously selected IDs such as `gold-survey-wave` remain valid.
- Members keep earlier unlocked choices and may select them from My profile.
- Existing contribution adapters, award values, reversals, privacy rules and authority checks are unchanged.

Titles and descriptions are symbolic design metadata. For example, choosing **Keeping It Running** does not claim that all of a member's points came from Maintenance. Eligibility continues to come only from the existing cumulative contribution-point rules.

## Deliberately unchanged

- No database migration or reset.
- No badge-ID, tier-threshold or scoring-rule change.
- No operational API, permission or security-role change.
- No recognition adapter or completion-rule change.
- No environment variable.
- No timer, MutationObserver, page decorator or shell movement.
- Mail Startup M01 remains byte-identical.
- UI84 company-workspace terminology, company logo and native Original Files route remain intact.

## Apply

Apply only over exact UI84. Copy all files from the release `UPLOAD_TO_GITHUB` folder into the Wavelink application repository, review every changed path, commit and push. Preserve the current commit as a rollback point.

UI85 has no schema migration. The cumulative UI83 account-security database boundary still applies: an earlier application rollback across UI83 requires the corresponding earlier complete database backup.

## Demo acceptance

- Open My profile and confirm all thirty choices use the new restrained maritime artwork.
- Confirm the selected badge appears in Profile, Team updates and the permanent top bar.
- Change to another already-unlocked badge and confirm the stable selection persists after reload.
- Confirm locked choices remain refused by the server.
- Check 1440, 390 and 320 CSS-pixel layouts for clipping or document-level horizontal overflow.
- Confirm likes, points, permissions and operational approvals do not change when selecting artwork.
- Confirm the UI84 company identity and Original Files route remain unchanged.
