from panda3d.bullet import BulletBoxShape, BulletConvexHullShape, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode
from panda3d.core import Vec3
from pathlib import Path
from direct.actor.Actor import Actor
from src.functionDecorators import tryFunc


class GameObject:
    @tryFunc
    def __init__(self, app, name="undefined", model="defaultMeshes/cube.bam", ground=False, x=0, y=0, z=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1, mass=0, overlapping=False, emission=False, animations={}):
        """
        __init__ A normal GameObject, which has no dynamic code

        :param app: The main application
        :type app: src.Application.Application
        :param name: The name of the gameobject, defaults to "undefined"
        :type name: str, optional
        :param model: The model it should display. A .bam file, defaults to "defaultMeshes/cube.bam"
        :type model: str, optional
        :param ground: Should the gameobject have the tag ground. Maybe important for the player to know where to jump off, defaults to False
        :type ground: bool, optional
        :param x: position x, defaults to 0
        :type x: float, optional
        :param y: position y, defaults to 0
        :type y: float, optional
        :param z: position z, defaults to 0
        :type z: float, optional
        :param rx: roation x (Horizontal), defaults to 0
        :type rx: float, optional
        :param ry: rotation y (Pitch), defaults to 0
        :type ry: float, optional
        :param rz: rotation z (Roll), defaults to 0
        :type rz: float, optional
        :param sx: scale x, defaults to 1
        :type sx: float, optional
        :param sy: scale y, defaults to 1
        :type sy: float, optional
        :param sz: scale z, defaults to 1
        :type sz: float, optional
        :param mass: physical mass of the object. If it's 0, it has no rigidbody, defaults to 0
        :type mass: int, optional
        :param overlapping: Can you pass through the object?, defaults to False
        :type overlapping: bool, optional
        :param animations: Dictionary for all the animations. First animation has to be the model as .egg file. The key musst be called model, defaults to {}
        :type animations: dict, optional
        """
        # Importent saves
        self.app = app #: The main application
        self.name = name #: The name of the object
        self.animations = animations #: Animations
        self.overlapping = overlapping #: Should the object be overlapping (cannot be changed while running)
        
        # Emission Lights
        self.lights = [] #: Emission lights attached to the object
        
        # Variables for API Reference
        self.model = None #: The model path
        self.node = None #: The main node which displays the object. You can get the physical node by self.node.node()
        
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
            node.setDeactivationEnabled(False)
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
        """
        transform Transforms the object
        """
        self.node.setPosHprScale(x, y, z, rx, ry, rz, sx, sy, sz)
    
    @tryFunc
    def createShape(self, model):
        """
        createShape Creates the collision Shape of the object. Gets called in the __init__ function

        :param model: The model it should display. A .bam file, defaults to "defaultMeshes/cube.bam"
        :type model: str
        :return: Collision shape
        :rtype: BulletCollisionShape
        """
        return self.convexHullShape(model)
    
    @tryFunc
    def simpleShape(self, *args):
        """
        simpleShape Just a box
        """
        self.collisionShape = BulletBoxShape(Vec3(1, 1, 1))
    
    @tryFunc
    def convexHullShape(self, model):
        """
        convexHullShape Hull shape from the model
        """
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
        """
        triangleShape Exact shape from the model. Can't be used for moving objects.
        """
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
    