from src.Application import Application
from src.GameObjects.GameObject import GameObject

from panda3d.bullet import BulletDebugNode

app = Application("Test", False)

go = GameObject(app, "Test", "terrain.bam")
dynamic = GameObject(app, "dynamic", "greenblock.bam", mass=10)
dynamic.node.setPos(0, 0, 10)

app.run()