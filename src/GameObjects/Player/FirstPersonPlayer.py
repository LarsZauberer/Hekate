from panda3d.core import Vec3
from src.GameObjects.GameObject import GameObject
from panda3d.bullet import BulletCapsuleShape

class FirstPersonPlayer(GameObject):
    def __init__(self, app):
        super().__init__(app, "Player", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, collisionShape=BulletCapsuleShape(0.5, 1.75), mass=1)
        self.app = app
        
    
    def update(self):
        if self.app.mv.hasMouse():
            deltaX = self.app.mv.getMouseX()
            deltaY = round(self.app.mv.getMouseY(), 2)
            deltaX *= 10
            deltaY *= 10
            
            self.node.setH(self.node.getH() - deltaX)
            self.app.camera.setP(self.node.getP() + deltaY)
            if self.node.getP() > 90:
                self.node.setP(90)
            if self.node.getP() < -90:
                self.node.setP(-90)
        
        if "w" in self.app.keys:
            camPos = self.node.getPos()
            forward = self.app.render.getRelativeVector(self.node,Vec3(0,1,0))
            forward.z = 0
            forward.normalize()
            self.node.node().setLinearVelocity(forward)
        if "s" in self.app.keys:
            camPos = self.node.getPos()
            forward = self.app.render.getRelativeVector(self.node, Vec3(0,1,0))
            forward.z = 0
            forward.normalize()
            self.node.node().setLinearVelocity(forward)
        if "d" in self.app.keys:
            camPos = self.node.getPos()
            forward = self.app.render.getRelativeVector(self.node, Vec3(1,0,0))
            forward.z = 0
            forward.normalize()
            self.node.node().setLinearVelocity(forward)
        if "a" in self.app.keys:
            camPos = self.node.getPos()
            forward = self.app.render.getRelativeVector(self.node, Vec3(1,0,0))
            forward.z = 0
            forward.normalize()
            self.node.node().setLinearVelocity(forward)
        
        pos = self.node.getPos()
        hpr = self.node.getHpr()
        self.app.camera.setPosHprScale(pos.x, pos.y, pos.z, hpr.x, self.app.camera.getHpr().y, hpr.z, 1, 1, 1)
        
        self.app.win.movePointer(0, int(self.app.win.getXSize()/2), int(self.app.win.getYSize()/2))
    