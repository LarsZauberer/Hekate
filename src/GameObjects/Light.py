from rpcore import PointLight
from src.functionDecorators import tryFunc


class Light(PointLight):
    # Generate render_pipeline Pointlight
    @tryFunc
    def __init__(self, app, x=0, y=0, z=0, color_x=255, color_y=255, color_z=255, energy=1000, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0, model=None):
        self.light = PointLight()
        self.app = app
        
        self.app.render_pipeline.add_light(self.light)
        self.light.set_color(color_x, color_y, color_z)
        self.light.pos = (x, y, z)
        self.light.energy = energy
