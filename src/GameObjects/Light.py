from rpcore import PointLight
from src.functionDecorators import tryFunc


class Light(PointLight):
    # Generate render_pipeline Pointlight
    @tryFunc
    def __init__(self, app, x=0, y=0, z=0, color_x=255, color_y=255, color_z=255, energy=1000, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0, model=None):
        """
        __init__ Simple Point Light object

        :param app: The main app instance
        :type app: src.Application.Application
        :param color_x: red, defaults to 255
        :type color_x: int, optional
        :param color_y: yellow, defaults to 255
        :type color_y: int, optional
        :param color_z: blue, defaults to 255
        :type color_z: int, optional
        :param energy: The power of the light, defaults to 1000
        :type energy: int, optional
        """
        self.light = PointLight()
        self.app = app
        
        self.app.render_pipeline.add_light(self.light)
        self.light.set_color(color_x, color_y, color_z)
        self.light.pos = (x, y, z)
        self.light.energy = energy
        
        self.app.lightRegistry.append(self.light)
