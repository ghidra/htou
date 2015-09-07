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

	#i need mt compressor
	c = Float16Compressor()

	for n in hou.selectedNodes():

		geo =  n.geometry()

		#print n.name()

		#---set up of basic urho export information
		uModel = UrhoModel()
		uModel.name = str(n.name())

		uGeometry = UrhoGeometry()
		uModel.geometries.append(uGeometry)

		uLodLevel = UrhoLodLevel()
		uLodLevel.distance = 0.0
		uLodLevel.primitiveType = TRIANGLE_LIST
		uLodLevel.vertexBuffer = 0
		uLodLevel.indexBuffer = 0
		uLodLevel.startIndex = 0
		print "number of points:"+str(len(geo.points()))
		uLodLevel.countIndex = len(geo.points())
		uGeometry.lodLevels.append(uLodLevel)

		vertexBuffer = UrhoVertexBuffer()
		vertexBuffer.morphMinIndex = 0
		vertexBuffer.morphMaxIndex = 0
		uModel.vertexBuffers.append(vertexBuffer)

		indexBuffer = UrhoIndexBuffer()
		indexBuffer.indexSize = 2
		uModel.indexBuffers.append(indexBuffer)

		#---end basic info, start filling it out

		#pp = [(0.0, 0.0, 0.0),(0.0, 5.0, 0.0),(5.0, 0.0, 0.0),(1.0, 0.0, 0.0),(0.0, -1.0, 0.0),(0.0, 0.0, 0.0)]
		#pp = [(6.0, 1.0, -3.0),(4.0, 0.2, 2.0),(-2.0, 0.1, 6.0),(1.0, 0.0, 0.0),(0.0, -1.0, 0.0),(0.0, 0.0, 0.0)]
		#verticies are the number of points
		#totalVertices=len(geo.points())
		pcount=0
		for p in geo.points():

			hp = p.position()
			hn = p.attribValue("N")
			#hp = pp[pcount]
			#hn = (0.0,0.0,-1.0)

			'''px = c.compress(hp[0])
			py = c.compress(hp[1])
			pz = c.compress(hp[2])
			nx = c.compress(hn[0])
			ny = c.compress(hn[1])
			nz = c.compress(hn[2])'''

			px = hp[0]
			py = hp[1]
			pz = hp[2]
			nx = hn[0]
			ny = hn[1]
			nz = hn[2]
			
			tVertex = TVertex()
			print "P:"+str(px)+":"+str(py)+":"+str(pz)
			print "N:"+str(nx)+":"+str(ny)+":"+str(nz)
			#tVertex.pos = Vector(p.attribValue("P"))
			tVertex.pos = Vector((px, py, pz))
			tVertex.normal = Vector((nx, ny, nz))

			uVertex = UrhoVertex(tVertex)
			vertexBuffer.updateMask(uVertex.mask)
			vertexBuffer.vertices.append(uVertex)
			#indexBuffer.indexes.append(pcount)
			uModel.boundingBox.merge(uVertex.pos)
			uGeometry.center += uVertex.pos;
			pcount+=1

		#uLodLevel.countIndex = pcount #set this so we know where how many points in this geo
		#uGeometry.center /= pcount;
		uGeometry.center = Vector(( ((uModel.boundingBox.min.x+uModel.boundingBox.max.x)/2.0),((uModel.boundingBox.min.y+uModel.boundingBox.max.y)/2.0),((uModel.boundingBox.min.z+uModel.boundingBox.max.z)/2.0) ))

		print "center:"+str(uGeometry.center.x)+":"+str(uGeometry.center.y)+":"+str(uGeometry.center.z)
		print "bbmin:"+str(uModel.boundingBox.min.x)+":"+str(uModel.boundingBox.min.y)+":"+str(uModel.boundingBox.min.z)
		print "bbmax:"+str(uModel.boundingBox.max.x)+":"+str(uModel.boundingBox.max.y)+":"+str(uModel.boundingBox.max.z)

		#now I need to build the index buffer
		prcount=0
		for pr in geo.prims():
			print "triangle:"+str(prcount)
			for v in pr.vertices():
				print v.point().number()
				indexBuffer.indexes.append( int(v.point().number()) )
			#prcount+=1

		#print "center:"+str(uGeometry.center.x)+":"+str(uGeometry.center.y)+":"+str(uGeometry.center.z)

		UrhoWriteModel(uModel, "/home/jimmy/projects/urho/urho_vania/bin/Resources/Models/test/"+n.name()+".mdl")

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

def write_mdl_l():
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
	uLodLevel.countIndex = 6
	uGeometry.lodLevels.append(uLodLevel)

	vertexBuffer = UrhoVertexBuffer()
	vertexBuffer.morphMinIndex = 0
	vertexBuffer.morphMaxIndex = 0
	uModel.vertexBuffers.append(vertexBuffer)

	#one triangle
	indexBuffer = UrhoIndexBuffer()
	indexBuffer.indexSize = 2
	uModel.indexBuffers.append(indexBuffer)
	

	p = [(0.0, 0.0, 0.0),(0.0, 1.0, 0.0),(1.0, 0.0, 0.0),(1.0, 0.0, 0.0),(0.0, -1.0, 0.0),(0.0, 0.0, 0.0)]
	for i in range(3):

		tVertex = TVertex()
		tVertex.pos = Vector(p[i])
		tVertex.normal = Vector((0.0, 0.0, -1.0))

		uVertex = UrhoVertex(tVertex)
		vertexBuffer.updateMask(uVertex.mask)
		vertexBuffer.vertices.append(uVertex)
		indexBuffer.indexes.append(i)
		uModel.boundingBox.merge(uVertex.pos)
		uGeometry.center += uVertex.pos;
	
	

	#two triangle
	#indexBuffer = UrhoIndexBuffer()
	#indexBuffer.indexSize = 2

	for i in range(3):

		tVertex = TVertex()
		tVertex.pos = Vector(p[i+3])
		tVertex.normal = Vector((0.0, 0.0, -1.0))

		uVertex = UrhoVertex(tVertex)
		vertexBuffer.updateMask(uVertex.mask)
		vertexBuffer.vertices.append(uVertex)
		indexBuffer.indexes.append(i+3)
		uModel.boundingBox.merge(uVertex.pos)
		uGeometry.center += uVertex.pos;

	#uModel.indexBuffers.append(indexBuffer)

	

	uGeometry.center /= 6;

	UrhoWriteModel(uModel, "/home/jimmy/projects/urho/urho_vania/bin/Resources/Models/test/tri2.mdl")