from src.Console import Command


class Test(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "test"
    
    def execute(self, cmd):
        print(cmd)
