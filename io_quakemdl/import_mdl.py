import re
import bpy
import mdl

def import_mdl(operator, context, filepath):

	# keeps a copy of the file in memory
	#bpy.context.user_preferences.edit.use_global_undo = False

	# deactivate objects in the scene
	#for obj in bpy.types.scene.objects:
	#	obj = False

	#mdl = MDL();

	print("inside the import_mdl")
	operator.report({'ERROR'}, "Inside import_mdl")
	return {'CANCEL'}
	#if not read_mdl(filename):
		

	#return {'FINISHED'}