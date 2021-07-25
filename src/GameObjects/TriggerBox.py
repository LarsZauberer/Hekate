from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import Vec3, BitMask32

from src.GameObjects.DynamicObject import DynamicObject
from src.functionDecorators import tryFunc
from pathlib import Path


class TriggerBox(DynamicObject):
    @tryFunc
    def __init__(self, app, name="undefined", x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, model=None):
        """
        __init__ Triggerbox object for simple triggering. Can be made visible through the console command: show triggers 1
        """
        self.app = app
        self.name = name
        
        self.emission = False
        
        # Collision
        self.touching = []

        shape = BulletBoxShape(Vec3(1, 1, 1))

        ghost = BulletGhostNode(name)
        ghost.addShape(shape)
        
        self.node = self.app.render.attachNewNode(ghost)
        self.node.setPos(0, 0, 0)
        self.node.setCollideMask(BitMask32(0x0f))
        self.node.setTag("ground", "False")

        self.app.world.attachGhost(ghost)
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        
        # Add the object to the object Registry
        self.app.objectRegistry.append(self)
        
        self.model = Path("src/defaultMeshes") / Path("metall.bam")
        self.modelObj = self.app.loader.loadModel(self.model)
        self.modelObj.copyTo(self.node)
        
        self.node.hide()
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
