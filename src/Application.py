from direct.showbase.ShowBase import ShowBase
from rpcore import RenderPipeline
from panda3d.core import load_prc_file_data, Vec3
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.gui.DirectGui import DirectEntry
from pathlib import Path

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
        
        
        load_prc_file_data("", f"""
            win-size 1920 1080
            window-title {prcName}
        """)

        # Construct and create the pipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.set_loading_screen_image("Content/loadingScreen.png")
        self.render_pipeline.create(self)
        
        self.createBulletWorld()
        self.doPhysics = True
        
        self.taskMgr.add(self.update, "update")
        
        # Camera Lense change
        self.camLens.set_fov(90)
        
        self.objectRegistry = []
        
        self.keys = []
        self.mv = self.mouseWatcherNode
        
        self.noclip = False
            
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
        
        
        # Finished -> Loading Map
        # TODO: Make map list variable
        maps = {"test": Path("Content/test.json"), "test2": Path("map.json")}
        self.mapLoader = MapLoader(self, maps)
        self.mapLoader.loadMap("test")
        
        # TODO: Create trough console
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        self.debugNP = self.render.attachNewNode(debugNode)
        self.debugNP.hide()

        self.world.setDebugNode(self.debugNP.node())
    
    def update(self, task):
        dt = globalClock.getDt()
        if self.doPhysics:
            # TODO: Numbers from CPU power
            self.world.doPhysics(dt, 500, 1.0/180.0)
        
        return task.cont
    
    def show_Console(self):
        self.entry = DirectEntry(text = "", scale=.05, command=self.execute,
        initialText="", numLines = 1, focus=1, pos=Vec3(0.8, 0, -0.95))
    
    def execute(self, cmd):
        cmd = cmd.lower()
        self.entry.destroy()
        if "noclip" in cmd:
            if not self.noclip:
                self.noclip = True
                from rpcore.util.movement_controller import MovementController
                self.controller = MovementController(self)
                self.controller.set_initial_position_hpr(
                    self.camera.getPos(),
                    self.camera.getHpr())
                self.controller.setup()
                self.taskMgr.remove("Player_update")
            else:
                self.noclip = False
                self.controller = False
                self.taskMgr.add(self.player.update, "Player_update")
        elif "show triggers" in cmd:
            for i in self.objectRegistry:
                from src.GameObjects.TriggerBox import TriggerBox
                if issubclass(type(i), TriggerBox):
                    if cmd[-1] == "1":
                        i.node.show()
                    elif cmd[-1] == "0":
                        i.node.hide()
        elif "map" in cmd:
            mapName = cmd.split("map ")[1]
            self.mapLoader.loadMap(mapName)
        elif "show collision" in cmd:
            if cmd[-1] == "1":
                self.debugNP.show()
            elif cmd[-1] == "0":
                self.debugNP.hide()
        elif "stop" in cmd:
            self.doPhysics = False
        elif "start" in cmd:
            self.doPhysics = True
        else:
            print("No Command found")
    
    def createBulletWorld(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))