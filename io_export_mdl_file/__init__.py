bl_info = {
    "name":         "Frost Tree MDL Exporter",
    "author":       "FrostTree Games",
    "blender":      (2,8,2),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Export MDL file formats",
    "category":     "Import-Export"
}
        
import bpy
from bpy_extras.io_utils import ExportHelper

class ExportMyFormat(bpy.types.Operator, ExportHelper):
    bl_idname       = "mdl_export_format.mdl";
    bl_label        = "My MDL Data Exporter";
    bl_options      = {'PRESET'};
    
    filename_ext    = ".mdl";
    
    def execute(self, context):
        print ("Hello World\n")
        return {'FINISHED'};

def menu_func(self, context):
    self.layout.operator(ExportMyFormat.bl_idname, text="FrostTree MDL Formal(.mdl)");

def register():
    bpy.utils.register_module(__name__);
    bpy.types.INFO_MT_file_export.append(menu_func);
    
def unregister():
    bpy.utils.unregister_module(__name__);
    bpy.types.INFO_MT_file_export.remove(menu_func);

if __name__ == "__main__":
    register()
