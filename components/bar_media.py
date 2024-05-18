import os

import gi
from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
    set_stylesheet_from_file,
)
from fabric.utils.fabricator import Fabricator
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import Window
from loguru import logger

from myutils.funcs import *
from myutils.usr_data import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk


class BarMedia(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.status: bool = None

        self.mainbox = Box(name="bar-media-main-box", v_align="center")

        self.sub_box = Box(
            name="sub-box",
            h_align="center",
            orientation="vertical",
        )

        self.song_info = Label(
            label="nothing playing...",
            name="bar-media-label",
            h_expand=False,
        )

        self.song_prog = Gtk.ProgressBar(fraction=True, halign=True)

        self.icon_button = Button(
            label="", name="status-icon", v_align="center", h_align="center"
        )
        self.icon_button.connect(
            "button-press-event",
            self.button_press,
        )

        self.song_cover = Box(
            name="cover-box",
            children=[
                Overlay(
                    children=Box(name="media-cover"),
                    overlays=[
                        self.icon_button,
                    ],
                ),
            ],
        )

        info = Fabricator(
            stream=True,
            poll_from=r"""playerctl --follow metadata --format {{title}},,{{artist}},,{{position}},,{{mpris:length}},,{{status}}""",
        )
        info.connect("changed", self.set_info)

        cover = Fabricator(
            stream=True,
            poll_from=r"""playerctl --follow metadata --format {{mpris:artUrl}}""",
        )
        cover.connect("changed", self.set_cover)

        self.sub_box.add_children([self.song_info, self.song_prog])
        self.revealer = Revealer(
            children=self.sub_box,
            transition_type="slide-right",
            transition_duration=400,
        )

        self.mainbox.add_children([self.song_cover, self.revealer])
        self.eventbox = EventBox(children=self.mainbox)
        self.eventbox.connect("button-press-event", self.on_click)
        self.add_children(self.eventbox)

    def set_info(self, _, data: str):
        try:
            title, artist, pos, length, status = data.split(",,")
            self.status = True
        except:
            print("no players to decode data... lol")
            self.song_cover.set_style("background-color: #0d0d0d;")
            self.mainbox.set_style("background-color: #D9D9D9;")
            self.status = False

        self.song_info.set_label(format_string(f"{title} • {artist}", 30))
        try:
            self.song_prog.set_fraction(float(pos) / float(length))
        except Exception as e:
            logger.info(e)

        sd = {"Playing": "", "Paused": "", "Stopped": ""}

        self.icon_button.set_label(sd[status])

    def set_cover(
        self, _, data: str
    ):  # fix by Gummy Bear for asynchronous image fetching...
        Gio.File.new_for_uri(uri=data).copy_async(
            destination=Gio.File.new_for_path(
                get_relative_path(f"{CONF_CACHE_DIR}/cover.png")
            ),
            flags=Gio.FileCopyFlags.OVERWRITE,
            io_priority=GLib.PRIORITY_HIGH,
            cancellable=None,
            progress_callback=None,
            callback=self.img_ready,
        )

    def img_ready(self, source, res):
        try:
            os.path.isfile(get_relative_path(f"{CONF_CACHE_DIR}/cover.png"))
            source.copy_finish(res)
            self.song_cover.set_style(
                f"background-image: url('{CONF_CACHE_DIR}/cover.png');"
            )

            img = Image.open(f"{CONF_CACHE_DIR}/cover.png")
            img = img.convert("RGB")
            dominant_color = get_domme_color(img)

            self.mainbox.set_style(
                f"background-image: linear-gradient(to right, rgb{dominant_color}, #D9D9D9);"
            )

        except ValueError as e:
            logger.info(e)

    def button_press(self, *args):
        if self.status:
            exec_shell_command_async("playerctl play-pause", None)
        else:
            try:
                exec_shell_command_async(r"spotify-launcher", None)
            except Exception as e:
                logger.info(e)
                print(
                    r"you prolly have installed some other package for spotify, use that command instead in components/bar_media.py #149"
                )

    def on_click(self, btn, event):
        if event.button == 2:
            exec_shell_command_async("playerctl previous", None)
        elif event.button == 3:
            exec_shell_command_async("playerctl next", None)


    def apply_styles(*args):
        logger.info("[Bar-Media] Applied Styles...")
        return set_stylesheet_from_file(get_relative_path("bar_media.css"))
