Houdini to Urho3d
-------
Currently this is a very bare bones exporter.
This will export static meshes only!

Make a shelf tool, with this simple script

```
import urho
reload(urho)

urho.write_mdl()
```
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
<li>It should be a string attribute that is the directory you want to write the mdl to.
MUST have a trailing "/"</li>
  <ul>
  <li>*example:</li>
  <li>*/tmp/Models/</li>
  </ul>
</ul>

----
To do:

Testing and support for anything not listed.
Bones, and Animation. LODs. Vertex Morphs.