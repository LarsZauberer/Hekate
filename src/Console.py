import inspect
from direct.gui.DirectGui import DirectEntry
from panda3d.core import Vec3

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
        
        self.cmds = self.getCommands(ic)
        self.cmds += self.getCommands(cc)
        
        log.debug(f"Commands loaded: {[i.executor for i in self.cmds]}")
        
        self.phy = self.app.doPhysics
    
    @tryFunc
    def show_Console(self):
        log = self.app.getLogger(self.show_Console)
        if self.entry is None:
            self.phy = self.app.doPhysics
            self.entry = DirectEntry(text = "", scale=.05, command=self.execute,
            initialText="", numLines = 1, focus=1, pos=Vec3(0.8, 0, -0.95))
            log.debug(f"Showing Console")
            self.app.doPhysics = False
        else:
            log.debug(f"Hiding Console")
            self.entry.destroy()
            self.app.doPhysics = self.phy
            self.entry = None
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        cmd = cmd.lower()
        self.entry.destroy()
        self.app.doPhysics = self.phy
        self.entry = None
        
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


class Command:
    @tryFunc
    def __init__(self, app):
        self.executor = ""
        self.app = app
    
    @tryFunc
    def execute(self, cmd):
        pass
