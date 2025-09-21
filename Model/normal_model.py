from .model import BaseApplicationModel

class NormalApplicationModel(BaseApplicationModel):
    def can_apply(self, job: dict, candidate: dict) -> bool:
        return candidate.get("Status") == "graduated"
