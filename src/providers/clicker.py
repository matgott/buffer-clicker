import win32api
from time import sleep
from .process import Process
from .mouse import Mouse


class Clicker:
    def __init__(self, handler, args):
        rect = Process.get_handler_rect(handler)
        self.handler = handler

        self.skills_container = {
            "right": int(rect["right"] / 3) + 35,
            "bottom": rect["bottom"] - 55,
            "left_step_offset": 55
        }

        self.mouse = Mouse(self.handler)
        self.click_functions = {
            "right": self.mouse.right_click,
            "left": self.mouse.left_click,
            "middle": self.mouse.middle_click
        }

        self.click_func = self.click_functions[args.click] or self.click_functions["right"]
        self.click_delay = args.click_delay
        self.default_skill = args.click_skill_default

        middle_left = int((rect["right"] - rect["left"]) / 2)
        middle_top = int((rect["bottom"] - rect["top"]) / 2) - 80
        self.lParam = win32api.MAKELONG(middle_left, middle_top)

    def __get_skill_lparam(self, skill):
        left_step = self.skills_container["right"] + (
            (skill-1) * self.skills_container["left_step_offset"])
        lParam = win32api.MAKELONG(
            left_step, self.skills_container["bottom"])

        return lParam

    def select_skill(self, skill):
        # Select the skill
        self.mouse.left_click(self.__get_skill_lparam(skill))

    def do(self):
        self.click_func(self.lParam)
        sleep(self.click_delay)
