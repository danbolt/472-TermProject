bl_info = {
    "name":         "FrostTree MDL Exporter",
    "author":       "FrostTree Games",
    "blender":      (2,8,2),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Export MDL file formats",
    "category":     "Import-Export"
}
        
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty

class ImportMDLFormat(bpy.types.Operator, ExportHelper)
    bl_idname       = "mdl_import_format.blender";
    bl_label        = "My MDL Data Importer";
    bl_options      = {'PRESENT'};

    filename_ext = ".mdl";


    def execute(self, context):

        print ("Hello World!")
        return {'FINISHED'};

class ExportMDLFormat(bpy.types.Operator, ExportHelper):
    bl_idname       = "mdl_export_format.mdl";
    bl_label        = "My MDL Data Exporter";
    bl_options      = {'PRESET'};
    
    filename_ext    = ".mdl";
    filter_name     = StringProperty(default = "*.mdl", options = {'HIDDEN'})

    def execute(self, context):
        print ("Hello World\n")
        return {'FINISHED'};

def menu_func_import(self, context):
    self.layout.operator(ImportMDLFormat.bl_idname, text = "FrostTree MDL Import Format(.mdl)");

def menu_func_export(self, context):
    self.layout.operator(ExportMDLFormat.bl_idname, text="FrostTree MDL Export Format(.mdl)");

def register():
    bpy.utils.register_module(__name__);

    bpy.types.INFO_MT_file_import.append(menu_func_import);
    bpy.types.INFO_MT_file_export.append(menu_func_export);
    
def unregister():
    bpy.utils.unregister_module(__name__);
    bpy.types.INFO_MT_file_export.remove(menu_func);

if __name__ == "__main__":
    register()
