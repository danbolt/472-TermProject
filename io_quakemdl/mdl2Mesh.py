import bpy

from io_quakemdl import mdl

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
	mesh = bpy.data.meshes.new(name="MDL mesh")
	coords = [[0, 0, 0], [1, 0, 0], [1, 1, 0]]
	mesh.from_pydata(coords, [], [])
	obj = bpy.data.objects.new("mdlName", mesh)
	bpy.context.scene.objects.link(obj)
	bpy.context.scene.objects.active = obj
	mesh.update()

	return None

if __name__ == "__main__":
	generateTestMDL()
