import json
from pathlib import Path
from src.GameObjects.Player.FirstPersonPlayer import FirstPersonPlayer


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
        except ModuleNotFoundError:
            exit("No Class Registry found")
        
        mapData = data["mapData"]
        for i in mapData:
            # Spawn objects
            classes[i["id"]](self.app, **i["data"])
    
    def unloadMap(self):
        newRegistry = self.app.objectRegistry.copy()
        for i in self.app.objectRegistry:
            if type(i) != FirstPersonPlayer:
                i.node.removeNode()
                self.app.taskMgr.remove(i.name + "_update")
                newRegistry.remove(i)
        self.app.objectRegistry = newRegistry
