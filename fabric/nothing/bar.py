import fabric
import gi
from fabric.widgets.overlay import Overlay
from loguru import logger

gi.require_version("Gtk", "3.0")
from fabric.system_tray.widgets import SystemTray
from fabric.utils.fabricator import Fabricator
from fabric.utils.helpers import get_relative_path, set_stylesheet_from_file
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.circular_progress_bar import CircularProgressBar
from fabric.widgets.date_time import DateTime
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import Window
from gi.repository import GLib, Gtk

from components.bar_media import BarMedia
from components.side_right import RightBar
from components.side_left import LeftBar
from components.volumewidget import VolumeWidget
from components.workspace import LeftBox
from components.bar_todo import BarToDo
from myutils.usr_data import *

class Bar(Window):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            layer="top",
            anchor="top left right",
            visible=False,
            all_visible=False,
        )

        self.right_button = Button(
            name="right-panel-button",
            label="",
        )

        self.battery_icon = Label(name="battery-icon", label="")
        self.battery_percentage = Label(
            name="battery-label",
            label="",
        )

        self.battery_box = Box(
            name="battery-box",
            children=[
                self.battery_icon,
                self.battery_percentage,
            ],
        )

        self.separator = Box(name="separator")

        self.mem_prog = CircularProgressBar(name="mem-prog", size=(28, 28))

        self.mem_box = Box(
            name="mem-box",
            children=[
                Overlay(
                    children=self.mem_prog,
                    overlays=[
                        Label(
                            label="󰧑",
                            style="font-size:14px; color: #d9d9d9; margin-right: 4px;",
                        )
                    ],
                )
            ],
        )

        self.cpu_prog = CircularProgressBar(name="mem-prog", size=(28, 28))

        self.cpu_box = Box(
            name="cpu-box",
            children=[
                Overlay(
                    children=self.cpu_prog,
                    overlays=[
                        Label(
                            label="",
                            style="font-size:14px; color: #d9d9d9; margin-right: 4px;",
                        )
                    ],
                )
            ],
        )

        self.sub_sys_info_box = Box(
            name="sub-sys-info-box", children=[self.battery_box, self.separator, self.cpu_box]
        )

        self.sys_revealer = Revealer(
            name="sigh",
            children=self.sub_sys_info_box,
            transition_type="slide-left",
            transition_duration=400,
        )
        self.sys_revealer.set_reveal_child(True)

        self.sys_info_box = Box(
            name="sys-info-box", children=[self.sys_revealer, self.mem_box]
        )

        self.right_button.connect("button-press-event", self.activate_right_bar)

        self.right = Box(
            name="bar-right-box",
            children=[
                VolumeWidget(),
                SystemTray(
                    name="sys-tray",
                    icon_size=20,
                ),
                self.right_button,
            ],
        )
        self.leftbox = LeftBox()
        self.leftbox.logo_button.connect("button-press-event", self.activate_left_bar)
        self.barmedia = BarMedia()
        self.bar_todo = BarToDo()
        self.main_box = CenterBox(
            start_children=[
                self.leftbox,
                self.barmedia,
                self.sys_info_box,
            ],
            center_children=[
                DateTime(
                    name="date-time",
                    format_list=["%H:%M:%S", "%A", "%d-%m-%Y"],
                    h_align="center",
                )
            ],
            end_children=[self.bar_todo, self.right],
        )

        player_status = Fabricator(
            stream=True, poll_from="playerctl --follow metadata --format {{status}}"
        )
        player_status.connect("changed", self.player_status_change)

        mem = Fabricator(
            stream=True,
            poll_from=f"""/home/{USER_NAME}/.config/nothing/fabric/nothing/scripts/memory""",
        )
        mem.connect("changed", self.sigh)

        cpu = Fabricator(
            stream=True,
            poll_from=f"""/home/{USER_NAME}/.config/nothing/fabric/nothing/scripts/cpu""",
        )
        cpu.connect("changed", self.cpu)

        batt = Fabricator(
            stream=True,
            poll_from=f"""/home/{USER_NAME}/.config/nothing/fabric/nothing/scripts/battery""",
        )
        batt.connect("changed", self.batt)

        RightBar.set_focus_task = self.bar_todo.set_focus_task
        self.right_panel = RightBar()
        self.left_panel = LeftBar()



        self.add(self.main_box)
        self.show_all()

    def apply_styles(*args):
        logger.info("[Bar] Applied Styles...")
        return set_stylesheet_from_file(get_relative_path("bar.css"))

    def activate_right_bar(self, *args):

        self.right_panel.show_all()
        self.right_panel.entry.get_focus_on_click()
        self.right_panel.revealer_box.set_reveal_child(
            not self.right_panel.revealer_box.get_reveal_child()
        )

    def activate_left_bar(self, *args):

        self.left_panel.show_all()
        self.left_panel.revealer.set_reveal_child(
            not self.left_panel.revealer.get_reveal_child()
        )

    def sigh(self, _, data):
        info = eval(data)
        self.mem_prog.percentage = float(info["percentage"])

    def cpu(self, _, data):
        self.cpu_prog.percentage = float(data)

    def batt(self, _, data):
        info = eval(data)
        self.battery_percentage.set_label(f"{int(info['percent'])}%")

        map = {
            0: "󰂃",
            10: "󰁺",
            20: "󰁻",
            30: "󰁼",
            40: "󰁽",
            50: "󰁿",
            60: "󰁿",
            70: "󰂀",
            80: "󰂁",
            90: "󰂂",
            100: "󰁹",
            "charging": "󰂄",
        }

        if info["status"]:
            self.battery_icon.set_label(map["charging"])
        else:
            self.battery_icon.set_label(map[(info["percent"] // 10) * 10])

    def player_status_change(self, _, data):
        if data == "":
            print("player exit")
            self.barmedia.revealer.set_reveal_child(False)
            self.sys_revealer.set_reveal_child(True)
            self.song_cover.set_style("background-color: #0d0d0d;")
        else:
            print("entered player")
            self.barmedia.revealer.set_reveal_child(True)
            self.sys_revealer.set_reveal_child(False)


if __name__ == "__main__":
    bar = Bar()
    bar.apply_styles()
    bar.leftbox.apply_styles()
    bar.barmedia.apply_styles()
    bar.bar_todo.apply_styles()
    print(bar.main_box.get_allocated_height())

    fabric.start()
