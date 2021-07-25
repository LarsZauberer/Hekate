from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

from src.Widgets.Widget import Widget
from src.functionDecorators import tryFunc

class Label(Widget):
    @tryFunc
    def __init__(self, app, name="undefined", text="", x=0, y=0, s=0.03):
        super().__init__(app, name)
        self.main = OnscreenText(text=text, pos=(x, y), scale=s)
        