from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

from src.Widgets.Widget import Widget
from src.functionDecorators import tryFunc

class Label(Widget):
    @tryFunc
    def __init__(self, app, name="undefined", text="", x=0, y=0, s=0.03):
        """
        __init__ A Simple Label(Text) Widget

        :param app: The Main application
        :type app: src.Application.Application
        :param name: Name for the widget, defaults to "undefined"
        :type name: str, optional
        :param text: Text it should display. Can be changed dynamicly, defaults to ""
        :type text: str, optional
        :param x: position x, defaults to 0
        :type x: float, optional
        :param y: position y, defaults to 0
        :type y: float, optional
        :param s: text size, defaults to 0.03
        :type s: float, optional
        """
        super().__init__(app, name)
        self.main = OnscreenText(text=text, pos=(x, y), scale=s, mayChange=True)
        