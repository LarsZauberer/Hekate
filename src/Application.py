from direct.showbase.ShowBase import ShowBase
from rpcore import RenderPipeline
from panda3d.core import load_prc_file_data, Vec3
from panda3d.bullet import BulletWorld, BulletDebugNode
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
from src.functionDecorators import tryFunc

class Application(ShowBase):
    
    def __init__(self, prcName, debug=False, forceDisableRenderPipelineDebug=True):
        # The main game class. Storing everything from world to models
        
        # Check if logs directory exists, if not create it
        import os
        if not os.path.exists("logs"):
            os.mkdir("logs")
        
        if os.path.exists(Path("logs/log.log")):
            os.remove(Path("logs/log.log"))
        
        FORMAT = "[%(name)s] %(message)s"
        FileHandler = logging.FileHandler(Path("logs/log.log"))
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(name)s] [%(levelname)-5.5s] %(message)s")
        FileHandler.setFormatter(logFormatter)
        if debug:
            from src.Console import ConsoleLogHandler
            logging.basicConfig(
                level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(), FileHandler, ConsoleLogHandler(self)]
            )
        else:
            logging.basicConfig(
                level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(), FileHandler]
            )

        log = self.getLogger(self.__init__)
        log.debug(f"Logging Initialized")
        
        load_prc_file_data("", f"""
            win-size 1920 1080
            window-title {prcName}
        """)

        try:
            # Construct and create the pipeline
            self.render_pipeline = RenderPipeline()
            
            self.render_pipeline.set_loading_screen_image("Content/loadingScreen.png")
            
            if forceDisableRenderPipelineDebug:
                # Force disable renderpipeline debugger
                def _debug_disabled():
                    class EmptyDebugger(object):  # pylint: disable=too-few-public-methods
                        def __getattr__(self, *args, **kwargs):
                            return lambda *args, **kwargs: None
                    self.render_pipeline.debugger = EmptyDebugger()  # pylint: disable=redefined-variable-type
                    del EmptyDebugger
                
                self.render_pipeline._init_debugger = _debug_disabled
            
            self.render_pipeline.create(self)
            
            log.debug(f"Render Pipeline started")
        except Exception:
            log.exception(f"Error while creating render_pipeline")
            exit("Error while creating render_pipeline")
            
        try:
            self.createBulletWorld()
            log.debug(f"Created Physics World")
            self.doPhysics = True
        except Exception:
            log.exception(f"Error while creating physics world")
            exit(f"Error while creating physics world")
        
        self.taskMgr.add(self.update, "update")
        
        # Camera Lense change
        self.camLens.set_fov(90)
        
        self.objectRegistry = []
        self.lightRegistry = []
        
        self.keys = []
        self.mv = self.mouseWatcherNode
        
        log.debug(f"Assigned Variables")
        
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
        
        log.debug(f"Assigned Keybinds")
        
        # Create developer console
        if debug:
            log.debug(f"Creating Console")
            from src.Console import Console
            self.console = Console(self)
            self.accept("tab", self.console.show_Console)
            
        
        
        # Finished -> Loading Map
        # TODO: #23 Make map list variable
        maps = {"test": Path("Content/map.json"), "test2": Path("Content/test.json")}
        self.mapLoader = MapLoader(self, maps)
        log.debug(f"Created Maploader")
        try:
            log.info(f"Loading Map: test")
            self.mapLoader.loadMap("test")
        except Exception:
            log.exception(f"Error while loading map: test")
        
    @tryFunc
    def update(self, task):
        dt = globalClock.getDt()
        if self.doPhysics:
            # TODO: Numbers from CPU power
            self.world.doPhysics(dt, 500, 1.0/180.0)
        
        return task.cont
    
    @tryFunc
    def createBulletWorld(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
    
    # Generates logging object to log to python console and a file
    def getLogger(self, func):
        log = logging.getLogger(str(func.__qualname__))
        
        return log
        