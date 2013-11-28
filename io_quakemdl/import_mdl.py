import bpy
from .mdl import MDL
from struct import pack, unpack

def extract_char(mdl_file, count = 1):
	data = mdl_file.read(count)
	name = ""
	for d in data:
		name = name + chr(d)

	if "\0" in name:
		name = name[:name.index("\0")]
	if count == 1:
		return name[0]
	return name

def extract_byte(mdl_file, count = 1):
	data = mdl_file.read(count)
	data = unpack("<%dB" %count, data)
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
		return  mdl.Skin(data, None)
	elif group == 1:
		num_of_pics = extract_int(mdl_file)
		time = extract_float(mdl_file, num_of_pics)
		print("time: " + str(time))
		data = []
		for x in range(0, num_of_pics):
			data.append(extract_skin_data(mdl_file, size))

		return mdl.Skin(data, time)
	else:
		# error check but return value is still valid, need to change
		operator.report({'ERROR'}, "skin group not a valid number")
		return -1;

def extract_text_coord(mdl, mdl_file):
	onseam, s, t = extract_int(mdl_file, 3)
	return mdl.TextureCoords(onseam, s, t)

def extract_triangles(mdl, mdl_file):
	facefront = extract_int(mdl_file)
	vertex = extract_int(mdl_file, 3)
	return mdl.Triangle(vertex[0], vertex[1], vertex[2], facefront)

def extract_name(mdl_file):
	return extract_char(mdl_file, 16)

def extract_bounds(mdl_file):
	return extract_byte(mdl_file, 4)

def extract_vertices(mdl, mdl_file, num_verts):
	vertex_array = []
	for x in range(0, num_verts):
		vertex = (extract_byte(mdl_file, 4))
		vertex_array.append(mdl.Vertex(vertex[0], vertex[1], vertex[2], vertex[3]))
	return vertex_array

def extract_frames(mdl, mdl_file, num_verts):
	type = extract_int(mdl_file)

	# type is 0 then model frame, else group of simple frames
	if type == 0:
		min_bound = extract_bounds(mdl_file)
		#print("min_bound: " + str(min_bound))
		max_bound = extract_bounds(mdl_file)
		name = extract_char(mdl_file, 16)
		vertices = extract_vertices(mdl, mdl_file, num_verts)
		return mdl.SimpleFrame(min_bound, max_bound, name, vertices)
	elif type == 1:
		num = extract_int(mdl_file)
		min_bound = extract_bounds(mdl_file)
		max_bound = extract_bounds(mdl_file)
		time = extract_float(mdl_file, num)
		frames = []
		for i in range(0, num):
			frames.append(mdl, mdl_file, num_verts)
		return mdl.Frames(frames, time)

def read_file(mdl, filename):
	mdl_file = open(filename, 'rb')
	
	# HEADER ##############################################################
	ident = extract_ident(mdl_file)
	version = extract_int(mdl_file, 1)
	if ident not in "IDPO" or version != 6:
		operator.report({'ERROR'}, "ident is not IPDO or version is not 6")
		return False
	
	scale = extract_float(mdl_file, 3)
	mdl.scale = mdl.Vec3(scale[0], scale[1], scale[2])

	translation = extract_float(mdl_file, 3)
	mdl.translation = mdl.Vec3(translation[0], translation[1], translation[2])
	#print ("translation: " + str(mdl.translation))
	
	mdl.boundingradius = extract_float(mdl_file)
	#print("boundingradius: " + str(mdl.boundingradius))

	eyePosition = extract_float(mdl_file, 3)
	mdl.eyePosition = mdl.Vec3(eyePosition[0], eyePosition[1], eyePosition[2])
	#print("eyePosition: " + str(mdl.eyePosition))

	num_skins = extract_int(mdl_file)
	#print("number of skins: " + str(num_skins))

	mdl.skinWidth = extract_int(mdl_file)
	#print("skin width: " + str(mdl.skinWidth))

	mdl.skinHeight = extract_int(mdl_file)
	#print("skin height: " + str(mdl.skinHeight))

	num_verts = extract_int(mdl_file)
	#print("number of vertices: " + str(num_verts))

	num_tris = extract_int(mdl_file)
	#print("number of triangles: " + str(num_tris))

	num_frames = extract_int(mdl_file)
	#print("number of frames: " + str(num_frames))

	sync_type = extract_int(mdl_file)
	#print("sync_type: " + str(sync_type))

	flags = extract_int(mdl_file)
	#print("flags: " + str(flags))

	size = extract_float(mdl_file)
	#print("size: " + str(size))
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
		texture_coordinates.append(extract_text_coord(mdl, mdl_file))

	#print("texture_coordinates: " + str(texture_coordinates))
	
	#extracts triangles from mdl
	for x in range(0, num_tris):
		mdl.triangles.append(extract_triangles(mdl, mdl_file))
	#print("triangles: " + str(mdl.triangles))

	#extracting frames
	for x in range(0, num_frames):
		mdl.frames.append(extract_frames(mdl, mdl_file, num_verts))
	#print("mdl.frames[0].box_min: "+ str(mdl.frames[0].box_min))

	return True

def import_mdl(operator, context, filepath):

	# keeps a copy of the file in memory
	bpy.context.user_preferences.edit.use_global_undo = False

	# deactivate objects in the scene
	#for obj in bpy.types.scene.objects:
		#obj = False

	mdl = MDL();

	if not read_file(mdl, filepath):
		operator.report({'ERROR'}, "File is not of mdl type")
		return {'CANCELLED'}
	
	return {'FINISHED'}