# Personal Home and company access — current boundary

UI63 implements personal Home and separates Workspaces. Existing named login, account IDs,
company databases, permissions and operational writers remain. Home offers exact own work,
configured review actions, saved personal handovers and a bounded actor-attributed activity feed.
This is not a complete security audit, a new account system or pending-member enforcement.

## Supplied company domain

Company ID: `sulmara`
Intended corporate email domain: `sulmara.com` (addresses ending in `@sulmara.com`).
Source: explicitly supplied by Adriano in this conversation on 29 September 2026.
Status: **user-supplied; domain control NOT verified; routing/self-registration NOT enabled**.

Do not treat the company display identity, this file, a DNS name or a typed email address as
proof of mailbox/domain ownership. This entry is planning documentation, not an authentication
registry, an environment setting or a permission grant. No email has been sent.

## Next coherent stages

B. Verified personal-email membership invitations, atomic pending/deny-all membership and a
request queue. Preserve existing local user IDs and evidence. A normal Technician's defaults
are NOT acceptable for an unapproved new member. Reviewers require explicit approval authority;
a department-head title is not automatic company administration.

Delegation must intersect the granter's current effective rights, explicit delegable envelope
and target department/site scope. Check dependencies transactionally; no self-promotion,
administrator edit, onward delegation, broad role-default reset or scope expansion. Preserve
independent grants and provenance; define and test revocation cascades. Current record-specific
assignee/approver and private-audience restrictions still apply. Do not merely hide checkboxes.

C. Professional email-first main-site sign-in; verify company domain ownership before enabling
optional domain admission, verify each mailbox, then trusted allowlisted company routing.
`sulmara.com` is the intended exact domain, not subdomains or lookalikes automatically. Private
email recipients use company-bound invitations. Keep existing direct named sign-in during the
reviewed transition. Do not reuse QR sign-only visitors as members or move operational data into
the public demo. Handoffs need short-lived single-use tenant/browser binding and server exchange;
no passwords or reusable tokens in URLs and no broad cross-company cookies.

These later stages require actual identity/data/deployment work, tested email delivery, abuse
controls and real HTTPS/company isolation acceptance. UI63 adds none of those capabilities.


## UI64 Stage B implementation
Invite-only verified mailbox enrollment, server-enforced pending/no-access state, review requests and bounded one-level delegation are implemented. Email remains OFF until configured and real delivery checked. See COMPANY_MEMBERSHIP.md. sulmara.com is still unverified planning metadata; Stage C main-site/domain/email sign-in remains unimplemented. Existing IDs/signatures and UI63 personal Home remain.
