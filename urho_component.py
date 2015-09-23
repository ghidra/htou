import hou
from urho_xml import strip_string
from urho_xml import strip_digits

#############
def c_staticmodel(n):
	group = n.parmTemplateGroup()
	folder = hou.FolderParmTemplate("folder", "Static Model Component")

	folder.addParmTemplate(hou.StringParmTemplate("model", "Model", 1))
	folder.addParmTemplate(hou.StringParmTemplate("material", "Material",1))

	folder.addParmTemplate(hou.ToggleParmTemplate("isoccluder", "Is Occluder", 0))
	folder.addParmTemplate(hou.ToggleParmTemplate("isoccludable", "Can Be Occluded", 1))
	folder.addParmTemplate(hou.ToggleParmTemplate("castshadows", "Cast Shadows", 0))
	folder.addParmTemplate(hou.FloatParmTemplate("drawdistance", "Draw Distance", 1 ) )
	folder.addParmTemplate(hou.FloatParmTemplate("shadowdistance", "Shadow Distance", 1 ) )
	folder.addParmTemplate(hou.FloatParmTemplate("lodbias", "LOD Bias", 1 ,(1.0,)) )
	folder.addParmTemplate(hou.FloatParmTemplate("maxlights", "Max Lights", 1 ) )

	folder.addParmTemplate(hou.IntParmTemplate("viewmask", "View Mask",1,(-1,)))
	folder.addParmTemplate(hou.IntParmTemplate("lightmask", "Light Mask",1,(-1,)))
	folder.addParmTemplate(hou.IntParmTemplate("shadowmask", "Shadow Mask",1,(-1,)))
	folder.addParmTemplate(hou.IntParmTemplate("zonemask", "Zone Mask",1,(-1,)))
	folder.addParmTemplate(hou.IntParmTemplate("occlodlevel", "Occ LOD Level",1,(-1,)))
	
	group.append(folder)
	n.setParmTemplateGroup(group)

def c_rigidbody(n):
	group = n.parmTemplateGroup()
	folder = hou.FolderParmTemplate("folder", "Rigid Body Component")

	folder.addParmTemplate(hou.FloatParmTemplate("mass", "Mass",1))
	folder.addParmTemplate(hou.FloatParmTemplate("friction", "Friction",1,(0.5,)))
	folder.addParmTemplate(hou.FloatParmTemplate("anifriction", "Anistropic Friction",3,(1.0,1.0,1.0,)))
	folder.addParmTemplate(hou.FloatParmTemplate("rollfriction", "Rolling Friction",1))
	folder.addParmTemplate(hou.FloatParmTemplate("restitution", "Restitution",1))
	folder.addParmTemplate(hou.FloatParmTemplate("linearvelocity", "Linear Velocity",3))
	folder.addParmTemplate(hou.FloatParmTemplate("angularvelocity", "Angular Velocity",3))
	folder.addParmTemplate(hou.FloatParmTemplate("linearfactor", "Linear Factor",3,(1.0,1.0,1.0,)))
	folder.addParmTemplate(hou.FloatParmTemplate("angularfactor", "Angular Factor",3,(1.0,1.0,1.0,)))
	folder.addParmTemplate(hou.FloatParmTemplate("lineardamping", "Linear Damping",1))
	folder.addParmTemplate(hou.FloatParmTemplate("angulardamping", "Angular Damping",1))
	folder.addParmTemplate(hou.FloatParmTemplate("linearrest", "Linear Rest Threshold",1,(0.8,)))
	folder.addParmTemplate(hou.FloatParmTemplate("angluarrest", "Angular Rest Threshold",1,(1.0,)))

	folder.addParmTemplate(hou.IntParmTemplate("collisionlayer", "Collision Layer",1,(1,)))
	folder.addParmTemplate(hou.IntParmTemplate("collisionmask", "Collision Mask",1,(-1,)))

	folder.addParmTemplate(hou.FloatParmTemplate("contactthreshold", "Contact Threshold",1,(1e+18,)))
	folder.addParmTemplate(hou.FloatParmTemplate("ccdradius", "CCD Radius",1))
	folder.addParmTemplate(hou.FloatParmTemplate("ccdmotion", "CCD Motion Threshold",1))

	#This needs to be a drop down
	#never, when active, always
	folder.addParmTemplate(hou.MenuParmTemplate("collisioneventmode", "Collision Event Mode",("Never","When Active","Always",),default_value=1))

	folder.addParmTemplate(hou.ToggleParmTemplate("usegravity", "Use Gravity", 0))
	folder.addParmTemplate(hou.ToggleParmTemplate("iskinematic", "Is Kinematic", 1))
	folder.addParmTemplate(hou.ToggleParmTemplate("istrigger", "Is Trigger", 0))

	folder.addParmTemplate(hou.FloatParmTemplate("gravityoverride", "Gravity Override",3))

	group.append(folder)
	n.setParmTemplateGroup(group)

def c_collisionshape(n):
	group = n.parmTemplateGroup()
	folder = hou.FolderParmTemplate("folder", "Collision Shape Component")
	
	folder.addParmTemplate(hou.MenuParmTemplate("shapetype", "Shape Type",("Box","Sphere","StaticPlane","Cylinder","Capsule","Cone","TriangleMesh","ConvexHull","Terrain",)))
	folder.addParmTemplate(hou.FloatParmTemplate("size", "Size",3,(1.0,1.0,1.0,)))
	folder.addParmTemplate(hou.FloatParmTemplate("offsetposition", "Offset Position",3))
	folder.addParmTemplate(hou.FloatParmTemplate("offsetrotation", "Offset Rotation",3))
	folder.addParmTemplate(hou.StringParmTemplate("model", "Model", 1))
	folder.addParmTemplate(hou.FloatParmTemplate("lodlevel", "LOD Level", 1 ) )
	folder.addParmTemplate(hou.FloatParmTemplate("collisionmargin", "Collision Margin", 1 ,(0.04,)) )
	folder.addParmTemplate(hou.FloatParmTemplate("customnodeid", "CustomGeometry NodeID", 1 ) )

	group.append(folder)
	n.setParmTemplateGroup(group)

#######
comp={
	"StaticModel":c_staticmodel,
	"RigidBody":c_rigidbody,
	"CollisionShape":c_collisionshape,
}
######

def make_parms():
	#we are going to make a lot of assumptions for now
	#one, you must name the node right to get an effect
	for n in hou.selectedNodes():
		
		ctype = strip_string( strip_digits(n.name()), 'COMP_')
		print ctype

		comp[ctype](n)

#test
def read_parms():
	for n in hou.selectedNodes():
		for p in n.spareParms():
			if not p.isAtDefault() :
				
				print p.description()
				print p.parmTemplate().type()
				if(p.parmTemplate().type() == hou.parmTemplateType.Menu):
					print p.menuLabels()[p.eval()]
				else:
					print p.eval()
