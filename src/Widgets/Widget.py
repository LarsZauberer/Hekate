from src.functionDecorators import tryFunc

class Widget:
    @tryFunc
    def __init__(self, app, name="undefined"):
        self.app = app
        self.name = name
        