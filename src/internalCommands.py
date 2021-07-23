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
        if not self.noclip:
            self.noclip = True
            from rpcore.util.movement_controller import MovementController
            self.app.controller = MovementController(self.app)
            self.app.controller.set_initial_position_hpr(
                self.app.camera.getPos(),
                self.app.camera.getHpr())
            self.app.controller.setup()
            self.app.taskMgr.remove("Player_update")
        else:
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
        self.app.doPhysics = True

class stopPhysics(Command):
    @tryFunc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = "stop"
    
    @tryFunc
    def execute(self, cmd):
        self.app.doPhysics = False
