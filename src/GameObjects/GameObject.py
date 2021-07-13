from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from pathlib import Path


class GameObject:
    def __init__(self, app, name="undefined", model=None, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, collisionShape=BulletBoxShape(Vec3(0.5, 0.5, 0.5)), mass=0):
        # Importent saves
        self.app = app
        self.collisionShape = collisionShape
        self.name = name
        
        self._createMainNode(mass)
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        self._loadModel(model, self.node)
    
    def _loadModel(self, model, node):
        # Loading the model for the object
        # TODO: Load Model multithreaded
        if model != None:
            self.model = Path("Content") / Path(model)
            modelObj = self.app.loader.loadModel(self.model)
            modelObj.copyTo(node)
            self.app.render_pipeline.prepare_scene(modelObj)
        else:
            self.model = None
    
    def _createMainNode(self, mass):
        # Creating the object
        node = BulletRigidBodyNode(self.name)
        node.setMass(mass)
        node.addShape(self.collisionShape)
        self.node = self.app.render.attachNewNode(node)
        self.app.world.attachRigidBody(node)
        
        # Add the object to the object Registry
        self.app.objectRegistry.append(self)
    
    def transform(self, x, y, z, rx, ry, rz, sx, sy, sz):
        self.node.setPosHprScale(x, y, z, rx, ry, rz, sx, sy, sz)
        