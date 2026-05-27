from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from contact_lookup.models import validate_record

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "contacts.json"
SEED_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "seed_contacts.json"


def _read_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def ensure_data_file(data_path: Path = DEFAULT_DATA_PATH) -> None:
    if data_path.exists():
        return
    seed_records = _read_json(SEED_DATA_PATH)
    _write_json(data_path, seed_records)


def load_contacts(data_path: Path = DEFAULT_DATA_PATH) -> list[dict[str, Any]]:
    ensure_data_file(data_path)
    records = _read_json(data_path)
    valid_records: list[dict[str, Any]] = []
    for record in records:
        is_valid, _ = validate_record(record)
        if is_valid:
            valid_records.append(record)
    return valid_records


def save_contacts(records: list[dict[str, Any]], data_path: Path = DEFAULT_DATA_PATH) -> None:
    _write_json(data_path, records)


def add_contact(contact: dict[str, Any], data_path: Path = DEFAULT_DATA_PATH) -> tuple[bool, list[str]]:
    records = load_contacts(data_path)
    is_valid, errors = validate_record(contact)
    if not is_valid:
        return False, errors
    if any(existing["id"] == contact["id"] for existing in records):
        return False, ["id must be unique"]
    records.append(contact)
    save_contacts(records, data_path)
    return True, []


def update_contact(contact_id: str, updated_contact: dict[str, Any], data_path: Path = DEFAULT_DATA_PATH) -> tuple[bool, list[str]]:
    records = load_contacts(data_path)
    is_valid, errors = validate_record(updated_contact)
    if not is_valid:
        return False, errors

    replaced = False
    for index, record in enumerate(records):
        if record["id"] == contact_id:
            records[index] = updated_contact
            replaced = True
            break

    if not replaced:
        return False, ["contact not found"]

    save_contacts(records, data_path)
    return True, []


def next_contact_id(records: list[dict[str, Any]]) -> str:
    max_id = 0
    for record in records:
        rid = str(record.get("id", ""))
        if rid.startswith("svc-"):
            try:
                max_id = max(max_id, int(rid.split("-")[-1]))
            except ValueError:
                continue
    return f"svc-{max_id + 1:03d}"
