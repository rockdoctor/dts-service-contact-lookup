from __future__ import annotations

from typing import Any

SEARCH_FIELDS = (
    "service_name",
    "department",
    "primary_contact_name",
    "role",
    "email",
    "notes",
    "escalation_contact",
)


def filter_contacts(
    contacts: list[dict[str, Any]],
    department: str = "All",
    coverage_type: str = "All",
    query: str = "",
) -> list[dict[str, Any]]:
    normalized_query = query.strip().lower()

    def matches(record: dict[str, Any]) -> bool:
        if department != "All" and record.get("department") != department:
            return False
        if coverage_type != "All" and record.get("coverage_type") != coverage_type:
            return False
        if not normalized_query:
            return True
        return any(normalized_query in str(record.get(field, "")).lower() for field in SEARCH_FIELDS)

    return [record for record in contacts if matches(record)]
