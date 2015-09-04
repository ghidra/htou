import hou
from export_urho import *
from urho_utils import *
#https://github.com/reattiva/Urho3D-Blender/issues/39
def write_mdl_BAK():

	uExportData = UrhoExportData()
	uModel = UrhoModel()
	uModel.name = hou.expandString("$HIPNAME:r")#"test"#tData.objectName
	uExportData.models.append(uModel)

	totalVertices = 0 #len(geo.points())

	# Urho lod vertex buffer
	vertexBuffer = None
	# Urho lod index buffer
	indexBuffer = None
	# Maps old vertex index to Urho vertex buffer index and Urho vertex index
	modelIndexMap = {}

	for n in hou.selectedNodes():

		geo =  n.geometry()

		#verticies are the number of points
		totalVertices=len(geo.points())

		#---per geo
		uGeometry = UrhoGeometry()
		uModel.geometries.append(uGeometry)
		geomIndex = len(uModel.geometries) - 1

		# Material name (can be None)
		uGeometry.uMaterialName = "none"#tGeometry.materialName
		
		# Start value for geometry center (one for each geometry)
		center = hou.Vector3()
		
		# Set of remapped vertices
		remappedVertices = set()

	print totalVertices


	

	#totalVertices = len(tData.verticesList)

	print uExportData.models[0].name

'''def UrhoWriteModel(model, filename):

	if not model.vertexBuffers or not model.indexBuffers or not model.geometries:
		log.error("No model data to export in {:s}".format(filename))
		return

	fw = BinaryFileWriter()
	try:
		fw.open(filename)
	except Exception as e:
		log.error("Cannot open file {:s} {:s}".format(filename, e))
		return

	# File Identifier
	fw.writeAsciiStr("UMDL")'''

def write_mdl():
	
	uModel = UrhoModel()
	uModel.name = "triangle"

	uGeometry = UrhoGeometry()
	uModel.geometries.append(uGeometry)

	uLodLevel = UrhoLodLevel()
	uLodLevel.distance = 0.0
	uLodLevel.primitiveType = TRIANGLE_LIST
	uLodLevel.vertexBuffer = 0
	uLodLevel.indexBuffer = 0
	uLodLevel.startIndex = 0
	uLodLevel.countIndex = 3
	uGeometry.lodLevels.append(uLodLevel)

	vertexBuffer = UrhoVertexBuffer()
	vertexBuffer.morphMinIndex = 0
	vertexBuffer.morphMaxIndex = 0
	uModel.vertexBuffers.append(vertexBuffer)

	indexBuffer = UrhoIndexBuffer()
	indexBuffer.indexSize = 2
	uModel.indexBuffers.append(indexBuffer)
#---------------------------------------------------------
	tVertex = TVertex()
	tVertex.pos = Vector((0.0, 0.0, 0.0))
	tVertex.normal = Vector((0.0, 0.0, -1.0))

	uVertex = UrhoVertex(tVertex)
	vertexBuffer.updateMask(uVertex.mask)
	vertexBuffer.vertices.append(uVertex)
	indexBuffer.indexes.append(0)
	uModel.boundingBox.merge(uVertex.pos)
	uGeometry.center += uVertex.pos;
#---------------------------------------------------------
	tVertex = TVertex()
	tVertex.pos = Vector((0.0, 1.0, 0.0))
	tVertex.normal = Vector((0.0, 0.0, -1.0))

	uVertex = UrhoVertex(tVertex)
	vertexBuffer.updateMask(uVertex.mask)
	vertexBuffer.vertices.append(uVertex)
	indexBuffer.indexes.append(1)
	uModel.boundingBox.merge(uVertex.pos)
	uGeometry.center += uVertex.pos;
#---------------------------------------------------------
	tVertex = TVertex()
	tVertex.pos = Vector((1.0, 0.0, 0.0))
	tVertex.normal = Vector((0.0, 0.0, -1.0))

	uVertex = UrhoVertex(tVertex)
	vertexBuffer.updateMask(uVertex.mask)
	vertexBuffer.vertices.append(uVertex)
	indexBuffer.indexes.append(2)
	uModel.boundingBox.merge(uVertex.pos)
	uGeometry.center += uVertex.pos;
#---------------------------------------------------------
	uGeometry.center /= 3;

	UrhoWriteModel(uModel, "/home/jimmy/projects/urho/urho_vania/bin/Resources/Models/test/tri.mdl")