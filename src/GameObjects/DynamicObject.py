from src.GameObjects.GameObject import GameObject
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from direct.actor.Actor import Actor
from pathlib import Path

from src.CollisionShapes import shapes


class DynamicObject(GameObject):
    def __init__(self, app, name="undefined", model=None, ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, collisionShapeClass=1, collisionShapeArgs=[(1, 1, 1)], mass=0, animations={}):
        self.app = app
        self.name = name
        self.collisionShape = shapes[collisionShapeClass](*collisionShapeArgs)
        self.animations = animations
        
        # Collision
        self.touching = []
        
        self._createMainNode(mass)
        self.node.setTag("ground", str(ground))
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        
        # ? Actor doesn't work
        # self.visNode = Actor(self.model, self.animations)
        
        self._loadModel(model, self.node)
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
    
    def update(self, task):
        self._handleCollision()
        return task.cont
    
    def onCollisionEnter(self, otherGameObject):
        pass
    
    def onCollisionStay(self, otherGameObject):
        pass
    
    def onCollisionExit(self, otherGameObject):
        pass
    
    def _handleCollision(self):
        # Collision Testing
        result = self.app.world.contactTest(self.node.node())
        
        # Variables Collision
        newTouching = self.touching.copy()
        thisTimeTouching = []
        
        for contact in result.getContacts():
            # Check if touching for the first time
            if contact.getNode1() not in self.touching:
                self.onCollisionEnter(contact.getNode1())
                newTouching.append(contact.getNode1())
            thisTimeTouching.append(contact.getNode1())
        self.touching = newTouching.copy()
        # Remove all exited objects
        exited = list(set(self.touching) - set(thisTimeTouching))
        for i in exited:
            self.touching.remove(i)
        # Call all staying objects
        for i in self.touching:
            self.onCollisionStay(i)
        # Call all exited objects
        for i in exited:
            self.onCollisionExit(i)
            
