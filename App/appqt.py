#!/usr/bin/env python3
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    # QAction, QFileDialog, QApplication, QWidget, QPushButton)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

            
    def initUI(self):
        tst_label = QLabel("Timestamps")
        tst_box = QTextEdit()
        tst_ok = QPushButton("OK")
        tst_ok.clicked.connect(self.tst_import)
        tst_clear = QPushButton("Clear")
        tst_clear.clicked.connect(self.tst_clear)

        mts_label = QLabel("Matches")
        mts_box = QTextEdit()
        mts_ok = QPushButton("OK")
        mts_ok.clicked.connect(self.mts_import)
        mts_clear = QPushButton("Clear")
        mts_clear.clicked.connect(self.mts_clear)

        video_player = QLabel("Video Player")
        video_skimmer = QLabel("Video Skimmer")

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(tst_label,0,0)
        grid.addWidget(tst_box,1,0,1,3)
        grid.addWidget(tst_ok,3,2)
        grid.addWidget(tst_clear,3,1)

        grid.addWidget(mts_label,5,0)
        grid.addWidget(mts_box,6,0,1,3)
        grid.addWidget(mts_ok,7,2)
        grid.addWidget(mts_clear,7,1)

        grid.addWidget(video_player,0,3,5,5)
        grid.addWidget(video_skimmer,5,3,5,5)

        self.setLayout(grid)

    def tst_import(self):
        confirm = QMessageBox.question(self, "Confirm", "Use this timeline?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            print("Do the actual importing")

    def tst_clear(self):
        confirm = QMessageBox.question(self, "Clear", "Clear this input?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            print("Do the actual clearing")

    def mts_import(self):
        confirm = QMessageBox.question(self, "Confirm", "Use this match?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            print("Do the actual importing")

    def mts_clear(self):
        confirm = QMessageBox.question(self, "Clear", "Clear this input?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            print("Do the actual clearing")
    

class Meta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.text_edit = Dashboard()
        self.setCentralWidget(self.text_edit)

        import_action = QMenu("Import", self)
        import_timeline = QAction("Timeline", self)
        import_match = QAction("Match", self)
        import_action.addAction(import_timeline)
        import_action.addAction(import_match)
        menubar = self.menuBar()
        menu = menubar.addMenu('&File')
        menu.addMenu(import_action)

        import_timeline.triggered.connect(self.import_timeline_file)
        import_match.triggered.connect(self.import_match_file)

        self.setGeometry(200,200,550,400)
        self.show()

    def import_timeline_file(self):
        timeline_name = QFileDialog.getOpenFileName(self, 'Import file', '/home')
        print(timeline_name)

    def import_match_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Import file', '/home')
        print(file_name)

        
app = QApplication(sys.argv)
window = Meta()
sys.exit(app.exec_())
