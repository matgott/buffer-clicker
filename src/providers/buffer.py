import win32api
from time import sleep
from .mouse import Mouse
from .process import Process


class Buffer:
    def __init__(self, args):
        self.handler = args.handler
        rect = Process.get_handler_rect(self.handler)
        self.party_container = {
            "right": rect["right"] - 80,
            "top": rect["top"] + 35,
            "top_step_offset": 38
        }
        self.party_members = args.party_members
        self.skills_container = {
            "right": int(rect["right"] / 3) + 35,
            "bottom": rect["bottom"] - 55,
            "left_step_offset": 55
        }
        self.mouse = Mouse(self.handler)
        self.buffs = args.party_buffs
        self.heal_buff = args.heal_buff
        self.must_heal = args.must_heal

    def __get_skill_lparam(self, skill):
        left_step = self.skills_container["right"] + (
            (skill-1) * self.skills_container["left_step_offset"])
        lParam = win32api.MAKELONG(
            left_step, self.skills_container["bottom"])

        return lParam

    def __get_party_member_lparam(self, member):
        top_step = self.party_container["top"] + (
            member * self.party_container["top_step_offset"])
        lParam = win32api.MAKELONG(
            self.party_container["right"], top_step)

        return lParam

    def __trigger_buff(self, skill, memberLParam):
        # Select the skill
        self.mouse.left_click(self.__get_skill_lparam(skill))
        # sleep(0.2)

        # Click on the member
        self.mouse.right_click(memberLParam)

        # sleep(0.2)

    def do(self):
        for x in range(0, self.party_members):
            party_member_lparam = self.__get_party_member_lparam(x)

            # Trigger bufs (skills 1 to 3)
            for b in self.buffs:
                self.__trigger_buff(b, party_member_lparam)

        # Trigger the healing buff a few times before start again
        if self.must_heal:
            for t in range(0, 4):
                for x in range(0, self.party_members):
                    party_member_lparam = self.__get_party_member_lparam(
                        x)
                    self.__trigger_buff(
                        self.heal_buff, party_member_lparam)

                sleep(2)
