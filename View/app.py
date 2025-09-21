from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(400, 300, 420, 220)
        self.controller = None

        cw = QWidget(self); self.setCentralWidget(cw)
        root = QVBoxLayout()

        root.addWidget(QLabel("Login"))

        btn_jobs = QPushButton("Go to Jobs (Candidate)")
        btn_jobs.clicked.connect(self._go_jobs)
        root.addWidget(btn_jobs)

        btn_admin = QPushButton("Admin")
        btn_admin.clicked.connect(self._go_admin)
        root.addWidget(btn_admin)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color:red;")
        root.addWidget(self.error_label)

        cw.setLayout(root)

    def set_controller(self, controller):
        self.controller = controller

    def _go_jobs(self):
        if not self.controller:
            self.show_error("Controller not set.")
            return
        self.controller.open_jobs_as_candidate()

    def _go_admin(self):
        if not self.controller:
            self.show_error("Controller not set.")
            return
        self.controller.open_admin()

    def show_jobs(self, jobs_view_class, role, candidate_id=None):
        self.child = jobs_view_class(self.controller, role, candidate_id)
        self.child.show()
        self.hide()

    def show_admin(self, admin_view_class):
        self.child = admin_view_class(self.controller)
        self.child.show()
        self.hide()

    def show_error(self, msg):
        self.error_label.setText(msg)
