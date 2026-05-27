from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

REQUIRED_FIELDS = [
    "id",
    "service_name",
    "department",
    "primary_contact_name",
    "role",
    "phone",
    "email",
    "escalation_contact",
    "support_hours",
    "coverage_type",
    "notes",
]

VALID_COVERAGE_TYPES = {"24x7", "Business Hours", "On-Call", "Extended Hours"}


@dataclass
class ContactRecord:
    id: str
    service_name: str
    department: str
    primary_contact_name: str
    role: str
    phone: str
    email: str
    escalation_contact: str
    support_hours: str
    coverage_type: str
    notes: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def validate_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        value = record.get(field, "")
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} is required")

    email = str(record.get("email", "")).strip()
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        errors.append("email must be in a valid format")

    coverage = str(record.get("coverage_type", "")).strip()
    if coverage and coverage not in VALID_COVERAGE_TYPES:
        errors.append("coverage_type is invalid")

    return len(errors) == 0, errors
