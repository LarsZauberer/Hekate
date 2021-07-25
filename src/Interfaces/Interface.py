from pathlib import Path
import json

from Content.widgetRegistry import widgets
from src.functionDecorators import tryFunc

class Interface:
    @tryFunc
    def __init__(self, app, name, file):
        self.app = app
        self.file = file
        self.name = name
        self.content = []
    
    @tryFunc    
    def load(self):
        with open(Path("Content") / Path(self.file), 'r') as f:
            data = json.load(f)
        
        for i in data["data"]:
            # TODO: Maybe children and parent system
            self.content.append(widgets[i["id"]](self.app, **i["data"]))
        
        self.app.task_mgr.add_task(self.update, self.name + "_interface_update")
    
    @tryFunc        
    def unload(self):
        pass
    
    @tryFunc    
    def update(self, task):
        return task.cont
        