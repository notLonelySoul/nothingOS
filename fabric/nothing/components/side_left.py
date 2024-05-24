from fabric.widgets.wayland import Window
from fabric.widgets.box import Box
from fabric.widgets.revealer import Revealer
from fabric.widgets.entry import Entry
from fabric.widgets.stack import Stack
from fabric.widgets.label import Label

from fabric.utils.helpers import set_stylesheet_from_file, get_relative_path

from loguru import logger

class GeminiChat(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # sigh...

class LeftBar(Window):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor='left top bottom',
            exclusive=False,
            visible=False,
            all_visible=False,
            keyboard_mode='on-demand'
        )

        self.inner_box = Box(
            name="left-inner-box",
            children=[Label("hello world")]
        )

        self.revealer = Revealer(
            transition_duration=400,
            transition_type="slide-right",
            children=self.inner_box
        )
        
        self.main_box = Box(
            name="left-main-box",
            children=[self.revealer],
        )

        self.add(self.main_box)
        self.apply_styles()

    def apply_styles(*args):
        logger.info("[Side-Right-Bar] Applied Styles...")
        return set_stylesheet_from_file(get_relative_path('side-left.css'))