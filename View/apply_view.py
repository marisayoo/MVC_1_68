from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIntValidator

class ApplyView(QDialog):
    def __init__(self, controller, job):
        super().__init__()
        self.controller = controller
        self.job = job

        self.setWindowTitle(f"Apply: {job['Title']} ({job['JobType']})")
        self.setGeometry(520, 360, 560, 340)

        display = self.controller.get_now_text()

        main = QVBoxLayout()
        main.addWidget(QLabel(f"JobID: {job['JobID']} | Company: {self.controller.get_company_name(job['CompanyID'])}"))
        main.addWidget(QLabel(f"Deadline: {job['Deadline']} | Status: {job['Status']}"))
        main.addWidget(QLabel(f"Application time (auto): {display}"))

        main.addWidget(QLabel("Candidate ID (8 digits, not start with 0):"))
        self.input_id = QLineEdit()
        self.input_id.setValidator(QIntValidator(1, 99999999, self))
        self.input_id.setMaxLength(8)
        main.addWidget(self.input_id)

        main.addWidget(QLabel("First name:"))
        self.input_firstname = QLineEdit(); main.addWidget(self.input_firstname)

        main.addWidget(QLabel("Last name:"))
        self.input_lastname = QLineEdit(); main.addWidget(self.input_lastname)

        main.addWidget(QLabel("Email:"))
        self.input_email = QLineEdit(); main.addWidget(self.input_email)

        row = QHBoxLayout()
        row.addWidget(QLabel("Status:"))
        self.input_status = QComboBox(); self.input_status.addItems(["studying", "graduated"])
        row.addWidget(self.input_status)
        main.addLayout(row)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Submit"); btn_ok.clicked.connect(self._submit)
        btn_cancel = QPushButton("Cancel"); btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_ok); btn_row.addWidget(btn_cancel)
        main.addLayout(btn_row)

        self.msg = QLabel(""); self.msg.setStyleSheet("color:red;")
        main.addWidget(self.msg)

        self.setLayout(main)

    def _submit(self):
        form = {
            "CandidateID": self.input_id.text().strip(),
            "FirstName":   self.input_firstname.text().strip(),
            "LastName":    self.input_lastname.text().strip(),
            "Email":       self.input_email.text().strip(),
            "Status":      self.input_status.currentText().strip().lower(),
        }
        ok, err = self.controller.apply_job_from_form(self.job, form)
        if not ok:
            self.msg.setText(err)
        else:
            self.accept()  # ปิด dialog -> กลับ JobsView
