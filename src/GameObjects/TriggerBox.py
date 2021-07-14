from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import Vec3, BitMask32

from src.GameObjects.DynamicObject import DynamicObject
from pathlib import Path


class TriggerBox(DynamicObject):
    def __init__(self, app, name="undefined", x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1):
        self.app = app
        self.name = name
        
        # Collision
        self.touching = []

        shape = BulletBoxShape(Vec3(sx, sy, sz))

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
        
        self.model = Path("Content") / Path("metall.bam")
        self.modelObj = self.app.loader.loadModel(self.model)
        self.modelObj.reparent_to(self.node)
        
        self.modelObj.hide()
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
