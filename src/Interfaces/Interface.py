from pathlib import Path
import json

from Content.widgetRegistry import widgets
from src.functionDecorators import tryFunc

class Interface:
    """
     A Basic Interface class
     An Interface is a collection of widgets, that will be shown on screen.
    """
    @tryFunc
    def __init__(self, app, name, file):
        """
        __init__ Creates an interface. It can be automatically created through the InterfaceManager

        :param app: The main application
        :type app: src.Application.Application
        :param name: The name of the interface
        :type name: str
        :param file: The construction file on how to construct the interface (Path begins in the Content folder)
        :type file: str
        """
        self.app = app
        self.file = file
        self.name = name
        self.content = []
    
    @tryFunc    
    def load(self):
        """
        load Loades all the widgets for the interface and creates the update task for the interface
        """
        with open(Path("Content") / Path(self.file), 'r') as f:
            data = json.load(f)
        
        for i in data["data"]:
            # TODO: Maybe children and parent system
            self.content.append(widgets[i["id"]](self.app, **i["data"]))
        
        self.app.taskMgr.add(self.update, self.name + "_interface_update")
    
    @tryFunc        
    def unload(self):
        """
        unload Unloads/Destroys all the widgets for the interface and removes the update task for the interface
        """
        for i in self.content:
            i.main.destroy()
        self.app.taskMgr.remove(self.name + "_interface_update")
    
    @tryFunc    
    def update(self, task):
        """
        update Update Task for the Interface

        :param task: Task from the taskmanager
        """
        return task.cont
        