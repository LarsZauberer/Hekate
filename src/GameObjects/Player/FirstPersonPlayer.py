from src.GameObjects.DynamicObject import DynamicObject
from panda3d.core import Vec3, BitMask32
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode


class FirstPersonPlayer(DynamicObject):
    def __init__(self, app):
        # Character
        self.crouching = False
        self.app = app
        self.name = "Player"
        
        self.speed = 0.5
        self.preJumpSpeed = Vec3(0, 0, 0)

        h = 1.75
        w = 0.4
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        # self.character.setMass(1.0)
        self.characterNP = self.app.render.attachNewNode(self.character)
        self.characterNP.setPos(-2, 0, 14)
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.app.world.attachCharacter(self.character)
        
        self.app.taskMgr.add(self.update, "Player_update")
    
    def update(self, task):
        super().update(task)
        
        self.app.camera.setPos(self.characterNP.getPos())
        if self.character.isOnGround():
            self.characterNP.setHpr(self.app.camera.getHpr().x, self.characterNP.getHpr().y, self.characterNP.getHpr().z)
        
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
            speed.setY(speed.y+1*self.speed)
        if "s" in self.app.keys:
            speed.setY(speed.y-1*self.speed)
        if "d" in self.app.keys:
            speed.setX(speed.x+1*self.speed)
        if "a" in self.app.keys:
            speed.setX(speed.x-1*self.speed)
        
        if self.character.isOnGround():
            self.character.setLinearMovement(speed, True)
            self.preJumpSpeed = speed
        else:
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
        

        
        self.app.win.movePointer(0, int(self.app.win.getXSize()/2), int(self.app.win.getYSize()/2))
        
        return task.cont

    def doJump(self):
        self.character.setMaxJumpHeight(5.0)
        self.character.setJumpSpeed(8.0)
        self.character.doJump()

    def doCrouch(self):
        self.crouching = not self.crouching
        sz = self.crouching and 0.6 or 1.0

        self.characterNP.setScale(Vec3(1, 1, sz))
