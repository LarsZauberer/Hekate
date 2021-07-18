import json


class MapLoader:
    def __init__(self, app, maps: dict):
        self.app = app
        self.maps = maps
    
    def loadMap(self, key):
        self.unloadMap()
        with open(self.maps[key], "r") as f:
            data = json.load(f)
            
        try:
            from Content.classRegistry import classes
        except ModuleNotFoundError as e:
            print(e)
            exit("No Class Registry found")
        
        mapData = data["mapData"]
        for i in mapData:
            # Spawn objects
            classes[i["id"]](self.app, **i["data"])
        
        # TODO: Spawn Player from mapData
        
    def unloadMap(self):
        newRegistry = self.app.objectRegistry.copy()
        for i in self.app.objectRegistry:
            # Delete Collisions
            self.app.createBulletWorld()
            
            # Delete Visual Object
            i.node.removeNode()
            # Remove Loop
            self.app.taskMgr.remove(i.name + "_update")
            # Remove from registry
            newRegistry.remove(i)
        self.app.objectRegistry = newRegistry
