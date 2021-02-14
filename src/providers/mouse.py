import win32con
import win32api
from time import sleep
from .process import Process


class Button():
    RIGHT = {
        "button": win32con.MK_RBUTTON,
        "actions": {
            "press": win32con.WM_RBUTTONDOWN,
            "up": win32con.WM_RBUTTONUP
        }
    }
    LEFT = {
        "button": win32con.MK_LBUTTON,
        "actions": {
            "press": win32con.WM_LBUTTONDOWN,
            "up": win32con.WM_LBUTTONUP
        }
    }
    MIDDLE = {
        "button": win32con.MK_MBUTTON,
        "actions": {
            "press": win32con.WM_MBUTTONDOWN,
            "up": win32con.WM_MBUTTONUP
        }
    }

    def __str__(self):
        return self.name + ": " + str(self.value)


class Mouse:
    def __init__(self, hwnd):
        self.handler = hwnd

    def __click(self, button, lParam):
        press_action = button["actions"]["press"]
        up_action = button["actions"]["up"]
        button = button["button"]

        Process.active_handler_window(self.handler)
        sleep(0.2)
        win32api.SendMessage(
            self.handler, win32con.WM_MOUSEMOVE, 0, lParam)
        sleep(0.1)
        win32api.SendMessage(
            self.handler, press_action, button, lParam)
        sleep(0.1)
        win32api.SendMessage(self.handler, up_action, 0, 0)

    def right_click(self, lParam):
        self.__click(Button.RIGHT, lParam)

    def left_click(self, lParam):
        self.__click(Button.LEFT, lParam)

    def middle_click(self, lParam):
        self.__click(Button.MIDDLE, lParam)

    # def clear(self):
    #   for b in Button:
    #     action = Action[button.name + "_UP"]
    #     win32api.SendMessage(self.handle, Action, 0, 0)
    #     sleep(0.2)
