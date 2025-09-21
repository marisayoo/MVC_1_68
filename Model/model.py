import re
from datetime import date, datetime

class BaseApplicationModel:
    email = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def validate_email(self, email: str) -> bool:
        return bool(self.email.match(email or ""))

    def validate_candidate_id(self, cid_text: str) -> bool:
        # 8 หลัก ตัวแรกไม่เป็น 0
        return cid_text.isdigit() and len(cid_text) == 8 and cid_text[0] != "0"

    def now_date(self):
        return datetime.now()

    def common_rules_ok(self, job: dict, candidate: dict, email: str):
        if not self.validate_email(email):
            return False, "Invalid email format."
        if job["Status"] != "open":
            return False, "Job is not open."
        if date.today() > job["Deadline"]:
            return False, "Deadline passed."
        return True, ""

    def can_apply(self, job: dict, candidate: dict) -> bool:
        raise NotImplementedError
