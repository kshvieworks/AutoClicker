"""
Auto Clicker User Interface using PyQt
"""

import AutoClicker as AC
from pynput.mouse import Button

import CustomUtility_PyQt6 as util
import sys
import numpy as np
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6 import QtCore
import cv2
from operator import itemgetter

ConfigurationVariables = {'Delay': 1.0, 'Button': Button.left}


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = MainWindow(self)
        self.setCentralWidget(self.window)
        self.setWindowTitle("Auto Clicker")
        self.show()
    # def closeEvent(self, event):
    #     print(1)
    #     asdf = 1
    #     # self.window Thread Stop


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)

    # Define Layout
        PageLayout = QtWidgets.QHBoxLayout()
        ConfigLayout = QtWidgets.QVBoxLayout()

        self.init_Layout(PageLayout, ConfigLayout)
        self.setLayout(PageLayout)
    def init_Layout(self, PageLayout, ConfigLayout):
        PageLayout.addLayout(ConfigLayout)

        self.init_ConfigureTab(ConfigLayout)

    def init_ConfigureTab(self, ConfigLayout):
        self.GeneralTab = GeneralWidget()
        ConfigLayout.addWidget(self.GeneralTab)


class GeneralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GeneralWidget, self).__init__(parent)

        self.DesignUtil = util.WidgetDesign()

        Layout = QtWidgets.QVBoxLayout()

        self.initUI(Layout)
        self.setLayout(Layout)

        self.AutoClickerThreadInit()

    def initUI(self, Layout):

        self.UI_Component()
        self.UI_Layout(Layout)
        self.EventProcess()

    def UI_Layout(self, Layout):

        Layout.addLayout(self.DesignUtil.Layout_Widget((self.Interval_Prompt, self.Interval_Entry), 'Horizontal'))
        Layout.addLayout(self.DesignUtil.Layout_Widget((self.Start_Button, self.PauseResume_Button, self.Stop_Button), 'Horizontal'))
        Layout.addLayout(self.DesignUtil.Layout_Widget((self.IntervalTime_Prompt, self.IntervalTime_Label), 'Horizontal'))
        Layout.addLayout(self.DesignUtil.Layout_Widget((self.ClickedNumber_Prompt, self.ClickedNumber_Label), 'Horizontal'))
        Layout.addLayout(self.DesignUtil.Layout_Widget((self.ElapsedTime_Prompt, self.ElapsedTime_Label), 'Horizontal'))

    def UI_Component(self):

        ButtonSize = (100, 40)
        LabelSize = (150, 30)
        EntrySize = (200, 30)

        self.Interval_Prompt = QtWidgets.QLabel("Interval Time in sec")
        self.Interval_Prompt.setFixedSize(LabelSize[0], LabelSize[1])
        self.Interval_Entry = QtWidgets.QLineEdit(placeholderText='Write Interval Time', clearButtonEnabled=True)
        self.DesignUtil.Init_Entry(self.Interval_Entry, ConfigurationVariables['Delay'], EntrySize, QtCore.Qt.AlignmentFlag.AlignRight)
        self.Interval_Entry.textChanged.connect(lambda checked=False: self.UpdateIntervalTimeLabel())

        self.Start_Button = QtWidgets.QPushButton("Start")
        self.Start_Button.setFixedSize(ButtonSize[0], ButtonSize[1])

        self.PauseResume_Button = QtWidgets.QPushButton()
        self.PauseResume_Button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPause))
        self.PauseResume_Button.setFixedSize(ButtonSize[0], ButtonSize[1])

        self.Stop_Button = QtWidgets.QPushButton("Stop")
        self.Stop_Button.setFixedSize(ButtonSize[0], ButtonSize[1])

        self.IntervalTime_Prompt = QtWidgets.QLabel("Interval Time")
        self.IntervalTime_Prompt.setFixedSize(LabelSize[0], LabelSize[1])
        self.IntervalTime_Label = QtWidgets.QLabel(f"{self.Interval_Entry.text()}")
        self.IntervalTime_Label.setFixedSize(LabelSize[0], LabelSize[1])

        self.ClickedNumber_Prompt = QtWidgets.QLabel("Clicked Number")
        self.ClickedNumber_Prompt.setFixedSize(LabelSize[0], LabelSize[1])
        self.ClickedNumber_Label = QtWidgets.QLabel()
        self.ClickedNumber_Label.setFixedSize(LabelSize[0], LabelSize[1])

        self.ElapsedTime_Prompt = QtWidgets.QLabel("Elapsed Time")
        self.ElapsedTime_Prompt.setFixedSize(LabelSize[0], LabelSize[1])
        self.ElapsedTime_Label = QtWidgets.QLabel()
        self.ElapsedTime_Label.setFixedSize(LabelSize[0], LabelSize[1])

    def EventProcess(self):
        self.Start_Button.clicked.connect(lambda checked=False: self.UpdateConfigureVariable())
        self.Start_Button.clicked.connect(lambda checked=False: self.AutoClickerThread.start_clicking(ConfigurationVariables['Delay']))
        self.Stop_Button.clicked.connect(lambda checked=False: self.AutoClickerThread.stop_clicking())
        # self.Initialization_Button.clicked.connect(lambda checked=False: self.AnalogOutput.Initialization())
        # self.PauseResume_Button.clicked.connect(lambda checked=False: self.AutoScanActiveControl(self.PauseResume_Button))

    # def AutoScanActiveControl(self, BTN):
    #     if self.AnalogOutput.ScanningLib.ThreadActive == False:
    #         BTN.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPause))
    #         self.AnalogOutput.start()
    #     else:
    #         BTN.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay))
    #         self.AnalogOutput.Pause()
    #
    def AutoClickerThreadInit(self):

        self.AutoClickerThread = AC.MouseClick(delay=ConfigurationVariables['Delay'], button=ConfigurationVariables['Button'])
        QtCore.QCoreApplication.processEvents()
        self.AutoClickerThread.ClickedInfo.connect(self.UpdateClickedNumberLabel)
        self.AutoClickerThread.start()

    def UpdateConfigureVariable(self):
        ConfigurationVariables['Delay'] = float(self.IntervalTime_Label.text())

    def UpdateClickedNumberLabel(self, AutoClickerThread):

        self.ClickedNumber_Label.setText(f"{AutoClickerThread}")

    def UpdateIntervalTimeLabel(self):
        self.IntervalTime_Label.setText(self.Interval_Entry.text())



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = App()
    app.exec()

