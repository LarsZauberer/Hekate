import json
from src.GameObjects.Player.FirstPersonPlayer import FirstPersonPlayer
from src.functionDecorators import tryFunc
from src.GameObjects.Light import Light


class MapLoader:
    @tryFunc
    def __init__(self, app, maps: dict):
        """
        __init__ The Maploader with all the maps

        :param app: The main application
        :type app: src.Application.Application
        :param maps: All the maps with name and mapfile
        :type maps: dict
        """
        self.app = app
        self.maps = maps
    
    @tryFunc
    def loadMap(self, key):
        """
        loadMap Loades the map specified by key from the map dict

        :param key: The name of the map
        :type key: str
        """
        log = self.app.getLogger(self.loadMap)
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
        log.debug(f"Successfully loaded objects from file")
        
        for i in self.app.objectRegistry:
            if i.name == "Player":
                log.debug(f"Player found and assigned to app")
                self.app.player = i
        
    @tryFunc
    def unloadMap(self):
        """
        unloadMap Unloads the current map
        """
        log = self.app.getLogger(self.unloadMap)
        newRegistry = self.app.objectRegistry.copy()
        for i in self.app.objectRegistry:
            # Delete Collisions
            self.app.createBulletWorld()
            
            # Clean up actor if it exists
            if hasattr(i, "actor"):
                i.actor.cleanup()
                i.actor.removeNode()
            
            # Delete Visual Object
            i.node.removeNode()
            # Remove Loop
            self.app.taskMgr.remove(i.name + "_update")
            # Remove from registry
            newRegistry.remove(i)
        self.app.objectRegistry = newRegistry
        
        newLightRegistry = self.app.lightRegistry.copy()
        for i in self.app.lightRegistry:
            self.app.render_pipeline.remove_light(i)
            newLightRegistry.remove(i)
        self.app.lightRegistry = newLightRegistry
        
        log.debug(f"Successfully unloaded map")
