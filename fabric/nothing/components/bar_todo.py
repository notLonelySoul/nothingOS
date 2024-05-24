import json

from fabric.widgets.box import Box
from fabric.widgets.button import Button 
from fabric.widgets.label import Label
from fabric.utils.helpers import set_stylesheet_from_file, get_relative_path

from myutils.usr_data import *
from myutils.widgets import ButtonWithId

from loguru import logger

class BarToDo(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.DATA_FILE_PATH = f"{DATA_DIR}/tasks.json"
        self.focus_no = '1'

        if not os.path.isfile(self.DATA_FILE_PATH): os.mknod(self.DATA_FILE_PATH)

        with open(self.DATA_FILE_PATH, 'r') as f:
            tasks = json.load(f)
            try:
                self.current_task = tasks[self.focus_no]
            except: 
                self.current_task = "add some tasks first lol..."

        self.todobox = Button(
            name="todo-main-box",
            label=self.current_task
        )

        self.box = Box(
            name="back-box",
            children=self.todobox
        )

        self.add_children(self.box)

    def apply_styles(self, *args):
        logger.info("[Bar] Applied Styles...")
        return set_stylesheet_from_file(get_relative_path("bar_todo.css"))
    
    def set_focus_task(self, button: ButtonWithId, event):
        self.focus_no = button.get_id()
        self.update_label()      


    def update_label(self):
        with open(self.DATA_FILE_PATH, 'r') as f:
            tasks = json.load(f)
            try:
                self.todobox.set_label(tasks[self.focus_no])
            except: 
                self.current_task = "omoshiroi"