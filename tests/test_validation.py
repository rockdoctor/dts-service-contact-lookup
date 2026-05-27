from contact_lookup.models import validate_record


def test_validate_record_success() -> None:
    valid_record = {
        "id": "svc-050",
        "service_name": "Demo Service",
        "department": "Integration Services",
        "primary_contact_name": "Jordan Demo",
        "role": "Engineer",
        "phone": "555-0150",
        "email": "jordan.demo@demo.internal",
        "escalation_contact": "Taylor Demo",
        "support_hours": "24x7",
        "coverage_type": "24x7",
        "notes": "Demo note",
    }

    is_valid, errors = validate_record(valid_record)

    assert is_valid
    assert errors == []


def test_validate_record_rejects_invalid_email_and_coverage() -> None:
    invalid_record = {
        "id": "svc-051",
        "service_name": "Demo Service",
        "department": "Integration Services",
        "primary_contact_name": "Jordan Demo",
        "role": "Engineer",
        "phone": "555-0151",
        "email": "not-an-email",
        "escalation_contact": "Taylor Demo",
        "support_hours": "24x7",
        "coverage_type": "Weekend",
        "notes": "Demo note",
    }

    is_valid, errors = validate_record(invalid_record)

    assert not is_valid
    assert "email must be in a valid format" in errors
    assert "coverage_type is invalid" in errors
