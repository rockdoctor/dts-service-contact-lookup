from __future__ import annotations

import streamlit as st

from contact_lookup.data_access import add_contact, load_contacts, next_contact_id, update_contact
from contact_lookup.filtering import filter_contacts
from contact_lookup.models import VALID_COVERAGE_TYPES

st.set_page_config(page_title="DTS Service Contact Lookup", page_icon="📇", layout="wide")

st.title("DTS Service Contact Lookup")
st.caption("Internal operations contact directory for demo purposes")
st.warning("Demo data notice: all contacts in this app are fictional and for demonstration only.")

contacts = load_contacts()
departments = sorted({contact["department"] for contact in contacts})
coverage_types = sorted(VALID_COVERAGE_TYPES)

st.subheader("Service Directory")
col1, col2, col3 = st.columns(3)
with col1:
    selected_department = st.selectbox("Department", ["All", *departments])
with col2:
    selected_coverage = st.selectbox("Coverage Type", ["All", *coverage_types])
with col3:
    search_text = st.text_input("Search", placeholder="Service, person, notes, escalation contact...")

filtered = filter_contacts(contacts, selected_department, selected_coverage, search_text)

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Total Contacts", len(contacts))
metric_col2.metric("Filtered Results", len(filtered))
metric_col3.metric("Departments", len(departments))

st.dataframe(
    [
        {
            "Service": c["service_name"],
            "Department": c["department"],
            "Primary Contact": c["primary_contact_name"],
            "Role": c["role"],
            "Coverage": c["coverage_type"],
            "Support Hours": c["support_hours"],
        }
        for c in filtered
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Contact Details")
if filtered:
    options = {f"{c['service_name']} ({c['department']})": c for c in filtered}
    selected_label = st.selectbox("Choose a service", list(options.keys()))
    selected_contact = options[selected_label]

    left, right = st.columns(2)
    with left:
        st.markdown(f"**Service:** {selected_contact['service_name']}")
        st.markdown(f"**Department:** {selected_contact['department']}")
        st.markdown(f"**Primary Contact:** {selected_contact['primary_contact_name']}")
        st.markdown(f"**Role:** {selected_contact['role']}")
        st.markdown(f"**Phone:** {selected_contact['phone']}")
    with right:
        st.markdown(f"**Email:** {selected_contact['email']}")
        st.markdown(f"**Escalation Contact:** {selected_contact['escalation_contact']}")
        st.markdown(f"**Support Hours:** {selected_contact['support_hours']}")
        st.markdown(f"**Coverage Type:** {selected_contact['coverage_type']}")
        st.markdown(f"**Notes:** {selected_contact['notes']}")
else:
    st.info("No contacts match the selected filters.")

st.divider()

add_tab, edit_tab = st.tabs(["Add Contact", "Edit Contact"])

with add_tab:
    st.markdown("### Add a New Contact")
    with st.form("add_contact_form", clear_on_submit=True):
        new_id = next_contact_id(contacts)
        service_name = st.text_input("Service Name")
        department = st.text_input("Department")
        primary_contact_name = st.text_input("Primary Contact Name")
        role = st.text_input("Role")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        escalation_contact = st.text_input("Escalation Contact")
        support_hours = st.text_input("Support Hours")
        coverage_type = st.selectbox("Coverage Type", coverage_types, key="new_coverage_type")
        notes = st.text_area("Notes")

        if st.form_submit_button("Add Contact"):
            success, errors = add_contact(
                {
                    "id": new_id,
                    "service_name": service_name,
                    "department": department,
                    "primary_contact_name": primary_contact_name,
                    "role": role,
                    "phone": phone,
                    "email": email,
                    "escalation_contact": escalation_contact,
                    "support_hours": support_hours,
                    "coverage_type": coverage_type,
                    "notes": notes,
                }
            )
            if success:
                st.success("Contact added successfully. Refresh filters if needed.")
            else:
                st.error("Could not add contact: " + "; ".join(errors))

with edit_tab:
    st.markdown("### Edit an Existing Contact")
    editable_contacts = {f"{c['service_name']} ({c['department']})": c for c in contacts}
    edit_label = st.selectbox("Select contact to edit", list(editable_contacts.keys()))
    selected_for_edit = editable_contacts[edit_label]

    with st.form("edit_contact_form"):
        service_name = st.text_input("Service Name", value=selected_for_edit["service_name"], key="edit_service_name")
        department = st.text_input("Department", value=selected_for_edit["department"], key="edit_department")
        primary_contact_name = st.text_input(
            "Primary Contact Name", value=selected_for_edit["primary_contact_name"], key="edit_primary_contact_name"
        )
        role = st.text_input("Role", value=selected_for_edit["role"], key="edit_role")
        phone = st.text_input("Phone", value=selected_for_edit["phone"], key="edit_phone")
        email = st.text_input("Email", value=selected_for_edit["email"], key="edit_email")
        escalation_contact = st.text_input(
            "Escalation Contact", value=selected_for_edit["escalation_contact"], key="edit_escalation_contact"
        )
        support_hours = st.text_input("Support Hours", value=selected_for_edit["support_hours"], key="edit_support_hours")
        coverage_type = st.selectbox(
            "Coverage Type",
            coverage_types,
            index=coverage_types.index(selected_for_edit["coverage_type"]),
            key="edit_coverage_type",
        )
        notes = st.text_area("Notes", value=selected_for_edit["notes"], key="edit_notes")

        if st.form_submit_button("Save Changes"):
            success, errors = update_contact(
                selected_for_edit["id"],
                {
                    "id": selected_for_edit["id"],
                    "service_name": service_name,
                    "department": department,
                    "primary_contact_name": primary_contact_name,
                    "role": role,
                    "phone": phone,
                    "email": email,
                    "escalation_contact": escalation_contact,
                    "support_hours": support_hours,
                    "coverage_type": coverage_type,
                    "notes": notes,
                },
            )
            if success:
                st.success("Contact updated successfully. Refresh filters if needed.")
            else:
                st.error("Could not update contact: " + "; ".join(errors))
