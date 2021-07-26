from panda3d.bullet import BulletBoxShape, BulletConvexHullShape, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode
from panda3d.core import Vec3
from pathlib import Path
from direct.actor.Actor import Actor
from src.functionDecorators import tryFunc


class GameObject:
    @tryFunc
    def __init__(self, app, name="undefined", model="defaultMeshes/cube.bam", ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, mass=0, overlapping=False, emission=False, animations={}):
        # Importent saves
        self.app = app
        self.name = name
        self.animations = animations
        self.overlapping = overlapping
        
        # Emission Lights
        self.lights = []
        
        self.createShape(model)
        self._createMainNode(mass)
        self.node.setTag("ground", str(ground))
        self.transform(x, y, z, rx, ry, rz, sx, sy, sz)
        if len(self.animations.keys()) == 0:
            self._loadModel(model, self.node)
    
    @tryFunc
    def _loadModel(self, model, node):
        # Loading the model for the object
        # TODO: Load Model multithreaded
        if model != None:
            if "defaultMeshes" in model:
                self.model = Path("src") / Path(model)
            else:
                self.model = Path("Content") / Path(model)
            modelObj = self.app.loader.loadModel(self.model)
            modelObj.copyTo(node)
            self.lights = self.app.render_pipeline.prepare_scene(node)["lights"]
            self.app.lightRegistry += self.lights
        else:
            self.model = None
    
    @tryFunc
    def _createMainNode(self, mass):
        # Creating the object
        if not self.overlapping:
            # Normal Collision Node
            node = BulletRigidBodyNode(self.name)
            node.setMass(mass)
            node.addShape(self.collisionShape)
            self.app.world.attachRigidBody(node)
        else:
            # Overlapping Node -> GhostNode
            node = BulletGhostNode(self.name)
            node.addShape(self.collisionShape)
            self.app.world.attachGhost(node)
            
        self.node = self.app.render.attachNewNode(node)
        
        if len(self.animations.keys()) > 0:
            self._createAnimationNode()
        
        # Add the object to the object Registry
        self.app.objectRegistry.append(self)
    
    @tryFunc
    def _createAnimationNode(self):
        log = self.app.getLogger(self._createAnimationNode)
        for i in self.animations.keys():
            self.animations[i] = Path("Content") / Path(self.animations[i])
        self.actor = Actor(self.animations["model"], self.animations)
        self.actor.reparentTo(self.node)
        try:
            self.actor.loop("idle")
        except Exception:
            log.debug(f"Couldn't play idle animation")
    
    @tryFunc
    def transform(self, x, y, z, rx, ry, rz, sx, sy, sz):
        self.node.setPosHprScale(x, y, z, rx, ry, rz, sx, sy, sz)
    
    @tryFunc
    def createShape(self, model):
        return self.convexHullShape(model)
    
    @tryFunc
    def simpleShape(self, *args):
        self.collisionShape = BulletBoxShape(Vec3(1, 1, 1))
    
    @tryFunc
    def convexHullShape(self, model):
        if "defaultMeshes" in model:
            geomNodes = self.app.loader.loadModel(Path("src") / Path(model)).findAllMatches('**/+GeomNode')
        else:
            geomNodes = self.app.loader.loadModel(Path("Content") / Path(model)).findAllMatches('**/+GeomNode')
        geomNode = geomNodes.getPath(0).node()
        geom = geomNode.getGeom(0)
        shape = BulletConvexHullShape()
        shape.addGeom(geom)
        self.collisionShape = shape
    
    @tryFunc
    def triangleShape(self, model):
        if "defaultMeshes" in model:
            geomNodes = self.app.loader.loadModel(Path("src") / Path(model)).findAllMatches('**/+GeomNode')
        else:
            geomNodes = self.app.loader.loadModel(Path("Content") / Path(model)).findAllMatches('**/+GeomNode')
        geomNode = geomNodes.getPath(0).node()
        geom = geomNode.getGeom(0)
        mesh = BulletTriangleMesh()
        mesh.addGeom(geom)
        shape = BulletTriangleMeshShape(mesh, dynamic=False)
        self.collisionShape = shape
    