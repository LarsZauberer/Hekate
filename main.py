from src.Application import Application

class App(Application):
    def update(self, task):
        super().update(task)
        return task.cont
        
app = App("Test", False)

app.run()