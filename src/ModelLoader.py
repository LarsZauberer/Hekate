import os
from pathlib import Path


class ModelLoader():
    def __init__(self, app):
        self.path = Path("Content")
        self.app = app
    
    def loadModels(self):
        models = []
        for file in os.listdir(self.path):
            if file.endswith(".bam"):
                models = self.app.loader.loadModel(self.path / file)
        return models
    
    def convertFiles(self):
        raise NotImplementedError
    
    def loadTextures(self):
        raise NotImplementedError
        textures = []
        for file in os.listdir(self.path):
            if file.endswith(".png"):
                textures = self.app.loader.loadModel(self.path / file)
        return textures
