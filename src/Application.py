from direct.showbase.ShowBase import ShowBase
from rpcore import RenderPipeline
from panda3d.core import load_prc_file_data, Vec3, BitMask32
from panda3d.bullet import BulletWorld

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

# Sorcery Engine
from src.ModelLoader import ModelLoader

class Application(ShowBase):
    
    def __init__(self, prcName, debug=False):
        # The main game class. Storing everything from world to models
        
        
        load_prc_file_data("", f"""
            win-size 1920 1080
            window-title {prcName}
        """)

        # Construct and create the pipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)
        
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        
        self.taskMgr.add(self.update, "update")
        
        # Camera Lense change
        self.camLens.set_fov(90)
        
        self.objectRegistry = []
        
        if debug:
            from rpcore.util.movement_controller import MovementController
            self.controller = MovementController(self)
            self.controller.set_initial_position_hpr(
                Vec3(-17.2912578583, -13.290019989, 6.88211250305),
                Vec3(-39.7285499573, -14.6770210266, 0.0))
            self.controller.setup()
        else:
            # TODO: Normal Player
            pass
    
    def update(self, task):
        # dt = globalClock.getDt()
        self.world.doPhysics(1)
        
        return task.cont
        