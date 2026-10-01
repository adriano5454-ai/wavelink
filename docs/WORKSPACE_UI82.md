# Wavelink UI82 — Authorised Search and Personal Action Centre Batch

**Date:** 1 October 2026  
**Core:** 1.34.19  
**Exact parent:** UI81 Workflow Foundation Batch  
**Runtime variant:** `workspace-ui82-authorised-search-action-centre-batch-2026-10-01`

## Purpose

UI82 combines two connected daily-work improvements: a permission-aware global search and a personal action centre. Both surfaces derive titles and deep links from the existing source services under the current named account. They are not a second operational database, social feed or generic activity-log search.

## Authorised global search

The permanent top bar now provides search on desktop and phone. Ctrl/Cmd+K opens the same dialog. A query requires at least two characters and may be filtered by category.

Initial sources are:

- member profiles;
- Tasks;
- Maintenance;
- Checklists;
- Handovers;
- Toolbox Talks;
- Inventory/equipment;
- Certificates;
- Logs;
- Fault Reports;
- HSE/QSHE;
- Fleet sites;
- Manifests.

Each source is queried through its existing service and current permission/scope rules. Results are ranked only after authorised rows have been collected. Restricted titles, people and snippets are not added to the response, and hidden matches are not included in a total or suggestion. A source that cannot be checked is identified as unavailable rather than inferred.

Search is deliberately not email-first identity routing, public directory search or a cross-company index. Login IDs and private email addresses are not returned in profile results.

## Personal action centre

The action centre combines current items already available through Personal Home and Attention services, including:

- assigned/current Tasks and other work;
- review or acknowledgement actions;
- due and overdue Maintenance;
- Certificate expiry attention;
- final receiving placement;
- Handover acknowledgements and saved drafts.

The list is personal and current. Source access is re-derived whenever it is opened or refreshed. Losing access removes the action and its title even when a read/dismiss receipt still exists.

The permanent badge reports unread open actions across all enabled categories. It does not change when the user selects the Dismissed tab or narrows the dialog to one category.

## Receipts and preferences

UI82 stores only account-scoped metadata:

- read/unread receipt;
- dismissed/restored receipt;
- enabled categories;
- optional quiet hours with an IANA time zone;
- idempotency receipts for mark/preference writes.

The metadata tables contain event keys and timestamps, not copied source titles, descriptions, signatures, evidence or participant lists. Marking an item read or dismissed does not approve, complete, publish, acknowledge or alter the source record.

Quiet hours are a preference/status foundation. UI82 does not send push, browser, email or mobile notifications.

## Stable updates and refresh ownership

Search uses a 250 ms input debounce and ignores stale responses. The action centre has no independent polling interval. It refreshes from existing lifecycle signals: sign-in/session sync, deliberate open/refresh, relevant successful writes, visibility return and existing WebSocket record-change hints.

When new action data is detected while the dialog is open, Wavelink shows **New updates are available · Show**. It does not force-scroll, replace the list under the reader or flash a full-width banner.

The implementation adds no MutationObserver, shell DOM re-parenting or post-render GUI decorator.

## Additive schema

UI82 creates four tables in the existing project database when absent:

- `action_center_meta`;
- `action_center_preferences`;
- `action_center_receipts`;
- `action_center_operations`.

Creation is transactional, additive and idempotent. Existing users, operational records, points, roles, invitations, signatures, files and source evidence are not rewritten. A partial table set fails closed rather than silently recreating mixed storage.

Preserve a complete backup before deployment. A UI81 rollback can ignore the additive tables, but it will not present or update UI82 receipts/preferences; pair production rollback with the reviewed application/database recovery procedure.

## Runtime delta

- Modified runtime files: **6**
- New runtime/test files: **7**
- Removed runtime files: **0**
- Embedded UI82 records: **13**
- Parent manifest: **2,022** files
- Target manifest: **2,029** files
- Parent overlay SHA-256: `30bc56415df22bc83576b36924a078cda0305bf3de769dd5dc47ff914f2f9aa1`
- Target overlay SHA-256: `f06816a54a06bb380b5f33629ff51fa47428284ddcc906df5f1fdc2f487d2ebc`
- Target release-manifest SHA-256: `179355e687271a21e052b91ab763b43d6d4232ce8eae8ab187807d83d35f514d`

## Authority boundary

UI82 adds authenticated operational read/write APIs for search, current-action retrieval and action-centre metadata. It adds no permission key, security-role mapping, invitation authority, recognition rule, point adapter, source-completion adapter or environment variable.

A result link is not authority. The destination service rechecks access. A receipt is not evidence of operational acknowledgement or completion. The source record remains authoritative.

The Mail Startup M01 launcher remains byte-identical:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

## Local verification scope

The dedicated tests cover authentication/project binding, query/category validation, private Task non-disclosure, profile privacy, personal action isolation, idempotent receipts, access loss, preference versioning/time-zone validation, metadata text minimisation and a global unread count independent of dialog view.

Browser checks use fictional local records at 1440, 390 and 320 CSS pixels. They cover search, grouped results, action views, preferences, New updates behaviour, keyboard opening and document overflow. They are not live Render, real-company, inbox, physical-device or independent security acceptance.

## Connected demo acceptance

1. Sign in with two fictional accounts having different departments/assignments.
2. Search for a private Task title with the assignee and confirm it appears.
3. Repeat with the unrelated account and confirm no title, participant, suggestion or hidden-match count appears.
4. Search each enabled module and open representative results; confirm destination access is rechecked.
5. Open My actions and verify current assignments/reviews/acknowledgements against the source records.
6. Mark one item read, dismiss it, restore it and repeat a lost-response retry.
7. Remove the fictional account's source access and confirm the title disappears immediately despite its receipt.
8. Change category and Dismissed views and confirm the permanent unread badge still reflects all unread open actions.
9. Save quiet hours using the deployment's real IANA time zone and confirm no operational action is hidden or changed.
10. Leave the dialog open, change a source record in another account and confirm a small New updates control appears without list replacement.
11. Repeat at desktop, 390-pixel and 320-pixel widths.
12. Confirm no company reset, browser-storage clear or repeated setup is required.

## Next batched direction

UI83 should group email-first identity entry, exact mailbox verification, two-step verification, session/device management, recovery safeguards and live SMTP/DNS inbox acceptance. That work is security-sensitive and remains separate from UI82 search/action surfaces.
