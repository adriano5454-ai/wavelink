# Wavelink checkpoint — UI44 + optional Company C01 + working G01

26 September 2026. Core **1.34.19**. UI44 is the clean-company Setup & builders release. User direction remains: simpler means easier to use and discover, not fewer capabilities. Anyone with the corresponding saved permission can create/import the reusable definition; administrator role is not required for builder actions.

## Exact source

Parent is verified **UI43 + Company C01**, over the user's uploaded UI30 repository and verified UI31–43 lineage. Parent application extractor: `56a0ea34f7bd6bb4648b464edf4d6746df6df4b9dc808e163757e33acbe16243`. UI44 extractor: `e2b8b8b3b8675ed67984655946ad54c503c31e3bd555956ce6c79feaff280a25`. C01 entrypoint remains `f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2`; G01 gate remains `9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701`. UI34 signing Nginx remains `752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8`.

Fresh extraction from the final extractor contains **1,780 tracked runtime files**, **192 application Python modules** and **71 application JavaScript files**. The repository keeps C01 hosting files; the existing executable repository change for UI44 is only `deploy/extract_source.py`.

## Implemented

- New permission-scoped **Setup & builders** workspace and navigation/Home destination.
- Explicit builder permissions for checklist templates, maintenance routines, toolbox forms, logbook designs and inventory structures. Existing non-admin accounts default false; administrators retain full access; dependencies on the relevant base module remain enforced.
- Non-admin permissioned accounts can use the existing checklist/maintenance/toolbox/logbook authoring services without general Administration authority.
- Browser reusable-definition imports: `.ajcheck`, `.ajtoolbox`, `.ajlogs` definitions only and `.ajinventory`. Exact file preview/review token, size/type checks and idempotent retry receipt. No users/passwords/signatures/completed operational history imported.
- Blank inventory structure creator; existing blank checklist/maintenance/toolbox/logbook builders reused.
- Existing Import Centre now points common reusable imports to Setup & builders; advanced workbook/project/setup transfers remain deliberately separate.
- Empty-company guidance appears inside Setup & builders; People & departments is an admin shortcut, not a requirement for builder authors.
- Help/navigation/catalogue/cache references updated. Original Files retains its existing permissions and admin-only upload/organisation.

No new SQL tables, migrations, dependencies, environment settings, account roles, operational writers or persistent browser stores. C01 company isolation and first-sign-in behaviour are unchanged.

## Selected local checks

Final selected checks completed in this work: UI44 builder/API/permission tests plus updated workspace catalogue checks **23 passed**; C01 company tests **71 passed**; demo/package/G01 package selection **59 passed**; builder workspace Chromium rendering passed at **1440 px and 390 px**; all **192 app Python modules parse** and all **71 app JavaScript files pass `node --check`**. The final extractor was freshly replayed and produced the expected 1,780-file runtime.

A broader inherited browser-template/logbook suite did not complete within the bounded run; one old release invariance assertion is intentionally obsolete because UI44 changes checklist/logbook definition-authority adapters. This is not a full-suite result. No live GitHub/Render deployment, real Sulmara data access, physical phone, durable IndexedDB/SW, Windows/PowerShell, Docker build, full accessibility/security/load or accepted off-host recovery is claimed.

## Preserve / next

Existing demo: preserve G01, `DEMO_PUBLIC_ENTRY=YES`, `INITIALISE_FICTIONAL_DEMO=NO`, guest/domain/disk/backups and unsent work. Company C01: preserve COMPANY mode, company ID/name/public URL, dedicated disk and activation marker; after successful first setup keep `INITIALISE_COMPANY=NO` and remove bootstrap secrets as documented. Never copy demo credentials/data into Sulmara.

For Sulmara onboarding after UI44: create departments/accounts, grant only the builder permissions each role needs, then create/import reusable definitions through Setup & builders. Test one permissioned non-admin account before using operational data. No reset/re-import/site-data clearing. Keep grouped substantial releases; broader workbook/setup browser imports remain separate review work.
