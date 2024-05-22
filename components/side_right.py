import json

from fabric.widgets.revealer import Revealer
from fabric.widgets.box import Box
from fabric.widgets.overlay import Overlay
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from fabric.widgets.wayland import Window
from fabric.widgets.scrolled_window import ScrolledWindow
from fabric.widgets.entry import Entry
from fabric.utils.helpers import set_stylesheet_from_file, get_relative_path, bulk_connect

from myutils.widgets import SideTaskElement, ButtonWithId
from myutils.usr_data import *

import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from loguru import logger
import os

class RightBar(Window):
    def __init__(self,):
        super().__init__(
            layer="top",
            anchor="right top bottom",
            exclusive=False,
            visible=False,
            all_visible= False,
            keyboard_mode='on-demand'
        )

        self.DATA_FILE_PATH = f"{DATA_DIR}/tasks.json"

        self.menu_box = Box(
            name="right-menu-box",
            children=Label("hello")
        )

        self.calendar = Box(
            name="calendar-box",
            children=[Gtk.Calendar(name="calendar")]
        )
        
        self.todo_label = Label(name="todo-label", label="TO-DO", h_align='start')

        self.tasks = self.get_tasks()
        self.tasks_list_box = Box(
            name="tasks-list-box",
            orientation='v',
            h_expand=True,
            children=self.tasks
        )
        self.tasks_list = ScrolledWindow(
            name="task-list-scroll-window",
            h_expand=True, 
            v_expand=True,
            children=self.tasks_list_box
        )

        self.entry = Entry(
            name="task-entry",
            placeholder_text="add task...",
        )
        self.entry.set_editable(True)
        self.entry.connect('activate', self.add_task)
        
        self.task_box = Box(
            name="side-task-box",
            orientation='v',
            children=[self.todo_label, self.tasks_list, self.entry]
        )

        for element in self.tasks:
            bulk_connect(
                element.focus_button,
                {
                    "button-press-event": self.set_focus_task
                }
            )

            bulk_connect(
                element.delete_button,
                {
                    "button-press-event": self.delete_task
                }
            )
            
        self.inside_box = Box(
            orientation='v',
            children=[self.menu_box, self.calendar, self.task_box],
        )

        self.revealer_box = Revealer(
            transition_duration=400,
            transition_type="slide-left",
            children=self.inside_box
        )

        self.main_box = Box(
            name="right-main-box",
            children=[self.revealer_box],
        )

        self.add(self.main_box)
        self.apply_styles()

    def apply_styles(*args):
        logger.info("[Side-Right-Bar] Applied Styles...")
        return set_stylesheet_from_file(get_relative_path('side_right.css'))

    def set_focus_task(self, button: ButtonWithId, event):
        ... # to be overridden

    def delete_task(self, button: ButtonWithId, event):

        id = button.get_id()
        with open(self.DATA_FILE_PATH, 'r') as f:
            tasks = json.load(f)
            del tasks[id]
            idx = 0
            for i in tasks: 
                idx +=1 
                i = f"{idx}"

            print(tasks)
            f2 = open(self.DATA_FILE_PATH, 'w')
            json.dump(tasks, f2)
            f2.close()

        self.tasks = self.get_tasks()

        self.tasks_list_box.set_children(self.tasks)

        for element in self.tasks:
            bulk_connect(
                element.focus_button,
                {
                    "button-press-event": self.set_focus_task
                }
            )

            bulk_connect(
                element.delete_button,
                {
                    "button-press-event": self.delete_task
                }
            )
    
    def get_tasks(self, *args):
        with open(self.DATA_FILE_PATH, 'r') as f:
            s = json.load(f)
            return [SideTaskElement(label=s[i], id=i) for i in s]

    def add_task(self, entry:Entry):
        task = entry.get_text()
        entry.set_text("")
        with open(self.DATA_FILE_PATH, 'r') as f:
            tasks = json.load(f)
            try:
                id = f"{int(max(tasks.keys()))+1}"
            except:
                id = 1
            tasks[id] = task

            f2 = open(self.DATA_FILE_PATH, 'w')
            json.dump(tasks, f2)
            f2.close()

        self.tasks = self.get_tasks()

        self.tasks_list_box.set_children(self.tasks)

        for element in self.tasks:
            bulk_connect(
                element.focus_button,
                {
                    "button-press-event": self.set_focus_task
                }
            )

            bulk_connect(
                element.delete_button,
                {
                    "button-press-event": self.delete_task
                }
            )



            
