from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout

class AdminView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Admin - Candidates")
        self.setGeometry(420, 320, 780, 480)

        cw = QWidget(self); self.setCentralWidget(cw)
        root = QVBoxLayout()

        root.addWidget(QLabel("Candidates:"))
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["CandidateID", "FirstName", "LastName", "Email", "Status"])
        root.addWidget(self.table)

        row = QHBoxLayout()
        btn_refresh = QPushButton("Refresh"); btn_refresh.clicked.connect(self._load)
        btn_back = QPushButton("Back to Login"); btn_back.clicked.connect(self._back)
        row.addStretch(1); row.addWidget(btn_refresh); row.addWidget(btn_back)
        root.addLayout(row)

        cw.setLayout(root)
        self._load()

    def _load(self):
        data = self.controller.get_candidate_sorted()
        self.table.setRowCount(len(data))
        for i, c in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(c.get("CandidateID", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(c.get("FirstName", "")))
            self.table.setItem(i, 2, QTableWidgetItem(c.get("LastName", "")))
            self.table.setItem(i, 3, QTableWidgetItem(c.get("Email", "")))
            self.table.setItem(i, 4, QTableWidgetItem(c.get("Status", "")))
        self.table.resizeColumnsToContents()

    def _back(self):
        self.controller.back_to_login(current=self)
