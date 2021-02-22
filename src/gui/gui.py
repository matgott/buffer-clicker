import sys
import multiprocessing
import webbrowser
from time import time
import PySimpleGUI as sg
from .theme import Theme
from .lang import Lang
from .layout import Layout
from providers.buffer import Buffer
from providers.clicker import Clicker
from providers.process import Process
from .images import icon


def buffer_thread_function(args):
    buffer = Buffer(args)

    if args.clicker not in [None, False, '', 0]:
        clicker = Clicker(args.handler, args)

    last_time = time()
    first_cycle = True

    if args.clicker not in [
            None, False, '', 0] and args.click_skill_default != 0:
        clicker.select_skill(args.click_skill_default)

    while True:
        if args.clicker in [None, False, '', 0]:
            buffer.do()

        if args.clicker not in [None, False, '', 0]:
            clicker.do()

            if time() - last_time >= args.click_skill_delay or first_cycle:
                last_time = time()
                buffer.do()
                if args.click_skill_default != 0:
                    clicker.select_skill(args.click_skill_default)

        first_cycle = False


def clicker_thread_function(args):
    clicker = Clicker(args.handler, args)
    while True:
        clicker.do()


class Args:
    def __init__(
            self, buffer=None, clicker=None, handler=None, pid=None,
            party_members=None, party_buffs=None, heal_buff=None,
            must_heal=None, click=None, click_delay=None,
            click_skill_default=None, click_skill_delay=None):
        self.handler = handler
        self.pid = pid
        self.buffer = buffer
        self.clicker = clicker
        self.party_members = party_members
        self.party_buffs = party_buffs
        self.heal_buff = heal_buff
        self.must_heal = must_heal
        self.click = click
        self.click_delay = click_delay
        self.click_skill_default = click_skill_default
        self.click_skill_delay = click_skill_delay


class Gui:
    def __init__(self, lang="EN"):
        self.THEME = Theme
        self.LANG = getattr(Lang, lang)
        self.layout = Layout(self.LANG, self.THEME)
        self.must_show_main_window = False
        self.active_threads = []
        self.end_buffer_thread = False
        self.end_clicker_thread = False
        self.main_window = None

    def __update_lang(self, lang):
        self.LANG = getattr(Lang, lang)

    def __open_url(self, url):
        webbrowser.open(url, new=0, autoraise=True)

    def __get_pid_from_process_name(self, process):
        return process.split("(")[1].split(")")[0] or ""

    def __test_process_handler(self, event, values):
        process = values["process_combo"]
        if process not in [None, ""]:
            pid = self.__get_pid_from_process_name(process)
            handler = Process.get_handler_by_pid(pid)

            Process.set_window_focus(handler)
        else:
            self.layout.error_popup(
                self.LANG.Errors.MUST_CHOOSE_PROCESS)

    def __update_button_onoff(self, event, values):
        status = self.main_window[event].get_text()
        text, colors = (
            self.LANG.OFF,
            (self.THEME.BUTTON_ERROR_COLOR, self.THEME.
             BUTTON_ERROR_BACKGROUND)) if status == self.LANG.ON else(
            self.LANG.ON,
            (self.THEME.BUTTON_COLOR, self.THEME.BUTTON_BACKGROUND))

        self.main_window[event].Update(
            text, button_color=colors)

        frame = "frame_" + event.split("_")[2]
        self.main_window[frame].Update(visible=text == "ON")

    def __wizard_image_click(self, event, values):
        github = "https://matgott.github.io/buffer-clicker/"
        self.__open_url(github)

    def __validate_process(self, process):
        if process in [None, ""]:
            self.layout.error_popup(
                self.LANG.Errors.MUST_CHOOSE_PROCESS)
            return None

        pid = self.__get_pid_from_process_name(process)
        if process in [None, "", 0]:
            self.layout.error_popup(
                self.LANG.Errors.MUST_CHOOSE_PROCESS)
            return None

        return pid

    def __validate_handler(self, pid):
        try:
            handler = Process.get_handler_by_pid(pid)
        except Exception:
            handler = None

        if handler in [None, 0, ""]:
            self.layout.error_popup(
                self.LANG.Errors.CANNOT_GET_HANDLER)
            return None

        return handler

    def __validate_buffer_party(self, buffer, values):
        if buffer:
            party_members = values["party_members_combo"]
            combos_buffs_keys = [
                key for key in values
                if key.find("combo_buff_skill-") >= 0]

            party_buffs = list(set([values[key]
                                    for key in combos_buffs_keys
                                    if values[key] not in [None, 0, ""]]))

            if party_members in [
                    None, "", 0] or len(party_buffs) == 0:
                self.layout.error_popup(
                    self.LANG.Errors.MUST_SETUP_PARTY)
                return None

            return (party_members, party_buffs, values["combo_heal_buff"], values["combo_heal_buff"] not in [None, "", 0])
        else:
            return (0, 0, 0, 0)

    def __validate_clicker(self, clicker, values):
        if clicker:
            click = values["combo_mouse_buttons"].lower() or ""

            if click == self.LANG.RIGHT.lower():
                click = "right"
            if click == self.LANG.LEFT.lower():
                click = "left"
            if click == self.LANG.MIDDLE.lower():
                click = "middle"

            click_delay = values["slider_mouse_delay"] or 0
            click_default_skill = values["combo_default_skill"]
            default_skill_delay = values["slider_default_skill_delay"]

            if click in [None, "", 0]:
                self.layout.error_popup(
                    self.LANG.Errors.MUST_CHOOSE_MOUSE_BUTTON)
                return None

            return (click, click_delay, click_default_skill, default_skill_delay)
        else:
            return (None, 0, 0, 0)

    def __end_threads(self):
        for thread in self.active_threads:
            thread.terminate()

    def __start(self, event, values):
        isStart = True if self.main_window[event].get_text(
        ) == self.LANG.START else False

        if not isStart:
            self.__end_threads()
            self.main_window[event].Update(self.LANG.START, button_color=(
                self.THEME.BUTTON_COLOR, self.THEME.BUTTON_BACKGROUND))

        if isStart:
            process = self.__validate_process(values["process_combo"])
            if not process:
                return

            handler = self.__validate_handler(process)
            if not handler:
                return

            buffer = self.main_window["button_onoff_buffer"].get_text(
            ) == "ON"

            clicker = self.main_window["button_onoff_clicker"].get_text(
            ) == "ON"

            buffer_party_valid = self.__validate_buffer_party(
                buffer, values)
            if not buffer_party_valid:
                return
            party_members, party_buffs, heal_buff, must_heal = buffer_party_valid

            clicker_valid = self.__validate_clicker(clicker, values)

            if not clicker_valid:
                return
            click, click_delay, click_default_skill, default_skill_delay = clicker_valid

            args = Args(
                buffer=buffer, clicker=clicker, handler=handler,
                pid=process, party_members=party_members,
                party_buffs=party_buffs, heal_buff=heal_buff,
                must_heal=must_heal, click=click,
                click_delay=click_delay,
                click_skill_default=click_default_skill,
                click_skill_delay=default_skill_delay)

            if buffer:
                clicker = None
                buffer_thread = multiprocessing.Process(
                    target=buffer_thread_function, args=(args,))
                buffer_thread.start()
                self.active_threads.append(buffer_thread)

            if clicker:
                clicker_thread = multiprocessing.Process(
                    target=clicker_thread_function, args=(args,))
                clicker_thread.start()
                self.active_threads.append(clicker_thread)

            self.main_window[event].Update(self.LANG.STOP, button_color=(
                self.THEME.BUTTON_INFO_COLOR, self.THEME.BUTTON_INFO_BACKGROUND))

    def __get_calls(self):
        return {
            "button_process_test": self.__test_process_handler,
            "button_onoff_buffer": self.__update_button_onoff,
            "button_onoff_clicker": self.__update_button_onoff,
            "image_wizard": self.__wizard_image_click,
            "button_start": self.__start
        }

    def __lang_window_event(self):
        lang_window = sg.Window(
            self.LANG.WINDOW_TITLE, self.layout.get_lang_layout(),
            size=(int(self.THEME.WINDOW_WIDTH * 0.6),
                  int(self.THEME.WINDOW_HEIGHT * 0.2)),
            background_color=self.THEME.MAIN_BACKGROUND,
            icon=icon.get_base64())

        while True:
            event, values = lang_window.read()

            if event in ["button_lang_en", "button_lang_es"]:
                lang = event.split("_")[2].upper()
                self.__update_lang(lang)
                self.layout = Layout(self.LANG, self.THEME)
                self.must_show_main_window = True
                break

            if event == sg.WIN_CLOSED or event == self.LANG.CANCEL:
                break

        lang_window.close()

    def __main_window_event(self):
        self.main_window = sg.Window(
            self.LANG.WINDOW_TITLE, self.layout.get_main_layout(),
            background_color=self.THEME.MAIN_BACKGROUND,
            finalize=True, icon=icon.get_base64())

        while True:
            calls = self.__get_calls()
            event, values = self.main_window.read()
            # print(event, values)

            if event in calls:
                calls[event](event, values)

            if event == sg.WIN_CLOSED or event == "button_exit":
                self.__end_threads()
                break

        self.main_window.close()

    def run(self):
        self.__lang_window_event()

        if self.must_show_main_window:
            self.__main_window_event()

        sys.exit()
