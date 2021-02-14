import os
import sys
import PySimpleGUI as sg
from .theme import Theme
from .lang import Lang
from .images import wizard
from providers.process import Process


class CommonComponents:
    THEME = Theme
    LANG = Lang

    @staticmethod
    def set_theme(theme):
        global THEME
        THEME = theme

    @staticmethod
    def set_lang(lang):
        global LANG
        LANG = lang

    @staticmethod
    def column(
            elements, key=None,
            size=(THEME.COLUMN_WIDTH, THEME.COLUMN_HEIGHT),
            background_color=THEME.MAIN_BACKGROUND, pad=(None, None),
            vertical_alignment="top", justification=None,
            element_justification=None, expand_x=False,
            expand_y=False, scrollable=False):
        return sg.Column(
            elements, key=key, size=size,
            background_color=background_color, pad=pad,
            vertical_alignment=vertical_alignment,
            justification=justification,
            element_justification=element_justification,
            expand_x=expand_x, expand_y=expand_y,
            scrollable=scrollable)

    @staticmethod
    def label(text, key=None, font=THEME.TEXT_FONT,
              text_color=THEME.TEXT_COLOR,
              background_color=THEME.SECONDARY_BACKGROUND,
              justification="left",
              tooltip=None, size=(None, None)):
        return sg.Text(
            text, key=key, font=font, text_color=text_color,
            background_color=background_color, tooltip=None,
            justification=justification, size=size)

    @staticmethod
    def button(
            button_text="No text", key=None, k=None,
            button_color=(THEME.BUTTON_COLOR,
                          THEME.BUTTON_BACKGROUND),
            size=(None, None), auto_size_button=False):
        return sg.Button(
            button_text=button_text, key=key, k=k,
            button_color=button_color,
            size=size, auto_size_button=auto_size_button)

    @staticmethod
    def combo(
            options, key=None, readonly=True, size=(None, None),
            auto_size_text=True, tooltip=None, default_value=None,
            pad=(None, None)):
        return sg.Combo(
            options, key=key, readonly=readonly, size=size,
            auto_size_text=auto_size_text, tooltip=tooltip,
            default_value=default_value, pad=pad)

    @staticmethod
    def divider(
            color=THEME.SECONDARY_BACKGROUND, pad=(0, 20),
            key=None):
        return sg.HorizontalSeparator(color=color, pad=pad, key=key)

    @staticmethod
    def slider(
            range, key=None, resolution=1, orientation="h",
            tick_interval=1, size=(None, None), pad=(None, None)):
        if range in [None, (0, 0), ""]:
            return "No range specified"

        return sg.Slider(
            range=range, key=key, resolution=resolution,
            orientation=orientation, tick_interval=tick_interval,
            size=size, pad=pad)

    @staticmethod
    def frame(
            title=None, key=None, background_color=None,
            relief="flat", layout=[], pad=(None, None)):
        return sg.Frame(title=title, key=key, pad=pad,
                        background_color=background_color,
                        relief=relief, layout=layout)

    @staticmethod
    def image(
            data=None, filename=None, key=None, size=(None, None),
            enable_events=False, pad=(None, None)):
        return sg.Image(
            data=data, filename=filename, key=key, size=size, pad=pad,
            enable_events=enable_events)


class Layout:
    def __init__(self, lang, theme):
        self.get_pids = Process.get_pids
        self.LANG = lang
        self.THEME = theme
        CommonComponents.set_theme(self.THEME)
        CommonComponents.set_lang(self.LANG)

    def get_process_list(self, process_name):
        process_list = self.get_pids(process_name)
        return [p["name"] +
                " (" + str(p["pid"]) + ")" for p in process_list]

    def error_popup(self, msg):
        sg.Popup(
            msg,
            button_color=(self.THEME.BUTTON_ERROR_COLOR, self.THEME.
                          BUTTON_ERROR_BACKGROUND),
            no_titlebar=True, custom_text=(self.LANG.OK))

    def get_lang_layout(self):
        text_window_title = CommonComponents.label(
            self.LANG.WINDOW_TITLE, font=self.THEME.HEADINGS_FONT,
            text_color=self.THEME.HEADINGS_COLOR,
            background_color=self.THEME.MAIN_BACKGROUND,
            justification="center", size=(self.THEME.COLUMN_WIDTH, None))

        button_english = CommonComponents.button(
            "English", key="button_lang_en")
        button_spanish = CommonComponents.button(
            "Español", key="button_lang_es")

        column_buttons = CommonComponents.column(
            [[button_english, button_spanish]],
            justification="center", element_justification="center",
            background_color=self.THEME.MAIN_BACKGROUND, size=(None, None))

        return [
            [text_window_title],
            [column_buttons]
        ]

    def get_main_layout(self):
        # Common padding to all elements
        padding = self.THEME.ELEMENT_PADDING
        pad = (padding, padding)

        # List of Mu process
        process_list = self.get_process_list("Main.exe")

        text_window_title = sg.Text(
            self.LANG.WINDOW_TITLE, font=self.THEME.HEADINGS_FONT,
            text_color=self.THEME.HEADINGS_COLOR,
            background_color=self.THEME.MAIN_BACKGROUND)

        column_header = CommonComponents.column(
            [[text_window_title]],
            pad=pad, expand_x=True, size=(None, None),
            element_justification="center")

        label_process_combo = CommonComponents.label(
            self.LANG.CHOOSE_PROCESS)
        combo_process = CommonComponents.combo(
            process_list, key="process_combo", auto_size_text=False, pad=pad,
            size=(int(self.THEME.COLUMN_WIDTH / self.THEME.PIXEL_CHARACTER_FACTOR / 1.5),
                  0))
        button_process_test = CommonComponents.button(
            button_text=self.LANG.TEST_IT_BUTTON, key="button_process_test",
            button_color=(self.THEME.BUTTON_COLOR,
                          self.THEME.BUTTON_BACKGROUND),
            size=(int(self.THEME.COLUMN_WIDTH / 8 / 3) - 3, 0))

        divider_label_buffs = CommonComponents.label(
            self.LANG.AUTOBUFF,
            font=self.THEME.CUSTOMIZABLE_FONT.format(
                size=11, style="bold"))
        divider_buffs = CommonComponents.divider()
        button_onoff_buffer = CommonComponents.button(
            self.LANG.ON, key="button_onoff_buffer",
            auto_size_button=True)
        divider_text_buffs = [divider_label_buffs,
                              button_onoff_buffer, divider_buffs]

        label_party_members_combo = CommonComponents.label(
            self.LANG.PARTY_MEMBERS)

        combo_party_members = CommonComponents.combo(
            [1, 2, 3, 4, 5], key="party_members_combo")

        label_buffs_skills = CommonComponents.label(
            self.LANG.BUFF_SKILLS)
        row_buffs_skills = [label_buffs_skills]
        skills_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in range(1, 6):
            input_buff_skill = CommonComponents.combo(
                skills_options, key="combo_buff_skill-" + str(x),
                default_value=skills_options[0])
            row_buffs_skills = row_buffs_skills + [input_buff_skill]

        label_heal_buff = CommonComponents.label(self.LANG.HEAL_BUFF)
        combo_heal_buff = CommonComponents.combo(
            skills_options, key="combo_heal_buff",
            default_value=skills_options[0])

        divider_label_clicks = CommonComponents.label(
            self.LANG.AUTOCLICKER,
            font=self.THEME.CUSTOMIZABLE_FONT.format(
                size=11, style="bold"))
        divider_clicks = CommonComponents.divider()
        button_onoff_clicker = CommonComponents.button(
            self.LANG.ON, key="button_onoff_clicker",
            auto_size_button=True)
        divider_text_clicks = [
            divider_label_clicks, button_onoff_clicker,
            divider_clicks]

        mouse_buttons_options = [
            self.LANG.LEFT, self.LANG.MIDDLE, self.LANG.RIGHT]
        label_mouse_buttons = CommonComponents.label(
            self.LANG.MOUSE_BUTTON)
        combo_mouse_buttons = CommonComponents.combo(
            mouse_buttons_options, key="combo_mouse_buttons",
            default_value=self.LANG.RIGHT)

        label_default_skill = CommonComponents.label(
            self.LANG.DEFAULT_SKILL)
        combo_default_skill = CommonComponents.combo(
            skills_options, key="combo_default_skill",
            default_value=skills_options[0])

        label_mouse_delay = CommonComponents.label(
            self.LANG.CLICK_DELAY)
        slider_mouse_delay = CommonComponents.slider(
            range=(0, 20.0),
            key="slider_mouse_delay",
            resolution=0.1, orientation="h", tick_interval=5,
            pad=((20, 0), (0, 0)),
            size=((self.THEME.COLUMN_WIDTH - 20) / self.THEME.
                  PIXEL_CHARACTER_FACTOR - 7, None))

        label_defaul_skill_delay = CommonComponents.label(
            self.LANG.CLICKER_BUFF_DELAY)
        slider_defaul_skill_delay = CommonComponents.slider(
            range=(0, 180),
            key="slider_default_skill_delay",
            resolution=0.1, orientation="h", tick_interval=30,
            pad=((20, 0), (0, 0)),
            size=((self.THEME.COLUMN_WIDTH - 20) / self.THEME.
                  PIXEL_CHARACTER_FACTOR - 7, None))

        frame_buffer = CommonComponents.frame(
            key="frame_buffer",
            background_color=self.THEME.SECONDARY_BACKGROUND,
            layout=[[label_party_members_combo, combo_party_members],
                    row_buffs_skills,
                    [label_heal_buff, combo_heal_buff]])

        frame_clicker = CommonComponents.frame(
            key="frame_clicker",
            pad=((0, 0), (0, padding)),
            background_color=self.THEME.SECONDARY_BACKGROUND,
            layout=[[label_mouse_buttons, combo_mouse_buttons,
                     label_default_skill, combo_default_skill],
                    [label_mouse_delay],
                    [slider_mouse_delay],
                    [label_defaul_skill_delay],
                    [slider_defaul_skill_delay]])

        column_settings = CommonComponents.column(
            [[label_process_combo],
             [combo_process, button_process_test],
             divider_text_buffs, [frame_buffer],
             divider_text_clicks, [frame_clicker]],
            background_color=self.THEME.SECONDARY_BACKGROUND, pad=pad,
            expand_y=True, size=(None, 450))

        column_actions_width = int(self.THEME.COLUMN_WIDTH / 3)
        buttons_actions_width = int(
            column_actions_width / self.THEME.PIXEL_CHARACTER_FACTOR)-1

        button_start = CommonComponents.button(
            button_text=self.LANG.START, key="button_start",
            size=(buttons_actions_width, None))

        button_exit = CommonComponents.button(
            button_text=self.LANG.EXIT, key="button_exit",
            button_color=(self.THEME.BUTTON_ERROR_COLOR, self.THEME.
                          BUTTON_ERROR_BACKGROUND),
            size=(buttons_actions_width, None))

        base64_wizard = wizard.get_base64()
        image_wizard = CommonComponents.image(
            data=base64_wizard, key="image_wizard", size=(114, 281),
            pad=((0, 0),
                 (100, 0)),
            enable_events=True)

        column_actions = CommonComponents.column(
            [[button_start],
             [button_exit],
             [image_wizard]],
            pad=pad, size=(column_actions_width, None),
            element_justification="center", expand_y=True)

        return [
            [column_header],
            [column_settings, column_actions]
        ]
