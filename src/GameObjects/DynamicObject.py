from src.GameObjects.GameObject import GameObject
from src.functionDecorators import tryFunc


class DynamicObject(GameObject):
    @tryFunc
    def __init__(self, app, name="undefined", model="defaultMeshes/cube.bam", ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, mass=0, animations={}, emission=False, overlapping=False):
        """
        __init__ An DynamicObject is a GameObject that can have code.

        :param emission: If it has lights that should be moved according to the object movement, defaults to False
        :type emission: bool, optional
        """
        self.app = app #: The main application object
        self.name = name #: The name of the object
        self.animations = animations #: The animation of the object
        self.overlapping = overlapping #: Should the object be overlapping with other objects? Cannot be changed while running
        
        self.lights = [] #: The lights attached to the object
        self.emission = emission #: If the object has lights that should be moved according to the object movement, defaults to False
        
        # Collision
        self.touching = [] #: The objects that are touching the object. (BulletNodes)
        self.ignoreCollisionTriggerNames = [] #: Name patterns which should be ignored at the collision detection
        
        # Variables for API Reference
        self.node = None #: The main node which displays the object. You can get the physical node by self.node.node()
        self.model = None #: The model path
        
        self.createShape(model)
        self._createMainNode(mass)
        self.node.setTag("ground", str(ground))
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        
        # ? Actor doesn't work
        # self.visNode = Actor(self.model, self.animations)
        
        if len(self.animations.keys()) == 0:
            self._loadModel(model, self.node)
        
        # Add update task to app
        self.app.taskMgr.add(self.update, f"{name}_update")
    
    @tryFunc
    def update(self, task):
        """
        update Update function for the dynamic object. Please execute super().__init__(task) on it.
        """
        self._handleCollision()
        if self.emission:
            self._updateEmissionLights()
        return task.cont
    
    @tryFunc
    def onCollisionEnter(self, otherGameObject):
        """
        onCollisionEnter On collision of an other object entered

        :param otherGameObject: the other GameObject
        :type otherGameObject: panda3d.core.NodePath
        """
        pass
    
    @tryFunc
    def onCollisionStay(self, otherGameObject):
        """
        onCollisionStay On collision of an other object still happening

        :param otherGameObject: the other GameObject
        :type otherGameObject: panda3d.core.NodePath
        """
        pass
    
    @tryFunc
    def onCollisionExit(self, otherGameObject):
        """
        onCollisionExit On collision of an other object stopped

        :param otherGameObject: the other GameObject
        :type otherGameObject: panda3d.core.NodePath
        """
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
            if contact.getNode1() not in self.touching and not self._shouldIgnoreCollision(contact.getNode1()):
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
    
    @tryFunc
    def _shouldIgnoreCollision(self, node):
        for i in self.ignoreCollisionTriggerNames:
            if i in node.name:
                return True
        return False
