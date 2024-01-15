import time
import numpy as np
from PyQt6 import QtCore
from PyQt6 import QtGui

from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# delay = 2
# button = Button.left
#
# start_stop_key = KeyCode(char="a")
# exit_key = KeyCode(char="z")


class MouseClick(QtCore.QThread):
    ClickedInfo = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, delay=2, button=Button.left):
        QtCore.QThread.__init__(self)

        self.mouse = Controller()
        self.delay, self.button = delay, button
        self.running = False
        self.program_run = True
        self.ClickedNumber = 0

    def start_clicking(self, delay):
        self.delay = delay
        self.running = True
        print("Start Clicking")

    def stop_clicking(self):
        self.running = False
        print("Stop Clicking")

    def exit(self):
        self.stop_clicking()
        self.program_run = False

    def run(self):
        while self.program_run:
            while self.running:
                self.mouse.click(self.button)
                self.ClickedNumber = self.ClickedNumber + 1
                self.ClickedInfo.emit(self.ClickedNumber)
                time.sleep(self.delay)
            time.sleep(0.01)


# click_thread = MouseClick(delay, button)
# # click_thread.start()

# def on_press(key, click_thread):
#     if key == start_stop_key:
#         if click_thread.running:
#             click_thread.stop_clicking()
#         else:
#             click_thread.start_clicking()
#     elif key == exit_key:
#         click_thread.exit()
#         listener.stop()
#
#
# with Listener(on_press=on_press) as listener:
#     listener.join()
# #
# if __name__=='__main__':
#
#     t = auto_clicker_class()
#     t.start()

