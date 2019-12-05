#/usr/bin/env python3
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
# QAction, QFileDialog, QApplication, QWidget, QPushButton)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QFont
from Splicer import splice
import sys
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timelineFile = ""
            
    def initUI(self):
        tst_label = QLabel("Timestamps")
        self.tst_box = QListWidget()
        self.tst_box.itemDoubleClicked.connect(self.tst_edit)
        self.tst_box.currentItemChanged.connect(self.seek)
        tst_ok = QPushButton("OK")
        tst_ok.clicked.connect(self.tst_import)
        tst_clear = QPushButton("Clear")
        tst_clear.clicked.connect(self.tst_clear)

        mts_label = QLabel("Matches")
        self.mts_box = QListWidget()
        mts_ok = QPushButton("OK")
        mts_ok.clicked.connect(self.tst_import)
        mts_clear = QPushButton("Clear")
        mts_clear.clicked.connect(self.mts_clear)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export)

        self.video_player = VideoPlayer()
        self.video_player.show()

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(tst_label,0,0)
        grid.addWidget(self.tst_box,1,0,1,3)
        grid.addWidget(tst_ok,3,2)
        grid.addWidget(tst_clear,3,1)

        grid.addWidget(mts_label,5,0)
        grid.addWidget(self.mts_box,6,0,1,3)
        grid.addWidget(mts_ok,7,2)
        grid.addWidget(mts_clear,7,1)

        grid.addWidget(self.video_player,0,3,10,10)
        grid.addWidget(export_btn,10,10)

        self.setLayout(grid)

    def tst_edit(self, item):
        newText, _ = QInputDialog.getText(self, "Edit Value","New Time", text=item.text()) 
        if newText is not "":
            item.setText(newText)
        else:
            item.setText(item.text())

    def tst_import(self, filename):
        self.timelineFile = filename
        confirm = QMessageBox.question(self, "Confirm", "Use this timeline?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            with open(filename, 'r') as f:
                for line in f.readlines():
                    timeA, timeB, playerA, playerB = line.split(';')
                    self.tst_box.addItem(timeA + " --> " + timeB)
                    self.mts_box.addItem(playerA + " vs " + playerB[:-1])


    def tst_clear(self):
        confirm = QMessageBox.question(self, "Clear", "Clear this input?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            self.tst_box.clear()

    def mts_clear(self):
        confirm = QMessageBox.question(self, "Clear", "Clear this input?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.Yes:
            self.mts_box.setText("") 

    def seek(self, item):
        try: 
            startTime = item.text().split(' ')[0]
            hour, minute, second = startTime.split(':')
        except Exceptiona as e:
            print(str(e))
            return None
        intSeekTime = (int(hour) * 60 * 60) + (int(minute) * 60) + int(second)
        self.video_player.setPosition(intSeekTime * 1000)


    def export(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Export Location"))
        splice(self.timelineFile, self.video_player.vodFile, directory) 
        
    

class Meta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.text_edit = Dashboard()
        self.setCentralWidget(self.text_edit)

        import_action = QMenu("Import", self)
        import_timeline = QAction("Timeline", self)
        import_action.addAction(import_timeline)
        menubar = self.menuBar()
        menu = menubar.addMenu('&File')
        menu.addMenu(import_action)

        import_timeline.triggered.connect(self.import_timeline_file)

        self.setGeometry(200,200,550,400)
        self.show()

    def import_timeline_file(self):
        timeline_name, _ = QFileDialog.getOpenFileName(self, 'Import file', '/home')
        self.text_edit.tst_import(timeline_name)

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.vodFile = ""
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
        self.vodFile = fileName
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
