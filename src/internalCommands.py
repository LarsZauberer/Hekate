from src.Console import Command
from src.functionDecorators import tryFunc


class noclip(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "noclip"
        self.noclip = False
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        if not self.noclip:
            log.info(f"Activating Noclip")
            self.noclip = True
            from rpcore.util.movement_controller import MovementController
            self.app.controller = MovementController(self.app)
            self.app.controller.set_initial_position_hpr(
                self.app.camera.getPos(),
                self.app.camera.getHpr())
            self.app.controller.setup()
            self.app.taskMgr.remove("Player_update")
        else:
            log.info(f"Deactivating Noclip")
            self.noclip = False
            self.app.controller = False
            self.app.taskMgr.add(self.app.player.update, "Player_update")


class startPhysics(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "start"
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        log.info(f"Starting Physics")
        self.app.doPhysics = True
        self.app.console.phy = True

class stopPhysics(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "stop"
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        log.info(f"Stopping Physics")
        self.app.doPhysics = False
        self.app.console.phy = False


class showTriggers(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "show triggers"
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        if cmd == "1":
            log.info(f"Showing triggers")
        elif cmd == "0":
            log.info(f"Hiding triggers")
        for i in self.app.objectRegistry:
            from src.GameObjects.TriggerBox import TriggerBox
            if issubclass(type(i), TriggerBox):
                if cmd == "1":
                    i.node.show()
                elif cmd == "0":
                    i.node.hide()

class map(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "map"
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        if cmd not in self.app.mapLoader.maps.keys():
            log.warning(f"The map {cmd} doesn't exist")
            return
        log.info(f"Loading map: {cmd}")
        self.app.mapLoader.loadMap(cmd)

class showCollisions(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "show collisions"
    
    @tryFunc
    def execute(self, cmd):
        log = self.app.getLogger(self.execute)
        if cmd == "1":
            log.info(f"Showing collisions")
            from panda3d.bullet import BulletDebugNode
            debugNode = BulletDebugNode('Debug')
            debugNode.showWireframe(True)
            debugNode.showConstraints(True)
            debugNode.showBoundingBoxes(False)
            debugNode.showNormals(False)
            self.app.debugNP = self.app.render.attachNewNode(debugNode)
            self.app.debugNP.show()

            self.app.world.setDebugNode(self.app.debugNP.node())
        elif cmd == "0":
            log.info(f"Hiding collisions")
            self.app.debugNP.removeNode()
            self.app.world.clearDebugNode()