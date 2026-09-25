# Wavelink — Home page improvement plan

**Requested by Adriano on 25 September 2026. Status: pending implementation.**

The Home page still needs work. Keep this as a separate, visible item alongside the ongoing app-wide interface and Help review. UI12 records the request but does not change Home. The current Home implementation and its permission/attention/local-work logic remain byte-identical to the supplied UI11 source.

## Intended direction — proposals to review against the actual implementation

| Area | Proposed improvement | Acceptance requirement |
|---|---|---|
| Starting point | Make the important daily destinations easier to recognise; reduce competing cards and introductory text. | A user can identify where to continue work or find equipment without opening unrelated modules. Preserve the existing sidebar. |
| Personal versus project work | Clearly label assigned work versus project-wide attention information. | No label implies personal assignment merely because an administrator can view an item. Never expose private records or counts through a shortcut. |
| Continue versus start | Distinguish resuming an existing task, checklist or handover from creating another record. | Shortcuts open the actual authorised workflow; viewing or navigating cannot submit or create work. No duplicate jobs or handovers. |
| Inventory and shipments | Make relevant equipment, in-transit and received-awaiting-placement destinations easier to reach. | Counts have an identified scope and use existing service meanings; groups, records and quantities are not conflated. |
| Saved work and errors | Keep unsent drafts, conflicts, connection failures and uncertain saves visible without overwhelming ordinary navigation. | Simplification never hides unsent work, converts unavailable information to a false zero, clears storage or silently changes the account/project. |
| Mobile and desktop layout | Improve hierarchy, alignment, spacing and touch navigation; show useful work earlier on a phone. | Test keyboard focus, narrow widths, large text, phone use, returning to context and protection of open forms. |
| Help and first visit | Use concise explanations and clear routes into the relevant reviewed Help article. | Help must reflect the implemented controls and distinguish hosted operation from local-vessel instructions. |

## Boundaries

These are design goals, not delivered Home features. Do not fabricate activity, alerts or metrics for a live project. Do not add a second login, change the working custom domain, or build a new private-data store for a cosmetic update.

Retain the operational terms **Task**, **standalone checklist**, **handover**, **inventory**, **manifest**, **receiving** and **placement** with their actual meanings. Home is a starting view, not another place to bypass the checks in those workspaces.

## Delivery approach

Review the actual Home source and current hosted feedback first. Implement a bounded Home update with before/after screenshots and tests for permissions, stale responses, local work and navigation. Deliver it in the cumulative Wavelink package and document what remains pending. Inventory or shipment faults reported during acceptance keep priority.


## UI13 progress — 25 September 2026

The original UI12 proposal above remains as history. UI13 implements the first browser Home pass; this does not mark every usability/acceptance item complete.

| Planned area | Implemented in UI13 | Remaining |
|---|---|---|
| Starting point | Compact Home heading, equipment shortcuts, separate Continue and Start lists; main sidebar retained. | Actual hosted feedback and further role-specific/personalised organisation. |
| Personal/project scope | Existing attention results split into Your follow-up and Accessible project work, with per-category scope and no combined total. | Broader role testing; no new personal-only Task endpoint or metric was invented. |
| Continue/start | Existing workspaces versus reviewed New checklist, New task and New work order forms. Retained new-record draft says Continue. Explicit-save paths tested. | Universal cross-workspace return history; direct new handover/log shortcuts remain in their own workspaces. |
| Equipment/shipments | Inventory shortcut by permission; administrator manifest and receiving destinations; receiving groups keep their actual meaning. | No in-transit counter on Home or new Fleet authority for project-mode users. |
| Saved work/errors | Existing local calculation/review retained; local conflict notice above navigation; unavailable overview clears old private summaries; stale reads and token changes guarded. | Real storage/network acceptance and broader interrupted-form tests. |
| Responsive layout | Desktop panels, stacked mobile navigation and initially collapsed mobile Start; five viewport widths checked. | Physical devices and complete assistive-technology/zoom/contrast acceptance. |
| Help | Dashboard article reviewed, outline/catalogue updated,75 other article bodies unchanged. | Remaining72 not-yet-wording-reviewed topics plus finer reviewed topics and native/master PDF. |

No automatic writes, new storage, permissions, domain change or new API accompany Home navigation. A narrow shared form post-save branch refreshes Home after explicit creation instead of falling into Toolbox. Normal workspaces retain their save callbacks and effects.
