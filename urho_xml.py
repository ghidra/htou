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
