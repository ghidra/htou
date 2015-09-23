import hou
from export_urho import *
from urho_utils import *
#https://github.com/reattiva/Urho3D-Blender/issues/39

def clamp(v,low,high):
	return max(low, min(high, v))


def write_mdl():

	#WE EXPECT NORMALS ON POINTS
	#WE EXPECT UVS ON POINTS (not yet)
	#WE EXPECT TRIANGULATION

	#first lest find out where you want to save this

	for n in hou.selectedNodes():

		geo =  n.geometry()

		#get path per node
		apath = geo.findGlobalAttrib("path")
		if(apath):
			path = geo.attribValue(apath)
		else:
			path = hou.ui.selectFile(title="pick save location")
			path = hou.expandString(path)


		print n.name()

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
		#print "number of points:"+str(len(geo.points()))
		#uLodLevel.countIndex = len(geo.points())
		uGeometry.lodLevels.append(uLodLevel)

		vertexBuffer = UrhoVertexBuffer()
		vertexBuffer.morphMinIndex = 0
		vertexBuffer.morphMaxIndex = 0
		uModel.vertexBuffers.append(vertexBuffer)

		indexBuffer = UrhoIndexBuffer()
		indexBuffer.indexSize = 2
		uModel.indexBuffers.append(indexBuffer)

		pcount=0
		for p in geo.points():

			hp = p.position()
			hn = p.attribValue("N")
			#get color if we have it
			
			
			tVertex = TVertex()
			tVertex.pos = Vector((hp[0], hp[1], hp[2]))
			tVertex.normal = Vector((hn[0], hn[1], hn[2]))

			#color
			cd = geo.findPointAttrib("Cd")
			cda = geo.findPointAttrib("Alpha")
			if(cd):
				hcd = p.attribValue(cd)
				halpha = 0
				if(cda):
					halpha = p.attribValue(cda)
					halpha = clamp(int(halpha*255),0,255)
					#print halpha
				tVertex.color = Vector(( clamp(int(hcd[0]*255),0,255), clamp(int(hcd[1]*255),0,255), clamp(int(hcd[2]*255),0,255), halpha))

			#uv
			uv = geo.findPointAttrib("uv")
			if(uv):
				huv = p.attribValue(uv)
				tVertex.uv = Vector((huv[0], huv[1],0.0))

			#uv2
			uv2 = geo.findPointAttrib("uv2")
			if(uv2):
				huv = p.attribValue(uv2)
				tVertex.uv2 = Vector((huv2[0], huv2[1],0.0))


			uVertex = UrhoVertex(tVertex)
			vertexBuffer.updateMask(uVertex.mask)
			vertexBuffer.vertices.append(uVertex)
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
		pcount=0
		for pr in geo.prims():
			#the poly winding is reversed in urho compared to houdini, instead of requiring user to reverse in h, do it here
			for v in reversed(pr.vertices()):
			#for v in pr.vertices():
				pcount+=1
				indexBuffer.indexes.append( int(v.point().number()) )
			#prcount+=1

		uLodLevel.countIndex = pcount# the total number of all points for all polys...

		UrhoWriteModel(uModel, path+n.name()+".mdl")
		#UrhoWriteModel(uModel, "/mill3d/work/jimmyg/urho/urho_vania/bin/Resources/Models/test/"+n.name()+".mdl")
		#UrhoWriteModel(uModel, "/home/jimmy/projects/urho/urho_vania/bin/Resources/Models/test/"+n.name()+".mdl")

'''def write_mdl_EXAMPLE():
	
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
	'''