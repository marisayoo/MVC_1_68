from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QListWidget, QPushButton, QHBoxLayout

class JobsView(QMainWindow):
    def __init__(self, controller, role, candidate_id=None):
        super().__init__()
        self.controller = controller
        self.role = role
        self.candidate_id = candidate_id

        self.setWindowTitle("Open Jobs")
        self.setGeometry(400, 300, 720, 440)

        cw = QWidget(self); self.setCentralWidget(cw)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Open Job Positions:"))

        self.jobs = self.controller.get_open_jobs_sorted()

        self.listw = QListWidget()
        for j in self.jobs:
            comp = self.controller.get_company_name(j["CompanyID"])
            self.listw.addItem(
                f"[{j['JobID']}] {j['Title']} | {comp} | Deadline: {j['Deadline']} | Type: {j['JobType']}"
            )
        layout.addWidget(self.listw)

        row = QHBoxLayout()
        self.btn_apply = QPushButton("Apply Selected Job")
        self.btn_apply.clicked.connect(self._apply)
        row.addWidget(self.btn_apply)

        btn_back = QPushButton("Back to Login")
        btn_back.clicked.connect(self._back)
        row.addWidget(btn_back)

        layout.addLayout(row)
        cw.setLayout(layout)

    def _apply(self):
        row = self.listw.currentRow()
        if row < 0:
            return
        job = self.jobs[row]
        self.controller.open_apply_view(job, self.candidate_id, parent=self)

    def _back(self):
        self.controller.back_to_login(current=self)
