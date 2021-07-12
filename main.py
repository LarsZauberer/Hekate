from src.Application import Application
from src.GameObjects.GameObject import GameObject

from panda3d.bullet import BulletDebugNode
from panda3d.core import Vec3, Material

from rpcore import PointLight


class App(Application):
    def update(self, task):
        super().update(task)
        radioLight.pos = (dynamic.node.getPos().x, dynamic.node.getPos().y, dynamic.node.getPos().z + 2)
        if dynamic.node.getPos().z < 2:
            dynamic.node.node().setLinearVelocity(Vec3(0, 0, 10))
        return task.cont
        
app = App("Test", True)

go = GameObject(app, "Test", "terrain.bam")
dynamic = GameObject(app, "dynamic", "radioactive.bam", mass=10)
dynamic.node.setPos(0, 0, 10)

my_light = PointLight()
my_light.energy = 5000
my_light.pos = (1, 1, 20)
app.render_pipeline.add_light(my_light)

radioLight = PointLight()
radioLight.energy = 10000
radioLight.color = (0, 255, 0)
app.render_pipeline.add_light(radioLight)

# dynamic.node.setMaterial(Material)


app.run()