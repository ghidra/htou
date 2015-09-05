import hou
from export_urho import *
from urho_utils import *
#https://github.com/reattiva/Urho3D-Blender/issues/39
def write_mdl():

	#WE EXPECT NORMALS ON POINTS
	#WE EXPECT UVS ON POINTS
	#WE EXPECT TRIANGULATION

	#uExportData = UrhoExportData()
	#uModel = UrhoModel()
	#uModel.name = hou.expandString("$HIPNAME:r")#"test"#tData.objectName
	#uExportData.models.append(uModel)

	#totalVertices = 0 #len(geo.points())

	# Urho lod vertex buffer
	#vertexBuffer = None
	# Urho lod index buffer
	#indexBuffer = None
	# Maps old vertex index to Urho vertex buffer index and Urho vertex index
	#modelIndexMap = {}

	for n in hou.selectedNodes():

		print n.name()

		#---set up of basic urho export information
		uModel = UrhoModel()
		uModel.name = n.name()

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
		#---end basic info, start filling it out

		geo =  n.geometry()

		#verticies are the number of points
		#totalVertices=len(geo.points())
		pcount=0
		for p in geo.points():

			hp = p.position()
			hn = p.attribValue("N")
			
			tVertex = TVertex()
			print str(hp[0])+":"+str(hp[1])+":"+str(hp[2])
			print str(hn[0])+":"+str(hn[1])+":"+str(hn[2])
			tVertex.pos = Vector((hp[0], hp[1], hp[2]))
			tVertex.normal = Vector((hn[0], hn[1], hn[2]))

			uVertex = UrhoVertex(tVertex)
			vertexBuffer.updateMask(uVertex.mask)
			vertexBuffer.vertices.append(uVertex)
			#indexBuffer.indexes.append(pcount)
			uModel.boundingBox.merge(uVertex.pos)
			uGeometry.center += uVertex.pos;
			pcount+=1

		#now I need to build the index buffer
		prcount=0
		for pr in geo.prims():
			print "triangle:"+str(prcount)
			for v in pr.vertices():
				print v.point().number()
				indexBuffer.indexes.append( int(v.point().number()) )
			#prcount+=1

		uGeometry.center /= pcount;
		print "center:"+str(uGeometry.center.x)+":"+str(uGeometry.center.y)+":"+str(uGeometry.center.z)

		UrhoWriteModel(uModel, "/home/jimmy/projects/urho/urho_vania/bin/Resources/Models/test/htou_exported.mdl")

		#---per geo
		#uGeometry = UrhoGeometry()
		#uModel.geometries.append(uGeometry)
		#geomIndex = len(uModel.geometries) - 1

		# Material name (can be None)
		#uGeometry.uMaterialName = "none"#tGeometry.materialName
		
		# Start value for geometry center (one for each geometry)
		
		# Set of remapped vertices
		#remappedVertices = set()

		#print totalVertices


	

	#totalVertices = len(tData.verticesList)

	#print uExportData.models[0].name

def write_mdl_EXAMPLE():
	
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