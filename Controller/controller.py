from Utils.csv import load_companies, load_jobs, load_candidate
from Model.model import BaseApplicationModel
from Model.coop_model import CoopApplicationModel
from Model.normal_model import NormalApplicationModel

from View.jobs_view import JobsView
from View.apply_view import ApplyView
from View.admin_view import AdminView

class Controller:
    def __init__(self, main_window):
        self.main = main_window
        self.companies = load_companies("companies.csv")
        self.jobs = load_jobs("jobs.csv")
        self.candidate = load_candidate("candidate.csv")

    def open_jobs_as_candidate(self):
        self.main.show_jobs(JobsView, role="Candidate", candidate_id=None)

    def open_admin(self):
        self.main.show_admin(AdminView)

    def back_to_login(self, current):
        current.close()
        self.main.show()
        self.main.raise_()

    def get_company_name(self, company_id: int) -> str:
        c = next((x for x in self.companies if x["CompanyID"] == company_id), None)
        return c["Name"] if c else f"Company {company_id}"

    def get_open_jobs_sorted(self):
        opened = [j for j in self.jobs if j["Status"] == "open"]
        opened.sort(key=lambda x: (x["Title"].lower(), x["CompanyID"]))
        return opened

    def get_candidate_sorted(self):
        return sorted(self.candidate, key=lambda x: x.get("CandidateID", 0))

    def get_now_text(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def open_apply_view(self, job, candidate_id, parent):
        dlg = ApplyView(self, job)
        dlg.exec_()

    def select_model_for_job(self, job: dict):
        return CoopApplicationModel() if job["JobType"] == "coop" else NormalApplicationModel()

    def apply_job_from_form(self, job: dict, form: dict):
        base = BaseApplicationModel()

        if not base.validate_candidate_id(form.get("CandidateID", "")):
            return False, "CandidateID must be 8 digits and not start with 0."
        try:
            cid = int(form["CandidateID"])
        except Exception:
            return False, "CandidateID must be numeric."

        candidate = {
            "CandidateID": cid,
            "FirstName":   form.get("FirstName", ""),
            "LastName":    form.get("LastName", ""),
            "Email":       form.get("Email", ""),
            "Status":      form.get("Status", ""),
        }

        ok, err = base.common_rules_ok(job, candidate, candidate["Email"])
        if not ok:
            return False, err

        model = self.select_model_for_job(job)
        if not model.can_apply(job, candidate):
            return False, "Not eligible for this job type."

        existing = next((c for c in self.candidate if c["CandidateID"] == cid), None)
        if existing:
            existing.update(candidate)
        else:
            self.candidate.append(candidate)

        applied_at = model.now_date()
        print(f"[APPLIED] cid={cid} job={job['JobID']} at {applied_at} email={candidate['Email']}")
        return True, ""
