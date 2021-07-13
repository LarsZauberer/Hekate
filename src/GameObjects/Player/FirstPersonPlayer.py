from src.GameObjects.DynamicObject import DynamicObject
from panda3d.core import Vec3, BitMask32
from panda3d.bullet import BulletCapsuleShape, ZUp, BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode


class FirstPersonPlayer(DynamicObject):
    def __init__(self, app):
        # Character
        self.speed = 50
        self.preJumpSpeed = Vec3(0, 0, 0)

        h = 1.75
        w = 0.4
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)
        shape2 = BulletBoxShape((1, 1, 1))

        super().__init__(app, name="Player", collisionShape=shape2, x=-10, y=-10, z=14, mass=10, model="Block.bam")
        # self.node.node().setLinearFactor((1, 0, 0))
    
    def update(self, task):
        super().update(task)
        
        self.app.camera.setPos(self.node.getPos().x, self.node.getPos().y, self.node.getPos().z+3)
        self.node.setHpr(self.app.camera.getHpr().x, 0, 0)
        
        if self.app.mv.hasMouse():
            deltaX = self.app.mv.getMouseX()
            deltaY = round(self.app.mv.getMouseY(), 2)
            deltaX *= 10
            deltaY *= 10
            
            self.app.camera.setH(self.app.camera.getH() - deltaX)
            self.app.camera.setP(self.app.camera.getP() + deltaY)
            if self.app.camera.getP() > 90:
                self.app.camera.setP(90)
            if self.app.camera.getP() < -90:
                self.app.camera.setP(-90)
        
        speed = Vec3(0, 0, 0)
        
        if "w" in self.app.keys:
            forward = self.app.render.getRelativeVector(self.app.camera, Vec3(0,1,0))
            forward.normalize()
            forward.z = 0
            speed += forward*self.speed
        if "s" in self.app.keys:
            forward = self.app.render.getRelativeVector(self.app.camera, Vec3(0,-1,0))
            forward.normalize()
            forward.z = 0
            speed += forward*self.speed
        if "d" in self.app.keys:
            forward = self.app.render.getRelativeVector(self.app.camera, Vec3(1,0,0))
            forward.normalize()
            forward.z = 0
            speed += forward*self.speed
        if "a" in self.app.keys:
            forward = self.app.render.getRelativeVector(self.app.camera, Vec3(-1,0,0))
            forward.normalize()
            forward.z = 0
            speed += forward*self.speed
        if "space" in self.app.keys and self.isGrounded():
            speed.z += 20
        
        print(speed, self.node.getPos())
        
        if self.isGrounded():
            self.node.node().setLinearVelocity((speed.x, speed.y, self.node.node().getLinearVelocity().z + speed.z))
        else:
            self.node.node().setLinearVelocity((self.node.node().getLinearVelocity().x + speed.x/self.speed, self.node.node().getLinearVelocity().y + speed.y/self.speed, self.node.node().getLinearVelocity().z + speed.z))
            if self.node.node().getLinearVelocity().x > self.speed:
                self.node.node().setLinearVelocity((self.speed, self.node.node().getLinearVelocity().y, self.node.node().getLinearVelocity().z))
            if self.node.node().getLinearVelocity().x < -self.speed:
                self.node.node().setLinearVelocity((-self.speed, self.node.node().getLinearVelocity().y, self.node.node().getLinearVelocity().z))
            if self.node.node().getLinearVelocity().y > self.speed:
                self.node.node().setLinearVelocity((self.node.node().getLinearVelocity().x, self.speed, self.node.node().getLinearVelocity().z))
            if self.node.node().getLinearVelocity().y < -self.speed:
                self.node.node().setLinearVelocity((self.node.node().getLinearVelocity().x, -self.speed, self.node.node().getLinearVelocity().z))
        """print(dir(self.character))
        newSpeed = self.preJumpSpeed
        if self.preJumpSpeed.x == 0:
            newSpeed.x = speed.x*0.5
        if self.preJumpSpeed.y == 0:
            newSpeed.y = speed.y*0.5
        print(newSpeed)
        self.character.setLinearMovement(newSpeed, True)"""
        """maxAirVel = self.speed*0.3
        newSpeed = self.preJumpSpeed*0.3
        if speed.x != 0:
            newSpeed.x = speed.x*0.7
        if speed.y != 0:
            newSpeed.y = speed.y*0.7
        if newSpeed.x > self.preJumpSpeed.x*0.3:
            newSpeed.x = self.preJumpSpeed.x*0.3
        if newSpeed.y > self.preJumpSpeed.y*0.3:
            newSpeed.y = self.preJumpSpeed.y*0.3"""
        """newSpeed = self.preJumpSpeed + speed
        if newSpeed > 0.5:
            newSpeed.normalize()
            newSpeed *= 0.5
        self.character.setLinearMovement(newSpeed, True)"""
        
        print(self.isGrounded())
        
        self.app.win.movePointer(0, int(self.app.win.getXSize()/2), int(self.app.win.getYSize()/2))
        
        return task.cont
    
    def isGrounded(self):
        return round(self.node.node().getLinearVelocity().z, 0) == 0
