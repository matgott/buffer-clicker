import win32gui
import win32process
import win32con
import wmi
from time import sleep


class Process:
    __wmi = wmi.WMI()

    @staticmethod
    def get_pids(name="*"):
        mu_processes = []
        for process in Process.__wmi.Win32_Process(name=name):
            try:
                if process.Name.lower().find('main') >= 0:
                    mu_processes.append(
                        {"pid": process.ProcessId, "name": process.Name,
                         "caption": process.Caption,
                         "description": process.Description})
            except Exception as e:
                e = e

        return mu_processes

    @staticmethod
    def get_handler_by_pid(pid):
        def callback(handler, selected_handler):
            # if win32gui.IsWindowVisible(handler):
            _, result = win32process.GetWindowThreadProcessId(
                handler)

            if int(result) == int(pid):
                selected_handler.append(handler)

            return True

        selected_handler = []
        win32gui.EnumWindows(callback, selected_handler)

        return selected_handler[0] if len(selected_handler) > 0 else None

    @staticmethod
    def get_handler_rect(handler):
        rect = win32gui.GetClientRect(handler)
        return {
            "left": rect[0],
            "top": rect[1],
            "right": rect[2],
            "bottom": rect[3]
        }

    @staticmethod
    def active_handler_window(handler):
        win32gui.SendMessage(handler, win32con.WM_ACTIVATE,
                             win32con.WA_ACTIVE, 0)
        sleep(0.2)

    @staticmethod
    def set_window_focus(handler):
        win32gui.ShowWindow(handler, win32con.SW_SHOWDEFAULT)
        win32gui.SetForegroundWindow(handler)
