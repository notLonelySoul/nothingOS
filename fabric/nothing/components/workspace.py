import gi
from loguru import logger

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.hyprland.widgets import Workspaces, WorkspaceButton
from fabric.hyprland.service import Hyprland
from fabric.utils.string_formatter import FormattedString
from fabric.utils.helpers import set_stylesheet_from_file, get_relative_path

connection = Hyprland()

class LeftBox(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            v_expand=False,
            **kwargs,
        )
        
        #defining boxes & buttons
        self.main_box = Box(name="main-box", v_expand=False)
        self.logo_button = Button(name="logo-button", label="󰣇")
        self.separator = Box(name="separator")
        
        Workspaces.scroll_handler = self.scroll_handler
        self.workspaces = Workspaces(
            spacing=2,
            name="workspaces",
            buttons_list=[
                WorkspaceButton(label=FormattedString("")),
                WorkspaceButton(label=FormattedString("")),
                WorkspaceButton(label=FormattedString("")),
                WorkspaceButton(label=FormattedString("")),
                WorkspaceButton(label=FormattedString("")),
                WorkspaceButton(label=FormattedString("")),
                WorkspaceButton(label=FormattedString("")),
            ],
        )
        self.main_box.add_children([self.logo_button, self.separator, self.workspaces])
        self.add(self.main_box)
        
    def scroll_handler(self, widget, event: Gdk.EventScroll):
        match event.direction:
            case Gdk.ScrollDirection.UP:
                connection.send_command(
                    "batch/dispatch workspace -1",
                )
                logger.info("[Workspaces] Moved to the next workspace")
            case Gdk.ScrollDirection.DOWN:
                connection.send_command(
                    "batch/dispatch workspace +1",
                )
                logger.info("[Workspaces] Moved to the previous workspace")
            case _:
                logger.info(
                    f"[Workspaces] Unknown scroll direction ({event.direction})"
                )
        return

    def apply_styles(*args):
        logger.info("[Workspaces] Applied Styles...")
        return set_stylesheet_from_file(get_relative_path('workspace_box.css'))
    
