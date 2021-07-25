from src.functionDecorators import tryFunc

class Widget:
    @tryFunc
    def __init__(self, app, name="undefined"):
        """
        __init__ A general Widget

        :param app: The main application
        :type app: src.Application.Application
        :param name: The name of the widget, defaults to "undefined"
        :type name: str, optional
        """
        self.app = app
        self.name = name
        