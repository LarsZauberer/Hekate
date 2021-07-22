from src.GameObjects.GameObject import GameObject
from panda3d.core import Vec3


class DynamicObject(GameObject):
    def __init__(self, app, name="undefined", model=None, ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, mass=0, animations={}, emission=False):
        self.app = app
        self.name = name
        self.animations = animations
        
        self.lights = []
        self.emission = emission
        
        # Collision
        self.touching = []
        
        self.createShape(model)
        self._createMainNode(mass)
        self.node.setTag("ground", str(ground))
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        self.oldPos = Vec3(x, y, z)
        
        # ? Actor doesn't work
        # self.visNode = Actor(self.model, self.animations)
        
        self._loadModel(model, self.node)
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
    
    def update(self, task):
        self._handleCollision()
        if self.emission:
            self._updateEmissionLights()
            self.oldPos = self.node.getPos()
        self.node.setPos(self.node.getPos()+0.01)
        for i in self.lights:
            print(i.pos)
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
            
    def createShape(self, model):
        return super().convexHullShape(model)
    
    def _updateEmissionLights(self):
        # TODO: Emission Rotation
        for i in self.lights:
            i.pos = i.pos + self.node.getPos() - self.oldPos
