from pathlib import Path

from contact_lookup.data_access import add_contact, load_contacts


def test_load_contacts_from_seed_when_data_missing(tmp_path: Path) -> None:
    data_file = tmp_path / "contacts.json"
    contacts = load_contacts(data_file)

    assert data_file.exists()
    assert len(contacts) >= 12


def test_add_contact_persists_record(tmp_path: Path) -> None:
    data_file = tmp_path / "contacts.json"
    contacts = load_contacts(data_file)

    new_contact = {
        "id": "svc-999",
        "service_name": "Sandbox Service",
        "department": "Help Desk",
        "primary_contact_name": "Demo Person",
        "role": "Demo Role",
        "phone": "555-0999",
        "email": "demo.person@demo.internal",
        "escalation_contact": "Escalation Demo",
        "support_hours": "09:00-17:00",
        "coverage_type": "Business Hours",
        "notes": "Temporary test contact.",
    }

    ok, errors = add_contact(new_contact, data_file)

    assert ok
    assert not errors
    updated_contacts = load_contacts(data_file)
    assert len(updated_contacts) == len(contacts) + 1
