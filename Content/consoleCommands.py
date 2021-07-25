from src.Console import Command


class Test(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "test"
    
    def execute(self, cmd):
        print(cmd)

class HideInterface(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "hideinter"
    
    def execute(self, cmd):
        self.app.interfaceManager.unload("main")
