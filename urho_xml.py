import hou
from xml.etree import ElementTree as xml
from urho_utils import XmlToPrettyString as tostring
from urho_utils import WriteXmlFile as WriteXml

count_node=16777216
def gen_node(d):
	global count_node
	node = xml.Element('node',{"id":str(count_node)})
	count_node+=1
	for a in d:
		gen_attribute(node,a)
	return node

count_component=16777216
def gen_component(d,t):
	global count_component
	component = xml.Element('component',{"type":t,"id":str(count_component)})
	count_component+=1
	for a in d:
		gen_attribute(component,a)
	return component

#-------
def test():
	for n in hou.selectedNodes():
		print attributes
		for attrib in n.attribs():
		#for attrib in l[attributes]:
			print attrib.name()
#-------
def node_data(n):
	t = n.outputs()[0]
	q=hou.Quaternion()
	q.setToEulerRotates( (t.parm("rx").eval(),t.parm("ry").eval(),t.parm("rz").eval()) )
	scl=hou.Vector3( (t.parm("sx").eval(),t.parm("sz").eval(),t.parm("sz").eval()) )
	scl*=t.parm("scale").eval()
	attribs = [
		{"name":"Is Enabled","value":"true"},
		{"name":"Name","value":n.name()[5:]},
		{"name":"Position","value":str(t.parm("tx").eval())+" "+str(t.parm("ty").eval())+" "+str(t.parm("tz").eval())},
		{"name":"Rotation","value":str(q[3])+" "+str(q[0])+" "+str(q[1])+" "+str(q[2])},
		{"name":"Scale","value":str(scl[0])+" "+str(scl[1])+" "+str(scl[2])},
		{"name":"Variables"}
	]
	return attribs

#component data
def gen_attribute(e,d):#element, and data
	xml.SubElement(e,'attribute',d)

def component_data(n):
	#bring in the node
	attribs=[]
	for p in n.spareParms():
		if not p.isAtDefault():
			sub = {}
			sub["name"]=p.description()
			if(p.parmTemplate().type() == hou.parmTemplateType.Menu):
				sub["value"] = p.menuLabels()[p.eval()]
				#print sub["value"]
			else:
				if p.description() in ("Model","Material"):
					#i have to prepend this for these
					#print "prepend"
					sub["value"] = p.description()+";"+p.evalAsString()
				else:
					sub["value"] = p.evalAsString()
			
			attribs.append(sub)


	#return comp[t](n)
	#print "test"
	return attribs

#utility functions
def strip_digits(s):
	return ''.join([i for i in s if not i.isdigit()])

def strip_string(s, to_strip):
    if to_strip:
        while s.startswith(to_strip):
            s = s[len(to_strip):]
    return s

#recursive function
def seek_component(n,data):
	for nnode in n.inputs():
		ntype = nnode.type().nameComponents()[2]
		if ntype not in ('null','merge'):
			seek_component(nnode,data)
		else:
			#it is a null, so It could be another node, or a component at this point
			trim = nnode.name().split("_")
			if(trim[0]=='COMP'):
				#it is a component, now I can do what i need spcifically with this
				ctype = strip_string( strip_digits(nnode.name()), 'COMP_')
				data.append(gen_component(component_data(nnode),ctype))
				#print "COMPONENT: "+strip_string( strip_digits(nnode.name()), 'COMP_' )
			elif(trim[0]=='NODE'):
				#add the node as a child and carry on with the recursion
				newnode = gen_node(node_data(nnode))
				seek_component(nnode,newnode)
				data.append(newnode)
				#print "MAKE A NODE: "+strip_string( nnode.name(), 'NODE_' )

#called from houdini
def collect_nodes():
	#we should only have one node selected
	for n in hou.selectedNodes():
		#first we should check that we have selected a node that is a urho NODE
		if n.type().nameComponents()[2] in ('null','merge'):
			if(n.name().split("_")[0]=='NODE'):
				#now lets find out where we want to save this bitch
				path = hou.ui.selectFile(title="pick save location")
				path = hou.expandString(path)

				data = gen_node(node_data(n))
				seek_component(n,data)

				print(path+strip_string( strip_digits(n.name()), 'NODE_')+".xml")
				WriteXml(data,path+strip_string( strip_digits(n.name()), 'NODE_')+".xml")
				#print tostring(data)
				#print xml.dump(node_data)
			else:
				print "ERROR: We expect the selected node to be labeled as NODE"
		else:
			print "ERROR: The selected nodes should be a null or merge. As well we expect the selected node to be labeled as NODE"
		'''node = gen_node(node_data(n))
		for transforms in n.inputs():#we should find a transform node first
			node.append( gen_node(node_data(transforms.inputs()[0])) )'''		


'''
nattribs = [
	{"name":"Is Enabled","value":"true"},
	{"name":"Name","value":"StageForest"},
	{"name":"Position","value":"-0.890503 -4.05726 -30.2741"},
	{"name":"Rotation","value":"1 0 0 0"},
	{"name":"Scale","value":"1 1 1"},
	{"name":"Variables"}
]
node = gen_node(nattribs)

#new node
nnode = gen_node(nattribs)

node.append(nnode)

#c = xml.SubElement(a, 'c')
#d = xml.SubElement(c, 'd')

print tostring(node)
#print xml.dump(node)
'''