# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_final2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

class ExtendedQGroupBox(QtWidgets.QGroupBox):
    currentQtFrame = 'default.jpg'
    camera_id = None
    camera_ip = ''
    camera_tag = None
    humans = 0
    unsafeHumans = 0
    safeHumans = 0
    clicked = QtCore.pyqtSignal()
    
    def __init__(self, camera_id, camera_ip):
        super().__init__()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(200, 200))
        self.setMaximumSize(QtCore.QSize(200, 200))
        self.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.setFlat(False)
        self.setCheckable(True)
        self.setChecked(False)
        self.setObjectName("cameraBox")
        self.cameraBoxLayout = QtWidgets.QVBoxLayout(self)
        self.cameraBoxLayout.setContentsMargins(1, 1, 1, 1)
        self.cameraBoxLayout.setSpacing(0)
        self.cameraBoxLayout.setObjectName("cameraBoxLayout")
        self.camera = QtWidgets.QLabel(self)
        self.camera.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera.sizePolicy().hasHeightForWidth())
        self.camera.setSizePolicy(sizePolicy)
        self.camera.setMinimumSize(QtCore.QSize(0, 140))
        self.camera.setMaximumSize(QtCore.QSize(16777215, 140))
        self.camera.setFrameShape(QtWidgets.QFrame.Box)
        self.camera.setLineWidth(1)
        self.camera.setText("")
        self.camera.setPixmap(QtGui.QPixmap(self.currentQtFrame))
        self.camera.setScaledContents(True)
        self.camera.setObjectName("camera")
        self.cameraBoxLayout.addWidget(self.camera)
        self.cameraBoxTag = QtWidgets.QLabel(self)
        self.cameraBoxTag.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraBoxTag.sizePolicy().hasHeightForWidth())
        self.cameraBoxTag.setSizePolicy(sizePolicy)
        self.cameraBoxTag.setMinimumSize(QtCore.QSize(0, 40))
        self.cameraBoxTag.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cameraBoxTag.setFont(font)
        self.cameraBoxTag.setFrameShape(QtWidgets.QFrame.Box)
        self.cameraBoxTag.setLineWidth(1)
        self.cameraBoxTag.setAlignment(QtCore.Qt.AlignCenter)
        self.cameraBoxTag.setText("Tag")
        self.cameraBoxTag.setObjectName("cameraBoxTag")
        self.cameraBoxLayout.addWidget(self.cameraBoxTag)

        self.camera_id = camera_id
        self.camera_ip = camera_ip
        self.camera_tag = f"Camera {self.camera_id}"

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
    #Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1450, 893)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setUnderline(False)
        font.setKerning(True)
        MainWindow.setFont(font)
    #Central Widget (Widget Area of Main Window)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(50, 5, 50, 5)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
    #Application Title
        self.applicationTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applicationTitle.sizePolicy().hasHeightForWidth())
        self.applicationTitle.setSizePolicy(sizePolicy)
        self.applicationTitle.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        self.applicationTitle.setFont(font)
        self.applicationTitle.setTextFormat(QtCore.Qt.AutoText)
        self.applicationTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.applicationTitle.setObjectName("applicationTitle")
        self.verticalLayout.addWidget(self.applicationTitle)
    #Application Layout
        self.applicationLayout = QtWidgets.QHBoxLayout()
        self.applicationLayout.setObjectName("applicationLayout")
    #Main Display Frame'
        self.selectedIndex = 0
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
    #Main of Main Display Frame
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
    #Main Display
        self.mainDisplay = QtWidgets.QLabel(self.frame)
        self.mainDisplay.setMinimumSize(QtCore.QSize(480, 360))
        self.mainDisplay.setFrameShape(QtWidgets.QFrame.Box)
        self.mainDisplay.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainDisplay.setLineWidth(3)
        self.mainDisplay.setMidLineWidth(5)
        self.mainDisplay.setText("")
        self.mainDisplay.setPixmap(QtGui.QPixmap("default.jpg"))
        self.mainDisplay.setScaledContents(True)
        self.mainDisplay.setObjectName("mainDisplay")
        self.verticalLayout_2.addWidget(self.mainDisplay)
    #Description Frame
        self.description = QtWidgets.QFrame(self.frame)
        self.description.setMinimumSize(QtCore.QSize(0, 250))
        self.description.setMaximumSize(QtCore.QSize(16777215, 250))
        self.description.setFrameShape(QtWidgets.QFrame.Box)
        self.description.setFrameShadow(QtWidgets.QFrame.Raised)
        self.description.setLineWidth(3)
        self.description.setMidLineWidth(0)
        self.description.setObjectName("description")
    #Grid Layout of Description Frame
        self.gridLayout = QtWidgets.QGridLayout(self.description)
        self.gridLayout.setObjectName("gridLayout")
    #Colors
        self.blue = 255
        self.green = 186
        self.red = 254
    #Number of Humans Value (humanValue)
        self.humanValue = QtWidgets.QLabel(self.description)
        #Set color
        palette = self.setWidgetTextColor(self.blue)
        self.humanValue.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.humanValue.setFont(font)
        self.humanValue.setAlignment(QtCore.Qt.AlignCenter)
        self.humanValue.setObjectName("humanValue")
        self.gridLayout.addWidget(self.humanValue, 3, 3, 1, 1)
    #Camera IP Value (ipValue)
        self.ipValue = QtWidgets.QLineEdit(self.description)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.ipValue.setFont(font)
        self.ipValue.setFrame(True)
        self.ipValue.setReadOnly(True)
        self.ipValue.setClearButtonEnabled(False)
        self.ipValue.setObjectName("ipValue")
        self.gridLayout.addWidget(self.ipValue, 1, 1, 1, 3)
    #Status Value (statusValue)
        self.statusValue = QtWidgets.QLabel(self.description)
        palette = self.setWidgetTextColor(self.green)
        self.statusValue.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.statusValue.setFont(font)
        self.statusValue.setAlignment(QtCore.Qt.AlignCenter)
        self.statusValue.setObjectName("statusValue")
        self.gridLayout.addWidget(self.statusValue, 3, 1, 1, 1)
    #Safe Human Value (safeHumanValue)
        self.safeHumanValue = QtWidgets.QLabel(self.description)
        palette = self.setWidgetTextColor(self.green)
        self.safeHumanValue.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.safeHumanValue.setFont(font)
        self.safeHumanValue.setAlignment(QtCore.Qt.AlignCenter)
        self.safeHumanValue.setObjectName("safeHumanValue")
        self.gridLayout.addWidget(self.safeHumanValue, 4, 1, 1, 1)
    #Status Label
        self.statusLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 3, 0, 1, 1)
    #Horizontal Line
        self.descriptionSeparator = QtWidgets.QFrame(self.description)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionSeparator.sizePolicy().hasHeightForWidth())
        self.descriptionSeparator.setSizePolicy(sizePolicy)
        self.descriptionSeparator.setFrameShadow(QtWidgets.QFrame.Raised)
        self.descriptionSeparator.setLineWidth(5)
        self.descriptionSeparator.setFrameShape(QtWidgets.QFrame.HLine)
        self.descriptionSeparator.setObjectName("descriptionSeparator")
        self.gridLayout.addWidget(self.descriptionSeparator, 2, 0, 1, 4)
    #Camera ID Label
        self.idLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.idLabel.setFont(font)
        self.idLabel.setObjectName("idLabel")
        self.gridLayout.addWidget(self.idLabel, 0, 0, 1, 1)
    #Unsafe Human Value (unsafeHumanValue)
        self.unsafeHumanValue = QtWidgets.QLabel(self.description)
        palette = self.setWidgetTextColor(self.red)
        self.unsafeHumanValue.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.unsafeHumanValue.setFont(font)
        self.unsafeHumanValue.setAlignment(QtCore.Qt.AlignCenter)
        self.unsafeHumanValue.setObjectName("unsafeHumanValue")
        self.gridLayout.addWidget(self.unsafeHumanValue, 4, 3, 1, 1)
    #Camera Tag Label
        self.tagLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tagLabel.setFont(font)
        self.tagLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tagLabel.setObjectName("tagLabel")
        self.gridLayout.addWidget(self.tagLabel, 0, 2, 1, 1)
    #Camera IP Label
        self.ipLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.ipLabel.setFont(font)
        self.ipLabel.setObjectName("ipLabel")
        self.gridLayout.addWidget(self.ipLabel, 1, 0, 1, 1)
    #Camera ID Value (idValue)
        self.idValue = QtWidgets.QLineEdit(self.description)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.idValue.setFont(font)
        self.idValue.setFrame(True)
        self.idValue.setReadOnly(True)
        self.idValue.setClearButtonEnabled(False)
        self.idValue.setObjectName("idValue")
        self.gridLayout.addWidget(self.idValue, 0, 1, 1, 1)
        self.humanLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.humanLabel.setFont(font)
        self.humanLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.humanLabel.setObjectName("humanLabel")
        self.gridLayout.addWidget(self.humanLabel, 3, 2, 1, 1)
    #Activity Label
        self.activityLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.activityLabel.setFont(font)
        self.activityLabel.setObjectName("activityLabel")
        self.gridLayout.addWidget(self.activityLabel, 5, 0, 1, 1)
    #Activty Value (activityValue)
        self.activityValue = QtWidgets.QLabel(self.description)
        palette = self.setWidgetTextColor(self.blue)
        self.activityValue.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activityValue.setFont(font)
        self.activityValue.setObjectName("activityValue")
        self.gridLayout.addWidget(self.activityValue, 5, 1, 1, 3)
    #tagValue
        self.tagValue = QtWidgets.QLineEdit(self.description)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.tagValue.setFont(font)
        self.tagValue.setFrame(True)
        self.tagValue.setReadOnly(True)
        self.tagValue.setClearButtonEnabled(False)
        self.tagValue.setObjectName("tagValue")
        self.gridLayout.addWidget(self.tagValue, 0, 3, 1, 1)
    #Safe Human Label
        self.safeHumanLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.safeHumanLabel.setFont(font)
        self.safeHumanLabel.setObjectName("safeHumanLabel")
        self.gridLayout.addWidget(self.safeHumanLabel, 4, 0, 1, 1)
    #Unsafe Human Label
        self.unsafeHumanLabel = QtWidgets.QLabel(self.description)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.unsafeHumanLabel.setFont(font)
        self.unsafeHumanLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.unsafeHumanLabel.setObjectName("unsafeHumanLabel")
        self.gridLayout.addWidget(self.unsafeHumanLabel, 4, 2, 1, 1)
    
        self.verticalLayout_2.addWidget(self.description)
        self.applicationLayout.addWidget(self.frame)

    #Scroll Area
        self.cameraScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraScrollArea.sizePolicy().hasHeightForWidth())
        self.cameraScrollArea.setSizePolicy(sizePolicy)
        self.cameraScrollArea.setMinimumSize(QtCore.QSize(500, 0))
        self.cameraScrollArea.setMaximumSize(QtCore.QSize(500, 16777215))
        self.cameraScrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.cameraScrollArea.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraScrollArea.setLineWidth(3)
        self.cameraScrollArea.setWidgetResizable(True)
        self.cameraScrollArea.setObjectName("cameraScrollArea")
    #Scroll Widgets Area
        self.CameraScrollWidgets = QtWidgets.QWidget()
        self.CameraScrollWidgets.setGeometry(QtCore.QRect(0, 0, 488, 748))
        self.CameraScrollWidgets.setObjectName("CameraScrollWidgets")
    #Form Layout of Scroll Widgets Area (formLayout)
        self.formLayout = QtWidgets.QFormLayout(self.CameraScrollWidgets)
        self.formLayout.setContentsMargins(15, 15, 15, 15)
        self.formLayout.setSpacing(15)
        self.formLayout.setObjectName("formLayout")
    
        self.cameraScrollArea.setWidget(self.CameraScrollWidgets)
        self.applicationLayout.addWidget(self.cameraScrollArea)
        self.verticalLayout.addLayout(self.applicationLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1450, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Camera = QtWidgets.QAction(MainWindow)
        self.actionAdd_Camera.setObjectName("actionAdd_Camera")
        self.actionEdit_Camera = QtWidgets.QAction(MainWindow)
        self.actionEdit_Camera.setObjectName("actionEdit_Camera")
        self.actionRestart = QtWidgets.QAction(MainWindow)
        self.actionRestart.setObjectName("actionRestart")
        self.actionRemove_Camera = QtWidgets.QAction(MainWindow)
        self.actionRemove_Camera.setObjectName("actionRemove_Camera")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionRestart)
        self.menuFile.addAction(self.actionAdd_Camera)
        self.menuFile.addAction(self.actionEdit_Camera)
        self.menuFile.addAction(self.actionRemove_Camera)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.applicationTitle.setText(_translate("MainWindow", "APPLICATION NAME"))
        self.humanValue.setText(_translate("MainWindow", "0"))
        self.statusValue.setText(_translate("MainWindow", "SAFE"))
        self.safeHumanValue.setText(_translate("MainWindow", "0"))
        self.statusLabel.setText(_translate("MainWindow", "STATUS:"))
        self.idLabel.setText(_translate("MainWindow", "CAMERA ID:"))
        self.unsafeHumanValue.setText(_translate("MainWindow", "0"))
        self.tagLabel.setText(_translate("MainWindow", "CAMERA TAG:"))
        self.ipLabel.setText(_translate("MainWindow", "CAMERA IP:"))
        self.humanLabel.setText(_translate("MainWindow", "NUMBER OF HUMANS:"))
        self.activityLabel.setText(_translate("MainWindow", "ACTIVITY:"))
        self.activityValue.setText(_translate("MainWindow", "\tSafe Conditions for 3 hours"))
        self.safeHumanLabel.setText(_translate("MainWindow", "NO. OF SAFE HUMANS:"))
        self.unsafeHumanLabel.setText(_translate("MainWindow", "NO. OF UNSAFE HUMANS:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAdd_Camera.setText(_translate("MainWindow", "New Camera"))
        self.actionEdit_Camera.setText(_translate("MainWindow", "Edit Camera"))
        self.actionRestart.setText(_translate("MainWindow", "Restart"))
        self.actionRemove_Camera.setText(_translate("MainWindow", "Remove Camera"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def setWidgetTextColor(self, color):
        palette = QtGui.QPalette()
        colorValue = self.getColorValue(color)
        brush = QtGui.QBrush(colorValue)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(colorValue)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        return palette
    
    def getColorValue(self, color):
        if color == self.blue:
            colorValue = QtGui.QColor(0, 0, color)
        elif color == self.green:
            colorValue = QtGui.QColor(0, color, 0)
        elif color == self.red:
            colorValue =  QtGui.QColor(color, 0, 0)
        return colorValue

    def setDescription(self, index):
        widget = self.getCameraWidget(index)
        self.idValue.setText(str(widget.camera_id))
        self.ipValue.setText(str(widget.camera_ip))
        self.tagValue.setText(str(widget.camera_tag))

    def scrollAreaClick(self, index):
        numberOfWidgets = self.formLayout.count()
        self.selectedIndex = index
        self.setDescription(index)
        for i in range(numberOfWidgets):
            widget = self.getCameraWidget(i)
            if i == index:
                widget.setChecked(True)
                widget.camera.setLineWidth(5)
                widget.cameraBoxTag.setLineWidth(5)
                widget.camera.setEnabled(True)
                widget.cameraBoxTag.setEnabled(True)   
                continue
            widget.setChecked(False)
            widget.camera.setLineWidth(1)
            widget.cameraBoxTag.setLineWidth(1)
            widget.camera.setEnabled(True)
            widget.cameraBoxTag.setEnabled(True)
            
       

    def addCamera(self, index, ip, tag = None):
        newCamera = ExtendedQGroupBox(index, ip)
        newCamera.clicked.connect(lambda: self.scrollAreaClick(index))
        
        #Deciding the location of camera feed
        rowIndex, columnIndexAttr = getCameraWidgetIndices(index)
        
        #Intialising Group Box Settings
        newCamera.setTitle(f"Camera ID: {index}")
        if tag is None:
            newCamera.cameraBoxTag.setText(f"Camera {index}")
        else:
            newCamera.cameraBoxTag.setText(tag)
        
        # Add Widget to form layout (LabelRole)
        self.formLayout.setWidget(
            rowIndex, columnIndexAttr, newCamera)
        
        if index == self.selectedIndex:
            self.setDescription(index)

    def getCameraWidget(self, index):
        i, j = getCameraWidgetIndices(index)
        widget = self.formLayout.itemAt(i, j).widget()
        return widget

    def setLabeltoFrame(self, frame, widget):
        widget.setPixmap(QtGui.QPixmap.fromImage(frame))
        #widget.camera.setScaledContents(True)


def ConvertFrametoQtFrame(frame):
    frame = QtGui.QImage(
        frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
    return frame


def getCameraWidgetIndices(index):
    rowIndex = index // 2
    columnIndex = index % 2
    columnIndexAttr = QtWidgets.QFormLayout.LabelRole if columnIndex == 0 else QtWidgets.QFormLayout.FieldRole
    return (rowIndex, columnIndexAttr)

