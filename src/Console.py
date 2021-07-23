import inspect
from direct.gui.DirectGui import DirectEntry, DirectFrame
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Vec3, TextNode
from logging import StreamHandler

from src.functionDecorators import tryFunc

class Console:
    @tryFunc
    def __init__(self, app):
        self.app = app
        self.entry = None
        
        log = self.app.getLogger(self.__init__)
        try:
            import src.internalCommands as ic
        except Exception:
            log.exception(f"Error while loading internal commands")
        
        try:
            import Content.consoleCommands as cc
        except ModuleNotFoundError:
            log.warning(f"Didn't find a custom consoleCommands file")
        except Exception:
            log.exception(f"Error while loading custom console commands")
        
        # List of commands
        self.cmds = self.getCommands(ic)
        self.cmds += self.getCommands(cc)
        
        log.debug(f"Commands loaded: {[i.executor for i in self.cmds]}")
        
        # Save the physics state
        self.phy = self.app.doPhysics
        
        # Console log text
        self.logConsole = OnscreenText(text='Console', pos=(-0.95, 0.75), scale=0.03, mayChange=True, align=TextNode.ALeft)
        self.logConsole.hide()
        
        # Template for the input box
        self.entryTemplate = {"text": "", "scale": .05, "command": self.execute, "initialText": "", "numLines": 1, "focus": 1, "pos": Vec3(-0.95, 0, -0.75), "width": 38}
    
    @tryFunc
    def show_Console(self):
        log = self.app.getLogger(self.show_Console)
        # Show the console
        if self.entry is None:
            self.phy = self.app.doPhysics
            self.buildConsole()
            log.debug(f"Showing Console")
            self.app.doPhysics = False
        else:
            # Hide the console
            log.debug(f"Hiding Console")
            self.entry.destroy()
            self.frame.destroy()
            self.logConsole.hide()
            self.app.doPhysics = self.phy
            self.entry = None
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        cmd = cmd.lower()
        self.entry.destroy()
        self.entry = DirectEntry(**self.entryTemplate)
        
        # Show Help
        if cmd == "help":
            for i in [i.executor for i in self.cmds]:
                log.info(i)
        else:
            for i in self.cmds:
                if i.executor in cmd:
                    log.info(f"Executing command: {i.executor}")
                    i.execute(cmd.split(i.executor + " ")[-1])
                    return
            log.warning(f"Command not found: {cmd}")

    @tryFunc
    def getCommands(self, module):
        cmds = []
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Command) and obj.__name__ != "Command":
                cmds.append(obj)
        
        for i in cmds:
            cmds[cmds.index(i)] = i(self.app)
        
        return cmds

    @tryFunc
    def buildConsole(self):
        self.frame = DirectFrame(frameColor=(200, 200, 200, 0.7),
                            frameSize=(-1, 1, -0.8, 0.8),
                            pos=(0, -1, 0))
        
        self.logConsole.show()
        
        self.entry = DirectEntry(**self.entryTemplate)


class Command:
    @tryFunc
    def __init__(self, app):
        self.executor = ""
        self.app = app
    
    @tryFunc
    def execute(self, cmd):
        pass


class ConsoleLogHandler(StreamHandler):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
    
    def emit(self, record):
        msg = self.format(record)
        if hasattr(self.app, "console"):
            self.app.console.logConsole.text += "\n" + msg
