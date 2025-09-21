# Utils/csv.py
import csv
from datetime import datetime

def _read_csv(path: str):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        for row in r:
            cleaned = {}
            for k, v in row.items():
                # กันคีย์เพี้ยน: ตัด BOM/ช่องว่าง และลบ space ในชื่อคีย์ (Company Name -> CompanyName)
                key = (k or "").lstrip("\ufeff").strip().replace(" ", "")
                val = (v or "").strip()
                cleaned[key] = val
            rows.append(cleaned)
    return rows

def load_companies(path="companies.csv"):
    rows = _read_csv(path)
    for r in rows:
        r["CompanyID"] = int(r["CompanyID"])
        # รองรับ Name หรือ CompanyName
        r["Name"] = r.get("Name") or r.get("CompanyName") or ""
    return rows

def _parse_date(s: str):
    s = (s or "").strip()
    if not s:
        raise ValueError("Empty date")

    formats = [
        "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
        "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass

    s2 = s.replace("/", "-") # replaye / to -
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(s2, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Error")

def load_jobs(path="jobs.csv"):
    rows = _read_csv(path)
    for r in rows:
        r["JobID"] = int(r["JobID"])
        r["CompanyID"] = int(r["CompanyID"])
        r["Deadline"] = _parse_date(r["Deadline"])
        r["Status"] = r["Status"].lower()
        r["JobType"] = r["JobType"].lower()
    return rows

def load_candidate(path="candidate.csv"):
    rows = _read_csv(path)
    for r in rows:
        r["CandidateID"] = int(r["CandidateID"])
        r["Status"] = r["Status"].lower()
    return rows
