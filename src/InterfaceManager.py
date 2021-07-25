from Content.interfaceRegistry import interfaces as interfaceIDs

class InterfaceManager:
    def __init__(self, app, interfaces):
        self.app = app
        self.interfaces = interfaces
        self.currentInterfaces = []
    
    def load(self, name):
        log = self.app.getLogger(self.load)
        if name in self.interfaces.keys():
            log.warning(f"Couldn't find {name} in list of interfaces")
            log.debug(f"List of interfaces: {self.interfaces}")
        
        inter = self.interfaces[name]
        log.debug(f"Creating Interface: {name}")
        inter = interfaceIDs[inter["id"]](self.app, name, inter["file"])
        log.debug(f"Loading Interface: {name}")
        inter.load()
        log.debug(f"Successfully loaded interface")
        self.currentInterfaces.append(inter)
    
    def unload(self, name):
        log = self.app.getLogger(self.unload)
        log.debug(f"Unloading interface with name: {name}")
        for i in self.currentInterfaces:
            if i.name == name:
                log.debug(f"Interface found -> Unloading")
                i.unload()
                return
        log.warning(f"No interface loaded with this name")
    