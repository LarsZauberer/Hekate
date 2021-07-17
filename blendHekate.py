import bpy
import json

class MyProperties(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty(name="ID")
    mapDir: bpy.props.StringProperty(
        name = "",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')

class Hekate(bpy.types.Panel):
    bl_label = "Hekate"
    bl_idname = "Hekate"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hekate"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        # Save ID for objects
        layout.label(text="Save Object ID")
        layout.prop(mytool, "id", text="Test")
        
        row = layout.row()
        row.operator("hekate.save_id")
        
        # General Operations
        layout.label(text="General Operations")
        layout.prop(mytool, "mapDir", text="Map Directory")
        row = layout.row()
        row.operator("hekate.generatemap")


class SaveOperator(bpy.types.Operator):
    bl_label = "Save"
    bl_idname = "hekate.save_id"
    
    def execute(self, context):
        print(context.scene.my_tool.id)
        context.active_object["id"] = context.scene.my_tool.id
        return {"FINISHED"}

class SaveMapOperator(bpy.types.Operator):
    bl_label = "Generate Map"
    bl_idname = "hekate.generatemap"
    
    def execute(self, context):
        data = {"mapData": []}
        for i in bpy.data.objects:
            objectData = {}
            try:
                objectData["id"] = i["id"]
            except Exception:
                objectData["id"] = 0
            
            datadata = {}
            datadata["x"] = i.location.x
            datadata["y"] = i.location.y
            datadata["z"] = i.location.z
            
            # Assemble
            objectData["data"] = datadata
            data["mapData"].append(objectData)
        
        with open(context.scene.my_tool.mapDir + "/map.json", "w") as f:
            json.dump(data, f)
        
        return {"FINISHED"}


def register():
    bpy.utils.register_class(Hekate)
    
    bpy.utils.register_class(MyProperties)
    bpy.utils.register_class(SaveOperator)
    bpy.utils.register_class(SaveMapOperator)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)
    

def unregister():
    bpy.utils.unregister_class(Hekate)
    bpy.utils.unregister_class(MyProperties)
    del bpy.utils.types.Window.my_tool
    
if __name__ == "__main__":
    register()
