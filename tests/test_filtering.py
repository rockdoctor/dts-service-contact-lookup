from contact_lookup.filtering import filter_contacts


CONTACTS = [
    {
        "service_name": "Interface Engine Monitoring",
        "department": "Integration Services",
        "primary_contact_name": "Avery Quill",
        "role": "Analyst",
        "email": "avery@demo.internal",
        "notes": "HL7 queue checks",
        "escalation_contact": "Morgan Vale",
        "coverage_type": "24x7",
    },
    {
        "service_name": "Epic Orders Build",
        "department": "Epic Support",
        "primary_contact_name": "Quinn Marlow",
        "role": "Analyst",
        "email": "quinn@demo.internal",
        "notes": "Order panel support",
        "escalation_contact": "Reese Hollow",
        "coverage_type": "Business Hours",
    },
]


def test_filter_contacts_by_department() -> None:
    filtered = filter_contacts(CONTACTS, department="Epic Support")

    assert len(filtered) == 1
    assert filtered[0]["service_name"] == "Epic Orders Build"


def test_filter_contacts_by_coverage() -> None:
    filtered = filter_contacts(CONTACTS, coverage_type="24x7")

    assert len(filtered) == 1
    assert filtered[0]["service_name"] == "Interface Engine Monitoring"


def test_filter_contacts_by_search_query() -> None:
    filtered = filter_contacts(CONTACTS, query="hl7")

    assert len(filtered) == 1
    assert filtered[0]["department"] == "Integration Services"
