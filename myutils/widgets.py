from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

class ButtonWithId(Button):
    def __init__(self, ID:str, **kwargs):
        super().__init__(**kwargs)
        self.ID = ID

    def set_id(self, id:str):
        self.ID = id

    def get_id(self):
        return self.ID    
    

class SideTaskElement(Box):
    def __init__(self, label:str, id:str, **kwargs):
        super().__init__(**kwargs)

        self.label = label
        self.ID = id

        self.label_element = Label(
            name="task-element-label",
            label=self.label
        )

        self.focus_button = ButtonWithId(
            name="task-element-focus-button",
            label="",
            ID=self.ID
        )

        self.delete_button = ButtonWithId(
            name="task-delete-button",
            label="",
            ID=self.ID
        )

        self.main_box = Box(
            name="task-element-main-box",
            children=[
                self.focus_button,
                self.label_element,
                self.delete_button
            ]
        )

        self.add_children(self.main_box)
