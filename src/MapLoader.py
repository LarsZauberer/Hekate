import json
from pathlib import Path


class MapLoader:
    def __init__(self, app, maps: dict):
        self.app = app
        self.maps = maps
    
    def loadMap(self, key):
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
        
