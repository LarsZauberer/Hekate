from src.GameObjects.GameObject import GameObject
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from direct.actor.Actor import Actor
from pathlib import Path


class DynamicObject(GameObject):
    def __init__(self, app, name="undefined", model=None, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, collisionShape=BulletBoxShape(Vec3(0.5, 0.5, 0.5)), mass=0, animations={}):
        self.app = app
        self.name = name
        self.collisionShape = collisionShape
        self.animations = animations
        
        self._createMainNode(mass)
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        
        # ? Actor doesn't work
        # self.visNode = Actor(self.model, self.animations)
        
        self._loadModel(model, self.node)
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
    
    def update(self, task):
         return task.cont
