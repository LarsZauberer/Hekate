from src.GameObjects.GameObject import GameObject
from src.functionDecorators import tryFunc


class DynamicObject(GameObject):
    @tryFunc
    def __init__(self, app, name="undefined", model="defaultMeshes/cube.bam", ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, mass=0, animations={}, emission=False, overlapping=False):
        self.app = app
        self.name = name
        self.animations = animations
        self.overlapping = overlapping
        
        self.lights = []
        self.emission = emission
        
        # Collision
        self.touching = []
        
        self.createShape(model)
        self._createMainNode(mass)
        self.node.setTag("ground", str(ground))
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        
        # ? Actor doesn't work
        # self.visNode = Actor(self.model, self.animations)
        
        self._loadModel(model, self.node)
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
    
    @tryFunc
    def update(self, task):
        self._handleCollision()
        if self.emission:
            self._updateEmissionLights()
        return task.cont
    
    @tryFunc
    def onCollisionEnter(self, otherGameObject):
        pass
    
    @tryFunc
    def onCollisionStay(self, otherGameObject):
        pass
    
    @tryFunc
    def onCollisionExit(self, otherGameObject):
        pass
    
    @tryFunc
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
     
    @tryFunc       
    def createShape(self, model):
        return super().convexHullShape(model)
    
    @tryFunc
    def _updateEmissionLights(self):
        # All node lights. They are not the real light.
        nodeLights = []
        for i in self.node.children[0].children[0].children:
            if "Light" in i.name:
                nodeLights.append(i)

        try:
            assert len(nodeLights) == len(self.lights)
        except AssertionError:
            print("Not enough lights in the model found. Make sure every light has the \"Light\" in the name.")
            print(f"Lights found: {nodeLights}")

        for i in self.lights:
            # Relative Light Vector to the parent object
            lightRelVec = nodeLights[self.lights.index(i)].getPos()
            i.pos = self.app.render.getRelativeVector(self.node, lightRelVec) + self.node.getPos()
