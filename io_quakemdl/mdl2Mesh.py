import bpy

from io_quakemdl import mdl
from .quakepal import palette

def generateTestMDL():
	test = mdl.MDL()
	test.skinWidth = 8
	test.skinHeight = 8
	
	# add some texture/skin data
	pixels = bytes([208, 208, 208, 208, 208, 208, 208, 208, 
					208, 250, 250, 250, 250, 250, 250, 208, 
					208, 250, 250, 250, 250, 250, 144, 208, 
					208, 250, 250, 250, 144, 144, 144, 208, 
					208, 250, 250, 144, 144, 144, 144, 208, 
					208, 250, 144, 144, 144, 144, 144, 208, 
					208, 250, 144, 144, 144, 144, 144, 208, 
					208, 208, 208, 208, 208, 208, 208, 208, ])
	t = mdl.MDL.Texture(pixels)
	s = mdl.MDL.Skin([t], [1.0])

	#add texture coordinates
	test.texCoords.append(mdl.MDL.TextureCoords(False, 0, 0))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 1, 0))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 0, 1))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 0, 0))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 1, 0))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 0, 1))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 0, 0))
	test.texCoords.append(mdl.MDL.TextureCoords(False, 1, 0))

	# foo
	f = mdl.MDL.SimpleFrame()
	f.box_min = mdl.MDL.Vertex(0, 0, 0, 0)
	f.box_max = mdl.MDL.Vertex(1, 1, 1, 0)
	f.name = "test cube"
	f.vertices.append(mdl.MDL.Vertex(0, 0, 0, 0))
	f.vertices.append(mdl.MDL.Vertex(1, 0, 0, 0))
	f.vertices.append(mdl.MDL.Vertex(1, 1, 0, 0))
	f.vertices.append(mdl.MDL.Vertex(0, 1, 0, 0))
	f.vertices.append(mdl.MDL.Vertex(0, 1, 1, 0))
	f.vertices.append(mdl.MDL.Vertex(0, 0, 1, 0))
	f.vertices.append(mdl.MDL.Vertex(1, 0, 1, 0))
	f.vertices.append(mdl.MDL.Vertex(1, 1, 1, 0))

	fr = mdl.MDL.Frames([f], [1.0])
	test.frames.append(fr)

	return test

def convertMDLToMesh(mdl):
	def loadTextures(mdl):
		def parseAddTexture(mdl, skin, name):
			img = bpy.data.images.new("skin", mdl.skinWidth, mdl.skinHeight)
			p = [0.0] * mdl.skinWidth * mdl.skinHeight * 4
			for i in range(mdl.skinWidth):
				for j in range(mdl.skinHeight):
					c = palette[skin[j * mdl.skinWidth + i]]
					l = ((mdl.skinHeight - 1 - i) * mdl.skinWidth + j) * 4
					p[l + 0] = c[0] / 255.0
					p[l + 1] = c[1] / 255.0
					p[l + 2] = c[2] / 255.0
					p[l + 3] = 1.0
			img.pixels[:] = p[:]
			img.pack(True)
			img.use_fake_user = True
			mdl.images.append(img)

		for i, skin in enumerate(mdl.skins):
			if (skin.group()):
				for j, subskin in enumerate(skin.frameData):
					parseAddTexture(mdl, subskin, "%s%d-%d" % ("skin", i, j))
			else:
				parseAddTexture(mdl, skin.frameData[0], "%s%d" % ("skin", i))

	def rigTextures(mdl, mesh):
		img = mdl.images[0]
		uvlay = mesh.uv_textures.new("mdl texture")
		uv_layer = mesh.uv_layers[0].data

		for poly in mesh.polygons:
			for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
				uv_layer[loop_index].uv = (mdl.texCoords[mesh.loops[loop_index].vertex_index].t * 1.0 / mdl.skinWidth, 1 - mdl.texCoords[mesh.loops[loop_index].vertex_index].s * 1.0 / mdl.skinHeight)

		mat = bpy.data.materials.new("mdl material")
		mat.diffuse_color = (1,1,1)
		mat.use_raytrace = False
		tex = bpy.data.textures.new("skin", 'IMAGE')
		tex.extension = 'CLIP'
		tex.use_preview_alpha = True
		tex.image = img
		mat.texture_slots.add()
		ts = mat.texture_slots[0]
		ts.texture = tex
		ts.use_map_alpha = True
		ts.texture_coords = 'UV'
		mesh.materials.append(mat)

	mesh = bpy.data.meshes.new(name="MDL mesh")
	coords = []
	trigs = []

	loadTextures(mdl)

	for vertex in mdl.frames[0].vertices:
		coords.append([vertex.x, vertex.y, vertex.z])

	for face in mdl.triangles:
		trigs.append((face.a, face.b, face.c))

	mesh.from_pydata(coords, [], trigs)
	rigTextures(mdl, mesh)

	obj = bpy.data.objects.new("mdlName", mesh)
	bpy.context.scene.objects.link(obj)
	bpy.context.scene.objects.active = obj
	mesh.update()

	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.normals_make_consistent(inside=False)
	bpy.ops.object.editmode_toggle()

if __name__ == "__main__":
	generateTestMDL()
