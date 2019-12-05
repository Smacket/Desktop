#!/usr/bin/env python3
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    # QAction, QFileDialog, QApplication, QWidget, QPushButton)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QFont
import sys

class PB_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(350,200,350,150)
        self.setWindowTitle("Progress")
        self.bar = QProgressBar(self)
        self.bar.setMaximum(100)
        bar_label = QLabel("In Progress...")
        bar_grid = QGridLayout()
        bar_grid.setSpacing(10)
        bar_grid.addWidget(bar_label,0,5)
        bar_grid.addWidget(self.bar,1,5,5,10)
        self.setLayout(bar_grid)
        self.show()

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

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export)

        video_player = VideoPlayer()
        video_player.show()

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
        grid.addWidget(export_btn,10,10)

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
    
    def export(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Export Location"))
        print(directory)
        self.pb = PB_Window() #Comment this out if you don't want to deal with a progress bar.
        #Do the exporting
        self.pb.bar.setValue(100)
        self.pb.hide()
    

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

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        btnSize = QSize(16,16)
        videoWidget = QVideoWidget()

        openButton = QPushButton("Open Video")   
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.setIconSize(btnSize)
        openButton.setFont(QFont("Noto Sans", 8))
        openButton.clicked.connect(self.open)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "", "Video Files (*.mp4, *.m4v)")
        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())


        
app = QApplication(sys.argv)
window = Meta()
sys.exit(app.exec_())
