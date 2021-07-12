from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from pathlib import Path


class GameObject:
    def __init__(self, app, name="undefined", model=None, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0, collisionShape=BulletBoxShape(Vec3(0.5, 0.5, 0.5)), mass=0):
        self.app = app
        self.collisionShape = collisionShape
        self.model = Path("Content") / Path(model)
        
        node = BulletRigidBodyNode(name)
        node.setMass(mass)
        node.addShape(collisionShape)
        self.node = self.app.render.attachNewNode(node)
        self.app.world.attachRigidBody(node)
        
        # TODO: Load Model multithreaded
        if self.model != None:
            modelObj = self.app.loader.loadModel(self.model)
            modelObj.copyTo(self.node)
            self.app.render_pipeline.prepare_scene(modelObj)
    
    def update():
        raise NotImplementedError
        