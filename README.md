Houdini to Urho3d
--
Currently this is a very bare bones exporter!<br/>
This will export static meshes only!<br/>

Based on Reativas Blender exporter for Urho3D.<br/>

This is NOT well tested. It's a tool I made for my project specifically!<br/>
It makes a lot of assumptions as far as set up and exporting.<br/>
Tested in Houdini 13 only. Using Python 2.* that is bundled with it.

![alt tag](https://cloud.githubusercontent.com/assets/5643219/10115780/a1682e58-63e3-11e5-8c42-fdadf75d6fcc.png)

"Installation"
--

![alt tag](https://cloud.githubusercontent.com/assets/5643219/10115770/99e76b12-63e3-11e5-8b3e-a5197f8d25c7.png)
<br/>

I've split it into 3 shelf tools.<br/>
Put the python scripts in your houdini user folder, usually ~/houdini[version]/scripts/python<br/>
<ul>
	<li>"urho mesh" : export a simple static mesh object</li>
	<li>"urho scene" : save XML prefab</li>
	<li>"urho component" : set up paramaters for components</li>
		<ul>
			<li>Currently only supports:</li>
			<li>Static Mesh</li>
			<li>Collision Shape</li>
			<li>Rigid Body</li>
			<li>"Light"</li>
		</ul>
<ul>

Each respective shelf tool uses the following python:

```
import urho
reload(urho)

urho.write_mdl()
```
```
import urho_xml
reload(urho_xml)

urho_xml.collect_nodes()
```
```
import urho_component
reload(urho_component)

urho_component.make_parms()
```

Meshes
--
![alt tag](https://cloud.githubusercontent.com/assets/5643219/10115771/99eadcde-63e3-11e5-84cd-669a49a0ac46.png)


select nodes (from inside a SOP) that you want to export as mdl, and push the shelf tool button.
<ul>
<li>Mdls will be names based on the node selected.</li>
<li>To be safe, Triangulate you mesh.</li>
<li>All attributes are read at the point context.</li>
<li>You MUST have normals at the point context.</li>
<li>Supports Cd, for vertex color.</li>
<li>Vertex color is a vector 4, the 4th element being alpha.</li>
<li>The export will use a float placed on the "Alpha" attribute. Otherwise, alpha is set to 1 [255].</li>
<li>Supports uv, and uv2.</li>
<li>You can put a detail attribute called "path" to bypass the folder selection for export.</li>
<li>It should be a string attribute that is the directory you want to write the mdl to.</li>
  <ul>
  <li>*example:</li>
  <li>*/tmp/Models/ (MUST have a trailing "/")</li>
  </ul>
</ul>

----
To do:<br/>

Bones, and Animation. LODs. Vertex Morphs.