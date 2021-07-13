from src.GameObjects.GameObject import GameObject
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from direct.actor.Actor import Actor
from pathlib import Path


class DynamicObject(GameObject):
    def __init__(self, app, name="undefined", model=None, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0, collisionShape=BulletBoxShape(Vec3(0.5, 0.5, 0.5)), mass=0, animations={}):
        self.app = app
        self.name = name
        if model is not None:
            self.model = Path("Content") / Path(model)
        else:
            self.model = model
        self.animations = animations
        
        # Creating the parent object
        node = BulletRigidBodyNode(name)
        node.setMass(mass)
        node.addShape(collisionShape)
        self.node = self.app.render.attachNewNode(node)
        self.app.world.attachRigidBody(node)
        
        self.visNode = Actor(self.model. self.animations)
        self.visNode.reparent_to(self.node)
        
        # Add the object to the object Registry
        self.app.objectRegistry.append(self)
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
    
    def update(self, task):
         return task.cont
