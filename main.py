from src.Application import Application

class App(Application):
    def __init__(self):
        super().__init__()
        # keybinds
        
        # Mousecatching
        # self.catchMouse(True)
        
        # Other important stuff for your game
    
    def update(self, task):
        super().update(task)
        return task.cont
        
app = App("Test", True)

app.run()