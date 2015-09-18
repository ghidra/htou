import hou
from xml.etree import ElementTree as xml
from urho_utils import XmlToPrettyString as tostring

count_node=16777216
def gen_node(d):
	global count_node
	node = xml.Element('node',{"id":str(count_node)})
	count_node+=1
	for a in d:
		gen_attribute(node,a)
	return node

count_component=16777216
def gen_component(d):
	global count_component
	component = xml.Element('component',{"type":"","id":str(count_component)})
	count_component+=1
	return component

def gen_attribute(e,d):#element, and data
	xml.SubElement(e,'attribute',d)

#-------
def test(l):
	for attributes in l:
		print attributes
		for attrib in attributes:
		#for attrib in l[attributes]:
			print str(attrib)+"_"+str(attributes[attrib])
#-------
def node_data(n):
	#we expect a nodes name to be NODE_*
	#this removes the NODE_ part
	t = n.outputs()[0]
	q=hou.Quaternion()
	q.setToEulerRotates( (t.parm("rx").eval(),t.parm("rz").eval(),t.parm("rz").eval()) )
	scl=hou.Vector3( (t.parm("sx").eval(),t.parm("sz").eval(),t.parm("sz").eval()) )
	scl*=t.parm("scale").eval()
	attribs = [
		{"name":"Is Enabled","value":"true"},
		{"name":"Name","value":n.name()[5:]},
		{"name":"Position","value":str(t.parm("tx").eval())+" "+str(t.parm("ty").eval())+" "+str(t.parm("tz").eval())},
		{"name":"Rotation","value":str(q[0])+" "+str(q[1])+" "+str(q[2])+" "+str(q[3])},
		{"name":"Scale","value":str(scl[0])+" "+str(scl[1])+" "+str(scl[2])},
		{"name":"Variables"}
	]
	TEST_attribs = [
		{"name":"Is Enabled","value":"true"},
		{"name":"Variables"}
	]
	return attribs



def collect_nodes():
	#we should only have one node selected
	for n in hou.selectedNodes():
		node = gen_node(node_data(n))
		#print n.name()#this is the main node everything is under
		#print n.outputs()[0].name()
		for transforms in n.inputs():#we should find a transform node first
			node.append( gen_node(node_data(transforms.inputs()[0])) )
			#print transforms.inputs()[0].name()#then a merge node that is the next child node
		print tostring(node)
		#print xml.dump(node)


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