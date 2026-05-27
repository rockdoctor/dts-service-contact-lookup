# dts-service-contact-lookup

A locally runnable Streamlit MVP that simulates an internal healthcare technology operations contact lookup tool using **fictional data only**.

## Project Overview

This application provides:
- Searchable and filterable service contact directory
- Contact detail view
- Add and edit forms
- Local JSON persistence with seeded fictional records
- Basic test coverage for loading, validation, and filtering logic

## Fictional Data Notice

All names, phone numbers, emails, roles, and notes in this repository are fictional and for demonstration purposes only.

## Repository Summary

`dts-service-contact-lookup` is a Python + Streamlit demo app for local laptop use that helps internal teams quickly find service ownership and escalation contacts across core operations departments.

## Suggested Initial Commit Message

`Create Streamlit MVP for fictional internal service contact lookup`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
python -m pytest
```

## Project Structure

- `app.py` - Streamlit UI and form workflows
- `contact_lookup/data_access.py` - local JSON persistence layer
- `contact_lookup/models.py` - validation and record model constants
- `contact_lookup/filtering.py` - list filtering/search behavior
- `data/seed_contacts.json` - fictional seed dataset
- `data/contacts.json` - local runtime data store
- `tests/` - unit tests

## Suggested Future Enhancements

- Add CSV import/export
- Add role-based edit controls
- Add stronger schema validation and audit history
- Add pagination and advanced sorting
- Add optional SQLite backend for larger datasets
