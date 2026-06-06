from dataclasses import dataclass
from enum import Enum, auto
from src.models import Entry


class ImportStatus(Enum):
    NEW = auto()       # date not in existing data
    SAME = auto()      # date exists with identical location + km
    CONFLICT = auto()  # date exists but location or km differs


@dataclass
class ImportRow:
    entry: Entry          # data from file
    existing: Entry | None  # current data in DDKI (None for NEW)
    status: ImportStatus
    month_key: str        # MM.YYYY


def _date_to_month_key(date_str: str) -> str:
    """Convert DD.MM.YY to MM.YYYY."""
    parts = date_str.split(".")
    month = int(parts[1])
    year = 2000 + int(parts[2]) if int(parts[2]) < 100 else int(parts[2])
    return f"{month:02d}.{year}"


def _is_valid_date(date_str: str) -> bool:
    parts = date_str.split(".")
    if len(parts) != 3:
        return False
    try:
        int(parts[0]); int(parts[1]); int(parts[2])
        return True
    except ValueError:
        return False


def parse_file(path: str) -> list[Entry]:
    lower = path.lower()
    if lower.endswith(".ods"):
        return _parse_ods(path)
    if lower.endswith((".xlsx", ".xls")):
        return _parse_xlsx(path)
    raise ValueError(f"Nicht unterstütztes Dateiformat: {path}")


def _parse_ods(path: str) -> list[Entry]:
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        return []

    entries = []
    for row in sheets[0].getElementsByType(TableRow):
        cells = row.getElementsByType(TableCell)
        row_data = []
        for cell in cells:
            ps = cell.getElementsByType(P)
            row_data.append("".join(str(p) for p in ps).strip() if ps else "")

        if not row_data or not row_data[0]:
            continue
        date_str = row_data[0]
        if not _is_valid_date(date_str):
            continue

        location = row_data[1] if len(row_data) > 1 else ""
        km = row_data[2] if len(row_data) > 2 else ""

        # Skip fully empty rows (no location and zero/empty km)
        if not location and (not km or km == "0"):
            continue

        entries.append(Entry(date=date_str, location=location, km=km))

    return entries


def _parse_xlsx(path: str) -> list[Entry]:
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active

    entries = []
    for row in ws.iter_rows(values_only=True):
        if not row or not row[0]:
            continue
        date_str = str(row[0]).strip()
        if not _is_valid_date(date_str):
            continue

        location = str(row[1]).strip() if len(row) > 1 and row[1] else ""
        km = str(row[2]).strip() if len(row) > 2 and row[2] else ""

        if not location and (not km or km == "0"):
            continue

        entries.append(Entry(date=date_str, location=location, km=km))

    return entries


def analyze_import(file_entries: list[Entry], existing_data: dict) -> list[ImportRow]:
    """Compare file entries against existing DDKI data and classify each row."""
    rows = []
    for entry in file_entries:
        month_key = _date_to_month_key(entry.date)
        month_entries = existing_data.get(month_key, [])
        existing = next((e for e in month_entries if e.date == entry.date), None)

        if existing is None:
            status = ImportStatus.NEW
        elif existing.location == entry.location and existing.km == entry.km:
            status = ImportStatus.SAME
        else:
            status = ImportStatus.CONFLICT

        rows.append(ImportRow(entry=entry, existing=existing, status=status, month_key=month_key))

    return rows


def apply_import(rows: list[ImportRow], data: dict) -> dict:
    """Apply selected rows to the data dict. Overwrites conflicts."""
    for row in rows:
        month_entries = data.setdefault(row.month_key, [])
        existing = next((e for e in month_entries if e.date == row.entry.date), None)
        if existing:
            existing.location = row.entry.location
            existing.km = row.entry.km
        else:
            month_entries.append(row.entry)
    return data
