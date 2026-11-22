"""Exercise saved project snapshots and scoped roster reads in isolated companies."""
from urllib.parse import urlencode
from tests.test_hr_ui117 import company_context, shift


def test_assignment_project_history_and_isolation(tmp_path):
    with company_context(tmp_path / "alpha") as first, company_context(tmp_path / "beta") as other:
        def rows(company, who, **filters):
            query = urlencode(dict(start_on="2026-10-15", end_on="2026-10-15", **filters))
            return company.get("workspace?" + query, key=who)["roster"]

        alice, bob = first.uid("alice"), first.uid("bob")
        project = first.action("save_timesheet_project", dict(version=0,name="PTB001",active=True,approver_ids=[]), key="admin")["project"]
        for user in [alice, bob]:
            first.action("save_shift", shift(user, project="PTB001"), key="hr")
        first.action("save_shift", shift(alice, project=""), key="hr")
        first.action("save_shift", shift(bob), key="hr")
        team = rows(first, "hr", project="ptb001")
        assert {p["id"] for p in team} == {alice, bob}
        assert all(r["project"] == "PTB001" for p in team for r in p["assignments"])
        assert {p["id"] for p in rows(first, "alice", project="PTB001")} == {alice}
        assert rows(other, "hr", project="PTB001") == []
        assert any(not r.get("project") for p in rows(first, "hr") for r in p["assignments"])
        assert all(r["roster_project_id"] == project["id"] for p in team for r in p["assignments"])
        change = dict(id=project["id"],version=project["version"],name="PTB002",active=True,approver_ids=[])
        renamed = first.action("save_timesheet_project", change, key="admin")["project"]
        assert {p["id"] for p in rows(first, "hr", project="PTB002")} == {alice, bob}
        first.action("save_timesheet_project", {**change,"version":renamed["version"],"active":False}, key="admin")
        assert {p["id"] for p in rows(first, "hr", project="PTB001")} == {alice, bob}
        assert rows(first, "hr", project="PTB002") == []
        assert rows(other, "admin", project="PTB002") == []
