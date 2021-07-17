from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from pathlib import Path

from src.CollisionShapes import shapes


class GameObject:
    def __init__(self, app, name="undefined", model=None, ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, collisionShapeClass=1, collisionShapeArgs=[(1, 1, 1)], mass=0):
        # Importent saves
        self.app = app
        for i in collisionShapeArgs:
            if type(i) is list:
                collisionShapeArgs[collisionShapeArgs.index(i)] = tuple(i)
        self.collisionShape = shapes[collisionShapeClass](*collisionShapeArgs)
        self.name = name
        
        self._createMainNode(mass)
        self.node.setTag("ground", str(ground))
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