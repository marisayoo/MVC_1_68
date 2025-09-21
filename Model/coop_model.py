from .model import BaseApplicationModel

class CoopApplicationModel(BaseApplicationModel):
    def can_apply(self, job: dict, candidate: dict) -> bool:
        return candidate.get("Status") == "studying"
