from direct.showbase.ShowBase import ShowBase
from rpcore import RenderPipeline
from panda3d.core import load_prc_file_data, Vec3
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.gui.DirectGui import DirectEntry
from pathlib import Path
import logging
from rich.logging import RichHandler

# Plugins for packaging
from rpplugins import ao, bloom, clouds, color_correction, dof, env_probes, forward_shading, fxaa, motion_blur, pssm, scattering, skin_shading, sky_ao, smaa, ssr, volumetrics, vxgi
from rpplugins.ao import plugin
from rpplugins.bloom import plugin
from rpplugins.clouds import plugin
from rpplugins.color_correction import plugin
from rpplugins.dof import plugin
from rpplugins.env_probes import plugin
from rpplugins.forward_shading import plugin
from rpplugins.fxaa import plugin
from rpplugins.motion_blur import plugin
from rpplugins.pssm import plugin
from rpplugins.scattering import plugin
from rpplugins.skin_shading import plugin
from rpplugins.sky_ao import plugin
from rpplugins.smaa import plugin
from rpplugins.ssr import plugin
from rpplugins.volumetrics import plugin
from rpplugins.vxgi import plugin

# Hekate Engine
from src.MapLoader import MapLoader

class Application(ShowBase):
    
    def __init__(self, prcName, debug=False):
        # The main game class. Storing everything from world to models
        
        FORMAT = "[%(name)s] %(message)s"
        if debug:
            logging.basicConfig(
                level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
            )
        else:
            logging.basicConfig(
                level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
            )

        self.log = self.getLogger("root")
        self.log.debug(f"Logging Initialized")
        
        load_prc_file_data("", f"""
            win-size 1920 1080
            window-title {prcName}
        """)

        try:
            # Construct and create the pipeline
            self.render_pipeline = RenderPipeline()
            self.render_pipeline.set_loading_screen_image("Content/loadingScreen.png")
            self.render_pipeline.create(self)
            self.log.debug(f"Render Pipeline started")
        except Exception:
            self.log.exception(f"Error while creating render_pipeline")
            
        try:
            self.createBulletWorld()
            self.log.debug(f"Created Physics World")
            self.doPhysics = True
        except Exception:
            self.log.exception(f"Error while creating physics world")
        
        self.taskMgr.add(self.update, "update")
        
        # Camera Lense change
        self.camLens.set_fov(90)
        
        self.objectRegistry = []
        
        self.keys = []
        self.mv = self.mouseWatcherNode
        
        self.noclip = False
        
        self.log.debug(f"Assigned Variables")
        
        # TODO: #26 Keybinding System
        self.accept("w", self.keys.append, ["w"])
        self.accept("w-up", self.keys.remove, ["w"])
        self.accept("s", self.keys.append, ["s"])
        self.accept("s-up", self.keys.remove, ["s"])
        self.accept("d", self.keys.append, ["d"])
        self.accept("d-up", self.keys.remove, ["d"])
        self.accept("a", self.keys.append, ["a"])
        self.accept("a-up", self.keys.remove, ["a"])
        self.accept("space", self.keys.append, ["space"])
        self.accept("space-up", self.keys.remove, ["space"])
        
        self.disable_mouse()

        self.accept("tab", self.show_Console)
        
        self.log.debug(f"Assigned Keybinds")
        
        
        # Finished -> Loading Map
        # TODO: #23 Make map list variable
        maps = {"test": Path("Content/map.json"), "test2": Path("map.json")}
        self.mapLoader = MapLoader(self, maps)
        self.log.debug(f"Created Maploader")
        try:
            self.mapLoader.loadMap("test")
        except Exception:
            self.log.exception(f"Error while loading map: test")
        self.log.info(f"Loading Map: test")
        
    
    def update(self, task):
        dt = globalClock.getDt()
        if self.doPhysics:
            # TODO: Numbers from CPU power
            self.world.doPhysics(dt, 500, 1.0/180.0)
        
        return task.cont
    
    def show_Console(self):
        self.entry = DirectEntry(text = "", scale=.05, command=self.execute,
        initialText="", numLines = 1, focus=1, pos=Vec3(0.8, 0, -0.95))
        self.log.debug(f"Showing Console")
    
    def execute(self, cmd):
        cmd = cmd.lower()
        self.log.info(f"Trying to execute command: {cmd}")
        self.entry.destroy()
        if "noclip" in cmd:
            if not self.noclip:
                self.log.info(f"Activating noclip")
                self.noclip = True
                from rpcore.util.movement_controller import MovementController
                self.controller = MovementController(self)
                self.controller.set_initial_position_hpr(
                    self.camera.getPos(),
                    self.camera.getHpr())
                self.controller.setup()
                self.taskMgr.remove("Player_update")
            else:
                self.log.info(f"Deactivating noclip")
                self.noclip = False
                self.controller = False
                self.taskMgr.add(self.player.update, "Player_update")
        elif "show triggers" in cmd:
            if cmd[-1] == "1":
                self.log.info(f"Showing triggers")
            elif cmd[-1] == "0":
                self.log.info(f"Hiding triggers")
            for i in self.objectRegistry:
                from src.GameObjects.TriggerBox import TriggerBox
                if issubclass(type(i), TriggerBox):
                    if cmd[-1] == "1":
                        i.node.show()
                    elif cmd[-1] == "0":
                        i.node.hide()
        elif "map" in cmd:
            mapName = cmd.split("map ")[1]
            self.log.info(f"Loading map: {mapName}")
            self.mapLoader.loadMap(mapName)
            self.log.debug(f"Successfully loaded map")
        elif "show collision" in cmd:
            if cmd[-1] == "1":
                self.log.info(f"Showing collisions")
                debugNode = BulletDebugNode('Debug')
                debugNode.showWireframe(True)
                debugNode.showConstraints(True)
                debugNode.showBoundingBoxes(False)
                debugNode.showNormals(False)
                self.debugNP = self.render.attachNewNode(debugNode)
                self.debugNP.show()

                self.world.setDebugNode(self.debugNP.node())
            elif cmd[-1] == "0":
                self.log.info(f"Hiding collisions")
                self.debugNP.removeNode()
                self.world.clearDebugNode()
        elif "stop" in cmd:
            self.log.info(f"Stopping physics")
            self.doPhysics = False
        elif "start" in cmd:
            self.log.info(f"Starting physics")
            self.doPhysics = True
        else:
            self.log.info(f"No Command found")
    
    def createBulletWorld(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
    
    # Generates logging object to log to python console and a file
    def getLogger(self, name):
        # Check if logs directory exists, if not create it
        import os
        if not os.path.exists("logs"):
            os.mkdir("logs")
        
        if name == "root":
            if os.path.exists(Path("logs/log.log")):
                os.remove(Path("logs/log.log"))
        
        log = logging.getLogger(name)
        log.addHandler(logging.StreamHandler())
        FileHandler = logging.FileHandler(Path("logs/log.log"))
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(name)s] [%(levelname)-5.5s] %(message)s")
        FileHandler.setFormatter(logFormatter)
        log.addHandler(FileHandler)
        
        return log
        