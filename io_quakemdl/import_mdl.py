import bpy
from .mdl import MDL
from struct import pack, unpack

def extract_char(mdl_file, count = 1):
	data = mdl_file.read(count)
	data = unpack("<%dB" count, data)

	if count == 1:
		return data[0]
	return data

def extract_float(mdl_file, count = 1):
	data = mdl_file.read(4*count)
	data = unpack("<%df" % count, data)

	if count == 1:
		return data[0]
	return data

""" integers are 4 bytes long, therefore multiply 4 to count to get accurate number of bytes to extract from the file"""
def extract_int(mdl_file, count = 1):
	data = mdl_file.read(4 * count)
	data = unpack("<%di" % count, data)
	if count == 1:
		return data[0]
	return data

def extract_ident(mdl_file):
	data = mdl_file.read(4)
	s = ""
	for d in data:
		s = s+chr(d)

	return s

def extract_skin_data(mdl_file, size = 1):
	return mdl_file.read(size)

def extract_skin_texture(mdl, mdl_file):
	group = extract_int(mdl_file)
	size = mdl.skinWidth * mdl.skinHeight
	if group == 0:
		data = extract_skin_data(mdl_file, size)
		return (group, data)
	elif group == 1:
		num_of_pics = extract_int(mdl_file)
		time = extract_float(mdl_file, num_of_pics)
		print("time: " + str(time))
		data = []
		for x in range(0, num_of_pics):
			data.append(extract_skin_data(mdl_file, size))

		return(group, num_of_pics, time, data)
	else:
		# error check but return value is still valid, need to change
		operator.report({'ERROR'}, "skin group not a valid number")
		return -1;

def extract_triangles(mdl_file):
	facefront = extract_int(mdl_file)
	vertex = extract_int(mdl_file, 3)
	return (facefront, vertex)

def extract_vertex(mdl_file):
	vertex_coordinate = extract_char(mdl_file, 3)

def extract_frames(mdl, mdl_file):
	type = extract_int(mdl_file)

	# type is 0 then model frame, else group of simple frames
	if type == 0:
		min_bound = extract_vertex(mdl_file)

def read_file(mdl, filename):
	mdl_file = open(filename, 'rb')
	
	# HEADER ##############################################################
	ident = extract_ident(mdl_file)
	version = extract_int(mdl_file, 1)
	if ident not in "IDPO" or version != 6:
		operator.report({'ERROR'}, "ident is not IPDO or version is not 6")
		return False
	
	mdl.scale = extract_float(mdl_file, 3)
	print ("scale: " + str(mdl.scale))

	mdl.translation = extract_float(mdl_file, 3)
	print ("translation: " + str(mdl.translation))

	mdl.boundingradius = extract_float(mdl_file)
	print("boundingradius: " + str(mdl.boundingradius))

	mdl.eyePosition = extract_float(mdl_file, 3)
	print("eyePosition: " + str(mdl.eyePosition))

	num_skins = extract_int(mdl_file)
	print("number of skins: " + str(num_skins))

	mdl.skinWidth = extract_int(mdl_file)
	print("skin width: " + str(mdl.skinWidth))

	mdl.skinHeight = extract_int(mdl_file)
	print("skin height: " + str(mdl.skinHeight))

	num_verts = extract_int(mdl_file)
	print("number of vertices: " + str(num_verts))

	num_tris = extract_int(mdl_file)
	print("number of triangles: " + str(num_tris))

	num_frames = extract_int(mdl_file)
	print("number of frames: " + str(num_frames))

	sync_type = extract_int(mdl_file)
	print("sync_type: " + str(sync_type))

	flags = extract_int(mdl_file)
	print("flags: " + str(flags))

	size = extract_float(mdl_file)
	print("size: " + str(size))
	##############################################################################

	#extracts the number of textures in mdl
	for x in range(0, num_skins):
		mdl.skins.append(extract_skin_texture(mdl, mdl_file))

	#check to see if texture is invalid
	if mdl.skins[0] == -1:
		return False
	#print("mdl.skins: " + str(mdl.skins))

	#extracts texture coordinates from mdl
	texture_coordinates = []
	for x in range(0, num_verts):
		texture_coordinates.append(extract_int(mdl_file, 3))

	print("texture_coordinates: " + str(texture_coordinates))
	
	#extracts triangles from mdl
	for x in range(0, num_tris):
		mdl.triangles.append(extract_triangles(mdl_file))
	#print("triangles: " + str(mdl.triangles))

	#extracting frames
	for x in range(0, num_frames):
		mdl.frames.append(extract_frames(mdl, mdl_file))

	return True

def import_mdl(operator, context, filepath):

	# keeps a copy of the file in memory
	bpy.context.user_preferences.edit.use_global_undo = False

	# deactivate objects in the scene
	#for obj in bpy.types.scene.objects:
	
	#	obj = False
	mdl = MDL();

	print("inside the import_mdl")

	if not read_file(mdl, filepath):
		operator.report({'ERROR'}, "File is not of mdl type")
		return {'CANCELLED'}
	
	return {'FINISHED'}